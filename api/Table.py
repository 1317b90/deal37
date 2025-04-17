from tortoise import fields
from tortoise.models import Model

# 资讯表
class Information(Model):
    id = fields.IntField(pk=True, generated=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    author = fields.CharField(max_length=50)
    img_url = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

# 用户表
class User(Model):
    id = fields.IntField(pk=True, generated=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=255)
    name = fields.CharField(max_length=50)
    phone = fields.CharField(max_length=20, null=True)
    balance=fields.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    role = fields.CharField(max_length=20, default='buy')
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

# 商品表
class Commodity(Model):
    id = fields.IntField(pk=True, generated=True)
    name = fields.CharField(max_length=255)  # 商品名称
    price = fields.DecimalField(max_digits=10, decimal_places=2,default=0.00)  # 商品价格
    specification = fields.CharField(max_length=10,default="统货")  # 商品规格
    inventory = fields.IntField(default=0)  # 商品库存
    sales = fields.IntField(default=0)  # 销量
    sell_id = fields.IntField()  # 对应卖家id
    sell_name = fields.CharField(max_length=50)  # 对应卖家名称
    image = fields.CharField(max_length=255)  # 图片链接
    onShelf = fields.BooleanField(default=True)  # 是否上架
    created_at = fields.DatetimeField(auto_now_add=True)  # 创建时间
    updated_at = fields.DatetimeField(auto_now=True)  # 更新时间

# 订单表
class Order(Model):
    id = fields.CharField(max_length=255, pk=True)  # 订单号
    buy_id = fields.IntField()  # 买家id
    sell_id = fields.IntField()  # 卖家id
    commodity_id = fields.IntField()  # 商品id
    amount = fields.DecimalField(max_digits=10, decimal_places=2,default=0.00)  # 订单价格
    number = fields.IntField(default=0)  # 订单数量
    address = fields.CharField(max_length=255)  # 订单地址
    phone = fields.CharField(max_length=20)  # 订单电话
    express_number = fields.CharField(max_length=255,default="")  # 快递单号
    status = fields.CharField(max_length=20, default="待付款")  # 订单状态
    pay_status = fields.BooleanField(default=False)  # 支付状态
    created_at = fields.DatetimeField(auto_now_add=True)  # 创建时间
    updated_at = fields.DatetimeField(auto_now=True)  # 更新时间


# 聊天消息表
class Message(Model):
    id = fields.IntField(pk=True, generated=True)
    sender_id = fields.IntField()  # 发送者ID
    receiver_id = fields.IntField()  # 接收者ID
    content = fields.TextField()  # 消息内容
    is_read = fields.BooleanField(default=False)  # 是否已读
    created_at = fields.DatetimeField(auto_now_add=True)  # 发送时间
