<template>
  <div>
    <el-card>
      <div>
        <el-button type="primary" @click="handleJump">创建店铺</el-button>
      </div>
      <el-table :data="modelData" style="width: 100%" v-loading="loading">
        <el-table-column prop="shop_name" label="店铺名称" width="180" />
        <el-table-column prop="shopId" label="店铺ID" width="180" />
        <el-table-column prop="location" label="店铺地区" />
        <el-table-column prop="description" label="店铺描述" />
        <el-table-column prop="createAt" label="创建时间" />
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
      <!-- 修改店铺弹出层 -->
      <div>
        <el-dialog v-model="dialogVisible">
          <div>
            <el-form class="demo-form-inline">
              <el-form-item label="店铺ID:">
                <el-input
                  v-model="formData.shopId"
                  placeholder="请输入店铺ID"
                  clearable
                />
              </el-form-item>
              <el-form-item label="店铺名称:">
                <el-input
                  v-model="formData.shop_name"
                  placeholder="请输入店铺ID"
                  clearable
                />
              </el-form-item>
              <el-form-item label="店铺地区:">
                <el-input
                  v-model="formData.location"
                  placeholder="请输入店铺地区"
                  clearable
                />
              </el-form-item>
              <el-form-item label="店铺描述:">
                <el-input
                  v-model="formData.description"
                  placeholder="请输入店铺描述"
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
    </el-card>
  </div>
</template>
<script setup lang="ts">
import {
  ApigetShopData,
  ApiAddShopData,
  ApiEditShopData,
  ApiDeleteShop,
} from "@/api/shop";
import { reactive, ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { useRouter } from "vue-router";
const router = useRouter();
const modelData = ref([]);
const loading = ref(false);
const pageObj = reactive({
  page: 1,
  size: 10,
  total: 0,
});

const getShopData = async () => {
  try {
    loading.value = true;
    const response = await ApigetShopData("", pageObj.page);
    modelData.value = [...response.shops];
    pageObj.total = response.total_shops;
  } catch (error) {
    ElMessage({
      message: err,
      type: "warning",
    });
  } finally {
    loading.value = false;
  }
};

const changePage = (page: number) => {
  pageObj.page = page;
  getShopData();
};
const changeSize = (size: number) => {
  pageObj.size = size;
  getShopData();
};
const dialogVisible = ref(false);
const formData = ref({
  shopId: "",
  shop_name: "",
  location: "",
  description: "",
});
const id = ref("");
const handleEdit = (row: any) => {
  dialogVisible.value = true;
  formData.value = {
    shopId: row.shopId,
    shop_name: row.shop_name,
    location: row.location,
    description: row.description,
  };
  id.value = row.shopId;
};
const submitEdit = () => {
  ApiEditShopData(formData.value, id.value).then((res) => {
    let resJson = res;
    if (JSON.stringify(resJson) != "{}") {
      ElMessage({
        message: "修改成功",
        type: "success",
      });
      dialogVisible.value = false;
      getShopData();
    }
  });
};
const handleDelete = (item: object) => {
  ElMessageBox.confirm("确定删除该店铺吗?")
    .then(() => {
      ApiDeleteShop(item.shopId).then((res) => {
        console.log(res, "删除");
        ElMessage({
          message: "操作成功",
          type: "success",
        });

        getShopData();
      });
    })
    .catch(() => {
      // catch error
    });
};
getShopData();

const handleJump = () => {
  const url = router.resolve({
    path: "/usercenter/shopmanagement/components/addOrEdit",
  });
  window.open(url.href, "_blank");
};

const handleExport = () => {};
</script>
<style lang=""></style>
