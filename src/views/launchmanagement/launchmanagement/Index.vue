<template>
  <div>
    <el-card>
      <el-button type="primary" @click="handleAdd">新建建联</el-button>
      <el-button v-if="!first" type="primary" @click="handleGetKey"
        >获取RPA客户端秘钥</el-button
      >
      <span v-if="viewKey != ''" style="padding-left: 10px">
        <span v-if="keyState" style="color: red; padding-right: 10px">{{
          viewKey.substr(0, 3).padEnd(viewKey.length, "*")
        }}</span>
        <span v-if="!keyState" style="color: red; padding-right: 10px">{{
          viewKey
        }}</span>
        <el-button
          size="small"
          @click="keyState = !keyState"
          :type="keyState ? 'danger' : 'info'"
          >{{ keyState ? "展示" : "隐藏" }}</el-button
        >
        <span>&nbsp;&nbsp;(请谨慎保管)</span>
      </span>

      <div style="margin-top: 1.25rem">
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
            prop="total_invitations"
            label="总邀约数"
            width="180"
          >
            <template #default="scope">
              {{ scope.row.willing_quantity || "/" }}
            </template>
          </el-table-column>
          <el-table-column
            prop="send_quantity"
            label="邀约发送成功数"
            width="180"
          >
            <template #default="scope">
              {{ scope.row.send_quantity || "/" }}
            </template>
          </el-table-column>

          <el-table-column prop="shop_name" label="店铺名称" width="180">
            <template #default="scope">
              {{ scope.row.shop_name || "/" }}
            </template>
          </el-table-column>
          <el-table-column prop="createAt" label="创建时间" width="260" />
          <el-table-column fixed="right" label="操作" width="120">
            <template #default="scope">
              <div style="display: flex">
                <el-button
                  v-if="scope.row.status == '未启动'"
                  link
                  type="primary"
                  size="small"
                  @click="handleStart(scope.row.taskId)"
                >
                  建联邀约
                </el-button>
                <el-button
                  v-if="scope.row.status == '未启动'"
                  link
                  type="primary"
                  size="small"
                  @click="handleStart(scope.row.taskId)"
                >
                  私信
                </el-button>
              </div>
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
    </el-card>
    <el-dialog width="500" v-model="dialogVisible" title="获取QTOSS秘钥">
      <el-form label-width="auto" class="demo-form-inline">
        <el-form-item label="QTOSS用户名">
          <el-input
            v-model="modelQtossParams.username"
            placeholder="请输入QTOSS用户名"
            clearable
          />
        </el-form-item>
        <el-form-item label="QTOSS用户密码">
          <el-input
            type="password"
            v-model="modelQtossParams.password"
            placeholder="请输入QTOSS用户密码"
            clearable
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button
            type="primary"
            :loading="submitLoading"
            @click="handleSubmitGetKey"
            >提交</el-button
          >
        </div>
      </template>
    </el-dialog>
    <!-- <el-card style="margin-top: 2rem">
      <el-form :inline="true" class="demo-form-inline" label-width="auto">
        <el-form-item label="任务名称:">
          <el-select
            v-model="taskName"
            value-key="taskId"
            placeholder="请选择任务"
            size="large"
            style="width: 240px"
            @change="handleSelectTask"
          >
            <el-option
              v-for="item in modelTasksData"
              :key="item.taskId"
              :label="item.name"
              :value="item"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="店铺名称:">
          <el-select
            v-model="shopName"
            value-key="shop_id"
            placeholder="请选择店铺"
            size="large"
            style="width: 240px"
            @change="handleSelectShop"
          >
            <el-option
              v-for="item in modelShopData"
              :key="item.shop_id"
              :label="item.shop_name"
              :value="item"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="商品信息:">
          <el-select
            v-model="goodName"
            multiple
            value-key="product_id"
            placeholder="请选择商品"
            size="large"
            style="width: 240px"
            @change="handleSelectGood"
          >
            <el-option
              v-for="item in modelGoodData"
              :key="item.product_id"
              :label="item.title"
              :value="item"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="GetRetrieval">查询</el-button>
        </el-form-item>
      </el-form>
      <div v-for="(item, index) in modelRetrieval" :key="index">
        <div style="width: 200px">{{ item.title }}</div>
        <div style="display: flex; flex-wrap: wrap">
          <div v-for="(sitem, sindex) in item.name" :key="sindex">
            <div style="border: 1px solid; padding: 5px; margin: 10px 10px">
              {{ sitem }}
            </div>
          </div>
        </div>
      </div>
    </el-card> -->
  </div>
</template>
<script setup lang="ts">
import { reactive, ref, onMounted } from "vue";
import {
  ApiGetTasks,
  ApiGetRetrieval,
  ApiStartTasks,
  ApiInvitationCreator,
  ApigetQtossKey,
  ApigetQtossUser,
} from "@/api/launchmanagement";
import { ApigetShop_tasks, ApigetGood_shop } from "@/api/shop";
import { ApiPostSendMsg_Invitation } from "../../../api/rpa";
import { useRouter } from "vue-router";

import { ElMessage, ElMessageBox } from "element-plus";
import { string } from "yup";
const modelTasksData = ref([]);
let formData = reactive({
  task_id: "",
  shop_id: "",
  products: "",
});

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
const GetTasks = () => {
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
};

const changePage = (page: number) => {
  pageObj.page = page;
  GetTasks();
};
const changeSize = (size: number) => {
  pageObj.size = size;
  pageObj.page = 1;
  GetTasks();
};
let dialogVisible = ref(false);
let modelQtossParams = reactive({
  username: "",
  password: "",
});
let viewKey = ref("");
let keyState = ref(true);
let first = ref(false);
const handleGetKey = () => {
  dialogVisible.value = true;
};
let submitLoading = ref(false);

const getQtossKey = () => {
  ApigetQtossKey().then((res) => {
    console.log(res, "========");
    first.value = res.data.has_requested;
    viewKey.value = res.data.key;
  });
};

const handleSubmitGetKey = () => {
  if (modelQtossParams.username == "") {
    return ElMessage({
      message: "请输入用户名",
      type: "warning",
    });
  } else if (modelQtossParams.password == "") {
    return ElMessage({
      message: "请输入密码",
      type: "warning",
    });
  }
  submitLoading.value = true;
  const data = {
    username: modelQtossParams.username,
    password: modelQtossParams.password,
  };
  ApigetQtossUser(data)
    .then((res) => {
      console.log(res, "==========");
      viewKey.value = res.msg;
    })
    .finally(() => {
      submitLoading.value = false;
    });
};
const handleAdd = () => {
  const url = router.resolve({
    path: "/launchmanagement/launchmanagement/components/addOrEdit",
  });
  window.open(url.href, "_blank");
};

const handleStart = (id) => {
  console.log(id);
  ElMessageBox.confirm("一旦启动,不可暂停")
    .then(() => {
      ApiStartTasks(id).then((res) => {
        console.log(res, "启动");
        if (res.code != 200) {
          return ElMessage({
            message: res.errmsg,
            type: "warning",
          });
        }
        ElMessage({
          message: res.msg,
          type: "success",
        });
        const data = {
          taskId: id,
        };
        ApiInvitationCreator(data).then((res) => {
          GetTasks(pageObj.page, pageObj.size);
        });
        // ApiPostSendMsg_Invitation(id).then((res) => {
        //   console.log(res, "rpa");
        // });
      });
    })
    .catch(() => {});
};
onMounted(() => {
  GetTasks();
  getQtossKey();
});

// let taskName = ref("");
// let shopName = ref("");
// let goodName = ref([]);
// let modelShopData = ref([]);
// let modelGoodData = ref([]);
// const handleSelectTask = (item: any) => {
//   // console.log(item);
//   formData.task_id = item.taskId.toString();
//   taskName.value = item.name;
//   shopName.value = "";
//   getShop_tasks(formData.task_id);
// };

// const getShop_tasks = (task_id) => {
//   ApigetShop_tasks(task_id).then((res) => {
//     let shopData = [];
//     shopData.push(res.data);
//     modelShopData.value = shopData;
//   });
// };

// const handleSelectShop = (data: any) => {
//   formData.shop_id = data.shop_id.toString();
//   console.log(formData.shop_id, "formData.shop_id");

//   shopName.value = data.shop_name;
//   modelRetrieval.value = [];
//   getGood_shop(formData.shop_id);
// };
// const getGood_shop = (shop_id) => {
//   ApigetGood_shop(shop_id).then((res) => {
//     console.log(res, "");
//     modelGoodData.value = res.data;
//   });
// };
// const handleSelectGood = (data) => {
//   console.log(data, "data");
//   let modelTag = [];
//   data.forEach((element) => {
//     console.log(element.match_tag, "element");
//     modelTag.push(element.match_tag);
//   });

//   formData.products = modelTag.join(",");
//   // console.log(modelTag, "formDat");
//   modelRetrieval.value = [];
// };
// let modelRetrieval = ref([]);
// const GetRetrieval = () => {
//   if (formData.task_id == "") {
//     return ElMessage({
//       message: "请选择任务",
//       type: "warning",
//     });
//   } else if (formData.shop_id == "") {
//     return ElMessage({
//       message: "请选择店铺",
//       type: "warning",
//     });
//   } else if (formData.products == "") {
//     return ElMessage({
//       message: "请选择商品",
//       type: "warning",
//     });
//   }

//   ApiGetRetrieval(formData).then((res) => {
//     console.log(res, "查询");
//     if (res.code != 200) {
//       return ElMessage({
//         message: res.errmsg,
//         type: "warning",
//       });
//     }
//     let modelData = [];
//     // modelData.push(res.data);
//     //
//     // console.log(modelRetrieval.value, "modelRetrieval.value");

//     let str = JSON.stringify(res.data);
//     let obj = JSON.parse(str);
//     console.log(obj);
//     for (var key in obj) {
//       if (obj.hasOwnProperty(key)) {
//         // 确保属性是对象自身的属性
//         var value = obj[key];
//         modelData.push({
//           title: key,
//           name: value,
//         });
//         console.log(key, value); // 输出键和值
//       }
//     }
//     modelRetrieval.value = modelData;
//     console.log(modelData, "=modelData");
//   });
// };
</script>
<style lang=""></style>
