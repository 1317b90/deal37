from fastapi import APIRouter, Request,Body,BackgroundTasks
from Table import Order,Commodity
import uuid
from Config import create_alipay,pay_notify_url,pay_return_url
from user import update_balance


app = APIRouter(tags=["支付"])


@app.post("/alipay/create")
async def create_pay(
    buy_id: int = Body(...),
    commodity_id: int = Body(...),
    number: float = Body(...),
    address: str = Body(...),
    phone: str = Body(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    # 生成支付路由，让前端页面来打开生成的支付链接 url
    commodity = await Commodity.get(id=commodity_id)
    total_amount=float(commodity.price)*number
    alipay = create_alipay()
    sell_id = commodity.sell_id
    order_id = str(uuid.uuid4().hex)
    order_string = alipay.api_alipay_trade_page_pay(
        # 这些数据应该从数据库获取，这里简化处理
        out_trade_no=order_id,   # 商品订单号（唯一）
        total_amount=total_amount,                       # 商品价格
        subject=commodity.name,                    # 商品名称
        return_url=pay_return_url,  # 前端回调网址
        notify_url=pay_notify_url   # 后端回调网址
    )
    url = f'https://openapi-sandbox.dl.alipaydev.com/gateway.do?{order_string}'

    # 保存到数据库
    data=Order(
        id=order_id,
        buy_id=buy_id,
        sell_id=sell_id,
        commodity_id=commodity_id,
        amount=total_amount,
        number=number,
        address=address,
        phone=phone,
        status="待付款",
        pay_status=False,
    )
    background_tasks.add_task(data.save)
    return {'order_id': order_id,'url': url}


@app.post("/alipay/result")
async def result_pay(request: Request):
    # 支付成功后的异步回调处理
    alipay = create_alipay()
    form_data = await request.form()
    data = dict(form_data)
    signature = data.pop("sign")
    success = alipay.verify(data, signature)

    if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
        # 修改数据库状态
        order_id=data["out_trade_no"]
        order=await Order.get(id=order_id)
        order.pay_status=True
        order.status="待发货"
        await order.save()
        # 买家扣钱
        await update_balance(order.buy_id,-order.amount)
        # 卖家加钱
        await update_balance(order.sell_id,order.amount)

        # 库存-1 销量+1
        commodity=await Commodity.get(id=order.commodity_id)
        commodity.sales+=1
        commodity.inventory-=1
        await commodity.save()
    return "支付失败啦！"




