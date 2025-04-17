from fastapi import APIRouter, HTTPException, Request,Body,BackgroundTasks
from Table import Order,Commodity
import uuid
from Config import create_alipay
from user import update_balance
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import Optional
from fastapi import Query

app = APIRouter(tags=["订单管理"])

Order_Pydantic = pydantic_model_creator(Order, name="Order")
OrderIn_Pydantic = pydantic_model_creator(Order, name="OrderIn", exclude_readonly=True)

@app.get("/order/list", summary="获取订单列表")
async def get_orders(
    page: int = Query(1, description="页码"),
    limit: int = Query(10, description="每页数量"),
    sell_id: Optional[str] = Query(None, description="卖家ID"),
    buy_id: Optional[str] = Query(None, description="买家ID")
):
    """
    获取订单列表，支持分页和按卖家/买家ID搜索
    """
    skip = (page - 1) * limit
    
    # 构建查询条件
    query = Order.all()
    if sell_id:
        query = query.filter(sell_id=sell_id)
    if buy_id:
        query = query.filter(buy_id=buy_id)
    
    # 获取总数
    total = await query.count()
    
    # 获取分页数据
    orders = query.offset(skip).limit(limit).order_by("-created_at")
    
    # 序列化数据
    order_list = await Order_Pydantic.from_queryset(orders)
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": order_list
    }

@app.put("/order/{order_id}", summary="更新订单")
async def update_order(
    order_id: str,
    status: Optional[str] = Body(None, description="订单状态"),
    express_number: Optional[str] = Body(None, description="快递单号")
):
    """
    根据订单ID修改订单状态和快递单号
    """
    # 查找订单
    order = await Order.filter(id=order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 更新字段
    update_data = {}
    if status is not None:
        update_data["status"] = status
    if express_number is not None:
        update_data["express_number"] = express_number
    
    # 如果没有要更新的字段，直接返回
    if not update_data:
        raise HTTPException(status_code=400, detail="未提供更新字段")
    
    # 更新订单
    await Order.filter(id=order_id).update(**update_data)

    return "订单更新成功"


