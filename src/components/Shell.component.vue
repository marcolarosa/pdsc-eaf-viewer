<template>
    <div class="container mx-auto font-mono p-4">
        <!-- <pre>{{index}}</pre> -->
        <render-data-table-component/>
    </div>
</template>

<script>
import { loadData } from "../data-loader.service.js";
import RenderDataTableComponent from "./RenderDataTable.component.vue";

export default {
    components: {
        RenderDataTableComponent
    },
    data() {
        return {};
    },
    computed: {
        index: function() {
            return this.$store.state.index;
        }
    },
    mounted() {
        (async () => {
            await loadData({ store: this.$store });
        })();
    }
};
</script>

<style scoped lang="scss">
</style>