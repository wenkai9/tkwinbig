from django.http import JsonResponse
from django.views import View
from app.areas.models import Area


class AreaView(View):
    def get(self, request, area_id=None):
        if area_id is None or area_id == 0:
            # 如果没有提供 area_id 或者 area_id 为 0，则返回所有省份信息
            provinces_model_list = Area.objects.filter(parent_id__isnull=True)
            # 将查询到的对象转换为 JSON 格式
            province_list = []
            for p in provinces_model_list:
                province_list.append({
                    'p_id': p.id,
                    'p_name': p.name
                })
            return JsonResponse({'code': 200, 'province_list': province_list})
        else:
            # 否则返回指定省份的市区信息
            try:
                province = Area.objects.get(id=area_id)
            except Area.DoesNotExist:
                return JsonResponse({'code': 404, 'message': 'Province not found'}, status=404)

            city_model_list = province.subs.all()

            # 将市区信息转换为 JSON 格式
            city_list = []
            for city in city_model_list:
                city_list.append({
                    'id': city.id,
                    'name': city.name
                })

            sub_data = {
                'id': province.id,
                'name': province.name,
                'subs': city_list
            }

            return JsonResponse({'code': 200, 'sub_data': sub_data})
