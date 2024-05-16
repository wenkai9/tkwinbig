<template>
  <div>
    <el-card>
      <el-form
        class="demo-form-inline"
        style="max-width: 600px"
        label-width="auto"
      >
        <el-form-item label="商品标题:">
          <el-input
            v-model="formData.title"
            placeholder="请输入商品标题"
            clearable
          />
        </el-form-item>
        <el-form-item label="商品描述:">
          <el-input
            v-model="formData.description"
            placeholder="请输入商品描述"
            clearable
          />
        </el-form-item>
        <el-form-item label="商品价格:">
          <el-input
            v-model="formData.price"
            placeholder="请输入商品价格"
            clearable
          />
        </el-form-item>
        <el-form-item label="商品链接:">
          <el-input
            v-model="formData.product_link"
            placeholder="请输入商品链接"
            clearable
          />
        </el-form-item>
        <el-form-item label="商品二级分类:">
          <!-- <el-input
            v-model="formData.base_category2_id"
            placeholder="请输入商品二级分类"
            clearable
          /> -->
          <el-cascader
            v-model="formData.base_category2_id"
            :options="options"
            @change="handleChange"
          />
        </el-form-item>
        <el-form-item label="店铺ID:">
          <el-input
            v-model="formData.shopId"
            placeholder="请输入店铺ID"
            clearable
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">提交</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref } from "vue";
import { ApiAddProducts } from "@/api/launchmanagement";
import { ElMessage } from "element-plus";
const formData = ref({
  title: "",
  description: "",
  price: "",
  product_link: "",
  // base_category2_id: "",
  base_category2_id: [],
  shopId: "",
});

const handleChange = (value) => {
  console.log(value);
};

const handleSubmit = () => {
  ApiAddProducts(formData.value).then((res) => {
    let resJson = res;
    if (JSON.stringify(resJson) != "{}") {
      ElMessage({
        message: "修改成功",
        type: "success",
      });
    }
  });
};
</script>
<style lang=""></style>
