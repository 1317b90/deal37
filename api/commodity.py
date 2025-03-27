from typing import List
from fastapi import APIRouter, HTTPException
from tortoise.contrib.pydantic import pydantic_model_creator
from Table import Commodity

app = APIRouter(tags=["商品管理"])

Commodity_Pydantic = pydantic_model_creator(Commodity, name="Commodity")
CommodityIn_Pydantic = pydantic_model_creator(Commodity, name="CommodityIn", exclude_readonly=True)

@app.post("/commodity", response_model=Commodity_Pydantic, summary="创建商品")
async def create_commodity(commodity: CommodityIn_Pydantic):
    commodity_obj = await Commodity.create(**commodity.dict(exclude_unset=True))
    return await Commodity_Pydantic.from_tortoise_orm(commodity_obj)

@app.get("/commodity/{commodity_id}", response_model=Commodity_Pydantic, summary="获取商品")
async def read_commodity(commodity_id: int):
    commodity = await Commodity_Pydantic.from_queryset_single(Commodity.get(id=commodity_id))
    if not commodity:
        raise HTTPException(status_code=404, detail="商品不存在")
    return commodity

@app.get("/commodities", response_model=List[Commodity_Pydantic], summary="获取所有商品")
async def get_all_commodities(onShelf: bool = None):
    if onShelf is not None:
        return await Commodity_Pydantic.from_queryset(Commodity.filter(onShelf=onShelf))
    return await Commodity_Pydantic.from_queryset(Commodity.all())

@app.put("/commodity/{commodity_id}", response_model=Commodity_Pydantic, summary="更新商品")
async def update_commodity(commodity_id: int, commodity: CommodityIn_Pydantic):
    commodity_obj = await Commodity.get(id=commodity_id)
    if not commodity_obj:
        raise HTTPException(status_code=404, detail="商品不存在")
    await commodity_obj.update_from_dict(commodity.dict(exclude_unset=True))
    await commodity_obj.save()
    return await Commodity_Pydantic.from_tortoise_orm(commodity_obj)

@app.delete("/commodity/{commodity_id}", summary="删除商品")
async def delete_commodity(commodity_id: int):
    deleted_count = await Commodity.filter(id=commodity_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="商品不存在")
    return {"detail": "商品删除成功"}

@app.get("/commodities/search", response_model=List[Commodity_Pydantic], summary="搜索商品")
async def search_commodities(name: str = None):
    query = Commodity.filter()
    if name:
        query = query.filter(name__icontains=name)
    return await Commodity_Pydantic.from_queryset(query)