<template>
  <div>
    <div class="data_content">
      <div class="grid5">
        <div class="grid5_value">
          {{ pageObj.total || "-" }}
        </div>
        <div>任务数</div>
      </div>
      <div class="grid5">
        <div class="grid5_value">
          {{ productsTotal || "-" }}
        </div>
        <div>产品数</div>
      </div>
      <div class="grid5">
        <div class="grid5_value">
          {{ modelSummary.total_invitations_sum || "-" }}
        </div>
        <div>总邀约数</div>
      </div>
      <div class="grid5">
        <div class="grid5_value">
          {{ modelSummary.willing_quantity_sum || "-" }}
        </div>
        <div>总邀约发送成功数</div>
      </div>

      <div class="grid5">
        <div class="grid5_value">
          {{ modelSummary.send_quantity_sum || "-" }}
        </div>
        <div>总邀约回复数</div>
      </div>
      <!-- <div class="grid5">
        <div class="grid5_value">
          {{ modelSummary.match_quantity_sum }}
        </div>
        <div>合作意向数</div>
      </div> -->
    </div>
    <div style="margin-top: 2rem">
      <el-table
        v-loading="loading"
        :data="modelTasksData"
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
        <el-table-column prop="total_invitations" label="总邀约数" width="180">
          <template #default="scope">
            {{ scope.row.total_invitations || "/" }}
          </template>
        </el-table-column>
        <el-table-column
          prop="send_quantity"
          label="邀约发送成功数"
          width="180"
        />

        <el-table-column prop="willing_quantity" label="邀约回复数" width="150">
          <template #default="scope">
            {{ scope.row.willing_quantity || "/" }}
          </template>
        </el-table-column>
        <el-table-column
          prop="match_quantity"
          label="达人同意合作数"
          width="180"
        >
          <template #default="scope">
            {{ scope.row.match_quantity || "/" }}
          </template>
        </el-table-column>

        <el-table-column fixed="right" label="查看投放任务详情">
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
      <el-dialog width="50%" v-model="userDialog" title="合作用户信息">
        <el-table
          v-loading="taskLoading"
          :data="modelRpaTasksData"
          :header-cell-style="{
            backgroundColor: '#f6f7fc',
            color: '#1f283c',
            fontSize: '14px',
            textAlign: 'left',
          }"
          :cell-style="{ textAlign: 'left' }"
        >
          <el-table-column prop="type" label="类型" width="100">
            <template #default="scope">
              <div>
                {{ modelTypeMap[scope.row.type] }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="360">
            <template #default="scope">
              <div>
                {{ modelStatusMap[scope.row.status] }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="region" label="国家/地区" />
          <el-table-column fixed="right" label="操作">
            <template #default="scope">
              <el-button
                link
                v-if="
                  scope.row.status == 3 ||
                  scope.row.status == 5 ||
                  scope.row.status == 8
                "
                type="primary"
                size="small"
                @click="handleViewCreator(scope.row)"
              >
                查看达人
              </el-button>
              <el-button
                v-if="scope.row.status == 4"
                link
                type="primary"
                size="small"
                @click="handleRest(scope.row)"
              >
                重新邀约
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <GlobalPage
          :page="taskPageObj.page"
          :pageSize="taskPageObj.size"
          :total="taskPageObj.total"
          @changePage="changeTaskPage"
          @changeSize="changeTaskSize"
        />
      </el-dialog>
    </div>
    <!-- 邀约达人 -->
    <div>
      <el-dialog v-model="CreatorDataDialo" width="50%">
        <div>
          <el-table
            :data="modelCreatorData"
            :header-cell-style="{
              backgroundColor: '#f6f7fc',
              color: '#1f283c',
              fontSize: '14px',
              textAlign: 'left',
            }"
            :cell-style="{ textAlign: 'left' }"
          >
            <el-table-column prop="nick_name" label="昵称" width="180" />
            <el-table-column prop="user_name" label="名称" />
            <el-table-column prop="selection_region" label="区域" />
            <el-table-column prop="product_add_cnt" label="添加产品内容数量" />
            <el-table-column
              prop="content_posted_cnt"
              label="发布产品内容数量"
            />
          </el-table>
          <div>
            <GlobalPage
              :page="CreatorPageObj.page"
              :pageSize="CreatorPageObj.size"
              :total="CreatorPageObj.total"
              @changePage="changeCreatorPage"
              @changeSize="changeCreatorSize"
            />
          </div>
        </div>
      </el-dialog>
    </div>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import {
  ApiGetTasks,
  ApiGetProducts,
  ApiGetSummary,
  ApiGetRpaTasks,
  ApiGetTaskCreator,
  ApiResetTask,
  ApiGetCreatorCount,
} from "@/api/launchmanagement";
import { ElMessage } from "element-plus";
const router = useRouter();
const modelTasksData = ref([]);
const modelTypeMap = reactive({
  1: "素人私信",
  2: "达人签约",
  3: "达人私信",
});
const modelStatusMap = reactive({
  1: "等待RPA接收任务",
  2: "RPA正在处理发送任务",
  3: "任务已成功执行并等待响应",
  4: "执行失败或应用程序错误，需要重试",
  5: "任务已成功执行并收到响应",
  7: "请求无效或违反规则，无需重试",
  8: "任务已完成",
  11: "用户已取消任务",
});
let loading = ref(false);
const pageObj = reactive({
  page: 1,
  size: 10,
  total: 0,
});
const GetTasks = () => {
  loading.value = true;
  ApiGetTasks(pageObj.page, pageObj.size)
    .then((res) => {
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
};
const GetCreatorCount = () => {
  ApiGetCreatorCount().then((res: any) => {
    console.log(res, "==========");
  });
};
const changePage = (page: number) => {
  pageObj.page = page;
  GetTasks();
};
const changeSize = (size: number) => {
  pageObj.size = size;
  pageObj.page = 1;
  GetTasks();
  // ApiGetTasks(pageObj.page, size);
};

const userDialog = ref(false);
const userObj = ref();
const taskId = ref("");
const handleJumpDetail = (row) => {
  userDialog.value = true;
  userObj.value = row.user;
  taskId.value = row.taskId;
  modelRpaTasksData.value = [];
  taskPageObj.page = 1;
  taskPageObj.size = 10;
  taskPageObj.total = null;
  GetRpaTasks(row.taskId);
};

const taskPageObj = {
  page: 1,
  size: 10,
  total: null,
};
const taskLoading = ref(false);
// 查询投放任务
let modelRpaTasksData = ref([]);
const GetRpaTasks = () => {
  taskLoading.value = true;
  ApiGetRpaTasks(taskId.value, taskPageObj.page, taskPageObj.size)
    .then((res: any) => {
      console.log(res, "任务列表");
      if (res.code !== 200) {
        return;
      }
      modelRpaTasksData.value = res.data;
      taskPageObj.total = res.total_tasks;
    })
    .finally(() => {
      taskLoading.value = false;
    });
};
const changeTaskPage = (page: number) => {
  taskPageObj.page = page;
  GetRpaTasks();
};
const changeTaskSize = (size: number) => {
  taskPageObj.size = size;
  GetRpaTasks();
};

// 重新 邀约
const handleRest = (row: Object) => {
  const taskId = row.taskId;
  ApiResetTask(taskId).then((res: any) => {
    console.log(res, "=========");
    if (res.code != 200) {
      return ElMessage({
        message: res.errmsg,
        type: "warning",
      });
    }
    GetRpaTasks();
  });
};

// 查看达人
let modelCreatorData = ref([]);
let CreatorDataDialo = ref(false);
let CreatorPageObj = {
  taskId: "",
  page: 1,
  size: 10,
  total: 0,
};
const handleViewCreator = (row: Object) => {
  CreatorDataDialo.value = true;
  CreatorPageObj.taskId = row || row.taskId;
  ApiGetTaskCreator(row.taskId, CreatorPageObj.page, CreatorPageObj.size).then(
    (res: any) => {
      modelCreatorData.value = res.creators;
      CreatorPageObj.total = res.total_creators;
    }
  );
};
const changeCreatorPage = (page: Number) => {
  CreatorPageObj.page = page;
  handleViewCreator(CreatorPageObj.taskId);
};
const changeCreatorSize = (size: Number) => {
  CreatorPageObj.size = page;
  CreatorPageObj.page = 1;
  handleViewCreator(CreatorPageObj.taskId);
};

let productsTotal = ref();
ApiGetProducts("", 1, 10).then((res) => {
  productsTotal.value = res.total_products;
});
const modelSummary = reactive({
  match_quantity_sum: "",
  send_quantity_sum: "",
  willing_quantity_sum: "",
  total_invitations_sum: "",
});
ApiGetSummary().then((res) => {
  modelSummary.match_quantity_sum = res.data.match_quantity_sum;
  modelSummary.send_quantity_sum = res.data.send_quantity_sum;
  modelSummary.willing_quantity_sum = res.data.willing_quantity_sum;
  modelSummary.total_invitations_sum = res.data.total_invitations_sum;
});
onMounted(() => {
  GetTasks();
  GetCreatorCount();
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
