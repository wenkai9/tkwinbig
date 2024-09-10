<template>
  <div>
    <el-table
      :data="modelData"
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
          <!-- {{ scope.row.title }} -->
          <el-tooltip
            class="item"
            effect="dark"
            :content="scope.row.title"
            placement="top"
          >
            <div class="wrap_title">{{ scope.row.title }}</div>
          </el-tooltip>
        </template>
      </el-table-column>
      <el-table-column label="物品描述" width="280">
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
      <el-table-column label="物品标签" width="220">
        <template #default="scope">
          {{ scope.row.match_tag }}
        </template>
      </el-table-column>
      <el-table-column label="是否免费邮寄商品" width="150">
        <template #default="scope">
          {{ SampleMap[scope.row.hasFreeSample] }}
        </template>
      </el-table-column>
      <el-table-column label="佣金率">
        <template #default="scope"> {{ scope.row.commissionRate }}</template>
      </el-table-column>
      <el-table-column label="合作费">
        <template #default="scope">
          {{ scope.row.CooperationFee }}
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
      <el-table-column fixed="right" label="操作" width="250">
        <template #default="scope">
          <el-button
            link
            v-if="!scope.row.product_status"
            type="primary"
            size="small"
            @click="handleBind(scope.row)"
          >
            绑定规则
          </el-button>
          <el-button
            link
            type="primary"
            size="small"
            @click="handleEdit(scope.row)"
          >
            编辑物品
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
          <el-table
            :header-cell-style="{
              backgroundColor: '#f6f7fc',
              color: '#1f283c',
              fontSize: '14px',
              textAlign: 'center',
            }"
            :cell-style="{ textAlign: 'center' }"
            :data="modelRulesData"
            @current-change="choiceRules"
            highlight-current-row
          >
            <el-table-column label="建联名称" width="280">
              <template #default="scope">
                {{ scope.row.name }}
              </template>
            </el-table-column>
            <el-table-column label="视频拍摄要求" width="580">
              <template #default="scope">
                <el-tooltip
                  class="item"
                  effect="dark"
                  :content="scope.row.requirement"
                  placement="top"
                >
                  <template #content>
                    <p style="width: 280px">
                      <span>{{ scope.row.requirement }} </span>
                    </p>
                  </template>
                  <div>
                    <div class="wrap_row2">{{ scope.row.requirement }}</div>
                  </div>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column label="佣金">
              <template #default="scope">
                ¥{{ scope.row.commission }}
              </template>
            </el-table-column>
          </el-table>
          <div style="margin-top: 20px; text-align: right">
            <el-button type="primary" @click="handleSubmitBindRule"
              >提交</el-button
            >
          </div>
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
    <!-- 编辑物品 -->
    <div>
      <el-dialog v-model="editDialog" title="编辑物品">
        <div>
          <el-form
            class="demo-form-inline"
            style="max-width: 600px"
            label-width="auto"
          >
            <el-form-item label="商品标题:">
              <el-input
                v-model.trim="editGoodsObj.title"
                placeholder="请输入商品标题"
                clearable
              />
            </el-form-item>
            <el-form-item label="商品描述:">
              <el-input
                type="textarea"
                v-model.trim="editGoodsObj.description"
                placeholder="请输入商品描述"
                clearable
              />
            </el-form-item>
            <el-form-item label="商品价格:">
              <el-input
                onkeyup="value=value.replace(/[^\d]/g,'')"
                v-model.trim="editGoodsObj.price"
                placeholder="请输入商品价格"
                clearable
              />
            </el-form-item>
            <el-form-item label="商品链接:">
              <el-input
                v-model.trim="editGoodsObj.product_link"
                placeholder="请输入商品链接"
                clearable
              />
            </el-form-item>

            <el-form-item label="是否免费寄样品:">
              <el-switch
                inline-prompt
                v-model="editGoodsObj.hasFreeSample"
                active-text="开启"
                inactive-text="关闭"
              />
            </el-form-item>
            <el-form-item label="佣金率:">
              <el-input
                v-model.trim="editGoodsObj.commissionRate"
                placeholder="请输入商品佣金率"
                clearable
              />
            </el-form-item>
            <el-form-item label="合作费:">
              <el-input
                v-model.trim="editGoodsObj.CooperationFee"
                placeholder="请输入商品合作费"
                clearable
              />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="handleSubmitEditGoods"
                >提交</el-button
              >
            </el-form-item>
          </el-form>
        </div>
      </el-dialog>
    </div>
  </div>
</template>
<script setup lang="ts">
import { reactive, ref } from "vue";
const props = defineProps({
  ShopId: String,
});
import {
  ApiGetProducts,
  ApiUpdataProducts,
  ApiBindProducts,
  ApiDeteleProducts,
  ApiGetListRules,
  ApiEditProducts,
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
const editDialog = ref(false);
let formData = ref({
  raidsysrule_id: "",
});
const id = ref("");
const GetProducts = async (id) => {
  try {
    loading.value = true;
    const params = {
      shopId: id || props.ShopId,
    };
    const response = await ApiGetProducts(params, pageObj.page, pageObj.size);
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
  GetProducts(props.ShopId);
};
const changeSize = (size: number) => {
  pageObj.size = size;
  GetProducts(props.ShopId);
};

const handleBind = (item: object) => {
  dialogVisible.value = true;
  id.value = item.product_id;
};

const editGoodsObj = ref();
const goodsId = ref("");
const handleEdit = (item: Object) => {
  editDialog.value = true;
  editGoodsObj.value = item;
  goodsId.value = item.product_id;
};

const handleSubmitEditGoods = () => {
  ApiEditProducts(goodsId.value, editGoodsObj.value).then((res) => {
    console.log(res, "修改商品======");
    if (res.code !== 200) {
      return ElMessage({
        message: res.errmsg,
        type: "warning",
      });
    }
    ElMessage({
      message: "操作成功",
      type: "success",
    });
    editDialog.value = false;
    GetProducts(props.ShopId);
  });
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
  if (data != null) {
    formData.value.raidsysrule_id = data.id;
  }
};
const handleSubmitBindRule = () => {
  ApiBindProducts(formData.value, id.value).then((res) => {
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
    GetProducts(props.ShopId);
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
        GetProducts(props.ShopId);
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
<style lang="scss" scoped>
.wrap_row2 {
  cursor: pointer;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
  text-overflow: ellipsis;
}
::v-deep .el-table__body tr.current-row > td {
  background: #61afff !important;
  color: #ffffff !important;
}
.wrap_title {
  cursor: pointer;
}
</style>
