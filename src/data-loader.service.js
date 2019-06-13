"use strict";

import { compact, orderBy } from "lodash";

export async function loadData({ store }) {
    const index = (await get(mapRepositoryRoot("/repository/index.json")))
        .statistics;
    store.commit(`saveIndex`, { index });

    async function get(path) {
        try {
            let response = await fetch(path);
            if (response.status !== 200) {
                throw new Error(response);
            }
            return await response.json();
        } catch (error) {
            console.log(error);
            return [];
        }
    }
}

export async function loadLanguageData({ code }) {
    let response = await fetch(
        mapRepositoryRoot(`/repository/${code}/index.json`)
    );
    if (response.status !== 200) {
        throw new Error(response);
    }
    let data = await response.json();
    data.words = data.words.map(w => {
        return {
            ...w,
            audio_file: mapRepositoryRoot(w.audio_file)
        };
    });
    return data;
}

export async function loadWordData({ word, words }) {
    let index = words.filter(w => {
        return w.name === word;
    })[0].index;
    let response = await fetch(mapRepositoryRoot(`/repository/${index}`));
    if (response.status !== 200) {
        throw new Error(response);
    }
    word = orderBy(await response.json(), "language");
    word = word.map(w => {
        return {
            ...w,
            audio_file: mapRepositoryRoot(w.audio_file)
        };
    });
    return word;
}

export function mapRepositoryRoot(path) {
    return path;
    const root =
        process.env.NODE_ENV === "development"
            ? "/repository"
            : "/50words/repository";
    return path.replace("/repository", root);
}
