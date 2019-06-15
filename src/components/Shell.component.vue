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
            <render-data-table-component v-on:row-selected="loadFileData"/>
        </el-card>
        <div class="flex flex-wrap" v-show="selection.file">
            <div class="w-full xl:w-2/5">
                <el-card class="mt-4 xl:mr-2 px-6">
                    <div slot="header">{{selection.file}}</div>
                    <render-issues-component :issues="dataFile.issues" v-if="dataFile"/>
                </el-card>
            </div>
            <div class="w-full xl:w-3/5">
                <el-card class="mt-4 xl:ml-2 px-6">
                    <div slot="header">
                        {{selection.file}}
                        <p class="text-gray-600">
                            Click on the first ring to zoom in to a timeslot or on the center to zoom back out. Hover over
                            any element to see the trail.
                        </p>
                    </div>
                    <render-sunburst-component :data="dataFile.data" v-if="dataFile"/>
                </el-card>
            </div>
        </div>
    </div>
</template>

<script>
import { loadIndex, loadFileData } from "../data-loader.service.js";
import RenderDataTableComponent from "./RenderDataTable.component.vue";
import RenderIssuesComponent from "./RenderIssues.component.vue";
import RenderSunburstComponent from "./RenderSunburst.component.vue";

export default {
    components: {
        RenderDataTableComponent,
        RenderIssuesComponent,
        RenderSunburstComponent
    },
    data() {
        return {
            dataFile: undefined,
            selection: {}
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
            // this.loadFileData(
            //     this.$store.state.index.filter(
            //         f => f.file === "NT5-TokelauOf-vid.eaf"
            //     )[0]
            // );
            // this.loadFileData(this.$store.state.index[0]);
        })();
    },
    methods: {
        async loadFileData(file) {
            this.selection = file;
            this.dataFile = await loadFileData({
                dataFile: file.dataFile
            });
        }
    }
};
</script>

<style scoped lang="scss">
</style>