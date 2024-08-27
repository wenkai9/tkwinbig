from django.urls import path
from . import views

urlpatterns = [
    # 创建任务
    path('create_task', views.create_task, name='create_task'),
    # 启动任务
    path('start_task/<str:taskId>', views.start_task, name='start_task'),
    # 获取全部任务
    path('list_tasks', views.list_tasks, name='list_tasks'),
    # 获取投放任务下的rpa任务
    path('get_rpa_tasks/<str:taskId>', views.get_rpa_tasks, name='get_rpa_tasks'),
    # 获取分页任务
    path('list_tasks/<int:page>', views.list_tasks, name='list_tasks_page'),
    # 获取任务下的店铺
    path('get_shop/<int:taskId>', views.get_shop, name='get_product'),
    # 所有任务总和
    path('tasks/summary', views.get_tasks_sum, name='tasks_summary'),
    # 删除任务
    path('delete_task/<int:taskId>', views.delete_task, name='delete_task'),
    # 向量检索
    path('retrieval', views.retrieval, name='retrieval'),
    # chat
    path('chat/<str:taskId>', views.chat, name='chat'),
    # chat2
    path('chat2', views.chat2, name='chat2'),
    # 达人邀约
    path('tk_invitation', views.tk_invitation, name='tk_invitation'),
    # 达人邀约接收邀约状态
    path('get_invitation/<str:taskId>', views.get_invitation, name='get_invitation'),
    # 展示邀约任务的达人
    path('get_task_creator/<str:taskId>', views.get_task_creator, name='get_task_creator'),
    # 达人私信
    path("seller_im/<str:taskId>", views.seller_im, name="seller_im"),
    # 获取达人私信状态
    path("get_im/<str:taskId>", views.get_im, name="get_im_msg"),
    # 获取达人私信信息
    path("get_im_info/<str:taskId>", views.get_im_info, name="get_im_info"),
    # 达人私信聊天记录
    path("seller_im_msg/<str:taskId>", views.seller_im_msg, name="seller_im_msg"),
    # 过滤达人
    path('filter_creator/<str:taskId>', views.filter_creator, name='filter_invitations')
]
