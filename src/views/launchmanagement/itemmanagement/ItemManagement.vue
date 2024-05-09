<template>
  <div>
    <el-card>
      <div>
        
      </div>
      <div>
        <el-table :data="modelData" style="width: 100%">
          <el-table-column prop="title" label="物品名称" width="180" />
          <el-table-column prop="description" label="物品描述" width="180" />
          <el-table-column prop="primary_category" label="一级分类" />
          <el-table-column prop="secondary_category" label="二级分类" />
          <el-table-column prop="description" label="物品标签" />
          <el-table-column prop="description" label="物品状态" />
          <el-table-column prop="description" label="建联规则" />
          <el-table-column fixed="right" label="操作" width="120">
            <template #default="scope">
              <el-button link type="primary" size="small" @click="handleEdit(scope.row)">
                修改
              </el-button>
              <el-button link type="primary" size="small" @click="handleDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <div>
          <el-pagination v-model:current-page="pageObj.page" v-model:page-size="pageObj.size" :page-sizes="[10, 20, 50]"
            layout="total, sizes, prev, pager, next, jumper" :total="pageObj.total" @size-change="handleSizeChange"
            @current-change="handleCurrentChange" />

        </div>
      </div>
    </el-card>
  </div>
</template>
<script setup lang="ts">
import { ApiGetProducts } from '@/api/launchmanagement'
import { reactive, ref } from 'vue'
const modelData = ref([])
const pageObj = reactive({
  page: 1,
  size: 10,
  total: 0
})
// pageObj.page,pageObj.size,
ApiGetProducts("").then((res) => {
  console.log(res);
  modelData.value = [...res.products]

})
const handleSizeChange = () => {

}
const handleCurrentChange = () => { }

const handleEdit = (item: object) => {
  console.log(item);
}
const handleDelete = (item: object) => {
  console.log(item);
}
</script>
<style lang="">

</style>