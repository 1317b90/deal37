<template>
  <div class="view-content">
    <span class="title">平台数据</span>
    <div class="platform-div card-box">
      <div class="platform-item" v-for="item in platformData" :key="item.title">
        <div>
          <span class="platform-value">{{ item.value }}</span>
          <span class="platform-unit">{{ item.unit }}</span>
        </div>
        <div class="platform-title">{{ item.title }}</div>
      </div>
    </div>

  <span class="title">行情分析</span>
  <div class="wave-div card-box">
    <waveChart/>
  </div>
  </div>

  
</template>

<script setup lang="ts">

import waveChart from "./wave.vue"

const platformData = [
  {
    title: '平台交易额',
    value: 50850.24,
    unit:"万"
  },
  {
    title: '买家数',
    value: 2998,
    unit:"人"
  },
  {
    title: '卖家数',
    value: 91,
    unit:"人"
  },
  {
    title:'平台用户数',
    value: 3089,
    unit:"人"
  }
]

</script>
<style scoped>
.view-content{
  height: 100%;
  width: 100%;
  padding:20px 100px 10px 100px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}



.title{
  margin-left: 10px;
  font-size: 24px;
  font-weight: 600;
  color: rgba(22, 119, 255,0.8);
}

.platform-div{
  display: flex;
}

.platform-item{
  border-right: 1px solid rgba(22, 119, 255,0.5);
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.platform-item:last-child {
  border-right: none;
}

.platform-value{
  color: rgb(22, 119, 255);
  padding-left: 10px;
  font-size: 30px;
  font-weight: 600;
  color: rgb(81, 90, 110);
}

.platform-unit{
  float: right;
  font-size: 16px;
  padding-left: 10px;
  padding-top: 15px;
}

.platform-title{
  font-size: 16px;
  color: rgb(153, 153, 153);
}

.wave-div{
  height: 500px;
  width: 100%;
}
</style>