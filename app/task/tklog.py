
''''''
'''
文杰这边处理：
        网络超时---修复--超时60s
        本地客户端超时请求或者是本地vpn的超时请求


5.31
    海平处理：
            闪退问题----已解决
            rpa建联的时间选择问题 ----未解决6.30号,7.1号后面无法选择
            rpa建联失败再执行的时候会执行之前失败的问题-----已解决
            rpa建联达人名相似，没法选择达人-----------已解决
6.1
    文杰处理：
        邀约计划检索接口需要是达人，不能是素人------待处理
        邀约计划生成的发送信息对应每个产品-------待处理
    海平处理：
        建联邀约接口那边判断是达人还是素人-----待处理
        建联接口达人广场搜不到需要继续执行，执行下一步-----待处理
        私信接口点击发送后不弹出浏览器，没办法看到私信的具体流程-----待处理
        私信消息没发出去 但是能够获取到状态RPA正在执行任务-----待处理
        接收信息没有返回私信信息-----待处理
        rpa私信状态怎么获取的-----待处理2


6.3
    海平处理：
        rpa邀约的时候如果有的达人之前已经被邀约过了，会停止邀约(达人:tommysmileyofficial)----待处理
        缺少真实达人数据测试----待处理

6.4
       rpa建联的时候有时候会走到选择商品的位置停止进行 -----已解决
       
6.5
        rpa素人私信需要传入userid，数据集里没有该字段，无法进行私信


6.11    rpa素人私信 如果之前私信的素人未回复消息，rpa会一直在浏览器上查看该达人私信，在查询的过程中，如果给新的素人发私信，会私信发给上一个素人

'''




'''
    rpa邀约流程：
          用户点击启动后启动任务 开始执行rpa建联 rpa建联期间如果有搜索不到的达人会直接拿该达人到素人私信接口根据素人的名称去进行私信
                                                            --->处理rpa邀约建联如果有搜索不到达人的情况 获取到达人广场搜不到的达人并将那些达人放入素人私信接口 根据素人的名称去进行私信 一直轮询完所有达人停止
          起一个定时任务，每次执行完rpa建联私信接口后，定时查询任务内容查询接口(参数为rpa邀约建联的taskId,私信的taskId) 时间为每隔2分钟执行一次 更新refTaskid,shopId,status以及message信息
          根据查询出来creatorIds的列表计算出邀约了多少人写入数据库表对应taskid的send_quantity字段中
          再起一个定时任务，定期查询rpa建联达人的私信的接口，查看是否回复 如果回复了计入数据库回复字段(willing_quantity)+1,如果同意邀约，记入同意邀约字段(match_quantity)+1
          达人私信和素人私信：如果该达人回复了，根据接收私信内容接口去拿到会话信息并放入chat接口生成新的信息然后在放入私信接口去执行----来回循环
    数据展示
          展示出任务总数,邀约总数,回复总数,同意邀约总数
          下面展示每个任务的情况，用户可以点击查看，会显示出该任务同意邀约的达人信息(列表的形式)
'''

'''
遍历excel里面的handle列的数据，把数据遍历给chat接口的参数creators，其中taskid和creator是这个chat接口的唯一标识，调用chat接口生成信息message，把chat的taskid，username和message存入数据库
之后再遍历message信息，给handle列下的达人发送私信，信息是每个达人对应的message信息，调用私信接口，把私信的信息存入数据库

查找数据库tkuser_im表，获取status状态，如果status状态是5则拿着这个status状态是5的taskid去查找对话内容，把对话内容的最后一条存入数据库，taskid，username，message
然后通过这个username去查chat接口的username，拿相同username下最后一行的数据，
拿着chat接口的taskid和username以及status状态是5的taskid的聊天记录表最后一条信息去再次调用chat接口，生成新的对话内容new_message,存入数据库

最后调用会话接口，其中参数username是chat接口的username，对话信息的新的内容new_message,发送回信
'''





'''
需修改
     检索接口的taskid, chat接口, rpa任务接口需要相关联
     检索表以及rpa任务表需要有chat接口的标识，这样可以通过该标识来回查找
     检索表
     class Creators(models.Model):
        taskId = models.CharField(max_length=255)
        tag = models.CharField(max_length=255)
        product = models.CharField(max_length=255)
        chat = models.ForeignKey(Tk_chat, on_delete=models.CASCADE, blank=True, null=True)
     
     chat表
     class Tk_chat(models.Model):
        taskId = models.CharField(max_length=255)
        role = models.CharField(max_length=20)
        userName = models.CharField(max_length=20)
        content = models.TextField()
        isAgree_invitation = models.BooleanField(default=False)
        sendTime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
     rpa任务表
class Tkuser_im(models.Model):
    taskId = models.CharField(max_length=255)
    type = models.IntegerField(blank=True, null=True)
    region = models.CharField(max_length=20)
    userId = models.CharField(max_length=255, blank=True, null=True)
    dialogId = models.CharField(max_length=255, blank=True, null=True)
    refTaskid = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    createAt = models.DateTimeField(auto_now_add=True)
    sendAt = models.DateTimeField(blank=True, null=True)
    complateAt = models.DateTimeField(auto_now=True, blank=True, null=True)
    chat = models.ForeignKey(Tk_chat, on_delete=models.CASCADE, blank=True, null=True, related_name='tkuser_ims', to_field='taskId')
     
'''