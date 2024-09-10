<template>
  <div>
    <el-card>
      <div style="display: flex">
        <div style="margin-right: 10px">
          <el-select
            clearable
            @change="changeShop"
            v-model="ShopId"
            placeholder="请选择店铺"
            style="width: 240px"
          >
            <el-option
              v-for="item in ShopOptions"
              :key="item.shopId"
              :label="item.shop_name"
              :value="item.shopId"
            />
          </el-select>
        </div>
        <el-button type="primary" @click="handleAdd">新增物品</el-button>
        <el-button type="primary" @click="handleUpdata" v-preventReClick="2000"
          >上传CSV文件
          <input
            ref="fileInput"
            type="file"
            @change="handleFileChange"
            style="display: none"
            class="custom-input"
          />
        </el-button>
        <el-button type="success" @click="handleExport" v-preventReClick="2000"
          >导出</el-button
        >
      </div>
      <div style="margin-top: 1.25rem" v-if="ShopId && ShopId != ''">
        <Good ref="GoodRef" :ShopId="ShopId" />
      </div>
    </el-card>
    <el-card style="margin-top: 1.25rem">
      <Rules />
    </el-card>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref, onMounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import { ApiExportProducts, ApiGetShop } from "@/api/launchmanagement";

import { ElMessage, ElMessageBox } from "element-plus";
import axios from "axios";
const router = useRouter();
import Good from "./components/goods.vue";
import Rules from "./components/rules.vue";
const pageObj = {
  page: 1,
  size: 10,
  total: null,
};
const ShopId = ref("");
const ShopOptions = ref([]);
const GetShop = () => {
  ApiGetShop().then((res) => {
    ShopOptions.value = res.data;
  });
};

const changeShop = (id) => {
  ShopId.value = id;
  nextTick(() => {
    GoodRef.value.GetProducts(ShopId.value);
  });
};

const handleExport = () => {
  ApiExportProducts();
};
const fileInput = ref(null);
const handleUpdata = () => {
  fileInput.value.click();
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    uploadCSV(file);
    event.target.value = "";
  }
};
const GoodRef = ref(null);
const uploadCSV = (file) => {
  const formData = new FormData();
  formData.append("csv_file", file);
  axios
    .post("user/upload_csv", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
    .then((res) => {
      if (res.data.code != 200) {
        return ElMessage({
          message: res.data.errmsg,
          type: "warning",
        });
      }
      ElMessage({
        message: "上传成功",
        type: "success",
      });
      GoodRef.value.GetProducts();
    })
    .catch((err) => {
      ElMessage({
        message: err.response.data.errmsg,
        type: "warning",
      });
    });
};
const handleAdd = () => {
  const url = router.resolve({
    path: "/launchmanagement/itemmanagement/components/addOrEdit",
  });
  window.open(url.href, "_blank");
};

onMounted(() => {
  GetShop();
});
</script>
<style></style>
