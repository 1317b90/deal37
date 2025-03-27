<template>
    <div class="view-content">
        <div class="header-actions">
            <h1>我的商品管理</h1>
            <a-button type="primary" @click="showModal = true">添加商品</a-button>
        </div>

        <a-spin :spinning="loading">
            <div class="products-list">
                <a-empty v-if="products.length === 0 && !loading" description="暂无商品" />
                <a-card v-else v-for="item in products" :key="item.id" class="product-card" :bordered="false">
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
                                <div class="price">¥{{ Number(item.price).toFixed(2) }}/Kg</div>
                                <div class="product-stats">
                                    <span>销量：{{ item.sales }}</span>
                                    <span>库存：{{ item.inventory }}</span>
                                </div>
                                <div class="status-info">
                                    状态：{{ item.onShelf ? '已上架' : '已下架' }}
                                </div>
                                <div class="publish-time">
                                    发布时间：{{ formatDate(item.created_at) }}
                                </div>
                                <div class="card-actions">
                                    <a-button type="link" @click="handleEdit(item)">编辑</a-button>
                                    <a-button type="link" @click="toggleShelf(item)">
                                        {{ item.onShelf ? '下架' : '上架' }}
                                    </a-button>
                                    <a-popconfirm title="确定要删除这个商品吗？" @confirm="handleDelete(item.id)">
                                        <a-button type="link" danger>删除</a-button>
                                    </a-popconfirm>
                                </div>
                            </div>
                        </template>
                    </a-card-meta>
                </a-card>
            </div>
        </a-spin>

        <a-modal v-model:visible="showModal" :title="editingProduct ? '编辑商品' : '添加商品'" @ok="handleSubmit"
            @cancel="resetForm">
            <a-form :model="formState" :rules="rules" ref="formRef">
                <a-form-item label="商品名称" name="name">
                    <a-input v-model:value="formState.name" />
                </a-form-item>
                <a-form-item label="价格" name="price">
                    <a-input-number v-model:value="formState.price" :min="0" style="width: 100%" />
                </a-form-item>
                <a-form-item label="规格" name="specification">
                    <a-select v-model:value="formState.specification">
                        <a-select-option v-for="spec in specifications" :key="spec" :value="spec">
                            {{ spec }}
                        </a-select-option>
                    </a-select>
                </a-form-item>
                <a-form-item label="库存" name="inventory">
                    <a-input-number v-model:value="formState.inventory" :min="0" style="width: 100%" />
                </a-form-item>
                <a-form-item label="图片链接" name="image">
                    <a-input v-model:value="formState.image" />
                </a-form-item>
            </a-form>
        </a-modal>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import type { CommodityI } from '@/interface'
import { specifications, formatDate } from '@/interface'
import { createCommodity, getAllCommodities, updateCommodity, deleteCommodity } from '@/request/api'
const userInfo = ref({
    id: '',
    name: '',
    role: ''
})

const loading = ref(false)
const products = ref<CommodityI[]>([])
const showModal = ref(false)
const editingProduct = ref<CommodityI | null>(null)
const formRef = ref()

const formState = ref({
    name: '',
    price: 0,
    specification: '统货',
    inventory: 0,
    image: '',
    onShelf: true
})

const rules = {
    name: [{ required: true, message: '请输入商品名称' }],
    price: [{ required: true, message: '请输入价格' }],
    specification: [{ required: true, message: '请选择规格' }],
    inventory: [{ required: true, message: '请输入库存' }],
    image: [{ required: true, message: '请输入图片链接' }]
}

// 获取商品列表
async function fetchProducts() {
    loading.value = true
    try {
        const response = await getAllCommodities()
        products.value = response.data.filter((item: CommodityI) => String(item.sell_id) == userInfo.value.id)
    } catch (error) {
        message.error('获取商品列表失败')
    } finally {
        loading.value = false
    }
}

// 处理表单提交
async function handleSubmit() {
    try {
        await formRef.value.validate()
        const productData = {
            name: formState.value.name,
            price: Number(formState.value.price),
            specification: formState.value.specification,
            inventory: formState.value.inventory,
            image: formState.value.image,
            onShelf: formState.value.onShelf,
            sell_id: Number(userInfo.value.id),
            sell_name: userInfo.value.name,
            sales: editingProduct.value?.sales || 0
        }

        if (editingProduct.value) {
            await updateCommodity(editingProduct.value.id, productData)
            message.success('商品更新成功')
        } else {
            await createCommodity(productData)
            message.success('商品添加成功')
        }
        showModal.value = false
        resetForm()
        fetchProducts()
    } catch (error) {
        message.error('操作失败，请重试')
    }
}

// 编辑商品
function handleEdit(product: CommodityI) {
    editingProduct.value = product
    formState.value = { ...product }
    showModal.value = true
}

// 删除商品
async function handleDelete(id: number) {
    try {
        await deleteCommodity(id)
        message.success('商品删除成功')
        fetchProducts()
    } catch (error) {
        message.error('删除失败，请重试')
    }
}

// 切换商品上下架状态
async function toggleShelf(product: CommodityI) {
    try {
        const updatedProduct = {
            name: product.name,
            price: product.price,
            specification: product.specification,
            inventory: product.inventory,
            sales: product.sales,
            sell_id: product.sell_id,
            sell_name: product.sell_name,
            image: product.image,
            onShelf: !product.onShelf
        }
        await updateCommodity(product.id, updatedProduct)
        message.success(`商品${product.onShelf ? '下架' : '上架'}成功`)
        fetchProducts()
    } catch (error) {
        message.error('操作失败，请重试')
    }
}

// 重置表单
function resetForm() {
    formRef.value?.resetFields()
    editingProduct.value = null
}

onMounted(() => {
    let localUserInfo = localStorage.getItem('userInfo')
    if (localUserInfo) {
        userInfo.value = JSON.parse(localUserInfo)
        fetchProducts()
    }
})
</script>

<style scoped>
.view-content {
    padding: 24px;
    max-width: 1200px;
    margin: 0 auto;
}

.header-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.products-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 24px;
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

.status-info {
    color: #666;
    margin: 8px 0;
}

.publish-time {
    color: #999;
    font-size: 12px;
    margin: 8px 0;
}

.card-actions {
    margin-top: 12px;
    display: flex;
    gap: 8px;
}
</style>