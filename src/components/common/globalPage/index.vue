<template>
  <div>
    <div style="margin-top: 20px">
      <el-pagination
        background
        :page-sizes="[5, 10, 20, 30]"
        :current-page="page"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ElPagination } from "element-plus";
const props = defineProps({
  total: Number,
  page: Number,
  pageSize: Number,
});

const emit = defineEmits(["changePage", "changeSize"]);
const handleCurrentChange = (newPage) => {
  emit("changePage", newPage);
};

const handleSizeChange = (newPageSize) => {
  emit("changeSize", newPageSize);
};
</script>
<style lang=""></style>
