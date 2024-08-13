import service from "@/service/service";


export function ApiGetChat(taskId: string) {
  return service.request({
    url: `/user/put_receive/${taskId}`,
    method: "put",

  });
}


// 对话 chat
export function ApiChat(data: any) {
  return service.request({
    url: `/user/chat`,
    method: "post",
    data
  });
}