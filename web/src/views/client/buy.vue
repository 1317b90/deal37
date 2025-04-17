<template>
    <a-spin :spinning="loading">
        <div class="view-content">
            <div class="filter-section">
                <a-row :gutter="16">
                    <a-col :span="8">
                        <a-input-search v-model:value="searchText" placeholder="搜索商品名称" @search="onSearch"
                            style="width: 100%" />
                    </a-col>
                    <a-col :span="8">
                        <a-select v-model:value="selectedSpec" style="width: 100%" placeholder="选择规格筛选" allowClear
                            @change="handleSpecChange">
                            <a-select-option v-for="spec in specifications" :key="spec" :value="spec">
                                {{ spec }}
                            </a-select-option>
                        </a-select>
                    </a-col>
                </a-row>
            </div>

            <div class="products-grid">
                <a-card v-for="item in filteredProducts" :key="item.id" class="product-card" :bordered="false">
                    <template #cover>
                        <a-image :src="item.image" :alt="item.name" style="height: 200px; object-fit: cover;" />
                    </template>
                    <a-card-meta>
                        <template #title>
                            <div class="title-row">
                                <span class="product-name">{{ item.name }}</span>
                                <span class="specification">{{ item.specification }}</span>
                            </div>
                        </template>
                        <template #description>
                            <div class="product-info">
                                <div class="price">¥{{ item.price.toFixed(2) }}/Kg</div>
                                <div class="product-stats">
                                    <span>销量：{{ item.sales }}</span>
                                    <span>库存：{{ item.inventory }}</span>
                                </div>
                                <div class="seller-info">
                                    卖家：<a @click="contactSeller(item.sell_id)">{{ item.sell_name }}</a>
                                </div>
                                <div class="publish-time">
                                    发布时间：{{ formatDate(item.created_at) }}
                                </div>
                                <a-button type="primary" shape="circle" class="buy-icon-button"
                                    @click="showBuyModal(item)" :disabled="item.inventory <= 0">
                                    <template #icon><shopping-cart-outlined /></template>
                                </a-button>
                            </div>
                        </template>
                    </a-card-meta>
                </a-card>
            </div>

            <a-empty v-if="filteredProducts.length === 0 && !loading" description="暂无商品" />

            <!-- 购买弹窗 -->
            <a-modal v-model:visible="buyModalVisible" title="购买商品" @ok="handleBuyConfirm" @cancel="handleBuyCancel"
                :okText="'确认购买'" :cancelText="'取消'"
                :okButtonProps="{ disabled: !isFormValid }">
                <a-form :model="buyForm" layout="vertical">
                    <a-form-item label="商品名称">
                        <span>{{ selectedProduct?.name }}</span>
                    </a-form-item>
                    <a-form-item label="单价">
                        <span>¥{{ selectedProduct?.price?.toFixed(2) }}/Kg</span>
                    </a-form-item>
                    <a-form-item label="购买数量 (Kg)" name="number" :rules="[{ required: true, message: '请输入购买数量' }]">
                        <a-input-number v-model:value="buyForm.number" :min="0.1" :max="selectedProduct?.inventory || 0"
                            :step="0.1" style="width: 100%" @change="calculateTotal" />
                    </a-form-item>
                    <a-form-item label="总价">
                        <span class="total-price">¥{{ totalPrice.toFixed(2) }}</span>
                    </a-form-item>
                    <a-form-item label="收货地址" name="address" :rules="[{ required: true, message: '请输入收货地址' }]">
                        <a-textarea v-model:value="buyForm.address" :rows="2" placeholder="请输入详细收货地址" />
                    </a-form-item>
                    <a-form-item label="联系电话" name="phone" :rules="[{ required: true, message: '请输入联系电话' }]">
                        <a-input v-model:value="buyForm.phone" placeholder="请输入联系电话" />
                    </a-form-item>
                </a-form>
            </a-modal>
        </div>
    </a-spin>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive, watch } from 'vue';
import { message } from 'ant-design-vue';
import { ShoppingCartOutlined } from '@ant-design/icons-vue';
import { getAllCommodities, initializeChat, createAlipayOrder } from '@/request/api';
import type { CommodityI } from '@/interface';
import { specifications, formatDate } from '@/interface';
import { useRouter } from 'vue-router';
const router = useRouter();

const products = ref<CommodityI[]>([]);
const loading = ref(false);
const searchText = ref('');
const selectedSpec = ref<string>();

// 购买相关
const buyModalVisible = ref(false);
const selectedProduct = ref<CommodityI | null>(null);
const buyForm = reactive({
    number: 0.1,
    address: '',
    phone: ''
});
const totalPrice = ref(0);

// 表单验证
const isFormValid = computed(() => {
    return buyForm.number > 0 &&
        buyForm.number <= (selectedProduct.value?.inventory || 0) &&
        buyForm.address.trim() !== '' &&
        buyForm.phone.trim() !== '';
});

// 计算总价
const calculateTotal = () => {
    if (selectedProduct.value && buyForm.number) {
        totalPrice.value = selectedProduct.value.price * buyForm.number;
    } else {
        totalPrice.value = 0;
    }
};

// 显示购买弹窗
const showBuyModal = (product: CommodityI) => {
    // 检查用户是否登录
    const userInfo = localStorage.getItem('userInfo');
    if (!userInfo) {
        message.error('请先登录');
        router.push('/login');
        return;
    }

    selectedProduct.value = product;
    buyForm.number = 0.1;
    calculateTotal();

    // 获取用户的历史地址和电话（如果有的话）
    const user = JSON.parse(userInfo);
    if (user.address) {
        buyForm.address = user.address;
    }
    if (user.phone) {
        buyForm.phone = user.phone;
    }

    buyModalVisible.value = true;
};

// 处理购买确认
const handleBuyConfirm = async () => {
    if (!isFormValid.value) {
        return;
    }

    const userInfo = localStorage.getItem('userInfo');
    if (!userInfo) {
        message.error('请先登录');
        router.push('/login');
        return;
    }

    const user = JSON.parse(userInfo);

    loading.value = true;
    try {
        const res = await createAlipayOrder({
            buy_id: user.id,
            commodity_id: selectedProduct.value?.id || 0,
            number: buyForm.number,
            address: buyForm.address,
            phone: buyForm.phone
        });

        if (res.data && res.data.url) {
            // 使用新窗口打开支付URL
            window.open(res.data.url, '_blank');
        } else {
            message.error('创建订单失败');
        }
    } catch (error) {
        console.error('创建订单错误:', error);
        message.error('创建订单失败');
    } finally {
        loading.value = false;
        buyModalVisible.value = false;
    }
};

// 处理取消购买
const handleBuyCancel = () => {
    buyModalVisible.value = false;
};

// 监听选中的商品变化
watch(selectedProduct, (newVal) => {
    if (newVal) {
        calculateTotal();
    }
});

// 筛选商品
const filteredProducts = computed(() => {
    let result = products.value;

    if (searchText.value) {
        result = result.filter(item =>
            item.name.toLowerCase().includes(searchText.value.toLowerCase())
        );
    }

    if (selectedSpec.value) {
        result = result.filter(item =>
            item.specification === selectedSpec.value
        );
    }

    return result;
});

// 搜索处理
const onSearch = (value: string) => {
    searchText.value = value;
};

// 规格筛选处理
const handleSpecChange = (value: string) => {
    selectedSpec.value = value;
};

// 联系卖家
const contactSeller = async (sellerId: number) => {
    const seller = products.value.find(item => item.sell_id === sellerId);
    console.log(seller);

    if (seller) {
        const userInfo = localStorage.getItem('userInfo');
        if (!userInfo) {
            message.error('请先登录');
            router.push('/login');
            return;
        }
        const currentUser = JSON.parse(userInfo);
        try {
            await initializeChat(currentUser.id, sellerId);
            router.push({
                path: '/chat',
                query: { contactId: sellerId }
            });
        } catch (error) {
            message.error('联系卖家失败');
        }
    }
};

// 获取商品数据
const fetchProducts = async () => {
    loading.value = true;
    try {
        const res = await getAllCommodities(true);
        products.value = res.data.map((item: CommodityI) => ({
            ...item,
            price: Number(item.price)
        }));
    } catch (error) {
        message.error('获取商品列表失败');
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    fetchProducts();
});
</script>

<style scoped>
.view-content {
    padding: 20px 100px;
}

.filter-section {
    margin-bottom: 24px;
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 24px;
}

.product-card {
    transition: all 0.3s;
    cursor: pointer;
    position: relative;
}

.product-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.title-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.product-name {
    font-size: 16px;
    font-weight: bold;
}

.specification {
    font-size: 12px;
    color: #666;
    background: #f5f5f5;
    padding: 2px 8px;
    border-radius: 4px;
}

.product-info {
    margin-top: 8px;
    position: relative;
}

.price {
    color: #f5222d;
    font-size: 18px;
    font-weight: bold;
    margin: 8px 0;
}

.product-stats {
    display: flex;
    justify-content: space-between;
    color: #666;
    margin: 8px 0;
}

.seller-info {
    margin: 8px 0;
    color: #666;
}

.seller-info a {
    color: #1890ff;
    text-decoration: none;
}

.publish-time {
    color: #999;
    font-size: 12px;
    margin: 8px 0;
}

.status-info {
    color: #666;
    margin: 8px 0;
}

.buy-icon-button {
    position: absolute;
    right: 0;
    bottom: 0px;
}

.card-actions {
    margin-top: 12px;
    display: flex;
    gap: 8px;
}

.total-price {
    color: #f5222d;
    font-size: 16px;
    font-weight: bold;
}
</style>