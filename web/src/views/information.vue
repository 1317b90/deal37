<template>
  <div class="view-content">
    <div class="card-box info-div" v-for="item in data" :key="item.id" @click="goInformation(item.src_url)">
      <div class="info-describe">
        <span class="info-title">{{item.title}}</span>
        <span class="info-time">{{ formatTime(item.created_at) }}</span>
      </div>
      <div class="info-img-div">
        <img  class="info-img" :src="item.img_url" alt="">
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { getAllInformation } from "@/request/api";
import { onMounted, ref } from 'vue';
import type { informationI } from '@/interface';
import { message } from "ant-design-vue";
const data = ref<informationI[]>([]); 


function formatTime(time: Date | undefined) {
  if (!time) return ""; 
  return new Date(time).toLocaleString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' })
}

function goInformation(src_url: string) {
  window.open(src_url, '_blank');
}

onMounted(async () => {
  getAllInformation().then((res) => {
    data.value = res.data;
    console.log("在这里：——")
    console.log(res.data);
    message.success("获取资讯成功");
  }).catch((error) => {
    message.error("获取资讯失败");
  })
})

</script>
<style scoped>
.view-content{
  height: 100%;
  width: 100%;
  padding:20px 200px 10px 200px;
  /* background-color: #fff; */
}

.info-div{
  display: flex;
  justify-content: space-between;
  width: 100%;
  padding: 0px 100px 0px 100px;
  transition: transform 0.3s ease;
  cursor: pointer;
  margin-bottom: 20px;
}


.info-div:hover .info-title {
  color: rgb(22, 119, 255);
}

.info-div:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: scale(1.02);
}

.info-describe{
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
  gap: 30px;
}

.info-title{
  font-size: 20px;
  font-weight: 600;
  transition: color 0.3s ease;
}

.info-img-div{
  align-self: flex-end;
}
.info-img{
  height: 200px;
  width: 350px; /* 保持图片的原始宽度 */
  object-fit: cover; /* 不缩放图片，保持原始宽度 */
  object-position: top; /* 显示图片顶部的部分 */
}
</style>