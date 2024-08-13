import service from "@/service/service";



export function ApiPostSendMsg(data: any) {
  return service.request({
    url: `/user/tiktok_im`,
    method: "post",
    data
  });
}


// export function ApiPostSendMsg_Invitation(data: any) {
//   return service.request({
//     url: `/user/tiktok_invitation`,
//     method: "post",
//     data
//   });
// }

export function ApiPostSendMsg_Invitation(task_id: string) {
  return service.request({
    url: `/user/tiktok_invitation/${task_id}`,
    method: "post",
  });
}