<template>
  <div>
    <el-card>
      <el-button type="primary" @click="handleAdd">新建建联</el-button>
      <div>
        <el-table :data="modelTasksData">
          <el-table-column prop="date" label="建立任务名称" width="180" />
          <el-table-column prop="product_title" label="物品名称" width="180" />
          <el-table-column label="任务状态" width="180">
            <template #default="scope">
              {{ scope.row.status }}
            </template>
          </el-table-column>
          <el-table-column
            prop="send_quantity"
            label="已发送邮件人数"
            width="180"
          />
          <el-table-column
            prop="willing_quantity"
            label="回复人数"
            width="180"
          />
          <el-table-column prop="createAt" label="创建时间" width="180" />
        </el-table>
        <div>
          <GlobalPage
            :page="pageObj.page"
            :pageSize="pageObj.size"
            :total="pageObj.total"
            @changePage="changePage"
            @changeSize="changeSize"
          />
        </div>
      </div>
    </el-card>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref } from "vue";
import { ApiGetTasks } from "@/api/launchmanagement";
const modelTasksData = ref([]);
const pageObj = reactive({
  page: 1,
  size: 10,
  total: 0,
});

const statusMap = ref({
  1: "未启动",
  2: "正在进行",
  3: "已经完成",
});

ApiGetTasks(pageObj.page, pageObj.size).then((res) => {
  console.log(res, "查询");
  if (res.code != 200) {
    return ElMessage({
      message: res.errmsg,
      type: "warning",
    });
  }
  modelTasksData.value = [...res.tasks];
  pageObj.total = res.total_tasks;
});

const changePage = (page: number) => {
  ApiGetTasks(page, pageObj.size);
};
const changeSize = (size: number) => {
  ApiGetTasks(pageObj.page, size);
};

const handleAdd = () => {};
</script>
<style lang=""></style>
