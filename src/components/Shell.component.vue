<template>
    <div class="container mx-auto font-mono p-4">
        <render-data-table-component v-on:row-selected="loadFileData"/>
        <div class="flex">
            <div class="w-1/2">
                <render-issues-component :issues="dataFile.issues" v-if="dataFile"/>
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