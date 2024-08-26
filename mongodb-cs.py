# from mongoengine import Document, EmbeddedDocument, StringField, IntField, DateTimeField, EmbeddedDocumentField, connect
# from datetime import datetime
#
# # 连接 MongoDB 数据库
# connect('tk', host='localhost', port=27017)
#
#
# # 定义嵌入文档
# class Content(EmbeddedDocument):
#     shop_id = StringField(required=True)
#     creator_id = StringField(required=True)
#     text = StringField(required=True)
#
#
# # 定义主文档
# class Invitation(Document):
#     user_id = StringField(required=True)
#     task_id = StringField(required=True)
#     status = IntField(required=True)
#     receive_status = IntField(required=True)
#     send_retry_count = IntField(required=True)
#     send_failure_code = StringField()
#     message = StringField(required=True)
#     created_at = DateTimeField(required=True)
#     completed_at = DateTimeField()
#     checked_at = DateTimeField()
#     sent_at = DateTimeField()
#     type = IntField(required=True)
#     region = StringField(required=True)
#     ref_task_id = StringField()
#     dialog_id = StringField()
#     content = EmbeddedDocumentField(Content)
#
#
# # 创建 Content 实例
# content_instance = Content(
#     shop_id='shop123',
#     creator_id='creator456',
#     text='This is a sample content'
# )
#
# # 创建 Invitation 实例
# invitation_instance = Invitation(
#     user_id='user789',
#     task_id='task001',
#     status=1,
#     receive_status=0,
#     send_retry_count=3,
#     send_failure_code=None,
#     message='Invitation message text',
#     created_at=datetime.utcnow(),
#     completed_at=None,
#     checked_at=None,
#     sent_at=None,
#     type=1,
#     region='US',
#     ref_task_id='ref001',
#     dialog_id=None,
#     content=content_instance
# )
#
# # 保存到数据库
# invitation_instance.save()
#
# print("Data successfully inserted into MongoDB.")

from bson import ObjectId

# 生成新的 ObjectId
new_id = ObjectId()

# 打印生成的 ObjectId
print("生成的 ObjectId:", new_id)

# 如果需要，可以将其转换为字符串
id_str = str(new_id)
print("ObjectId 的字符串表示:", id_str)
