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
        <div class="grid5_value">
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
    <!-- 投放任务 -->
    <div>
      <el-dialog v-model="userDialog" title="合作用户信息">
        <el-table
          :data="modelRpaTasksData"
          :header-cell-style="{
            backgroundColor: '#f6f7fc',
            color: '#1f283c',
            fontSize: '14px',
            textAlign: 'center',
          }"
          :cell-style="{ textAlign: 'center' }"
        >
          <el-table-column prop="type" label="类型" width="180">
            <template #default="scope">
              <div>
                {{ modelTypeMap[scope.row.type] }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="180">
            <template #default="scope">
              <div>
                {{ modelStatusMap[scope.row.status] }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="message" label="消息" width="250" />
          <el-table-column fixed="right" label="操作">
            <template #default="scope">
              <el-button
                link
                type="primary"
                size="small"
                @click="handleViewCreator(scope.row)"
              >
                查看达人
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-dialog>
    </div>
    <!-- 邀约达人 -->
    <div>
      <el-dialog v-model="CreatorDataDialo">
        <div>
          <el-table
            :data="modelCreatorData"
            :header-cell-style="{
              backgroundColor: '#f6f7fc',
              color: '#1f283c',
              fontSize: '14px',
              textAlign: 'center',
            }"
            :cell-style="{ textAlign: 'center' }"
          >
            <!-- <el-table-column prop="creator_id" label="达人ID" width="220" /> -->
            <el-table-column prop="nick_name" label="昵称" width="180" />
            <el-table-column prop="user_name" label="名称" />
            <el-table-column prop="selection_region" label="区域" />
            <el-table-column prop="product_add_cnt" label="添加产品内容数量" />
            <el-table-column
              prop="content_posted_cnt"
              label="发布产品内容数量"
            />
          </el-table>
        </div>
      </el-dialog>
    </div>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import {
  ApiGetTasks,
  ApiGetProducts,
  ApiGetSummary,
  ApiGetRpaTasks,
  ApiGetTaskCreator,
} from "@/api/launchmanagement";
const router = useRouter();
const modelTasksData = ref([]);
const modelTypeMap = reactive({
  1: "素人私信",
  2: "达人签约",
  3: "达人私信",
});
const modelStatusMap = reactive({
  1: "等待接收任务",
  2: "正在处理发送任务",
  3: "执行失败或应用程序错误，需要重试",
  4: "任务已成功执行并收到响应",
  5: "请求无效或违反规则，无需重试",
  7: "任务已完成",
  8: "完成",
  11: "取消",
});
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

const userDialog = ref(false);
const userObj = ref();
const handleJumpDetail = (row) => {
  userDialog.value = true;
  userObj.value = row.user;
  GetRpaTasks(row.taskId);
};

// 查询投放任务
let modelRpaTasksData = ref([]);
const GetRpaTasks = (id: String) => {
  ApiGetRpaTasks(id).then((res: any) => {
    console.log(res, "任务列表");
    modelRpaTasksData.value = res.data;
  });
};
// 查看达人
let modelCreatorData = ref([]);
let CreatorDataDialo = ref(false);
const handleViewCreator = (row: Object) => {
  console.log(row, "-------------");
  CreatorDataDialo.value = true;
  ApiGetTaskCreator(row.taskId).then((res: any) => {
    console.log(res, "达人=========");
    modelCreatorData.value = res.creators;
  });
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
