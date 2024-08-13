<template>
  <div>
    <el-card style="margin-top: 2rem">
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
          <!--  -->
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
    </el-card>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref } from "vue";
import { ApiGetTasks, ApiGetRetrieval } from "@/api/launchmanagement";
import { ApigetShop_tasks, ApigetGood_shop } from "@/api/shop";
import { ElMessage, ElMessageBox } from "element-plus";
const modelTasksData = ref([]);
const pageObj = reactive({
  page: 1,
  size: 10,
  total: 0,
});
let formData = reactive({
  task_id: "",
  shop_id: "",
  products: "",
});

const GetTasks = () => {
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
    .finally(() => {});
};
GetTasks();
let taskName = ref("");
let shopName = ref("");
let goodName = ref([]);
let modelShopData = ref([]);
let modelGoodData = ref([]);
let modelRetrieval = ref([]);
const handleSelectTask = (item: any) => {
  if (item && item.taskId) {
    formData.task_id = item.taskId.toString();
  } else {
    formData.task_id = "";
  }
  setFormFieldValue(taskName, item ? item.name : "");
  setFormFieldValue(shopName, "");
  formData.shop_id = "";
  setFormFieldArrayValue(goodName, []);
  formData.products = "";
  setFormFieldArrayValue(modelRetrieval, []);
  getShop_tasks(formData.task_id);
};

const setFormFieldValue = (field, value) => {
  if (field) {
    field.value = value;
  }
};

const setFormFieldArrayValue = (field, value) => {
  if (field) {
    field.value = value;
  }
};

const getShop_tasks = (task_id) => {
  ApigetShop_tasks(task_id).then((res) => {
    let shopData = [];
    shopData.push(res.data);
    modelShopData.value = shopData;
  });
};

const handleSelectShop = (data: any) => {
  formData.shop_id = data.shop_id.toString();
  shopName.value = data.shop_name;
  modelRetrieval.value = [];
  getGood_shop(formData.shop_id);
};
const getGood_shop = (shop_id) => {
  ApigetGood_shop(shop_id).then((res) => {
    console.log(res, "");
    modelGoodData.value = res.data;
  });
};
const handleSelectGood = (data) => {
  console.log(data, "data");
  let modelTag = [];
  data.forEach((element) => {
    console.log(element.match_tag, "element");
    modelTag.push(element.match_tag);
  });

  formData.products = modelTag.join(",");
  // console.log(modelTag, "formDat");
  modelRetrieval.value = [];
};

const GetRetrieval = () => {
  if (formData.task_id == "") {
    return ElMessage({
      message: "请选择任务",
      type: "warning",
    });
  } else if (formData.shop_id == "") {
    return ElMessage({
      message: "请选择店铺",
      type: "warning",
    });
  } else if (formData.products == "") {
    return ElMessage({
      message: "请选择商品",
      type: "warning",
    });
  }

  ApiGetRetrieval(formData).then((res) => {
    console.log(res, "查询");
    if (res.code != 200) {
      return ElMessage({
        message: res.errmsg,
        type: "warning",
      });
    }
    let modelData = [];
    // modelData.push(res.data);
    //
    // console.log(modelRetrieval.value, "modelRetrieval.value");

    let str = JSON.stringify(res.data);
    let obj = JSON.parse(str);
    console.log(obj);
    for (var key in obj) {
      if (obj.hasOwnProperty(key)) {
        var value = obj[key];
        modelData.push({
          title: key,
          name: value,
        });
        // console.log(key, value); // 输出键和值
      }
    }
    console.log(modelRetrieval, "modelRetrieval");

    modelRetrieval.value = modelData;
    console.log(modelData, "=modelData");
  });
};
</script>
<style lang=""></style>
