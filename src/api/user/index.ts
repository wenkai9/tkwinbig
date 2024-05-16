import service from "@/service/service";



export function ApigetUser() {
  return service.request({
    url: `user/user/user_profile`,
    method: "get",

  });
}

export function ApiChangePsw(data: any) {
  return service.request({
    url: `user/user/change_password`,
    method: "post",
    data
  });
}