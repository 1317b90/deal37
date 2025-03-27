from typing import List
from fastapi import APIRouter, HTTPException
from tortoise.contrib.pydantic import pydantic_model_creator
from Table import User

app = APIRouter(tags=["用户管理"])

User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)

@app.post("/user", response_model=User_Pydantic, summary="创建用户")
async def create_user(user: UserIn_Pydantic):
    existing_user = await User.filter(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)

@app.get("/user/{user_id}", response_model=User_Pydantic, summary="获取用户")
async def read_user(user_id: int):
    user = await User_Pydantic.from_queryset_single(User.get(id=user_id))
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@app.get("/users", response_model=List[User_Pydantic], summary="获取所有用户")
async def get_all_users():
    return await User_Pydantic.from_queryset(User.all())

@app.put("/user/{user_id}", response_model=User_Pydantic, summary="更新用户")
async def update_user(user_id: int, user: UserIn_Pydantic):
    user_obj = await User.get(id=user_id)
    if not user_obj:
        raise HTTPException(status_code=404, detail="用户不存在")
    await user_obj.update_from_dict(user.dict(exclude_unset=True))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

@app.delete("/user/{user_id}", summary="删除用户")
async def delete_user(user_id: int):
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"detail": "用户删除成功"}

@app.get("/users/search", response_model=List[User_Pydantic], summary="搜索用户")
async def search_users(username: str = None, phone: str = None):
    query = User.filter()
    if username:
        query = query.filter(username__icontains=username)
    if phone:
        query = query.filter(phone__icontains=phone)
    return await User_Pydantic.from_queryset(query)


@app.get("/user/username/{username}", response_model=User_Pydantic, summary="根据用户名获取用户")
async def get_user_by_username(username: str):
    user = await User.filter(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return await User_Pydantic.from_tortoise_orm(user)
