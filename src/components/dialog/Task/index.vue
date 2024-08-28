<template>
  <div>
    <el-dialog
      v-model="props.taskDialog"
      title="任务列表"
      :before-close="handleCloseTask"
    >
      <div>
        <el-table
          :data="modelTasksData"
          border
          :header-cell-style="{
            backgroundColor: '#f6f7fc',
            color: '#1f283c',
            fontSize: '14px',
            textAlign: 'left',
          }"
          :cell-style="{ textAlign: 'left' }"
          v-loading="taskLoading"
          @current-change="choiceTask"
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
          <el-table-column prop="shop_name" label="店铺名称" width="180">
            <template #default="scope">
              {{ scope.row.shop_name || "/" }}
            </template>
          </el-table-column>
          <el-table-column prop="createAt" label="创建时间" width="260" />
        </el-table>
      </div>
      <!-- <template #footer>
        <div class="dialog-footer">
          <el-button @click="taskDialog = false">取消</el-button>
          <el-button type="primary" @click="dialogVisible = false">
            确认
          </el-button>
        </div>
      </template> -->
    </el-dialog>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref, defineProps, defineEmits } from "vue";
import { ApiGetTasks } from "@/api/launchmanagement";
const props = defineProps({
  taskDialog: Boolean,
});
const pageObj = reactive({
  page: 1,
  size: 10,
  total: 0,
});
let modelTasksData = ref([]);
let taskLoading = ref(false);
const GetTasks = async () => {
  try {
    taskLoading.value = true;
    const response = await ApiGetTasks(pageObj.page, pageObj.size);
    modelTasksData.value = [...response.tasks];
    pageObj.total = response.total_tasks;
  } finally {
    taskLoading.value = false;
  }
};
GetTasks();
const emit = defineEmits(["handleCloseTask", "choiceTask"]);

const handleCloseTask = (val) => {
  emit("handleCloseTask", false);
};

const choiceTask = (val) => {
  console.log(val, "选中=============");
  emit("choiceTask", val);
  emit("handleCloseTask", false);
};
</script>
<style lang=""></style>
