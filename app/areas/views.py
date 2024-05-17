from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from app.areas.models import Area

"""
# 1.确认已经进入数据库
# select * from tb_areas;

# 2.查询所有的省份
# select * from tb_areas
# where parent_id is null;

# 3. 根据 省份id 查询所有的市
# 河北省下面所有市
# select id from tb_areas
# where name='北京市';

# select * from tb_areas
# where parent_id=(select id from tb_areas
# where name='北京市' order by id desc limit 1);
"""


class ProvinceView(View):
    def get(self, request):
        provinces_model_list = Area.objects.filter(parent_id__isnull=True)

        # objects==>json
        province_list = []
        for p in provinces_model_list:
            province_list.append({
                'p_id': p.id,
                'p_name': p.name
            })

        return JsonResponse({'code': 0, 'province_list': province_list})


class CityDistrictView(View):
    def get(self, request, area_id):
        # 1. 先找 省份
        province = Area.objects.get(id=area_id)

        # #  城市 ==> 省份 n:1
        # province = city_model_list[0].parent
        # 2. 通过省份 找下面所有城市 ： 1：n
        city_model_list = province.subs.all()

        # objects==>json
        province_list = []
        for p in city_model_list:
            province_list.append({
                'id': p.id,
                'name': p.name
            })

        sub_data = {
            'id': province.id,
            'name': province.name,
            'subs': province_list
        }

        return JsonResponse({'code': 0, 'sub_data': sub_data})
