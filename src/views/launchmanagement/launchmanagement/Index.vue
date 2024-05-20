<template>
  <div>
    <el-card>
      <el-button type="primary" @click="handleAdd">新建建联</el-button>
      <div style="margin-top: 1.25rem">
        <el-table
          :data="modelTasksData"
          border
          :header-cell-style="{
            backgroundColor: '#f6f7fc',
            color: '#1f283c',
            fontSize: '14px',
            textAlign: 'center',
          }"
          :cell-style="{ textAlign: 'center' }"
          v-loading="loading"
        >
          <el-table-column label="建立任务名称" width="225">
            <template #default="scope">
              {{ scope.row.name }}
            </template>
          </el-table-column>
          <el-table-column prop="product_title" label="物品名称" width="450" />
          <el-table-column label="任务状态" width="180">
            <template #default="scope">
              {{ scope.row.status }}
            </template>
          </el-table-column>
          <el-table-column
            prop="send_quantity"
            label="已发送邮件人数"
            width="180"
          >
            <template #default="scope">
              {{ scope.row.send_quantity || "/" }}
            </template>
          </el-table-column>
          <el-table-column prop="willing_quantity" label="回复人数" width="180">
            <template #default="scope">
              {{ scope.row.willing_quantity || "/" }}
            </template>
          </el-table-column>
          <el-table-column prop="createAt" label="创建时间" width="260" />
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
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
const modelTasksData = ref([]);
let loading = ref(false);
const pageObj = reactive({
  page: 1,
  size: 10,
  total: 0,
});
const router = useRouter();
const statusMap = ref({
  1: "未启动",
  2: "正在进行",
  3: "已经完成",
});

ApiGetTasks(pageObj.page, pageObj.size)
  .then((res) => {
    loading.value = true;
    console.log(res, "查询");
    if (res.code != 200) {
      return ElMessage({
        message: res.errmsg,
        type: "warning",
      });
    }
    modelTasksData.value = [...res.tasks];
    pageObj.total = res.total_tasks;
  })
  .finally(() => {
    loading.value = false;
  });

const changePage = (page: number) => {
  ApiGetTasks(page, pageObj.size);
};
const changeSize = (size: number) => {
  ApiGetTasks(pageObj.page, size);
};

const handleAdd = () => {
  const url = router.resolve({
    path: "/launchmanagement/launchmanagement/components/addOrEdit",
  });
  window.open(url.href, "_blank");
};
</script>
<style lang=""></style>
