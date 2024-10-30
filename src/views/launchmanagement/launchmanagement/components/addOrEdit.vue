<template>
  <div>
    <el-card>
      <el-form class="demo-form-inline">
        <el-form-item label="任务名称:">
          <el-input
            v-model.trim="formData.name"
            style="width: 240px"
            placeholder="请输入任务名称"
          />
        </el-form-item>
        <el-form-item label="店铺信息:">
          <el-button type="primary" @click="handleOpenShop">
            {{ modelShop != null ? "重新选择" : "选择店铺" }}
          </el-button>
        </el-form-item>
        <el-form-item label="商品信息:">
          <el-button type="primary" @click="handleOpenGood">
            {{ modelGood != null ? "重新选择" : "选择商品" }}
          </el-button>
        </el-form-item>
        <el-form-item label="已选商品:" v-if="modelGood && modelGood != null">
          <div style="background: #eee; padding: 20px">
            <div style="display: flex">
              <div>商品名称:&nbsp{{ modelGood.title }}</div>
              <div style="padding-left: 10px">
                商品标签:&nbsp{{ modelGood.match_tag }}
              </div>
            </div>
            <div>商品简介:{{ modelGood.description }}</div>
            <div>
              <span>商品价格:&nbsp</span>

              <span style="color: red">¥{{ modelGood.price }}</span>
            </div>
            <div>商品链接:&nbsp{{ modelGood.product_link }}</div>
          </div>
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
        <el-form-item label="地区信息:">
          <el-select
            value-key="p_id"
            v-model="regionObj.province"
            placeholder="请选择省份"
            size="large"
            style="width: 240px"
            @change="changeP"
          >
            <el-option
              v-for="item in regionObj.modelProvince"
              :key="item.p_id"
              :label="item.p_name"
              :value="item"
            />
          </el-select>
          <el-select
            value-key="id"
            v-model="regionObj.city"
            placeholder="请选择城市"
            size="large"
            style="width: 240px"
            @change="changeC"
          >
            <el-option
              v-for="item in regionObj.modelCity"
              :key="item.id"
              :label="item.name"
              :value="item"
            />
          </el-select>
          <el-select
            value-key="id"
            v-model="regionObj.area"
            placeholder="请选择地区"
            size="large"
            style="width: 240px"
            @change="changeA"
          >
            <el-option
              v-for="item in regionObj.modelArea"
              :key="item.id"
              :label="item.name"
              :value="item"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <div>
        <el-button type="primary" @click="handleSubmit" :loading="loading">
          提交
        </el-button>
      </div>
    </el-card>
    <!-- 商品弹出层 -->
    <div>
      <Good
        :goodDialog="goodDialog"
        @handleCloseGoodDialog="handleCloseGoodDialog"
        @choiceGood="choiceGood"
      />
    </div>
    <div>
      <Shop
        :shopDialog="shopDialog"
        @handleClose="handleClose"
        @choiceShop="choiceShop"
      />
    </div>
  </div>
</template>
<script lang="ts" setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import Shop from "@/components/dialog/Shop/index.vue";
import Good from "@/components/dialog/Good/index.vue";

import { ApiGetRegion } from "@/api/public";
import { ApiAddTasks } from "@/api/launchmanagement";
import { ElMessage } from "element-plus";
const formData = reactive({
  name: "",
});
const router = useRouter();
// 省市区
const regionObj = reactive({
  province: "",
  modelProvince: [],
  city: "",
  modelCity: [],
  area: "",
  modelArea: [],
});

// 商品
const goodDialog = ref(false);
const handleOpenGood = () => {
  goodDialog.value = true;
};

const handleCloseGoodDialog = (value) => {
  goodDialog.value = value;
};

const modelGood = ref(null);
const choiceGood = (data) => {
  modelGood.value = data;
};

// 店铺------------
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
};

const GetRegion = () => {
  ApiGetRegion(0).then((res) => {
    console.log(res, "--------");
    regionObj.modelProvince = res.province_list;
  });
};

const changeP = (data) => {
  console.log(data, "选中省份");
  if (data != "") {
    regionObj.province = data.p_name;
    regionObj.city = "";
    regionObj.area = "";
    ApiGetRegion(data.p_id).then((res) => {
      console.log(res, "城市");
      regionObj.modelCity = res.sub_data.subs;
    });
  }
};

const changeC = (data) => {
  if (data != "") {
    regionObj.city = data.name;
    regionObj.area = "";
    ApiGetRegion(data.id).then((res) => {
      console.log(res, "地区");
      regionObj.modelArea = res.sub_data.subs;
    });
  }
};
const changeA = (data) => {
  regionObj.area = data.name;
};
GetRegion();

const loading = ref(false);

const handleSubmit = () => {
  const data = {
    name: formData.name,
    productId: modelGood.value.product_id,
    userId: window.localStorage.getItem("userId"),
    shopId: modelShop.value.shopId,
    p_name: regionObj.province,
    c_name: regionObj.city,
    r_name: regionObj.area,
    match_quantity: null,
    willing_quantity: null,
    send_quantity: null,
    // region: regionObj.province + "-" + regionObj.city + "-" + regionObj.area,
  };
  // debugger;
  ApiAddTasks(data)
    .then((res) => {
      console.log(res, "新增============");
      if (res.code != 200) {
        return ElMessage({
          message: res.errmsg,
          type: "warning",
        });
      }
      ElMessage({
        message: "操作成功",
        type: "success",
      });
      router.push({
        path: "/launchmanagement/launchmanagement",
      });
    })
    .finally(() => {
      loading.value = false;
    });
};
</script>
<style lang=""></style>
