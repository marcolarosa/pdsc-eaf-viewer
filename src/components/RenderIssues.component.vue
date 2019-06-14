<template>
    <div>
        <el-table :data="issues" :height="height" stripe>
            <el-table-column prop="msg" label="Error" sortable></el-table-column>
        </el-table>
    </div>
</template>

<script>
export default {
    props: {
        issues: {
            type: Array
        }
    },
    data() {
        return {
            height: 300
        };
    }
};
</script>

<style lang="scss" scoped>
</style>

