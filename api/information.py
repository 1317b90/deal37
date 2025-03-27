from typing import List
from fastapi import APIRouter, HTTPException
from tortoise.contrib.pydantic import pydantic_model_creator
from Table import Information

app = APIRouter(tags=["知识资讯"])

Information_Pydantic = pydantic_model_creator(Information, name="Information")
InformationIn_Pydantic = pydantic_model_creator(Information, name="InformationIn", exclude_readonly=True)

@app.post("/information", response_model=Information_Pydantic,summary="创建资讯")
async def create_information(information:InformationIn_Pydantic):
    information_obj = await Information.create(**information.dict(exclude_unset=True))
    return await Information_Pydantic.from_tortoise_orm(information_obj)

@app.get("/information/{information_id}", response_model=Information_Pydantic,summary="获取资讯")
async def read_information(information_id: int):
    information = await Information_Pydantic.from_queryset_single(Information.get(id=information_id))
    if information is None:
        raise HTTPException(status_code=404, detail="Information not found")
    return information

@app.get("/information", response_model=List[Information_Pydantic], summary="获取所有资讯")
async def get_all_information():
    informations = await Information_Pydantic.from_queryset(Information.all())
    return informations

@app.put("/information/{information_id}", response_model=Information_Pydantic,summary="更新资讯")
async def update_information(information_id: int, information: InformationIn_Pydantic):
    information_obj = await Information.get(id=information_id)
    if information_obj is None:
        raise HTTPException(status_code=404, detail="Information not found")
    information_obj.update_from_dict(information.dict(exclude_unset=True))
    await information_obj.save()
    return await Information_Pydantic.from_tortoise_orm(information_obj)

@app.delete("/information/{information_id}",summary="删除资讯")
async def delete_information(information_id: int):
    information_obj = await Information.get(id=information_id)
    if information_obj is None:
        raise HTTPException(status_code=404, detail="Information not found")
    await information_obj.delete()
    return {"detail": "Information deleted successfully"}

@app.get("/information/search", response_model=List[Information_Pydantic],summary="搜索资讯")
async def search_information(title: str):
    informations = Information.filter(title__icontains=title)
    print(title)
    print(informations)
    return await Information_Pydantic.from_queryset(informations)
