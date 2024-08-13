<template>
  <div>
    <el-table
      :data="modelData"
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
      <el-table-column label="物品名称" width="220">
        <template #default="scope">
          {{ scope.row.title }}
        </template>
      </el-table-column>
      <el-table-column label="物品描述" width="280">
        <template #default="scope">
          {{ scope.row.description }}
        </template>
      </el-table-column>
      <el-table-column label="物品标签">
        <template #default="scope">
          {{ scope.row.match_tag }}
        </template>
      </el-table-column>
      <el-table-column label="是否免费邮寄商品">
        <template #default="scope">
          {{ SampleMap[scope.row.hasFreeSample] }}
        </template>
      </el-table-column>
      <el-table-column label="佣金率">
        <template #default="scope">
          {{ scope.row.commissionRate }}
        </template>
      </el-table-column>
      <el-table-column label="合作费">
        <template #default="scope"> {{ scope.row.CooperationFee }} </template>
      </el-table-column>
      <el-table-column label="物品状态">
        <template #default="scope">
          {{ scope.row.product_status ? "已经建联" : "未建联" }}
        </template>
      </el-table-column>
      <el-table-column label="建联规则">
        <template #default="scope">
          {{ scope.row.rule_name }}
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
      <GlobalPage
        :page="pageObj.page"
        :pageSize="pageObj.size"
        :total="pageObj.total"
        @changePage="changePage"
        @changeSize="changeSize"
      />
    </div>
    <div>
      <el-dialog v-model="dialogVisible">
        <div>
          <el-table :data="modelRulesData" @current-change="choiceRules">
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
              <template #default="scope">
                ¥{{ scope.row.commission }}
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div>
          <GlobalPage
            :page="RulesPageObj.page"
            :pageSize="RulesPageObj.size"
            :total="RulesPageObj.total"
            @changePage="changeRulesPage"
            @changeSize="changeRulesSize"
          />
        </div>
      </el-dialog>
    </div>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref } from "vue";
import {
  ApiGetProducts,
  ApiUpdataProducts,
  ApiEditProducts,
  ApiDeteleProducts,
  ApiGetListRules,
} from "@/api/launchmanagement";
import { ElMessage, ElMessageBox } from "element-plus";
const modelData = ref([]);
let loading = ref(false);
let pageObj = reactive({
  page: 1,
  size: 10,
  total: 0,
});
const SampleMap = reactive({
  true: "是",
  false: "否",
});
const dialogVisible = ref(false);
let formData = ref({
  raidsysrule_id: "",
});
const id = ref("");
const GetProducts = async () => {
  try {
    loading.value = true;
    const response = await ApiGetProducts("", pageObj.page, pageObj.size);
    modelData.value = [...response.products];
    pageObj.total = response.total_products || 0;
  } catch (error) {
    console.log(error);
  } finally {
    loading.value = false;
  }
};

const changePage = (page: number) => {
  pageObj.page = page;
  GetProducts();
};
const changeSize = (size: number) => {
  pageObj.size = size;
  GetProducts();
};

const handleEdit = (item: object) => {
  dialogVisible.value = true;
  id.value = item.product_id;
};

let RulesPageObj = reactive({
  page: 1,
  size: 10,
  total: 0,
});
let modelRulesData = ref([]);
const GetListRules = () => {
  ApiGetListRules(RulesPageObj.page, RulesPageObj.size).then((res) => {
    modelRulesData.value = [...res.rules];
    RulesPageObj.total = res.total_rules;
  });
};
GetListRules();

const changeRulesPage = (page: number) => {
  RulesPageObj.page = page;
  GetListRules();
};
const changeRulesSize = (size: number) => {
  RulesPageObj.page = 1;
  RulesPageObj.size = size;
  GetListRules();
};
const choiceRules = (data) => {
  console.log(data, "------");
  formData.value.raidsysrule_id = data.id;
  ApiEditProducts(formData.value, id.value).then((res) => {
    console.log(res.code, "==========");
    if (res.code != 200) {
      return ElMessage({
        message: res.errormsg,
        type: "warning",
      });
    }
    ElMessage({
      message: "修改成功",
      type: "success",
    });
    dialogVisible.value = false;
    GetProducts();
  });
};

const handleDelete = (item: object) => {
  ElMessageBox.confirm("确定删除该商品吗?")
    .then(() => {
      ApiDeteleProducts(item.product_id).then((res) => {
        console.log(res, "删除");
        ElMessage({
          message: "操作成功",
          type: "success",
        });
        GetProducts();
      });
    })
    .catch(() => {
      // catch error
    });
};
GetProducts();

defineExpose({
  GetProducts,
});
</script>
<style lang=""></style>
