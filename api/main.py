from datetime import datetime, timedelta
import random
from fastapi import FastAPI      
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.testclient import TestClient
from fastapi import  HTTPException

from tortoise.contrib.fastapi import register_tortoise
import Config
import information

app = FastAPI(title="Deal37—API")

app.include_router(information.app)

# 解决跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

register_tortoise(
    app,
    db_url=Config.SQL_URL,  # 这里可以根据需要更换为其他数据库，如 PostgreSQL
    modules={'models': ['Table']},  
    generate_schemas=True, # 自动生成数据库表
    add_exception_handlers=False,# 数据库调试信息
)




if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
