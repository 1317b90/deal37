<template>
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

        <a-spin :spinning="loading">
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
                            </div>
                        </template>
                    </a-card-meta>
                </a-card>
            </div>
        </a-spin>

        <a-empty v-if="filteredProducts.length === 0 && !loading" description="暂无商品" />
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { getAllCommodities, initializeChat } from '@/request/api';
import type { CommodityI } from '@/interface';
import { specifications, formatDate } from '@/interface';
import { useRouter } from 'vue-router';
const router = useRouter();

const products = ref<CommodityI[]>([]);
const loading = ref(false);
const searchText = ref('');
const selectedSpec = ref<string>();

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
    padding: 24px;
    max-width: 1200px;
    margin: 0 auto;
}

.filter-section {
    margin-bottom: 24px;
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 24px;
    margin-top: 24px;
}

.product-card {
    transition: all 0.3s;
    cursor: pointer;
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

.card-actions {
    margin-top: 12px;
    display: flex;
    gap: 8px;
}

.specification {
    margin-left: 10px;
    color: #666;
    background: #f5f5f5;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 14px;
}

.price {
    color: #ff4d4f;
    font-size: 16px;
    font-weight: bold;
}

.specification {
    color: #666;
}

.product-stats {
    display: flex;
    gap: 16px;
    color: #666;
    margin: 8px 0;
}

.publish-time {
    color: #999;
    font-size: 12px;
}
</style>