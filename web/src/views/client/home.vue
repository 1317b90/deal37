<template>
  <div class="view-content">
    <div class="hero-section">
      <h1 class="main-title">文山三七交易平台</h1>
      <p class="subtitle">专业 · 可靠 · 便捷</p>
      <div class="hero-buttons">
        <a-button type="primary" size="large" @click="$router.push('/market')">查看行情</a-button>
        <a-button size="large" @click="$router.push('/information')">了解更多</a-button>
      </div>
    </div>

    <div class="features-section">
      <div class="feature-card">
        <div class="icon">
          <SafetyCertificateOutlined style="font-size: 48px" />
        </div>
        <h3>优质三七</h3>
        <p>严选文山道地三七，层层把关品质，确保每一份三七都是上等好货</p>
      </div>
      <div class="feature-card">
        <div class="icon">
          <ShoppingOutlined style="font-size: 48px" />
        </div>
        <h3>便捷交易</h3>
        <p>一站式交易流程，买卖双方直接对接，省去中间环节，让交易更加高效</p>
      </div>
      <div class="feature-card">
        <div class="icon">
          <SmileOutlined style="font-size: 48px" />
        </div>
        <h3>安全保障</h3>
        <p>平台担保交易，资金安全有保障，让您买卖无忧，专注品质</p>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { SmileOutlined, ShoppingOutlined, SafetyCertificateOutlined } from '@ant-design/icons-vue';
</script>

<style scoped>
.view-content {
  min-height: 100%;
  width: 100%;
  padding: 0;
  background-color: #f8f9fa;
}

.hero-section {
  text-align: center;
  padding: 120px 0;
  background-image: linear-gradient(-225deg, #2CD8D5 0%, #C5C1FF 56%, #FFBAC3 100%);
  color: white;
  margin-bottom: 60px;
  position: relative;
  overflow: hidden;
}

.main-title {
  font-size: 3.5rem;
  margin-bottom: 20px;
  font-weight: 700;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.subtitle {
  font-size: 1.5rem;
  opacity: 0.9;
  margin-bottom: 30px;
  letter-spacing: 4px;
}

.hero-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.features-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto 80px;
  padding: 0 20px;
}

.feature-card {
  background: white;
  padding: 40px 30px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
}

.icon {
  margin-bottom: 25px;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  color: #1a5f7a;
}

.feature-card p {
  color: #666;
  line-height: 1.8;
  font-size: 1.1rem;
}

.about-section {
  background: white;
  padding: 80px 20px;
}

.about-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

.about-text h2 {
  color: #1a5f7a;
  font-size: 2.5rem;
  margin-bottom: 30px;
}

.about-text p {
  color: #444;
  line-height: 2;
  font-size: 1.1rem;
  margin-bottom: 20px;
}

.about-image img {
  width: 100%;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}
</style>