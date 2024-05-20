import service from "@/service/service";


export function ApiGetRegion(area_id) {
  return service.request({
    // url: `user/areas/?area_id=${area_id}`,
    url: `user/areas/${area_id}/`,
    method: "get",
  });
}