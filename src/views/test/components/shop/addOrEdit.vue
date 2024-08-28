<template>
  <div>
    <el-card>
      <el-form
        class="demo-form-inline"
        style="max-width: 600px"
        label-width="auto"
      >
        <el-form-item label="店铺名称:">
          <el-input
            v-model.trim="formData.shop_name"
            placeholder="请输入店铺名称"
            clearable
          />
        </el-form-item>
        <el-form-item label="店铺ID:">
          <el-input
            v-model.trim="formData.shopId"
            placeholder="请输入店铺ID"
            clearable
          />
        </el-form-item>
        <el-form-item label="店铺地区:">
          <el-input
            v-model.trim="formData.location"
            placeholder="请输入店铺地区"
            clearable
          />
        </el-form-item>
        <el-form-item label="店铺描述:">
          <el-input
            v-model.trim="formData.description"
            placeholder="请输入店铺描述"
            clearable
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit"
            >提交</el-button
          >
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>
<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { ApiAddShopData } from "@/api/shop";
import { getFormData } from "@/utils/server";
import { ElMessage } from "element-plus";
const router = useRouter();
const formData = ref({
  shop_name: "",
  shopId: "",
  location: "",
  description: "",
});
const loading = ref(false);
const handleSubmit = () => {
  const requiredFields = [
    { key: "shop_name", message: "请输入店铺名称" },
    { key: "shopId", message: "请输入店铺ID" },
    { key: "location", message: "请输入店铺地区" },
    { key: "description", message: "请输入店铺描述" },
  ];
  for (let field of requiredFields) {
    if (typeof field.check === "function") {
      if (!field.check(formData.value[field.key])) {
        return showError(field.message);
      }
    } else if (formData.value[field.key] === "") {
      return showError(field.message);
    }
  }
  loading.value = true;
  ApiAddShopData(getFormData(formData.value))
    .then((res) => {
      console.log(res, "新增");
      let resJson = res;
      if (JSON.stringify(resJson) != "{}") {
        ElMessage({
          message: "操作成功",
          type: "success",
        });
      }
      router.push({ path: "/usercenter/shopmanagement/ShopManagement" });
    })
    .finally(() => {
      loading.value = false;
    });
};
const showError = (message) => {
  return ElMessage({
    message: message,
    type: "warning",
  });
};
</script>
<style lang=""></style>
