<template>
    <div class="mx-auto font-mono p-5">
        <el-card class="px-6">
            <div slot="header">
                File Statistics
                <p class="text-gray-600">
                    Click on a row to see the list of issues discovered in that file and view a visualisation
                    of the structure.
                </p>
            </div>
            <render-data-table-component v-on:row-selected="loadFile" />
        </el-card>
        <el-card class="mt-4" id="top">
            <span v-show="!loading && selection.file">
                <div slot="header">{{selection.file}}</div>
                <div class="w-full">
                    <el-button type="text" @click="showErrors = !showErrors">
                        <span v-if="showErrors">
                            <font-awesome-icon :icon="['fal', 'minus-square']"></font-awesome-icon>&nbsp;hide errors
                        </span>
                        <span v-if="!showErrors">
                            <font-awesome-icon :icon="['fal', 'plus-square']"></font-awesome-icon>&nbsp;show errors
                        </span>
                    </el-button>
                    <render-issues-component
                        :issues="dataFile.issues"
                        v-if="showErrors && dataFile.issues.length"
                    />
                </div>
                <div class="flex flex-wrap">
                    <div class="w-full xl:w-1/2">
                        <el-card class="mt-4 xl:mr-2 px-6">
                            <div slot="header" class="style-header">
                                A visualisation of the timeslots
                                <p class="text-gray-600">
                                    This visualisation depicts the timeslots and annotations found in the file. The first ring
                                    (from the centre) has a block for each timeslot. Selecting one of the timeslots will zoom the visualisation
                                    to show only that timeslot and its associated annotations. To zoom back out, select the central node.
                                </p>
                            </div>
                            <render-timeslot-sunburst-component
                                :data="dataFile.timeslots"
                                v-if="dataFile.timeslots"
                            />
                        </el-card>
                    </div>
                    <div class="w-full xl:w-1/2">
                        <el-card class="mt-4 xl:ml-2 px-6">
                            <div slot="header" class="style-header">
                                A visualisation of the tiers
                                <p class="text-gray-600">
                                    This visualisation depicts the tiers and annotations found in the file. The first ring
                                    (from the centre) has a block for each tier. Selecting one of the tiers will zoom the visualisation
                                    to show only that tier and its associated annotations. To zoom back out, select the central node.
                                </p>
                            </div>
                            <render-tier-sunburst-component
                                :data="dataFile.tiers"
                                v-if="dataFile.tiers"
                            />
                        </el-card>
                    </div>
                </div>
            </span>
        </el-card>
    </div>
</template>

<script>
import { loadIndex, loadFileData } from "../data-loader.service.js";
import RenderDataTableComponent from "./RenderDataTable.component.vue";
import RenderIssuesComponent from "./RenderIssues.component.vue";
import RenderTimeslotSunburstComponent from "./RenderTimeslotSunburst.component.vue";
import RenderTierSunburstComponent from "./RenderTierSunburst.component.vue";
import VueScrollTo from "vue-scrollto";

export default {
    components: {
        RenderDataTableComponent,
        RenderIssuesComponent,
        RenderTimeslotSunburstComponent,
        RenderTierSunburstComponent
    },
    data() {
        return {
            dataFile: {
                issues: [],
                timeslots: {},
                tiers: {}
            },
            selection: {},
            showErrors: false,
            loading: false
        };
    },
    computed: {
        index: function() {
            return this.$store.state.index;
        }
    },
    mounted() {
        (async () => {
            await loadIndex({ store: this.$store });
        })();
    },
    methods: {
        async loadFile(file) {
            this.loading = true;
            this.dataFile = {
                issues: [],
                tiers: {},
                timeslots: {}
            };
            setTimeout(async () => {
                this.selection = file;
                this.dataFile = await loadFileData({
                    dataFile: file.dataFile
                });
                this.loading = false;
                VueScrollTo.scrollTo("#top", 2000);
            }, 1000);
        }
    }
};
</script>

<style scoped lang="scss">
.style-header {
    height: 120px;
}
</style>