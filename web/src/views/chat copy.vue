<template>
  <div class="view-content">
    <!-- 联系人列表 -->
    <div class="linkman">

    </div>

    <!-- 聊天窗 -->
    <div class="chat-div">

      <!-- 聊天头部，显示对方的头像和用户名 -->
      <div class="chat-header">
        <a-avatar  size="large" :style="{ backgroundColor: color, verticalAlign: 'middle' }" gap="4">
          {{ other_username }}
        </a-avatar>
        <div class="chat-header-title">
          {{ other_username }}
        </div>
      </div>

      <!-- 聊天消息窗口 -->
      <div class="chat-content">
        <!-- 对方的消息左对齐，自己的消息右对齐，消息样式为气泡，气泡的高度和宽度随着消息内容变化，在气泡外的下方显示消息发送时间 -->

      </div>

      <!-- 发送消息 -->
      <div class="chat-footer">

      </div>
    </div>


  </div>


</template>

<script setup lang="ts">
import { ref } from 'vue';
const colorList = ['#f56a00', '#7265e6', '#ffbf00', '#00a2ae'];
const color = ref(colorList[1]);
const other_username=ref("other")

const data=ref(
  [
    {
      "username":"self",
      "content":"你好",
      "time":"2024-02-01 12:00:00"
    },
    {
      "username":"other",
      "content":"你好，吃了吗",
      "time":"2024-02-01 12:01:00"
    }
  ]
)

</script>
<style scoped>
.view-content{
  height: 100%;
  width: 100%;
  padding:20px 100px 10px 100px;
  background-color: #fff;
}
.title{
  font-size: 20px;
  font-weight: bold;
}



</style>