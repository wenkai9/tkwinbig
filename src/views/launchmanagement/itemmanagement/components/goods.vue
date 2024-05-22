<template>
  <div>
    <h2>物品管理</h2>
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
      <el-table-column label="物品名称" width="280">
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
      <el-table-column label="是否免费寄送样品">
        <template #default="scope">
          {{ SampleMap[scope.row.hasFreeSample] }}
        </template>
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
          <el-form class="demo-form-inline" label-width="auto">
            <el-form-item label="商品ID:">
              <el-input
                v-model="formData.product_id"
                placeholder="请输入商品ID"
                clearable
              />
            </el-form-item>
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
            <el-form-item label="商品类目ID:">
              <el-input
                v-model="formData.base_category2"
                placeholder="请输入商品类目ID"
                clearable
              />
            </el-form-item>
            <el-form-item label="商品链接:">
              <el-input
                v-model="formData.Product_link"
                placeholder="请输入商品链接"
                clearable
              />
            </el-form-item>
          </el-form>
        </div>
        <template #footer>
          <div class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitEdit"> 确认 </el-button>
          </div>
        </template>
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
  product_id: "",
  title: "",
  description: "",
  price: "",
  base_category2: "",
  Product_link: "",
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
  console.log(item);
  dialogVisible.value = true;
  formData.value = {
    product_id: item.product_id,
    title: item.title,
    description: item.description,
    price: item.price,
    base_category2: item.base_category2_id,
    Product_link: item.product_link,
  };
  id.value = item.product_id;
};

const submitEdit = () => {
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
