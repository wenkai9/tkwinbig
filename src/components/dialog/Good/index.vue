<template>
  <div>
    <el-dialog
      v-model="props.goodDialog"
      title="选择商品"
      :before-close="handleCloseGoodDialog"
    >
      <div>
        <el-table
          :data="goodData"
          :header-cell-style="{
            backgroundColor: '#f6f7fc',
            color: '#1f283c',
            fontSize: '14px',
            textAlign: 'left',
          }"
          :cell-style="{ textAlign: 'left' }"
          v-loading="loading"
          style="width: 100%"
          @current-change="choiceGood"
        >
          <el-table-column prop="title" label="物品名称" width="280" />
          <el-table-column prop="description" label="物品描述" width="280">
            <template #default="scope">
              <el-tooltip
                class="item"
                effect="dark"
                :content="scope.row.description"
                placement="top"
              >
                <template #content>
                  <p style="width: 280px">
                    <span>{{ scope.row.description }} </span>
                  </p>
                </template>
                <div>
                  <div class="wrap_row2">{{ scope.row.description }}</div>
                </div>
              </el-tooltip>
            </template>
          </el-table-column>

          <el-table-column prop="match_tag" label="物品标签" />
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
          <el-button @click="handleCloseGoodDialog">取消</el-button>
          <el-button type="primary" @click="dialogVisible = false">
            Confirm
          </el-button>
        </div>
      </template> -->
    </el-dialog>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref, defineProps, defineEmits } from "vue";
import { ApiGetProducts } from "@/api/launchmanagement";
const props = defineProps({
  goodDialog: Boolean,
  shopId: Number,
});

let goodData = ref([]);
const loading = ref(false);
let pageObj = reactive({
  page: 1,
  size: 10,
  total: 0,
});
const GetProducts = async () => {
  console.log(444)
  const params = {
    shopId: props.shopId,
  };
  try {
    loading.value = true;
    const response = await ApiGetProducts(params, pageObj.page, pageObj.size);
    goodData.value = [...response.products];
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

const emit = defineEmits(["handleCloseGoodDialog", "choiceGood"]);

const handleCloseGoodDialog = () => {
  emit("handleCloseGoodDialog", false);
};

GetProducts();

const choiceGood = (val) => {
  // console.log(val, "选中商品");
  emit("choiceGood", val);
  emit("handleCloseGoodDialog", false);
};
defineExpose({
  GetProducts,
});
</script>
<style lang="scss" scoped>
.wrap_row2 {
  cursor: pointer;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
