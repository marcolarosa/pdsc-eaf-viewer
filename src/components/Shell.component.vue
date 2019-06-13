<template>
    <div class="container mx-auto font-mono">
        <!-- <pre>{{index}}</pre> -->
        <el-table
            :data="index"
            :height="height"
            width="800"
            :default-sort="{prop: 'file', order: 'ascending'}"
            stripe
            class="text-lg"
        >
            <el-table-column prop="file" label="File" width="500" fixed sortable></el-table-column>
            <el-table-column prop="start" label="Start Time" :width="dataColumnWidth"></el-table-column>
            <el-table-column prop="end" label="End Time" :width="dataColumnWidth"></el-table-column>
            <el-table-column prop="duration" label="Duration" :width="dataColumnWidth" sortable></el-table-column>
            <el-table-column prop="timeslots" label="# Timeslots" :width="dataColumnWidth" sortable></el-table-column>
            <el-table-column
                prop="totalRefAnnotations"
                label="# Ref Annotations"
                :width="dataColumnWidth"
                sortable
            ></el-table-column>
            <el-table-column
                prop="totalMappedAnnotations"
                label="# Mapped Annotations"
                :width="dataColumnWidth"
                sortable
            ></el-table-column>
            <el-table-column prop="totalIssues" label="Issues" :width="dataColumnWidth" sortable></el-table-column>
        </el-table>
    </div>
</template>

<script>
import { loadData } from "../data-loader.service.js";

export default {
    data() {
        return {
            height: 500,
            dataColumnWidth: 280
        };
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