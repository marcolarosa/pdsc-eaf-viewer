<template>
    <div class="container mx-auto font-mono p-4">
        <el-card>
            <div slot="header">
                File Statistics
                <p class="text-gray-600">
                    Click on a row to see the list of issues discovered in that file and view a visualisation
                    of the structure.
                </p>
            </div>
            <render-data-table-component v-on:row-selected="loadFileData"/>
        </el-card>
        <div class="flex">
            <div class="w-1/2">
                <el-card class="mt-4">
                    <div slot="header">Selected File Issues</div>
                    <render-issues-component :issues="dataFile.issues" v-if="dataFile"/>
                </el-card>
            </div>
        </div>
    </div>
</template>

<script>
import { loadIndex, loadFileData } from "../data-loader.service.js";
import RenderDataTableComponent from "./RenderDataTable.component.vue";
import RenderIssuesComponent from "./RenderIssues.component.vue";

export default {
    components: {
        RenderDataTableComponent,
        RenderIssuesComponent
    },
    data() {
        return {
            dataFile: undefined
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
        async loadFileData(file) {
            this.dataFile = await loadFileData({ dataFile: file.dataFile });
        }
    }
};
</script>

<style scoped lang="scss">
</style>