<template>
  <div>
    <el-dialog
      v-model="props.shopDialog"
      title="选择商店"
      :before-close="handleClose"
    >
      <div>
        <el-table
          :data="shopData"
          v-loading="shopLoading"
          :header-cell-style="{
            backgroundColor: '#f6f7fc',
            color: '#1f283c',
            fontSize: '14px',
            textAlign: 'left',
          }"
          :cell-style="{ textAlign: 'left' }"
          style="width: 100%"
          @current-change="choiceShop"
        >
          <el-table-column prop="shop_name" label="店铺名称" width="180" />
          <el-table-column prop="shopId" label="店铺ID" width="180" />
          <el-table-column prop="location" label="店铺地区" />
          <el-table-column prop="description" label="店铺描述" />
          <el-table-column prop="createAt" label="创建时间" />
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
      </div>
      <!-- <template #footer>
        <div class="dialog-footer">
          <el-button @click="props.shopDialog = false">取消</el-button>
          <el-button type="primary" @click="props.shopDialog = false">
            提交
          </el-button>
        </div>
      </template> -->
    </el-dialog>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref, defineProps, defineEmits } from "vue";
import { ApiAddProducts } from "@/api/launchmanagement";
import { string } from "yup";
const props = defineProps({
  shopDialog: Boolean,
  task_id: String,
});

const emit = defineEmits(["handleClose", "choiceShop"]);

const handleClose = () => {
  emit("handleClose", false);
};
let shopData = ref([]);
const shopLoading = ref(false);
let pageObj = reactive({
  page: 1,
  size: 10,
  total: 0,
});

const getShopData = async () => {
  try {
    shopLoading.value = true;
    const response = await ApiAddProducts("", pageObj.page, pageObj.size);
    shopData.value = [...response.shop_data];

    pageObj.total = response.total_shops;
  } finally {
    shopLoading.value = false;
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
getShopData();

const choiceShop = (val) => {
  emit("choiceShop", val);
  emit("handleClose", false);
};
</script>
<style lang=""></style>
