<template>
  <div>
    <el-card>
      <!-- 用户管理 -->
      <el-form
        class="demo-form-inline"
        style="max-width: 600px"
        label-width="auto"
      >
        <el-form-item label="用户名:">
          <el-input
            v-model="formData.username"
            placeholder="Approved by"
            clearable
          />
        </el-form-item>
        <el-form-item label="手机号:">
          <el-input v-model="formData.number" placeholder="手机号" clearable />
        </el-form-item>
        <el-form-item label="邮箱:">
          <el-input
            v-model="formData.email"
            placeholder="请输入邮箱"
            clearable
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleOpenDialog"
            >修改密码</el-button
          >
        </el-form-item>
      </el-form>
      <div>
        <el-dialog v-model="dialogVisible" title="修改密码" width="500">
          <el-form
            class="demo-form-inline"
            style="max-width: 600px"
            label-width="auto"
          >
            <el-form-item label="旧密码:">
              <el-input
                v-model="editFormData.old_password"
                placeholder="请输入旧密码"
                clearable
                type="password"
              />
            </el-form-item>
            <el-form-item label="新密码:">
              <el-input
                v-model="editFormData.new_password"
                placeholder="请输入新密码"
                clearable
                type="password"
              />
            </el-form-item>
            <el-form-item label="确认密码:">
              <el-input
                v-model="editFormData.confirm_password"
                placeholder="请输入新密码"
                clearable
                type="password"
              />
            </el-form-item>
          </el-form>
          <template #footer>
            <div class="dialog-footer">
              <el-button type="primary" :loading="loading" @click="handleSubmit"
                >提交</el-button
              >
            </div>
          </template>
        </el-dialog>
      </div>
    </el-card>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref } from "vue";
import { ElMessage } from "element-plus";
import { ApigetUser, ApiChangePsw } from "@/api/user/index";
import { getFormData } from "@/utils/server";
import { useRouter } from "vue-router";
const router = useRouter();
let formData = ref({
  username: "",
  number: "",
  email: "",
});

let loading = ref(false);
let editFormData = ref({
  old_password: "",
  new_password: "",
  confirm_password: "",
});
const getUser = () => {
  ApigetUser()
    .then((res) => {
      console.log(res, "登录=-==");

      if (res.data.errmsg == "用户未登录") {
        router.push({ name: "sign-in" });
      }
      if (res.code == 200) {
        formData.value = res.data;
      }
    })
    .catch((err) => {
      router.push({ name: "sign-in" });
    });
};
let dialogVisible = ref(false);
const handleOpenDialog = () => {
  dialogVisible.value = true;
};

const handleSubmit = () => {
  if (
    editFormData.value.old_password == "" ||
    editFormData.value.old_password == null
  ) {
    return ElMessage({
      message: "请输入旧密码",
      type: "warning",
    });
  } else if (
    editFormData.value.new_password == "" ||
    editFormData.value.new_password == null
  ) {
    return ElMessage({
      message: "请输入新的密码",
      type: "warning",
    });
  } else if (
    editFormData.value.new_password != editFormData.value.confirm_password
  ) {
    return ElMessage({
      message: "新的密码与确认密码需一致",
      type: "warning",
    });
  }
  loading.value = true;
  ApiChangePsw(getFormData(editFormData.value))
    .then((res) => {
      console.log(res, "------------");
      if (res.code != 0) {
        return;
      }
      ElMessage({
        message: "操作成功",
        type: "success",
      });
    })
    .finally(() => {
      loading.value = false;
    });
};

getUser();
</script>
<style lang=""></style>
