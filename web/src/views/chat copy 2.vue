<template>
  <div class="chat-container">
    <div class="chat-header">
      <a-avatar size="large" :style="{ backgroundColor: color, verticalAlign: 'middle' }" gap="4">
        {{ name }}
      </a-avatar>
      <span class="chat-title">{{ name }}的聊天</span>
    </div>
    <div class="chat-messages">
      <div 
        class="message" 
        v-for="(message, index) in messages" 
        :key="index" 
        :class="{ 'message-self': message.user === name, 'message-other': message.user !== name }"
      >
        <span class="message-text">{{ message.text }}</span>
        <span class="message-time">{{ message.time }}</span>
      </div>
    </div>
    <div class="chat-input">
      <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="输入消息..." />
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const colorList = ['#f56a00', '#7265e6', '#ffbf00', '#00a2ae'];
const color = ref(colorList[1]);
const name = ref("小兰花");

const messages = ref([
  { user: '小兰花', text: '你好！', time: '10:00' },
  { user: '小明', text: '你好我是小明！', time: '10:01' }
]);

const newMessage = ref('');

function sendMessage() {
  if (newMessage.value.trim() !== '') {
    const currentTime = new Date().toLocaleTimeString();
    messages.value.push({ user: name.value, text: newMessage.value, time: currentTime });
    newMessage.value = '';
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  padding: 20px;
  background-color: #fff;
}

.chat-header {
  display: flex;
  align-items: center;
  padding-bottom: 10px;
  border-bottom: 1px solid #eaeaea;
}

.chat-title {
  margin-left: 10px;
  font-size: 20px;
  font-weight: bold;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px 0;
}

.message {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 10px;
  word-wrap: break-word;
  position: relative;
  max-width: fit-content;
  transition: transform 0.3s ease;
  margin-bottom: 20px;
}

.message-self {
  align-self: flex-end !important; /* 右对齐 */
  background-color: #e6f7ff;
  text-align: right;
}

.message-other {
  align-self: flex-start !important; /* 左对齐 */
  background-color: #f5f5f5;
}

.message-text {
  margin-bottom: 5px;
}

.message-time {
  font-size: 12px;
  color: #888;
  position: absolute;
  bottom: -20px;
  right: 10px;
}

.message-other .message-time {
  right: auto;
  left: 10px;
}

.chat-input {
  display: flex;
  align-items: center;
  border-top: 1px solid #eaeaea;
  padding-top: 10px;
}

.chat-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #eaeaea;
  border-radius: 4px;
  margin-right: 10px;
}

.chat-input button {
  padding: 10px 20px;
  background-color: #1890ff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.chat-input button:hover {
  background-color: #40a9ff;
}
</style>