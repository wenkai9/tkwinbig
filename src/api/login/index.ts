import service from "@/service/service";

export function ApiHandlelogin(data: any) {
  return service.request({
    url: "user/user/login",
    method: "post",
    data,
  });
}