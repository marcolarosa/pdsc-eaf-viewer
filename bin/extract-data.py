#!/usr/bin/env pythn

import base64
import coloredlogs
import json
import hashlib
import logging as log
from lxml import etree
import lxml
import os
import os.path
import pprint
import sys

coloredlogs.install()
pp = pprint.PrettyPrinter(indent=2, width=300)

log.basicConfig(level=log.INFO)


class DataExtractor:
    def __init__(self):
        self.data = {}
        self.words = {}
        self.languages = {}
        self.data_path = "/srv/data"
        self.repository = "/srv/dist/repository"
        try:
            os.makedirs(self.repository)
        except FileExistsError:
            pass

    def extract(self):
        self.process_datafiles()

    def process_datafiles(self):
        stats = []
        for root, dirs, files in os.walk(self.data_path):
            for file in files:
                if "eaf" in file:
                    fpath = f"{root}/{file}"
                    try:
                        tree = etree.parse(fpath)
                        stats.append(self.process_elan_file(fpath, tree))
                    except lxml.etree.XMLSyntaxError:
                        log.error(f"Invalid file: {fpath}")
        with open(f"{self.repository}/index.json", "w") as f:
            f.write(json.dumps({"statistics": stats}))

    def process_elan_file(self, fpath, tree):
        log.info(f"Processing: {fpath}")
        issues = []
        statistics = {"file": fpath.replace(f"{self.data_path}/", "")}
        annotations = {}

        (tiers_to_annotations, annotations_to_tier) = self.map_annotations_to_tiers(
            tree
        )
        timeslots, statistics = self.extract_timeslots(tree, statistics)
        timeslots, annotations, issues = self.extract_alignable_annotations(
            tree, issues, timeslots, annotations_to_tier
        )
        annotations, issues, statistics = self.extract_reference_annotations(
            tree, issues, statistics, annotations, annotations_to_tier
        )
        timeslots, statistics = self.map_annotations_to_timeslots(
            timeslots, statistics, annotations
        )

        statistics["totalIssues"] = len(issues)

        m = hashlib.sha256()
        m.update(statistics["file"].encode())
        digest = m.hexdigest()
        statistics["dataFile"] = f"/repository/{digest}.json"
        statistics["tiers"] = [k for k in tiers_to_annotations.keys()]
        ts = []
        for (key, value) in timeslots.items():
            # value["name"] = key
            ts.append(value)

        with open(f"{self.repository}/{digest}.json", "w") as f:
            f.write(
                json.dumps(
                    {
                        "timeslots": {"name": statistics["file"], "children": ts},
                        "tiers": {
                            "tiers": "tiers",
                            "children": [
                                {"name": key, "children": item["annotations"]}
                                for (key, item) in tiers_to_annotations.items()
                            ],
                        },
                        "issues": issues,
                    }
                )
            )
        # pp.pprint(timeslots)
        # pp.pprint(issues)
        # log.debug(statistics)
        return statistics

    def map_annotations_to_tiers(self, tree):
        tiers_to_annotations = {}
        annotations_to_tier = {}
        for tier in tree.findall("//TIER"):
            t = {"annotations": []}
            for annotation in tier.findall("ANNOTATION"):
                for child in annotation.iterchildren():
                    t["annotations"].append(
                        {"name": child.attrib["ANNOTATION_ID"], "children": []}
                    )
                    annotations_to_tier[child.attrib["ANNOTATION_ID"]] = tier.attrib[
                        "TIER_ID"
                    ]
            tiers_to_annotations[tier.attrib["TIER_ID"]] = t
        return (tiers_to_annotations, annotations_to_tier)

    def extract_timeslots(self, tree, statistics):
        timeslots = {}
        ts_elements = tree.findall("//TIME_SLOT")
        for ts in ts_elements:
            timeslots[ts.attrib["TIME_SLOT_ID"]] = {
                "ts": {"start": ts.attrib["TIME_SLOT_ID"], "end": None},
                "time": {"start": ts.attrib["TIME_VALUE"], "end": None},
                "children": [],
            }
        statistics["start"] = int(ts_elements[0].attrib["TIME_VALUE"])
        statistics["end"] = int(ts_elements[-1:][0].attrib["TIME_VALUE"])
        statistics["duration"] = statistics["end"] - statistics["start"]
        statistics["timeslots"] = len(ts_elements)
        return timeslots, statistics

    def extract_alignable_annotations(
        self, tree, issues, timeslots, annotations_to_tier
    ):
        annotations = {}

        log.debug(
            f"Total number of alignable annotations: {len(tree.findall('//ALIGNABLE_ANNOTATION'))}"
        )
        for aa in tree.findall("//ALIGNABLE_ANNOTATION"):
            if "TIME_SLOT_REF1" not in aa.attrib:
                issues.append(
                    {
                        "msg": f"TIME_SLOT_REF1 missing from ALIGNABLE_ANNOTATION {aa.attrib['ANNOTATION_ID']}"
                    }
                )
            if "TIME_SLOT_REF2" not in aa.attrib:
                issues.append(
                    {
                        "msg": f"TIME_SLOT_REF2 missing from ALIGNABLE_ANNOTATION {aa.attrib['ANNOTATION_ID']}"
                    }
                )
            tsref = aa.attrib["TIME_SLOT_REF1"]
            timeslots[tsref]["name"] = aa.attrib["ANNOTATION_ID"]
            timeslots[tsref]["value"] = aa.find("ANNOTATION_VALUE").text
            timeslots[tsref]["tier"] = annotations_to_tier[aa.attrib["ANNOTATION_ID"]]
            timeslots[tsref]["time"]["end"] = timeslots[aa.attrib["TIME_SLOT_REF2"]][
                "time"
            ]["start"]
            timeslots[tsref]["ts"]["end"] = timeslots[aa.attrib["TIME_SLOT_REF2"]][
                "ts"
            ]["start"]
            del timeslots[aa.attrib["TIME_SLOT_REF2"]]

        for (key, ts) in timeslots.items():
            if "name" not in ts:
                issues.append(
                    {"msg": f"TIMESLOT {key} has no alignable annotation mapped to it"}
                )
        return timeslots, annotations, issues

    def extract_reference_annotations(
        self, tree, issues, statistics, annotations, annotations_to_tier
    ):
        annotatddions = {}
        ref_annotations = tree.findall("//REF_ANNOTATION")
        log.debug(f"Total number of ref annotations: {len(ref_annotations)}")
        statistics["totalRefAnnotations"] = len(ref_annotations)
        for ra in ref_annotations:
            annotations[ra.attrib["ANNOTATION_ID"]] = {
                "tier": annotations_to_tier[ra.attrib["ANNOTATION_ID"]],
                "value": ra.find("ANNOTATION_VALUE").text,
                "ref": ra.attrib["ANNOTATION_REF"],
                "name": ra.attrib["ANNOTATION_ID"],
                "type": "ref annotation",
                "children": [],
            }
            # print(ra.find("ANNOTATION_VALUE").text)
            if not ra.find("ANNOTATION_VALUE").text:
                issues.append(
                    {"msg": f"REF_ANNOTATION {ra.attrib['ANNOTATION_ID']} has no data"}
                )
        return annotations, issues, statistics

    def map_annotations_to_timeslots(self, timeslots, statistics, annotations):
        def map_annotation(i, ann, children):
            for child in children:
                if ann["ref"] == child["name"]:
                    i += 1
                    child["children"].append(ann)
                else:
                    i = map_annotation(i, ann, child["children"])
            return i

        i = 0
        for (annkey, annvalue) in annotations.items():
            for (tskey, tsvalue) in timeslots.items():
                if "name" in tsvalue and annvalue["ref"] == tsvalue["name"]:
                    i += 1
                    tsvalue["children"].append(annvalue)
                else:
                    i = map_annotation(i, annvalue, tsvalue["children"])
        statistics["totalMappedAnnotations"] = i
        log.debug(f"Total number of annotations mapped: {i}")
        return timeslots, statistics


if __name__ == "__main__":
    d = DataExtractor()
    d.extract()

