from django.db import models
from app.goods.models import Goods
from app.shops.models import Shop
from app.users.models import User


class Task(models.Model):
    TASK_STATUS_CHOICES = (
        ('1', '未启动'),
        ('2', '正在进行'),
        ('3', '已完成'),
    )
    taskId = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)  # 任务可以对应多个店铺  shops = models.ManyToManyField(Shop)
    product = models.ForeignKey(Goods, on_delete=models.CASCADE)
    region = models.CharField(max_length=20)
    status = models.CharField(max_length=1, choices=TASK_STATUS_CHOICES, default='1')
    match_quantity = models.IntegerField(null=True)
    willing_quantity = models.IntegerField(null=True)
    send_quantity = models.IntegerField(null=True)
    total_invitations = models.IntegerField(null=True)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.taskId)

    class Meta:
        db_table = 'tk_tasks'


class Creators(models.Model):
    taskId = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    product = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.taskId)

    class Meta:
        db_table = 'creators'


# 达人私信的信息
class Tk_im(models.Model):  #需修改成Tk_seller及修改字段
    taskId = models.CharField(max_length=255)
    type = models.IntegerField(blank=True, null=True)
    region = models.CharField(max_length=20)
    dialogId = models.CharField(max_length=255, blank=True, null=True)
    refTaskid = models.CharField(max_length=255, blank=True, null=True)
    userId = models.CharField(max_length=255, blank=True, null=True)
    shopId = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    receivestatus = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    createAt = models.DateTimeField(auto_now_add=True)
    sendAt = models.DateTimeField(blank=True, null=True)
    complateAt = models.DateTimeField(auto_now=True, blank=True, null=True)
    checkedAt = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.taskId)

    class Meta:
        db_table = 'tk_im'


#素人私信的信息
class Tkuser_im(models.Model):  # 需修改字段及修改表名为Tkuser_im
    taskId = models.CharField(max_length=255)
    type = models.IntegerField(blank=True, null=True)
    region = models.CharField(max_length=20)
    userId = models.CharField(max_length=255, blank=True, null=True)
    dialogId = models.CharField(max_length=255, blank=True, null=True)
    refTaskid = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    receivestatus = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    createAt = models.DateTimeField(auto_now_add=True)
    sendAt = models.DateTimeField(blank=True, null=True)
    complateAt = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.taskId)

    class Meta:
        db_table = 'tkuser_im'


# 邀约信息
class Tk_invacation(models.Model):
    type = models.IntegerField(blank=True, null=True)
    taskId = models.CharField(max_length=255)
    region = models.CharField(max_length=20)
    refTaskid = models.CharField(max_length=255, blank=True, null=True)
    userId = models.CharField(max_length=255, blank=True, null=True)
    dialogId = models.CharField(max_length=255, blank=True, null=True)
    shopId = models.CharField(max_length=255, blank=True, null=True)
    productId = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    receivestatus = models.IntegerField(blank=True, null=True)
    delivery_id = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    createAt = models.DateTimeField(auto_now_add=True)
    complateAt = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.taskId)

    class Meta:
        db_table = 'tk_invacation'


#聊天记录表
class Tk_information(models.Model):
    taskId = models.CharField(max_length=255)
    role = models.CharField(max_length=20)
    userName = models.CharField(max_length=20)
    content = models.TextField()
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.taskId)

    class Meta:
        db_table = 'tk_information'


# chat对话表
class Tk_chat(models.Model):
    taskId = models.CharField(max_length=255)
    role = models.CharField(max_length=20)
    userName = models.CharField(max_length=100)
    content = models.TextField()
    isAgree_invitation = models.BooleanField(default=False)
    sendTime = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.taskId)

    class Meta:
        db_table = 'tk_chat'


from mongoengine import Document, EmbeddedDocument, fields


# 达人私信信息
class Content(EmbeddedDocument):
    shopId = fields.StringField(required=True)
    creatorId = fields.StringField(required=True)
    text = fields.StringField(required=True)


class Tk_seller_im(Document):
    _id = fields.StringField(required=True)
    userId = fields.StringField(required=True)
    taskId = fields.StringField(required=True)
    status = fields.IntField(required=True)
    receiveStatus = fields.IntField(required=True)
    sendRetryCount = fields.IntField(required=True)
    sendFailureCode = fields.StringField()
    message = fields.StringField(required=True)
    createdAt = fields.DateTimeField(required=True)
    completedAt = fields.DateTimeField()
    checkedAt = fields.DateTimeField()
    sentAt = fields.DateTimeField()
    type = fields.IntField(required=True)
    region = fields.StringField(required=True)
    refTaskId = fields.StringField()
    dialogId = fields.StringField()
    content = fields.EmbeddedDocumentField(Content)


# 达人私信聊天记录
class Tk_seller_dialog(Document):
    _id = fields.StringField(required=True)
    shopId = fields.StringField(required=True)
    CreatorId = fields.StringField(required=True)
    Content = fields.EmbeddedDocumentField(Content)
    UpdateAt = fields.DateTimeField(required=True)

# 达人邀约信息
class Image(EmbeddedDocument):
    thumb_url_list = fields.ListField(fields.URLField())


class Product(EmbeddedDocument):
    product_id = fields.StringField(required=True)
    product_status = fields.IntField(required=True)
    group_product_status = fields.IntField(required=True)
    title = fields.StringField(required=True)
    image = fields.EmbeddedDocumentField(Image)
    item_sold = fields.IntField(required=True)
    target_commission = fields.IntField(required=True)
    commission_effective_time = fields.StringField(required=True)
    open_commission = fields.IntField(required=True)
    effective_status = fields.IntField(required=True)


class BaseInfo(EmbeddedDocument):
    creator_id = fields.StringField(required=True)
    nick_name = fields.StringField(required=True)
    user_name = fields.StringField(required=True)
    selection_region = fields.StringField(required=True)


class Creator(EmbeddedDocument):
    product_add_cnt = fields.IntField(required=True)
    content_posted_cnt = fields.IntField(required=True)
    base_info = fields.EmbeddedDocumentField(BaseInfo)


class Tk_Invitation(Document):
    id = fields.StringField(required=True, primary_key=True)
    name = fields.StringField(required=True)
    creator_cnt = fields.IntField(required=True)
    creator_added_cnt = fields.IntField(required=True)
    creator_posted_cnt = fields.IntField(required=True)
    product_cnt = fields.IntField(required=True)
    group_type = fields.IntField(required=True)
    start_time = fields.StringField(required=True)
    end_time = fields.StringField(required=True)
    update_time = fields.StringField(required=True)
    creator_id_list = fields.ListField(fields.EmbeddedDocumentField(Creator))
    product_list = fields.ListField(fields.EmbeddedDocumentField(Product))
