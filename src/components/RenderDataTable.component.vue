<template>
    <div>
        <el-form label-width="200px" @submit.native.prevent>
            <el-form-item label="Filter files">
                <el-input v-model="fileFilter" type="text" placeholder="Filter file list..."></el-input>
            </el-form-item>
        </el-form>
        <el-table
            :data="index"
            :height="height"
            width="800"
            :default-sort="{prop: 'file', order: 'ascending'}"
            :highlight-current-row="true"
            stripe
            @row-click="triggerRowSelection"
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
export default {
    data() {
        return {
            height: 300,
            dataColumnWidth: 280,
            fileFilter: undefined
        };
    },
    computed: {
        index: function() {
            return this.$store.state.index.filter(f =>
                f.file.match(this.fileFilter)
            );
        }
    },
    methods: {
        triggerRowSelection(row) {
            this.$emit("row-selected", row);
        }
    }
};
</script>

<style lang="scss" scoped>
</style>
