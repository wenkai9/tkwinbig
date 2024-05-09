import service from "@/service/service";
// page: number, size: number
export function ApiGetProducts(params: any) {
  return service.request({
    // url: `/user/list_products?page=${page}&size=${size}`,
    url: `/user/list_products`,
    method: "get",
    params,
  });
}