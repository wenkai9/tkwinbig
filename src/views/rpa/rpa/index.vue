<template>
  <div>
    <el-card>
      <el-form label-width="auto" style="max-width: 600px">
        <el-form-item label="类型:">
          <el-input
            readonly
            v-model="modelData.type"
            placeholder="请输入类型"
            clearable
          />
        </el-form-item>
        <el-form-item label="国家/地区:">
          <el-input
            v-model="modelData.region"
            placeholder="请输入国家/地区"
            clearable
          />
        </el-form-item>
        <el-form-item label="关联任务ID:">
          <el-input
            readonly
            v-model="modelData.refTaskId"
            placeholder="自动随机生成"
            clearable
          />
        </el-form-item>
        <el-form-item label="店铺ID:">
          <el-input
            v-model="modelData.shopId"
            placeholder="请输入店铺ID"
            clearable
          />
        </el-form-item>
        <el-form-item label="是否立即执行:">
          <el-radio-group v-model="status" @change="handleChangeStatus">
            <el-radio disabled :label="1" :value="1">是</el-radio>
            <!-- <el-radio :label="2" :value="2">否</el-radio> -->
          </el-radio-group>
        </el-form-item>
        <el-form-item label="达人ID:">
          <div style="display: flex">
            <div>
              <el-input
                v-model="modelData.content.creatorId"
                placeholder="请输入达人ID"
                clearable
              />
            </div>
            <div style="margin-left: 1rem">
              <el-input
                v-model="modelData.content.text"
                placeholder="请输入要发送的文本信息"
                clearable
              />
            </div>
          </div>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSend" :loading="loading"
            >发送</el-button
          >
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>
<script lang="ts" setup>
import { reactive, ref } from "vue";
import { ApiPostSendMsg } from "@/api/rpa/index.ts";
let modelData = reactive({
  type: 1,
  region: "",
  refTaskId: "",
  shopId: "",
  executeNow: true,
  content: {
    creatorId: "",
    text: "",
  },
});
let status = ref(1);
let loading = ref(false);
const handleSend = () => {
  loading.value = true;

  modelData.refTaskId = generateRandomFiveDigitNumber(modelData.refTaskId);
  ApiPostSendMsg(modelData)
    .then((res: any) => {
      console.log(res, "发送");
    })
    .finally(() => {
      loading.value = false;
    });
};

const handleChangeStatus = (value) => {
  status.value = value;
};

const generateRandomFiveDigitNumber = (string) => {
  string = Math.floor(Math.random() * 100000);
  const formattedNumber = String(string).padStart(5, "0");
  return formattedNumber;
};
</script>
<style lang="scss" scoped></style>
