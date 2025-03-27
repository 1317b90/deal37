<template>
  <div class="view-content">
    <div class="all-div">
      <!-- 联系人列表 -->
      <div class="linkman-div">
        <div class="linkman-item" v-for="(contact, index) in contacts" :key="index" @click="switchContact(contact)"
          :class="{ 'active': currentContact?.id === contact.id }">
          <div class="avatar-container">
            <a-avatar :style="{ backgroundColor: contact.color, verticalAlign: 'middle' }" gap="4">
              {{ contact.name.slice(0, 4) }}
            </a-avatar>
            <span class="online-status" :class="{ 'online': contact.online }"></span>
          </div>
          <div class="contact-info">
            <span class="linkman-name">{{ contact.name }}</span>
            <span class="unread-badge" v-if="contact.unreadCount">{{ contact.unreadCount }}</span>
          </div>
        </div>
      </div>

      <!-- 聊天窗 -->
      <div class="chat-div">
        <!-- 聊天头部，显示对方的头像和用户名 -->
        <div class="chat-header">
          <a-avatar size="large" :style="{ backgroundColor: color, verticalAlign: 'middle' }" gap="4">
            {{ other_name.slice(0, 4) }}
          </a-avatar>
          <div class="chat-header-title">
            {{ other_name }}
          </div>
        </div>

        <!-- 聊天消息窗口 -->
        <div class="chat-content" ref="chatContent">
          <div class="message" v-for="(message, index) in data" :key="index"
            :class="{ 'message-self': message.username === 'self', 'message-other': message.username !== 'self' }">
            <div class="message-bubble">
              <span class="message-text">{{ message.content }}</span>
              <span class="message-time">{{ message.time }}</span>
            </div>
          </div>
        </div>

        <!-- 发送消息 -->
        <div class="chat-footer">
          <a-input v-model:value="newMessage" placeholder="输入消息..." @keyup.enter="sendMessage" />
          <a-button type="primary" @click="sendMessage">发送</a-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { message } from 'ant-design-vue';
import { getChatHistory, getUserContacts, markMessageAsRead, getUnreadMessages } from '@/request/api';

// 用户信息接口
export interface UserInfo {
  id: number;
  name: string;
  role: string;
}

// 联系人接口
export interface Contact {
  id: number;
  name: string;
  online: boolean;
  color?: string;
  unreadCount?: number;
}

// 消息接口
export interface Message {
  username: 'self' | 'other';
  content: string;
  time: string;
}

const route = useRoute();
const userInfo = ref<UserInfo>({
  id: 0,
  name: '',
  role: ''
});
const storedUserInfo = localStorage.getItem('userInfo');
userInfo.value = storedUserInfo ? JSON.parse(storedUserInfo) : userInfo.value;

const contacts = ref<Contact[]>([]);
const currentContact = ref<Contact | null>(null);
const data = ref<Message[]>([]);
const newMessage = ref('');
const colorList = ['#f56a00', '#7265e6', '#ffbf00', '#00a2ae'];
const color = ref(colorList[1]);
const other_name = ref('');
const ws = ref<WebSocket | null>(null);
const chatContent = ref<HTMLElement | null>(null);

// 连接WebSocket
const connectWebSocket = () => {
  if (!userInfo.value.id) return;
  ws.value = new WebSocket(`ws://8.137.105.108:377/ws/${userInfo.value.id}`);

  ws.value.onmessage = (event) => {
    const messageData = JSON.parse(event.data);
    if (messageData.type === 'message') {
      // 如果是当前聊天对象的消息，直接添加到消息列表
      if (currentContact.value && messageData.sender_id === currentContact.value.id) {
        data.value.push({
          username: 'other',
          content: messageData.content,
          time: new Date(messageData.created_at).toLocaleString()
        });
        // 滚动到底部
        nextTick(() => {
          if (chatContent.value) {
            chatContent.value.scrollTop = chatContent.value.scrollHeight;
          }
        });
      } else {
        // 更新未读消息数
        const contact = contacts.value.find(c => c.id === messageData.sender_id);
        if (contact) {
          contact.unreadCount = (contact.unreadCount || 0) + 1;
        }
      }
    }
  };

  ws.value.onclose = () => {
    // 断线重连
    setTimeout(connectWebSocket, 3000);
  };
};

// 获取历史消息
const fetchHistoryMessages = async () => {
  if (!currentContact.value || !userInfo.value.id) return;
  try {
    const response = await getChatHistory(userInfo.value.id, currentContact.value.id);
    data.value = response.data.map((msg: { sender_id: number; content: any; created_at: string | number | Date; }) => ({
      username: msg.sender_id === userInfo.value.id ? 'self' : 'other',
      content: msg.content,
      time: new Date(msg.created_at).toLocaleString()
    }));
    // 滚动到底部
    nextTick(() => {
      if (chatContent.value) {
        chatContent.value.scrollTop = chatContent.value.scrollHeight;
      }
    });
  } catch (error) {
    message.error('获取历史消息失败');
  }
};

// 切换联系人
const switchContact = async (contact: Contact) => {
  currentContact.value = contact;
  other_name.value = contact.name;
  color.value = contact.color || colorList[0];
  data.value = [];

  try {
    await fetchHistoryMessages();
    // 重置未读消息计数
    if (contact.unreadCount) {
      // 获取未读消息
      const unreadMessages = await getUnreadMessages(userInfo.value.id);
      // 标记所有未读消息为已读
      for (const message of unreadMessages.data) {
        if (message.sender_id === contact.id) {
          await markMessageAsRead(message.id);
        }
      }
      contact.unreadCount = 0;
    }
  } catch (error) {
    message.error('获取历史消息失败');
  }
};

// 发送消息
const sendMessage = async () => {
  if (!currentContact.value) {
    message.warning('请先选择聊天对象');
    return;
  }

  if (newMessage.value.trim() !== '') {
    try {
      // 通过WebSocket发送消息
      ws.value?.send(JSON.stringify({
        type: 'message',
        receiver_id: currentContact.value.id,
        content: newMessage.value.trim()
      }));

      // 添加到本地消息列表
      data.value.push({
        username: 'self',
        content: newMessage.value,
        time: new Date().toLocaleString()
      });

      newMessage.value = '';

      // 滚动到底部
      nextTick(() => {
        if (chatContent.value) {
          chatContent.value.scrollTop = chatContent.value.scrollHeight;
        }
      });
    } catch (error) {
      message.error('发送消息失败');
    }
  }
};

// 获取联系人列表
const fetchContacts = async () => {
  try {
    const response = await getUserContacts(Number(userInfo.value.id));
    contacts.value = response.data.map((contact: any) => ({
      id: Number(contact.id),
      name: contact.name,
      online: contact.online,
      color: colorList[Math.floor(Math.random() * colorList.length)],
      unreadCount: contact.unread_count || 0
    }));
  } catch (error) {
    message.error('获取联系人列表失败');
  }
};

// 生命周期钩子
onMounted(async () => {
  await fetchContacts();
  connectWebSocket();

  // 处理从buy.vue传递过来的contactId
  const contactId = route.query.contactId;
  if (contactId) {
    const contact = contacts.value.find(c => c.id === Number(contactId));
    if (contact) {
      await switchContact(contact);
    }
  }
});

onUnmounted(() => {
  ws.value?.close();
});
</script>

<style scoped>
.view-content {
  height: 100%;
  padding: 20px;
}

.all-div {
  display: flex;
  height: 100%;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-left: 100px;
  margin-right: 100px;
}

.linkman-div {
  width: 300px;
  border-right: 1px solid #e8e8e8;
  overflow-y: auto;
}

.linkman-item {
  display: flex;
  align-items: center;
  padding: 12px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.linkman-item:hover {
  background-color: #f5f5f5;
}

.linkman-item.active {
  background-color: #e6f7ff;
}

.avatar-container {
  position: relative;
  margin-right: 12px;
}

.online-status {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #d9d9d9;
  border: 2px solid #fff;
}

.online-status.online {
  background-color: #52c41a;
}

.contact-info {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.linkman-name {
  font-size: 14px;
  color: #333;
}

.unread-badge {
  background-color: #ff4d4f;
  color: #fff;
  border-radius: 10px;
  padding: 2px 6px;
  font-size: 12px;
}

.chat-div {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chat-header {
  padding: 16px;
  border-bottom: 1px solid #e8e8e8;
  display: flex;
  align-items: center;
}

.chat-header-title {
  margin-left: 12px;
  font-size: 16px;
  font-weight: 500;
}

.chat-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.message {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
}

.message-self {
  align-items: flex-end;
}

.message-other {
  align-items: flex-start;
}

.message-bubble {
  max-width: 70%;
  padding: 8px 12px;
  border-radius: 8px;
  background-color: #f0f2f5;
}

.message-self .message-bubble {
  background-color: #1890ff;
  color: #fff;
}

.message-text {
  display: block;
  margin-bottom: 4px;
}

.message-time {
  font-size: 12px;
  color: #999;
}

.message-self .message-time {
  color: rgba(255, 255, 255, 0.8);
}

.chat-footer {
  padding: 16px;
  border-top: 1px solid #e8e8e8;
  display: flex;
  gap: 8px;
}

.chat-footer .ant-input {
  flex: 1;
}
</style>