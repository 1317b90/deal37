<template>
  <div class="view-content">
    <!-- 联系人列表 -->
    <div class="linkman-div">
      <!-- 示例联系人 -->
      <div class="linkman-item" v-for="(contact, index) in contacts" :key="index">
        <a-avatar :style="{ backgroundColor: contact.color, verticalAlign: 'middle' }" gap="4">
          {{ contact.username }}
        </a-avatar>
        <span class="linkman-name">{{ contact.username }}</span>
      </div>
    </div>

    <!-- 聊天窗 -->
    <div class="chat-div">

      <!-- 聊天头部，显示对方的头像和用户名 -->
      <div class="chat-header">
        <a-avatar size="large" :style="{ backgroundColor: color, verticalAlign: 'middle' }" gap="4">
          {{ other_username }}
        </a-avatar>
        <div class="chat-header-title">
          {{ other_username }}
        </div>
      </div>

      <!-- 聊天消息窗口 -->
      <div class="chat-content">
        <!-- 对方的消息左对齐，自己的消息右对齐，消息样式为气泡，气泡的高度和宽度随着消息内容变化，在气泡外的下方显示消息发送时间 -->
        <div 
          class="message" 
          v-for="(message, index) in data" 
          :key="index" 
          :class="{ 'message-self': message.username === 'self', 'message-other': message.username !== 'self' }"
        >
          <div class="message-bubble">
            <span class="message-text">{{ message.content }}</span>
            <span class="message-time">{{ message.time }}</span>
          </div>
        </div>
      </div>

      <!-- 发送消息 -->
      <div class="chat-footer">
        <!-- <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="输入消息..." />
        <button @click="sendMessage">发送</button> -->

        <a-input v-model:value="newMessage" placeholder="输入消息..."  @keyup.enter="sendMessage" />
        <a-button type="primary"  @click="sendMessage">发送</a-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const colorList = ['#f56a00', '#7265e6', '#ffbf00', '#00a2ae'];
const color = ref(colorList[1]);
const other_username = ref("other");

const contacts = ref([
  { username: '小兰花', color: colorList[0] },
  { username: '小明', color: colorList[1] }
]);

const data = ref([
  {
    username: "self",
    content: "你好",
    time: "2024-02-01 12:00:00"
  },
  {
    username: "other",
    content: "你好，吃了吗",
    time: "2024-02-01 12:01:00"
  }
]);

const newMessage = ref('');

function sendMessage() {
  if (newMessage.value.trim() !== '') {
    const currentTime = new Date().toLocaleTimeString();
    data.value.push({ username: 'self', content: newMessage.value, time: currentTime });
    newMessage.value = '';
  }
}
</script>

<style scoped>
.view-content {
  height: 100%;
  width: 100%;
  padding: 20px 100px 10px 100px;
  background-color: white;
  display: flex;
}

.linkman-div {
  flex: 1;
  margin-bottom: 20px;
}

.linkman-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.linkman-name {
  margin-left: 10px;
}

.chat-div {
  flex: 7;
  border: 1px solid #e8e8e8;
  border-radius: 5px;
  padding: 10px;
}

.chat-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  height: 10%;
}

.chat-header-title {
  margin-left: 10px;
  font-weight: bold;
}

.chat-content {
  height: 70%;
  /* height: 500px; */
  overflow-y: auto;
  margin-bottom: 10px;
}

.message {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}

.message-self {
  align-items: flex-end;
}

.message-other {
  align-items: flex-start;
}

.message-bubble {
  max-width: 60%;
  padding: 10px;
  border-radius: 10px;
  background-color: #f1f1f1;
  position: relative;
}

.message-self .message-bubble {
  background-color: #d1eaff;
}

.message-text {
  display: block;
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

.chat-footer {
  height: 19%;
  display: flex;
  align-items: center;
}
</style>