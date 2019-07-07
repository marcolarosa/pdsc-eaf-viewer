<template>
    <div class="mx-auto font-mono p-2">
        <folder-selection-component />
        <el-card class="px-6 mt-4" v-if="Object.keys(index).length">
            <div slot="header">
                File Statistics
                <p class="text-gray-600">
                    Click on a row to see the list of issues discovered in that file and view a visualisation
                    of the structure.
                </p>
            </div>
            <render-data-table-component v-on:row-selected="loadFile" />
        </el-card>
        <span id="top"></span>
        <el-card class="mt-4" v-if="!loading && selection.file && index.length">
            <div slot="header">{{selection.file}}</div>
            <!-- <div class="w-full">
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
            </div>-->
            <div class="flex flex-wrap">
                <div class="w-full xxl:w-1/2">
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
                            :data="selection.timeslots"
                            v-if="selection.timeslots"
                        />
                    </el-card>
                </div>
                <div class="w-full xxl:w-1/2">
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
                            :data="selection.tiers"
                            v-if="selection.tiers"
                        />
                    </el-card>
                </div>
            </div>
        </el-card>
    </div>
</template>

<script>
import { loadFileData } from "../renderer/data-loader.service.js";
import RenderDataTableComponent from "./RenderDataTable.component.vue";
import RenderIssuesComponent from "./RenderIssues.component.vue";
import RenderTimeslotSunburstComponent from "./RenderTimeslotSunburst.component.vue";
import RenderTierSunburstComponent from "./RenderTierSunburst.component.vue";
import FolderSelectionComponent from "./FolderSelection.component.vue";
import VueScrollTo from "vue-scrollto";

export default {
    components: {
        FolderSelectionComponent,
        RenderDataTableComponent,
        RenderIssuesComponent,
        RenderTimeslotSunburstComponent,
        RenderTierSunburstComponent
    },
    data() {
        return {
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
    mounted() {},
    methods: {
        async loadFile(item) {
            this.loading = true;
            this.selection = {};
            setTimeout(async () => {
                this.selection = item;
                this.loading = false;
                VueScrollTo.scrollTo("#top", 1000);
            }, 1000);
        }
    }
};
</script>

<style scoped lang="scss">
.style-header {
    height: 120px;
}

.style-white {
    background-color: white;
    height: 100px;
}
</style>