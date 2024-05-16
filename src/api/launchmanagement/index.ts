import service from "@/service/service";
import axios from 'axios';
export function ApiGetProducts(params: any, page: number, size: number) {
  return service.request({
    url: `/user/list_products?page=${page}&size=${size}`,
    method: "get",
    params,
  });
}

export function ApiAddProducts(data: any) {
  return service.request({
    url: `/user/products/upload`,
    method: "post",
    data,
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


// 查询建联列表
export function ApiGetTasks(tage: number, size: number) {
  return service.request({
    url: `/user/list_tasks?tage=${tage}&size=${size}`,
    method: "get",
  });
}