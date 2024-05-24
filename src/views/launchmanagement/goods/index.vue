<template>
  <div>
    <el-form class="demo-form-inline">
      <el-form-item label="商品分类:">
        <div
          class="card_classContent"
          v-for="(item, index) in modelClassification"
          :key="index"
          @click="handleSelectProduct(item)"
        >
          <div>
            <el-popover placement="bottom" :width="250" trigger="click">
              <template #reference>
                <div v-if="item.name != '全部'">
                  <div
                    :class="[
                      'item-name',
                      selectIndex == item.id ? 'select' : '',
                    ]"
                  >
                    {{ item.name }}
                  </div>
                </div>
              </template>
              <div class="card_classContent">
                <div
                  v-for="(item, index) in options"
                  :key="index"
                  @click="handleChange(item)"
                  :class="[
                    'item-name-sub',
                    selectIndexSub == item.id ? 'select-sub' : '',
                  ]"
                >
                  {{ item.name }}
                </div>
              </div>
            </el-popover>
          </div>
        </div>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleClear">清空选项</el-button>
      </el-form-item>
    </el-form>
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
      </el-table>
    </div>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref, onMounted } from "vue";
import {
  ApiGetProductsCategory,
  ApiGetProductsList,
} from "@/api/launchmanagement";
const props = {
  expandTrigger: "hover" as const,
  value: "id",
  label: "name",
  children: "sub",
  checkStrictly: true,
};
const SampleMap = reactive({
  true: "是",
  false: "否",
});
let modelClassification = ref([]);
const GetProductsCategory = () => {
  ApiGetProductsCategory().then((res) => {
    modelClassification.value = res.sub;
  });
};

let options = ref([]);
let selectIndex = ref("");
let type = ref("");
const handleSelectProduct = (item) => {
  selectIndex.value = item.id;
  options.value = item.sub;
  type.value = "lv_1";
  GetProductsList(selectIndex.value, type.value);
};
let selectIndexSub = ref("");
const handleChange = (item) => {
  selectIndexSub.value = item.id;
  type.value = "lv_2";
  GetProductsList(selectIndexSub.value, type.value);
};

let modelData = ref([]);
let pageObj = reactive({
  page: 1,
  size: 10,
  total: 0,
});
const GetProductsList = (id, type) => {
  ApiGetProductsList(id, type).then((res) => {
    modelData.value = res.data;
  });
};
const handleClear = () => {
  selectIndex.value = "";
  selectIndexSub.value = "";
  type.value = "";
  GetProductsList(selectIndexSub.value, type.value);
};
onMounted(() => {
  GetProductsCategory();
  GetProductsList(selectIndex.value, type.value);
});
</script>
<style lang="scss" scoped>
.card_classContent {
  .item-name {
    padding: 0rem 1rem;
    margin: 0rem 1rem;
    cursor: pointer;
  }
  .select {
    background-color: #f1f1f4;
    color: #46029a;
    border-radius: 0.5rem;
  }
}

.item-name-sub {
  padding: 0.3rem 0.625rem;
  margin: 0.5rem 0rem;
  cursor: pointer;
}
.select-sub {
  background-color: #f1f1f4;
  color: #46029a;
  border-radius: 0.5rem;
  cursor: pointer;
}
</style>
