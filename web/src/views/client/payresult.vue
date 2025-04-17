<template>
    <div class="payresult-container">
        <a-result status="success" title="支付成功" sub-title="您的订单已经支付完成，感谢您的购买！">
            <template #extra>
                <div class="order-info" v-if="orderInfo.outTradeNo">
                    <p>订单号: {{ orderInfo.outTradeNo }}</p>
                    <p>交易号: {{ orderInfo.tradeNo }}</p>
                    <p>金额: ¥{{ orderInfo.totalAmount }}</p>
                </div>
                <a-space>
                    <a-button type="primary" @click="goToOrder">查看订单</a-button>
                    <a-button @click="goToBuy">继续购买</a-button>
                </a-space>
            </template>
        </a-result>
    </div>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router';
import { reactive, onMounted } from 'vue';

const router = useRouter();
const route = useRoute();

const orderInfo = reactive({
    outTradeNo: '',
    tradeNo: '',
    totalAmount: '',
});

onMounted(() => {
    // 获取URL参数
    if (route.query.out_trade_no) {
        orderInfo.outTradeNo = route.query.out_trade_no as string;
    }
    if (route.query.trade_no) {
        orderInfo.tradeNo = route.query.trade_no as string;
    }
    if (route.query.total_amount) {
        orderInfo.totalAmount = route.query.total_amount as string;
    }
});

const goToOrder = () => {
    router.push('/order');
};

const goToBuy = () => {
    router.push('/buy');
};
</script>

<style scoped>
.payresult-container {
    padding: 50px;
    background-color: #f0f2f5;
    min-height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.order-info {
    text-align: left;
    margin-bottom: 20px;
    padding: 15px;
    background-color: #fafafa;
    border-radius: 4px;
    border: 1px solid #f0f0f0;
}
</style>
