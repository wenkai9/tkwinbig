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
            v-model.trim="formData.title"
            placeholder="请输入商品标题"
            clearable
          />
        </el-form-item>
        <el-form-item label="商品描述:">
          <el-input
            type="textarea"
            :rows="5"
            v-model.trim="formData.description"
            placeholder="请输入商品描述"
            clearable
          />
        </el-form-item>
        <el-form-item label="商品价格:">
          <el-input
            onkeyup="value=value.replace(/[^\d]/g,'')"
            v-model.trim="formData.price"
            placeholder="请输入商品价格"
            clearable
          />
        </el-form-item>
        <el-form-item label="商品链接:">
          <el-input
            v-model.trim="formData.product_link"
            placeholder="请输入商品链接"
            clearable
          />
        </el-form-item>
        <el-form-item label="商品ID:">
          <el-input
            v-model.trim="formData.product_id"
            placeholder="请输入商品商品ID"
            clearable
          />
        </el-form-item>
        <el-form-item label="是否免费寄样品:">
          <el-switch
            inline-prompt
            v-model="formData.hasFreeSample"
            active-text="开启"
            inactive-text="关闭"
          />
        </el-form-item>
        <el-form-item label="佣金率:">
          <el-input
            v-model.trim="formData.commissionRate"
            placeholder="请输入商品佣金率"
            clearable
          />
        </el-form-item>
        <el-form-item label="合作费:">
          <el-input
            v-model.trim="formData.CooperationFee"
            placeholder="请输入商品合作费"
            clearable
          />
        </el-form-item>
        <el-form-item label="商品二级分类:">
          <el-select
            v-model="formData.base_category2_id"
            placeholder="Select"
            size="large"
            style="width: 240px"
            @change="handleChange"
          >
            <el-option
              v-for="item in options"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="店铺ID:">
          <el-button type="primary" @click="handleOpenShop">
            {{ modelShop != null ? "重新选择" : "选择店铺" }}
          </el-button>
        </el-form-item>
        <el-form-item label="已选商店:" v-if="modelShop && modelShop != null">
          <div style="background: #eee; padding: 20px">
            <div>
              <div>店铺名称:&nbsp{{ modelShop.shop_name }}</div>
            </div>
            <div>店铺描述:{{ modelShop.description }}</div>
            <div>店铺地区:&nbsp{{ modelShop.location }}</div>
          </div>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit"
            >提交</el-button
          >
        </el-form-item>
      </el-form>
    </el-card>
    <div>
      <Shop
        :shopDialog="shopDialog"
        @handleClose="handleClose"
        @choiceShop="choiceShop"
      />
    </div>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ApiAddProducts } from "@/api/launchmanagement";
import { ApigetShopData } from "@/api/shop";
import { ElMessage } from "element-plus";
import Shop from "@/components/dialog/Shop/index.vue";
const router = useRouter();
const formData = ref({
  title: "",
  description: "",
  price: "",
  product_link: "",
  product_id: "",
  hasFreeSample: false,
  commissionRate: "",
  CooperationFee: "",
  base_category2_id: "",
  // base_category2_id: [],
  shopId: "",
  shopName: "",
});

const modelData = ref([]);
const loading = ref(false);
const pageObj = reactive({
  page: 1,
  size: 10,
  total: 0,
});
const options = ref([]);

ApiAddProducts("", pageObj.page, pageObj.size).then((res) => {
  options.value = [...res.category2_data];
});

let shopDialog = ref(false);
const handleOpenShop = () => {
  shopDialog.value = true;
};
const handleClose = (value) => {
  shopDialog.value = value;
};
const modelShop = ref(null);
const choiceShop = (data) => {
  modelShop.value = data;
  formData.value.shopName = data.shop_name;
  formData.value.shopId = data.shopId;
};

const handleChange = (value) => {
  console.log(value);
  formData.value.base_category2_id = value;
};
const generateRandomFiveDigitNumber = (string) => {
  string = Math.floor(Math.random() * 100000);
  const formattedNumber = String(string).padStart(5, "0");
  return formattedNumber;
};
const handleSubmit = () => {
  const requiredFields = [
    { key: "title", message: "请输入商品标题" },
    { key: "description", message: "请输入商品简介" },
    { key: "price", message: "请输入商品价格" },
    { key: "product_link", message: "请输入商品链接" },
    { key: "product_id", message: "请输入商品ID" },
    { key: "hasFreeSample", message: "请选中是否免费寄样品" },
    { key: "commissionRate", message: "请输入佣金率" },
    { key: "CooperationFee", message: "请输入合作费" },

    {
      key: "base_category2_id",
      // check: (value) => value.length > 0,
      message: "请选择商品分类",
    },
    {
      key: "shopId",
      message: "请选择店铺",
    },
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
  formData.value.hasFreeSample = false ? 0 : 1;
  // formData.value.id = generateRandomFiveDigitNumber(formData.value.id);
  ApiAddProducts(formData.value)
    .then((res) => {
      let resJson = res;
      if (JSON.stringify(resJson) != "{}") {
        ElMessage({
          message: "新增成功",
          type: "success",
        });
      }
      router.push({
        path: "/launchmanagement/itemmanagement/ItemManagement",
      });
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
<style></style>
