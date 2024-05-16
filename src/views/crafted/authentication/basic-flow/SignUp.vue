<template>
  <!--begin::Wrapper-->
  <div class="w-lg-500px p-10">
    <div class="text-center mb-10">
      <!--begin::Title-->
      <h1 class="text-gray-900 mb-3">Create an Account</h1>
      <!--end::Title-->

      <!--begin::Link-->
      <div class="text-gray-500 fw-semibold fs-4">
        Already have an account?

        <router-link to="/sign-in" class="link-primary fw-bold">
          Sign in here
        </router-link>
      </div>
      <div class="mb-10 bg-light-info p-8 rounded">
        <div class="text-info">
          Use account <strong>admin@demo.com</strong> and password
          <strong>demo</strong> to continue.
        </div>
      </div>
      <!--end::Link-->
    </div>
    <!--begin::Form-->
    <el-form
      label-width="auto"
      :model="formLabelAlign"
      style="max-width: 600px"
    >
      <label class="form-label fs-6 fw-bold text-gray-900">username</label>
      <el-form-item>
        <el-input v-model="formLabelAlign.username" />
      </el-form-item>
      <label class="form-label fs-6 fw-bold text-gray-900">password</label>
      <el-form-item>
        <el-input v-model="formLabelAlign.password" type="password" />
      </el-form-item>
      <label class="form-label fs-6 fw-bold text-gray-900">email</label>
      <el-form-item>
        <el-input v-model="formLabelAlign.email" />
      </el-form-item>
      <label class="form-label fs-6 fw-bold text-gray-900">电话</label>
      <el-form-item>
        <el-input v-model="formLabelAlign.number" />
      </el-form-item>
      <label class="form-label fs-6 fw-bold text-gray-900">公司</label>
      <el-form-item>
        <el-input v-model="formLabelAlign.company" />
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          style="width: 100%"
          @click="handleRegister"
          :loading="loading"
          >注册</el-button
        >
      </el-form-item>
    </el-form>
    <!--end::Form-->
    <a href="#" class="btn btn-flex flex-center btn-light btn-lg w-100 mb-5">
      <img
        alt="Logo"
        :src="getAssetPath('media/svg/brand-logos/google-icon.svg')"
        class="h-20px me-3"
      />
      Continue with Google
    </a>
    <a href="#" class="btn btn-flex flex-center btn-light btn-lg w-100 mb-5">
      <img
        alt="Logo"
        :src="getAssetPath('media/svg/brand-logos/facebook-4.svg')"
        class="h-20px me-3"
      />
      Continue with Facebook
    </a>
    <a href="#" class="btn btn-flex flex-center btn-light btn-lg w-100">
      <img
        alt="Logo"
        :src="getAssetPath('media/svg/brand-logos/apple-black.svg')"
        class="h-20px me-3"
      />
      Continue with Apple
    </a>
  </div>
  <!--end::Wrapper-->
</template>

<script lang="ts" setup>
import { getAssetPath } from "@/core/helpers/assets";
import { reactive, ref } from "vue";
import { useAuthStore, type User } from "@/stores/auth";
import { useRouter } from "vue-router";
import { ApiHandleRegister } from "@/api/login";
import { getFormData } from "@/utils/server";
import { ElMessage, ElMessageBox } from "element-plus";
const formLabelAlign = reactive({
  username: "",
  password: "",
  email: "",
  number: "",
  company: "",
});
const loading = ref(false);
const store = useAuthStore();
const router = useRouter();

const handleRegister = async () => {
  loading.value = true;
  ApiHandleRegister(getFormData(formLabelAlign))
    .then((res) => {
      //console.log(res, "注册");
      if (res.code != 200) {
        return;
      }
      ElMessageBox.alert(res.msg, {
        confirmButtonText: "OK",
        callback: () => {
          return router.push({ name: "sign-in" });
        },
      });
    })
    .catch((err) => {
      return ElMessage({
        message: err.errmsg,
        type: "warning",
      });
    })
    .finally(() => {
      loading.value = false;
    });
};
</script>
