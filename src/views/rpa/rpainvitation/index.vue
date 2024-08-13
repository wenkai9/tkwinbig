<template>
  <div>
    <el-card>
      <el-form
        class="demo-form-inline"
        label-width="auto"
        style="max-width: 800px"
      >
        <el-form-item label="类型:">
          <el-input
            readonly
            v-model="modelData.type"
            placeholder="请输入类型"
            clearable
          />
        </el-form-item>
        <el-form-item label="国家/地区(达人):">
          <el-input
            readonly
            v-model="modelData.region"
            placeholder="请输入国家/地区"
            clearable
          />
        </el-form-item>
        <el-form-item label="关联任务ID:">
          <!-- <el-input
            readonly
            v-model="modelData.refTaskId"
            placeholder="自动随机生成"
            clearable
          /> -->
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
        <el-form-item label="店铺ID:">
          <!-- <el-input
            onkeyup="value=value.replace(/[^\d]/g,'')"
            v-model.trim="modelData.shopId"
            placeholder="请输入店铺ID"
            clearable
          /> -->
          <el-select
            :disabled="taskName == ''"
            v-model="shopName"
            value-key="shop_id"
            placeholder="请选择店铺"
            size="large"
            style="width: 240px"
            @change="handleSelectShop"
          >
            <!--  -->
            <el-option
              v-for="item in modelShopData"
              :key="item.shop_id"
              :label="item.shop_name"
              :value="item"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="是否立即执行:">
          <el-radio-group v-model="status" @change="handleChangeStatus">
            <el-radio disabled :label="1" :value="1">是</el-radio>
            <!-- <el-radio :label="2" :value="2">否</el-radio> -->
          </el-radio-group>
        </el-form-item>
        <el-form-item label="联系人名称:">
          <el-input
            v-model="modelData.content.name"
            placeholder="请输入联系人名称"
            clearable
          />
        </el-form-item>
        <el-form-item label="商品名称:">
          <!-- <el-select
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
          </el-select> -->
          <div
            style="width: 500px"
            v-for="(item, index) in productId"
            :key="index + '_input'"
          >
            <div>
              <div style="display: flex">
                <!-- <el-input
                  onkeyup="value=value.replace(/[^\d]/g,'')"
                  v-model="productId[index].productId"
                  :placeholder="'已选商品' + (index + 1)"
                ></el-input> -->
                <el-select
                  v-model="productId[index]"
                  value-key="product_id"
                  placeholder="请选择商品"
                  size="large"
                  style="width: 240px"
                  @change="handleSelectGood(productId[index])"
                >
                  <el-option
                    v-for="item in modelGoodData"
                    :key="item.product_id"
                    :label="item.title"
                    :value="item"
                  />
                </el-select>

                <el-input
                  v-model="productId[index].commissionRate"
                  :placeholder="'佣金比例'"
                ></el-input>
                <div
                  style="
                    width: 200px;
                    line-height: 38px;
                    padding-left: 10px;
                    color: red;
                  "
                  v-show="productId.length >= 2"
                  @click="handleDeletePd(index)"
                >
                  删除
                </div>
              </div>
              <div
                style="
                  width: 500px;
                  height: 1px;
                  border-bottom: 1px dotted #000;
                  margin: 10px 0px;
                "
              ></div>
            </div>
          </div>
        </el-form-item>
        <!-- <el-form-item label="费率:">
          <div
            v-for="(item, index) in productId"
            :key="index + '_input'"
            style="width: 500px"
          >
            <div style="display: flex">
              <el-input
                style="margin-top: 5px"
                v-model="productId[index].commissionRate"
                :placeholder="'已填写费率' + (index + 1)"
              ></el-input>
              <div
                style="
                  width: 200px;
                  line-height: 38px;
                  padding-left: 10px;
                  color: red;
                "
                v-show="productId.length >= 2"
                @click="handleDeletePd(index)"
              >
                删除
              </div>
            </div>
          </div>
        </el-form-item> -->
        <el-form-item label="新增商品以及佣金率:">
          <el-button
            type="primary"
            @click="handleAddPd"
            :disabled="taskName == '' || shopName == ''"
            >新增(商品/费率)</el-button
          >
        </el-form-item>
        <el-form-item label="达人名称:">
          <el-input
            v-model="originalString"
            placeholder="请输入达人名称,多个达人请以逗号分隔"
            clearable
          />
        </el-form-item>
        <el-form-item label="时间:">
          <el-date-picker
            :disabled-date="disabledDate"
            @change="changeTime"
            v-model="modelData.content.expireDateTime"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="选中日期"
          />
        </el-form-item>
        <el-form-item label="是否免费邮寄商品:">
          <el-radio-group
            v-model="hasFreeSample"
            @change="handleChangehasFreeSample"
          >
            <el-radio :label="1" :value="1">是</el-radio>
            <el-radio :label="2" :value="2">否</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="合作费:">
          <el-input
            onkeyup="value=value.replace(/[^\d]/g,'')"
            v-model="modelData.content.sampleRule.sampleQuantity"
            placeholder="请输入合作费"
            clearable
          />
        </el-form-item>
        <el-form-item label="文本信息:">
          <el-input
            readonly
            v-model="modelData.content.message"
            style="width: 670px"
            :rows="5"
            type="textarea"
            placeholder="请输入文本信息"
          />
        </el-form-item>
        <el-form-item label="邮箱:">
          <el-input
            readonly
            v-model="modelData.content.contactInfo.email"
            placeholder="请输入邮箱"
            clearable
          />
        </el-form-item>
        <el-form-item label="手机:">
          <el-input
            readonly
            v-model="modelData.content.contactInfo.phone"
            placeholder="请输入手机"
            clearable
          />
        </el-form-item>

        <el-form-item label="国家/地区(商家):">
          <el-input
            readonly
            v-model="modelData.content.contactInfo.country"
            placeholder="请输入国家/地区"
            clearable
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">提交</el-button>
          <!-- :loading="loading" -->
          <!-- :loading="loading" -->
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref } from "vue";
import { ApiPostSendMsg_Invitation } from "@/api/rpa";
import { ApiGetTasks, ApiGetRetrieval } from "@/api/launchmanagement";
import { ApigetShop_tasks, ApigetGood_shop } from "@/api/shop";
import { ElMessage } from "element-plus";
import { dayjs } from "element-plus";
import { Minus } from "@element-plus/icons-vue";
let modelData = reactive({
  type: 2,
  region: "US",
  refTaskId: "",
  shopId: "",
  executeNow: true,
  content: {
    name: "",
    products: [],
    creatorIds: [],
    expireDateTime: "",
    message:
      "Hi, dear! We have been following your amazing content and believe that your unique style and creativity would be a perfect fit for our brand! We are here to invite you to try and test our head shavers for bald men and women. If you have any interest, please let us know, so that we can discuss more details. Thank you so much!",
    sampleRule: {
      hasFreeSample: "",
      sampleQuantity: "",
    },
    contactInfo: {
      email: "vexloria.official@outlook.com",
      phone: "3122926741",
      country: "US",
    },
  },
});
let taskName = ref("");
let shopName = ref("");
let goodName = ref([]);
let modelShopData = ref([]);
let modelGoodData = ref([]);
const modelTasksData = ref([]);
let status = ref(1);
let hasFreeSample = ref(1);
let loading = ref(false);

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

// 任务
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
  // setFormFieldArrayValue(modelRetrieval, []);
  getShop_tasks(formData.task_id);
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

  getGood_shop(formData.shop_id);
};
const getGood_shop = (shop_id) => {
  ApigetGood_shop(shop_id).then((res) => {
    console.log(res, "");
    modelGoodData.value = res.data;
  });
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

const handleSelectGood = (data, index) => {
  console.log(data, "data");
  console.log(productId[index]);

  // let modelTag = [];
  // data.forEach((element) => {
  //   console.log(element.match_tag, "element");
  //   modelTag.push(element.match_tag);
  // });

  // formData.products = modelTag.join(",");
  productId[index] = data.product_id;
  // console.log(modelTag, "formDat");
  // modelRetrieval.value = [];
};

const handleChangeStatus = (value) => {
  status.value = value;
};

const changeTime = (time) => {
  modelData.content.expireDateTime = time;
};

const handleChangehasFreeSample = (value) => {
  hasFreeSample.value = value;
  value == 1 ? (modelData.content.sampleRule.hasFreeSample = true) : false;
};
const generateRandomFiveDigitNumber = (string) => {
  string = Math.floor(Math.random() * 100000);
  const formattedNumber = String(string).padStart(5, "0");
  return formattedNumber;
};
const disabledDate = (time) => {
  return dayjs(time).isBefore(dayjs(), "day");
};

const originalString = ref("");

const handleSubmit = () => {
  console.log(modelData, "modelData");

  loading.value = true;
  modelData.refTaskId = generateRandomFiveDigitNumber(modelData.refTaskId);
  // modelData.refTaskId = formData.task_id;
  modelData.shopId = formData.shop_id;
  console.log(productId.value, "productId.value");

  productId.value.forEach((item) => {
    modelData.content.products.push({
      productId: item.product_id,
      commissionRate: item.commissionRate,
    });
  });
  hasFreeSample.value == 1
    ? (modelData.content.sampleRule.hasFreeSample = true)
    : false;
  modelData.content.creatorIds = originalString.value.split(",");
  ApiPostSendMsg_Invitation(modelData)
    .then((res) => {
      console.log(res, "提交");
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
    })
    .finally(() => {
      // loading.value = false;
    });
};
// 商品
let productId = ref([]);
const handleAddPd = () => {
  productId.value.push({
    productId: "",
    commissionRate: "",
  });
};
const handleDeletePd = (index) => {
  productId.value.splice(index, 1);
};
</script>
<style lang=""></style>
