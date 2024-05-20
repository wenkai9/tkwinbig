import service from "@/service/service";


export function ApigetShopData(params: any, page: number, size: number) {
  return service.request({
    url: `user/list_shops?page=${page}&size=${size}`,
    method: "get",
    params
  });
}

export function ApiAddShopData(data: any) {
  return service.request({
    url: `user/create_shop`,
    method: "post",
    data
  });
}

export function ApiEditShopData(data, shopId) {
  return service.request({
    url: `user/update_shop/${shopId}`,
    method: "put",
    data
  });
}

export function ApiDeleteShop(shopId) {
  return service.request({
    url: `user/delete_shop/${shopId}`,
    method: "delete",

  });
}

