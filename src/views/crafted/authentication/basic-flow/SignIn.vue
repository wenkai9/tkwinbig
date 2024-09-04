<template>
  <!--begin::Wrapper-->
  <div class="w-lg-500px p-10">
    <div class="text-center mb-10">
      <!--begin::Title-->
      <h1 class="text-gray-900 mb-3">Sign In</h1>
      <!--end::Title-->

      <!--begin::Link-->
      <div class="text-gray-500 fw-semibold fs-4">
        New Here?

        <router-link to="/sign-up" class="link-primary fw-bold">
          Create an Account
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
      <el-form-item>
        <el-button type="primary" style="width: 100%" @click="handleLogin"
          >登录</el-button
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
import { reactive, onMounted } from "vue";
import { useAuthStore, type User } from "@/stores/auth";
import { useRouter } from "vue-router";
import { ApiHandlelogin } from "@/api/login";
import { getFormData } from "@/utils/server";
import { ElMessage } from "element-plus";
import Cookies from "js-cookie";
const formLabelAlign = reactive({
  username: "",
  password: "",
});
const store = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  let res = await ApiHandlelogin(getFormData(formLabelAlign));

  if (res.code != 200) {
    return;
  }
  ElMessage({
    message: res.msg,
    type: "success",
  });
  setTimeout(() => {
    console.log(res.token, "res.data.token");

    Cookies.set("Authorization", res.token);
    window.localStorage.setItem("userId", res.data.user_id);
    window.localStorage.setItem("userName", res.data.username);
    router.push({ name: "dashboard" });
  }, 1000);
};

onMounted(() => {
  Cookies.remove("Authorization");
  window.localStorage.setItem("kt_theme_mode_value", "light");
  window.localStorage.setItem("kt_theme_mode_menu", "light");
});
</script>
