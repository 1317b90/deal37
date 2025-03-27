from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import Dict, List
from datetime import datetime
from Table import Message, User
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.expressions import Q
import json

Message_Pydantic = pydantic_model_creator(Message, name="Message")
MessageIn_Pydantic = pydantic_model_creator(Message, name="MessageIn", exclude_readonly=True)
User_Pydantic = pydantic_model_creator(User, name="User")

app = APIRouter(tags=["聊天管理"])

# 存储WebSocket连接
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_message(self, message: str, user_id: int):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)

manager = ConnectionManager()

@app.post("/messages", response_model=Message_Pydantic, summary="发送消息")
async def send_message(message: MessageIn_Pydantic):
    message_obj = await Message.create(**message.dict(exclude_unset=True))
    return await Message_Pydantic.from_tortoise_orm(message_obj)

@app.get("/messages/{user_id}", response_model=List[Message_Pydantic], summary="获取用户的聊天记录")
async def get_user_messages(user_id: int):
    messages = await Message.filter(receiver_id=user_id).order_by('-created_at').all()
    return await Message_Pydantic.from_queryset(Message.filter(receiver_id=user_id))

@app.get("/messages/{user_id}/contacts", response_model=List[dict], summary="获取用户的联系人列表")
async def get_user_contacts(user_id: int):
    # 获取所有与该用户有过通信的用户ID
    sent_messages = await Message.filter(sender_id=user_id).values_list('receiver_id', flat=True)
    received_messages = await Message.filter(receiver_id=user_id).values_list('sender_id', flat=True)
    
    # 合并并去重
    contact_ids = list(set(list(sent_messages) + list(received_messages)))
    
    # 获取联系人详细信息
    contacts = []
    for contact_id in contact_ids:
        try:
            user = await User.get(id=contact_id)
            # 获取未读消息数
            unread_count = await Message.filter(
                sender_id=contact_id,
                receiver_id=user_id,
                is_read=False
            ).count()
            
            contacts.append({
                "id": user.id,
                "name": user.name,
                "online": contact_id in manager.active_connections,
                "unread_count": unread_count
            })
        except:
            continue

    return contacts

@app.get("/messages/{user_id}/unread", response_model=List[Message_Pydantic], summary="获取用户的未读消息")
async def get_unread_messages(user_id: int):
    messages = await Message.filter(receiver_id=user_id, is_read=False).order_by('-created_at').all()
    return await Message_Pydantic.from_queryset(Message.filter(receiver_id=user_id, is_read=False))

@app.get("/messages/{sender_id}/{receiver_id}", response_model=List[Message_Pydantic], summary="获取两个用户之间的聊天记录")
async def get_chat_history(sender_id: int, receiver_id: int):
    messages = await Message.filter(
        (Q(sender_id=sender_id) & Q(receiver_id=receiver_id)) |
        (Q(sender_id=receiver_id) & Q(receiver_id=sender_id))
    ).order_by('created_at').all()
    return await Message_Pydantic.from_queryset(
        Message.filter(
            (Q(sender_id=sender_id) & Q(receiver_id=receiver_id)) |
            (Q(sender_id=receiver_id) & Q(receiver_id=sender_id))
        ).order_by('created_at')
    )

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # 处理接收到的消息
            message_data = json.loads(data)
            if message_data.get("type") == "message":
                # 保存消息到数据库
                message_obj = await Message.create(
                    sender_id=user_id,
                    receiver_id=message_data["receiver_id"],
                    content=message_data["content"]
                )
                # 发送消息给接收者
                await manager.send_message(
                    json.dumps({
                        "type": "message",
                        "sender_id": user_id,
                        "content": message_data["content"],
                        "created_at": message_obj.created_at.isoformat()
                    }),
                    message_data["receiver_id"]
                )
    except WebSocketDisconnect:
        manager.disconnect(user_id)

@app.put("/messages/{message_id}/read", response_model=Message_Pydantic, summary="标记消息为已读")
async def mark_message_as_read(message_id: int):
    try:
        message = await Message.get(id=message_id)
        if not message:
            raise HTTPException(status_code=404, detail="消息不存在")
        
        # 确保消息被标记为已读
        message.is_read = True
        await message.save()
        
        # 验证更新是否成功
        updated_message = await Message.get(id=message_id)
        if not updated_message.is_read:
            raise HTTPException(status_code=500, detail="消息状态更新失败")
            
        return await Message_Pydantic.from_tortoise_orm(updated_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新消息状态时出错: {str(e)}")

@app.post("/messages/init", response_model=Message_Pydantic, summary="创建初始消息")
async def create_initial_message(sender_id: int, receiver_id: int):
    # 检查是否已存在消息
    existing_message = await Message.filter(
        (Q(sender_id=sender_id) & Q(receiver_id=receiver_id)) |
        (Q(sender_id=receiver_id) & Q(receiver_id=sender_id))
    ).first()
    
    if not existing_message:
        # 创建一条初始消息
        message_obj = await Message.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content="你好，我想咨询一下商品信息。"
        )
        return await Message_Pydantic.from_tortoise_orm(message_obj)
    return await Message_Pydantic.from_tortoise_orm(existing_message)