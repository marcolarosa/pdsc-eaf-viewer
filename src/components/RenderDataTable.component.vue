<template>
    <div>
        <el-form label-width="200px" @submit.native.prevent>
            <el-form-item label="Filter files">
                <el-input v-model="fileFilter" type="text" placeholder="Filter file list..."></el-input>
            </el-form-item>
        </el-form>
        <el-pagination
            background
            layout="total, prev, pager, next"
            :current-page.sync="currentPage"
            :total="total"
        ></el-pagination>
        <el-table
            :data="index"
            :height="height"
            width="800"
            :default-sort="{prop: 'duration', order: 'ascending'}"
            :highlight-current-row="true"
            :row-style="{'cursor': 'pointer'}"
            stripe
            @row-click="triggerRowSelection"
            @sort-change="updateSortParams"
            class="text-md"
        >
            <el-table-column prop="file" label="File" width="300" fixed sortable="custom"></el-table-column>
            <el-table-column prop="duration" label="Duration" width="120" sortable="custom"></el-table-column>
            <el-table-column prop="timeslots" label="# Timeslots" width="150" sortable="custom"></el-table-column>
            <el-table-column prop="totalIssues" label="Issues" width="120" sortable="custom"></el-table-column>
            <el-table-column prop="start" label="Start Time" width="120"></el-table-column>
            <el-table-column prop="end" label="End Time" width="120"></el-table-column>
            <el-table-column
                prop="totalRefAnnotations"
                label="Ref Annotations"
                width="180"
                sortable="custom"
            ></el-table-column>
            <el-table-column
                prop="totalMappedAnnotations"
                label="Mapped Annotations"
                width="200"
                sortable="custom"
            ></el-table-column>
        </el-table>
    </div>
</template>

<script>
import { orderBy } from "lodash";

export default {
    data() {
        return {
            height: 600,
            fileFilter: undefined,
            pageSize: 10,
            currentPage: 1,
            sort: {
                prop: "duration",
                order: "ascending"
            }
        };
    },
    computed: {
        index: function() {
            return orderBy(
                this.$store.state.index.filter(f =>
                    f.file.match(this.fileFilter)
                ),
                [this.sort.prop],
                [this.sort.order]
            ).slice(
                (this.currentPage - 1) * this.pageSize,
                this.currentPage * this.pageSize
            );
        },
        total: function() {
            return this.$store.state.index.filter(f =>
                f.file.match(this.fileFilter)
            ).length;
        }
    },
    methods: {
        triggerRowSelection(row) {
            this.$emit("row-selected", row);
        },
        updateSortParams({ column, prop, order }) {
            this.sort = {
                prop,
                order: order === "descending" ? "desc" : "asc"
            };
        },
    }
};
</script>

<style lang="scss" scoped>
</style>
