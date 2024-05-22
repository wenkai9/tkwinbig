<template>
  <div>
    <h2>建联规则</h2>
    <div>
      <el-button type="primary" @click="handleAdd">新增建联规则</el-button>
    </div>
    <div style="margin-top: 1.25rem">
      <el-table
        :data="modelRulesData"
        border
        :header-cell-style="{
          backgroundColor: '#f6f7fc',
          color: '#1f283c',
          fontSize: '14px',
          textAlign: 'center',
        }"
        :cell-style="{ textAlign: 'center' }"
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column label="建联名称" width="280">
          <template #default="scope">
            {{ scope.row.name }}
          </template>
        </el-table-column>
        <el-table-column label="视频拍摄要求" width="280">
          <template #default="scope">
            {{ scope.row.requirement }}
          </template>
        </el-table-column>
        <el-table-column label="佣金">
          <template #default="scope"> ¥{{ scope.row.commission }} </template>
        </el-table-column>
        <el-table-column label="创建日期">
          <template #default="scope">
            {{ scope.row.createdAt }}
          </template>
        </el-table-column>

        <el-table-column fixed="right" label="操作" width="120">
          <template #default="scope">
            <el-button
              link
              type="primary"
              size="small"
              @click="handleEdit(scope.row)"
            >
              修改
            </el-button>
            <el-button
              link
              type="primary"
              size="small"
              @click="handleDelete(scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <div>
        <div>
          <GlobalPage
            :page="pageObj.page"
            :pageSize="pageObj.size"
            :total="pageObj.total"
            @changePage="changePage"
            @changeSize="changeSize"
          />
        </div>
      </div>
    </div>

    <!-- 修改建联 -->
    <div>
      <el-dialog v-model="dialogVisible">
        <div>
          <el-form class="demo-form-inline" label-width="auto">
            <el-form-item label="建联名称:">
              <el-input
                v-model.trim="formData.name"
                placeholder="请输入建联名称"
                clearable
              />
            </el-form-item>
            <el-form-item label="建联要求:">
              <el-input
                v-model.trim="formData.requirement"
                placeholder="请输入建联要求"
                clearable
              />
            </el-form-item>
            <el-form-item label="建联佣金:">
              <el-input
                onkeyup="value=value.replace(/[^\d]/g,'')"
                v-model.trim="formData.commission"
                placeholder="请输入建联佣金"
                clearable
              />
            </el-form-item>
          </el-form>
        </div>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitAddorEdit">
              确认
            </el-button>
          </div>
        </template>
      </el-dialog>
    </div>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref } from "vue";
import {
  ApiGetListRules,
  ApiAddRulesRules,
  ApiEditRules,
  ApiDeteleRules,
} from "@/api/launchmanagement";
import { ElMessage, ElMessageBox } from "element-plus";
// 建联规则
let pageObj = reactive({
  page: 1,
  size: 10,
  total: 0,
});
let loading = ref(false);
let modelRulesData = ref([]);
const GetListRules = () => {
  loading.value = true;
  ApiGetListRules(pageObj.page, pageObj.size)
    .then((res) => {
      modelRulesData.value = [...res.rules];
      pageObj.total = res.total_rules;
    })
    .finally(() => {
      loading.value = false;
    });
};
GetListRules();

const changePage = (page: Number) => {
  pageObj.page = page;
  GetListRules();
};

const changeSize = (size: Number) => {
  pageObj.size = size;
  GetListRules();
};

let dialogVisible = ref(false);
let formData = ref({
  name: "",
  requirement: "",
  commission: "",
  // shop_info: "",
});
const id = ref("");
const handleEdit = (item: Object) => {
  dialogVisible.value = true;
  formData.value = {
    name: item.name,
    requirement: item.requirement,
    commission: item.commission,
    // shop_info: item.shop_info,
  };
  id.value = item.id;
};

const handleAdd = () => {
  dialogVisible.value = true;
  formData.value = {
    name: "",
    requirement: "",
    commission: "",
  };
  id.value = "";
};

const SUCCESS_CODE = 200;
const handleError = (res) => {
  ElMessage({
    message: res.errormsg,
    type: "warning",
  });
};
const showSuccessMessage = (message) => {
  ElMessage({
    message,
    type: "success",
  });
};

const handleApi = (formData, idValue) => {
  const promise = idValue
    ? ApiEditRules(formData, idValue)
    : ApiAddRulesRules(formData);
  return promise.then((res) => {
    if (res.code === SUCCESS_CODE) {
      showSuccessMessage(idValue ? "修改成功" : "操作成功");
      dialogVisible.value = false;
      GetListRules();
    } else {
      handleError(res);
    }
  });
};

const submitAddorEdit = () => {
  if (id.value) {
    handleApi(formData.value, id.value);
  } else {
    handleApi(formData.value);
  }
};

const handleDelete = (item: object) => {
  ElMessageBox.confirm("确定删除该规则吗?")
    .then(() => {
      ApiDeteleRules(item.id).then((res) => {
        console.log(res, "删除");
        ElMessage({
          message: "操作成功",
          type: "success",
        });
        GetListRules();
      });
    })
    .catch(() => {
      // catch error
    });
};
</script>
<style lang=""></style>
