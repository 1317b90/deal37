from datetime import datetime, timedelta
from fastapi import FastAPI      
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from tortoise.contrib.fastapi import register_tortoise
import Config
import information
import user
import commodity
import file
import chat
import pay
import order

app = FastAPI(title="Deal37—API")
FILE_DIR = Path("./files")
FILE_DIR.mkdir(exist_ok=True)
app.mount("/files", StaticFiles(directory=FILE_DIR), name="file")

app.include_router(information.app)
app.include_router(user.app)
app.include_router(commodity.app)
app.include_router(file.app)
app.include_router(chat.app)
app.include_router(pay.app)
app.include_router(order.app)

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
