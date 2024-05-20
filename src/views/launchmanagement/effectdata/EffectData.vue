<template>
  <div>
    <div class="data_content">
      <div class="grid5">
        <div class="grid5_value">
          {{ pageObj.total }}
        </div>
        <div>任务数</div>
      </div>
      <div class="grid5">
        <div class="grid5_value">
          {{ productsTotal }}
        </div>
        <div>产品数</div>
      </div>
      <div class="grid5">
        <div class="grid5_value">
          {{ modelSummary.willing_quantity_sum }}
        </div>
        <div>达人沟通数</div>
      </div>
      <div class="grid5">
        <div class="grid5_value">
          {{ modelSummary.send_quantity_sum }}
        </div>
        <div>有效回复数</div>
      </div>
      <div class="grid5">
        <div style="line-height: 50px">
          {{ modelSummary.match_quantity_sum }}
        </div>
        <div>合作意向数</div>
      </div>
    </div>
    <div style="margin-top: 2rem">
      <el-table
        v-loading="loading"
        :data="modelTasksData"
        border
        :header-cell-style="{
          backgroundColor: '#f6f7fc',
          color: '#1f283c',
          fontSize: '14px',
          textAlign: 'center',
        }"
        :cell-style="{ textAlign: 'center' }"
      >
        <el-table-column label="建立任务名称" width="200">
          <template #default="scope">
            {{ scope.row.name }}
          </template>
        </el-table-column>
        <el-table-column prop="product_title" label="物品名称" width="350" />
        <el-table-column label="任务状态" width="120">
          <template #default="scope">
            {{ scope.row.status }}
          </template>
        </el-table-column>
        <el-table-column
          prop="send_quantity"
          label="已发送邮件人数"
          width="150"
        >
          <template #default="scope">
            {{ scope.row.send_quantity || "/" }}
          </template>
        </el-table-column>
        <el-table-column prop="willing_quantity" label="回复人数" width="150">
          <template #default="scope">
            {{ scope.row.willing_quantity || "/" }}
          </template>
        </el-table-column>
        <el-table-column prop="match_quantity" label="合作意向数" width="180">
          <template #default="scope">
            {{ scope.row.match_quantity || "/" }}
          </template>
        </el-table-column>
        <el-table-column prop="createAt" label="创建时间" width="180" />
        <el-table-column fixed="right" label="查看合作用户详情" width="180">
          <template #default="scope">
            <el-button
              link
              type="primary"
              size="small"
              @click="handleJumpDetail(scope.row)"
            >
              查看
            </el-button>
          </template>
        </el-table-column>
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
  </div>
</template>
<script setup lang="ts">
import { reactive, ref } from "vue";
import {
  ApiGetTasks,
  ApiGetProducts,
  ApiGetSummary,
} from "@/api/launchmanagement";
const modelTasksData = ref([]);
let loading = ref(false);
const pageObj = reactive({
  page: 1,
  size: 10,
  total: 0,
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

const handleJumpDetail = (row) => {
  console.log(row, "=========");
};

let productsTotal = ref();
ApiGetProducts("", 1, 10).then((res) => {
  productsTotal.value = res.total_products;
});
const modelSummary = reactive({
  match_quantity_sum: "",
  send_quantity_sum: "",
  willing_quantity_sum: "",
});
ApiGetSummary().then((res) => {
  modelSummary.match_quantity_sum = res.data.match_quantity_sum;
  modelSummary.send_quantity_sum = res.data.send_quantity_sum;
  modelSummary.willing_quantity_sum = res.data.willing_quantity_sum;
});
</script>
<style scoped lang="scss">
.data_content {
  display: flex;
  justify-content: space-around;
  .grid5 {
    width: 10rem;
    height: 10rem;
    background: #4471c4;
    border-radius: 50%;
    text-align: center;
    color: #fff;
    .grid5_value {
      line-height: 5rem;
    }
  }
}
</style>
