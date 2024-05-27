from django.urls import path
from . import views

urlpatterns = [
    # 创建任务
    path('create_task', views.create_task, name='create_task'),
    # 启动任务
    path('start_task/<int:taskId>', views.start_task, name='start_task'),
    # 获取全部任务
    path('list_tasks', views.list_tasks, name='list_tasks'),
    path('list_tasks/<int:page>', views.list_tasks, name='list_tasks_page'),
    # 所有任务总和
    path('tasks/summary', views.get_tasks_sum, name='tasks_summary'),
    # 删除任务
    path('delete_task/<int:taskId>', views.delete_task, name='delete_task'),
    # 向量检索
    path('retrieval', views.retrieval, name='retrieval'),
    # chat对话
    path('chat', views.chat, name='chat'),
]
