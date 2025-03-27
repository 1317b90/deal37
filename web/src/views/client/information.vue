<template>
  <div class="view-content">
    <div class="card-box info-div" v-for="item in data" :key="item.id" @click="showDetail(item)">
      <div class="info-describe">
        <span class="info-title">{{ item.title }}</span>
        <div class="info-meta">
          <span class="info-author">作者：{{ item.author }}</span>
          <span class="info-time">{{ formatTime(item.created_at) }}</span>
        </div>
      </div>
      <div class="info-img-div">
        <img class="info-img" :src="item.img_url" alt="">
      </div>
    </div>

    <a-modal v-model:visible="detailVisible" :title="currentInfo?.title" width="800px" :footer="null"
      @cancel="handleCancel">
      <div class="detail-content">
        <div class="detail-header">
          <div class="detail-meta">
            <span class="detail-author">作者：{{ currentInfo?.author }}</span>
            <span class="detail-time">{{ formatTime(currentInfo?.created_at) }}</span>
          </div>
          <img class="detail-img" :src="currentInfo?.img_url" alt="">
        </div>
        <div class="detail-text">{{ currentInfo?.content }}</div>
      </div>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { getAllInformation } from "@/request/api";
import { onMounted, ref } from 'vue';
import type { informationI } from '@/interface';
import { message } from "ant-design-vue";

const data = ref<informationI[]>([]);
const detailVisible = ref<boolean>(false);
const currentInfo = ref<informationI | null>(null);

function formatTime(time: Date | undefined) {
  if (!time) return "";
  return new Date(time).toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric'
  })
}

function showDetail(info: informationI) {
  currentInfo.value = info;
  detailVisible.value = true;
}

function handleCancel() {
  currentInfo.value = null;
  detailVisible.value = false;
}

onMounted(async () => {
  getAllInformation().then((res) => {
    data.value = res.data;
  }).catch((error) => {
    message.error("获取资讯失败");
  })
})
</script>

<style scoped>
.view-content {
  height: 100%;
  width: 100%;
  padding: 20px 200px 10px 200px;
}

.info-div {
  display: flex;
  justify-content: space-between;
  width: 100%;
  padding: 20px 100px;
  transition: all 0.3s ease;
  cursor: pointer;
  margin-bottom: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.info-div:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.info-describe {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 20px;
  flex: 1;
  padding-right: 30px;
}

.info-title {
  font-size: 22px;
  font-weight: 600;
  color: #333;
  transition: color 0.3s ease;
}

.info-meta {
  display: flex;
  gap: 20px;
  color: #666;
  font-size: 14px;
}

.info-div:hover .info-title {
  color: #1890ff;
}

.info-img-div {
  width: 350px;
  height: 200px;
  overflow: hidden;
  border-radius: 4px;
}

.info-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.info-div:hover .info-img {
  transform: scale(1.05);
}

.detail-content {
  padding: 20px;
  max-height: 70vh;
  overflow-y: auto;
}

.detail-header {
  margin-bottom: 24px;
}

.detail-meta {
  display: flex;
  gap: 20px;
  color: #666;
  font-size: 14px;
  margin-bottom: 16px;
}

.detail-img {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
  border-radius: 8px;
}

.detail-text {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
  white-space: pre-wrap;
}
</style>