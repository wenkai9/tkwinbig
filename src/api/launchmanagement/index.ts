import service from "@/service/service";
import axios from 'axios';
export function ApiGetProducts(params: any, page: number, size: number) {
  return service.request({
    url: `/user/list_products?page=${page}&size=${size}`,
    method: "get",
    params,
  });
}

export function ApiAddProducts(data: any, page: number, size: number) {
  return service.request({
    url: `/user/add_products?page=${page}&size=${size}`,
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

export function ApiEditProducts(data: any, product_id) {
  return service.request({
    url: `/user/update_product/${product_id}`,
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
export function ApiGetListRules(page: number, size: number) {
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
export function ApiGetTasks(tage: number, size: number) {
  return service.request({
    url: `/user/list_tasks?tage=${tage}&size=${size}`,
    method: "get",
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

