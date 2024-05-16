<template>
  <div>
    <el-card>
      <el-form
        class="demo-form-inline"
        style="max-width: 600px"
        label-width="auto"
      >
        <!-- <el-form-item label="店铺ID:">
          <el-input
            v-model="formData.shopId"
            placeholder="请输入店铺ID"
            clearable
          />
        </el-form-item> -->
        <el-form-item label="店铺名称:">
          <el-input
            v-model="formData.shop_name"
            placeholder="请输入店铺名称"
            clearable
          />
        </el-form-item>
        <el-form-item label="店铺地区:">
          <el-input
            v-model="formData.location"
            placeholder="请输入店铺地区"
            clearable
          />
        </el-form-item>
        <el-form-item label="店铺描述:">
          <el-input
            v-model="formData.description"
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
import { ApiAddShopData } from "@/api/shop";
import { getFormData } from "@/utils/server";
import { ElMessage } from "element-plus";
const formData = ref({
  // shopId: "",
  shop_name: "",
  location: "",
  description: "",
});
const loading = ref(false);
const handleSubmit = () => {
  loading.value = true;
  ApiAddShopData(getFormData(formData.value))
    .then((res) => {
      console.log(res, "新增");
      let resJson = res;
      if (JSON.stringify(resJson) != "{}") {
        ElMessage({
          message: "修改成功",
          type: "success",
        });
      }
    })
    .finally(() => {
      loading.value = false;
    });
};
</script>
<style lang=""></style>
