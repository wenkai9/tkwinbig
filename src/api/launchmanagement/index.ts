import service from "@/service/service";
import axios from 'axios';
export function ApiGetProducts(params: any, page: Number, size: Number) {
  return service.request({
    url: `/user/list_products?page=${page}&size=${size}`,
    method: "get",
    params,
  });
}

export function ApiAddProducts(data: any, page: Number, size: Number) {
  return service.request({
    url: data == '' ? `/user/add_products?page=${page}&size=${size}` : `/user/add_products`,
    // method: "post",
    method: data == '' ? 'get' : 'post',
    data,
  });
}

// 查询商品所有分类all_category_products
export function ApiGetProductsCategory() {
  return service.request({
    url: `/user/all_category_products`,
    method: "get",
  });
}
// 商品列表
export function ApiGetProductsList(id: string, type: string) {
  return service.request({
    url: `/user/all_produts?id=${id}&type=${type}`,
    method: "get",
  });
}

// 修改商品
export function ApiEditProducts(id: string, data: Object) {
  return service.request({
    url: `/user/update_product/${id}`,
    method: "put",
    data
  });
}

export function ApiUpdataProducts(data: any) {
  const formData = new FormData();
  formData.append("csv_file", data);
  axios
    .post("user/upload_csv", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
    .then((res) => {
      console.log(res, "===========");
    });
}

export function ApiBindProducts(data: any, product_id) {
  return service.request({
    url: `/user/bind_rule/${product_id}`,
    method: "put",
    data,
  });
}


export function ApiDeteleProducts(product_id) {
  return service.request({
    url: `/user/delete_product/${product_id}`,
    method: "delete",
  });
}


// export function ApiExportProducts(url) {
export function ApiExportProducts() {
  const link = document.createElement('a');
  axios({
    url: `user/download_excel`,
    method: 'GET',
    responseType: 'blob',
  }).then((response) => {
    const blob = new Blob([response.data], { type: 'application/vnd.ms-excel' });
    const objectUrl = URL.createObjectURL(blob);
    link.href = objectUrl;
    link.setAttribute('download', 'export.xls');
    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);
    URL.revokeObjectURL(objectUrl);

  }).catch((error) => {

    console.error('下载Excel失败:', error);
  });

}

// 查询建联规则列表
export function ApiGetListRules(page: Number, size: Number) {
  return service.request({
    url: `/user/list_rules?page=${page}&size=${size}`,
    method: "get",
  });
}
//修改建联规则
export function ApiEditRules(data: object, id: string) {
  return service.request({
    url: `/user/update_rule/${id}`,
    method: "put",
    data
  });
}
// 删除建联规则
export function ApiDeteleRules(id) {
  return service.request({
    url: `/user/delete_rule/${id}`,
    method: "delete",
  });
}

// 新增建联规则 
export function ApiAddRulesRules(data: object) {
  return service.request({
    url: `/user/add_rules`,
    method: "post",
    data
  });
}


// 查询任务列表
export function ApiGetTasks(page: Number, size: Number) {
  return service.request({
    url: `/user/list_tasks?page=${page}&size=${size}`,
    method: "get",
  });
}
export function ApiGetRetrieval(data: any) {
  return service.request({
    url: `/user/retrieval`,
    method: "post",
    data
  });
}

//启动任务
export function ApiStartTasks(taskId) {
  return service.request({
    url: `/user/start_task/${taskId}`,
    // url: `/user/tk_invitation`,
    method: "post",
    // data
  });
}
// 达人邀约
export function ApiInvitationCreator(data) {
  return service.request({
    url: `/user/tk_invitation`,
    method: "post",
    data
  });
}
// 查看秘钥 get_db_key
export function ApigetQtossKey(data) {
  return service.request({
    url: `/user/get_db_key`,
    method: "post",
    data
  });
}


//获取秘钥
export function ApigetQtossUser(data) {
  return service.request({
    url: `/user/get_rpa_key`,
    method: "post",
    data
  });
}


// 新增建联
export function ApiAddTasks(data) {
  return service.request({
    url: `/user/create_task`,
    method: "post",
    data
  });
}

export function ApiGetSummary() {
  return service.request({
    url: `/user/tasks/summary`,
    method: "get",

  });
}
// 查询投放任务
export function ApiGetRpaTasks(taskId: String, page: Number, size: Number) {
  return service.request({
    url: `/user/get_rpa_tasks/${taskId}?page=${page}&size=${size}`,
    method: "get",

  });
}
// 查看达人
export function ApiGetTaskCreator(taskId: String, page: Number, size: Number) {
  return service.request({
    url: `/user/get_task_creator/${taskId}?page=${page}&size=${size}`,
    method: "get",

  });
}
// 重新邀约
export function ApiResetTask(taskId: String) {
  return service.request({
    url: `/user/modify_rpa_state/${taskId}`,
    method: "PUT",

  });
}

