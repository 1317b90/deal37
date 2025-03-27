<template>
    <div class="admin-container">
        <div class="operation-bar">
            <a-space>
                <a-button type="primary" @click="showModal">新增商品</a-button>
                <a-input-search v-model:value="searchText" placeholder="搜索商品名称" @search="onSearch"
                    style="width: 200px" />
            </a-space>
        </div>

        <a-table :dataSource="filteredDataSource" :columns="columns" :loading="loading" :pagination="{
                    total: filteredDataSource.length,
                    pageSize: pageSize,
                    showSizeChanger: true,
                    showQuickJumper: true,
                }">
            <template #bodyCell="{ column, record }">
                <template v-if="column.dataIndex === 'action'">
                    <a-space>
                        <a-tooltip title="编辑商品">
                            <a-button type="primary" size="small" :icon="h(FormOutlined)"
                                @click="handleEdit(record)">编辑</a-button>
                        </a-tooltip>
                        <a-tooltip title="删除商品">
                            <a-button type="primary" danger size="small" :icon="h(DeleteOutlined)"
                                @click="handleDelete(record.id)">删除</a-button>
                        </a-tooltip>
                    </a-space>
                </template>
                <template v-if="column.dataIndex === 'image'">
                    <a-image :src="record.image" :width="50" />
                </template>
                <template v-if="column.dataIndex === 'price'">
                    ¥{{ typeof record.price === 'number' ? record.price.toFixed(2) : '0.00' }}
                </template>
                <template v-if="column.dataIndex === 'onShelf'">
                    <a-switch v-model:checked="record.onShelf" size="small" disabled />
                </template>
            </template>
        </a-table>

        <a-modal v-model:visible="visible" :title="modalTitle" @ok="handleOk" @cancel="handleCancel"
            :confirmLoading="submitLoading" :maskClosable="false">
            <a-form :model="formState" :rules="rules" ref="formRef" layout="vertical">
                <a-form-item label="商品名称" name="name">
                    <a-input v-model:value="formState.name" placeholder="请输入商品名称" :maxLength="100" show-count />
                </a-form-item>
                <a-form-item label="商品价格(元/Kg)" name="price">
                    <a-input-number v-model:value="formState.price" :min="0" :precision="2" style="width: 100%"
                        placeholder="请输入商品价格" />
                </a-form-item>
                <a-form-item label="商品规格" name="specification">
                    <a-select v-model:value="formState.specification" placeholder="请选择商品规格">
                        <a-select-option v-for="spec in specifications" :key="spec" :value="spec">{{ spec
                            }}</a-select-option>
                    </a-select>
                </a-form-item>
                <a-form-item label="商品库存" name="inventory">
                    <a-input-number v-model:value="formState.inventory" :min="0" style="width: 100%"
                        placeholder="请输入商品库存" />
                </a-form-item>
                <a-form-item label="图片链接" name="image">
                    <a-input v-model:value="formState.image" placeholder="请输入图片链接" />
                    <div class="preview-image" v-if="formState.image">
                        <a-image :src="formState.image" :width="200" />
                    </div>
                </a-form-item>
                <a-form-item label="卖家ID" name="sell_id">
                    <a-input-number v-model:value="formState.sell_id" :min="1" style="width: 100%"
                        placeholder="请输入卖家ID" />
                </a-form-item>
                <a-form-item label="卖家名称" name="sell_name">
                    <a-input v-model:value="formState.sell_name" placeholder="请输入卖家名称" :maxLength="50" show-count />
                </a-form-item>
                <a-form-item label="上架状态" name="onShelf">
                    <a-switch v-model:checked="formState.onShelf" />
                </a-form-item>
            </a-form>
        </a-modal>

        <a-modal v-model:visible="deleteModalVisible" title="确认删除" @ok="confirmDelete" @cancel="cancelDelete"
            :confirmLoading="deleteLoading" :maskClosable="false">
            <template #icon>
                <ExclamationCircleOutlined style="color: #ff4d4f" />
            </template>
            <p>确定要删除这个商品吗？此操作不可恢复。</p>
        </a-modal>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, h } from 'vue';
import { message } from 'ant-design-vue';
import { FormOutlined, DeleteOutlined, ExclamationCircleOutlined } from '@ant-design/icons-vue';
import type { FormInstance } from 'ant-design-vue';
import { createCommodity, getAllCommodities, updateCommodity, deleteCommodity } from '@/request/api';
import type { CommodityI } from '@/interface';
import { specifications } from '@/interface';
const dataSource = ref<CommodityI[]>([]);
const visible = ref<boolean>(false);
const deleteModalVisible = ref<boolean>(false);
const modalTitle = ref<string>('新增商品');
const editingId = ref<number | null>(null);
const deleteId = ref<number | null>(null);
const formRef = ref<FormInstance>();
const loading = ref<boolean>(false);
const submitLoading = ref<boolean>(false);
const deleteLoading = ref<boolean>(false);
const searchText = ref<string>('');
const pageSize = ref<number>(10);

const formState = reactive<Omit<CommodityI, 'id' | 'created_at' | 'updated_at'>>({
    name: '',
    price: 0,
    specification: "统货", // 默认选择'统货'
    sales: 0,
    inventory: 0,
    image: '',
    sell_id: 0,
    sell_name: '',
    onShelf: true, // 默认上架
});

const filteredDataSource = computed(() => {
    if (!searchText.value) return dataSource.value;
    return dataSource.value.filter(item =>
        item.name.toLowerCase().includes(searchText.value.toLowerCase())
    );
});

const rules = {
    name: [
        { required: true, message: '请输入商品名称' },
        { max: 100, message: '商品名称长度不能超过100个字符' }
    ],
    price: [
        { required: true, message: '请输入商品价格' },
        { type: 'number', min: 0, message: '价格必须大于等于0' }
    ],
    inventory: [
        { required: true, message: '请输入商品库存' },
        { type: 'number', min: 0, message: '库存必须大于等于0' }
    ],
    image: [
        { required: true, message: '请输入图片链接' },
        { type: 'url', message: '请输入有效的URL地址' }
    ],
    sell_id: [
        { required: true, message: '请输入卖家ID' },
        { type: 'number' }
    ],
    sell_name: [
        { required: true, message: '请输入卖家名称' }
    ],
};

const columns = [
    {
        title: '商品名称',
        dataIndex: 'name',
        key: 'name',
        ellipsis: true,
        width: '10%',
    },
    {
        title: '预览图',
        dataIndex: 'image',
        key: 'image',
        width: 80,
    },
    {
        title: '价格',
        dataIndex: 'price',
        key: 'price',
        width: '10%',
    },
    {
        title: '规格',
        dataIndex: 'specification',
        key: 'specification',
        width: '10%',
    },
    {
        title: '库存',
        dataIndex: 'inventory',
        key: 'inventory',
        width: '10%',
    },
    {
        title: '销量',
        dataIndex: 'sales',
        key: 'sales',
        width: '8%',
    },
    {
        title: '上架状态',
        dataIndex: 'onShelf',
        key: 'onShelf',
        width: '8%',
    },
    {
        title: '卖家',
        dataIndex: 'sell_name',
        key: 'sell_name',
        width: '12%',
    },
    {
        title: '创建时间',
        dataIndex: 'created_at',
        key: 'created_at',
        width: '12%',
    },
    {
        title: '操作',
        key: 'action',
        dataIndex: 'action',
        width: 150,
        fixed: 'right',
    },
];

const fetchData = async () => {
    loading.value = true;
    try {
        const res = await getAllCommodities();
        // 确保价格字段为数字类型
        dataSource.value = res.data.map((item: CommodityI) => ({
            ...item,
            price: Number(item.price)
        }));
    } catch (error) {
        message.error('获取商品列表失败');
    } finally {
        loading.value = false;
    }
};

const onSearch = (value: string) => {
    searchText.value = value;
};

const resetForm = () => {
    formState.name = '';
    formState.price = 0;
    formState.inventory = 0;
    formState.image = '';
    formState.sell_id = 0;
    formState.sell_name = '';
    formState.onShelf = true; // 重置时设为默认上架
    formRef.value?.resetFields();
};

const showModal = () => {
    editingId.value = null;
    modalTitle.value = '新增商品';
    resetForm();
    visible.value = true;
};

const handleEdit = (record: CommodityI) => {
    editingId.value = record.id;
    modalTitle.value = '编辑商品';
    Object.assign(formState, {
        name: record.name,
        price: record.price,
        inventory: record.inventory,
        image: record.image,
        sell_id: record.sell_id,
        sell_name: record.sell_name,
        onShelf: record.onShelf,
    });
    visible.value = true;
};

const handleDelete = (id: number) => {
    deleteId.value = id;
    deleteModalVisible.value = true;
};

const confirmDelete = async () => {
    if (deleteId.value === null) return;
    deleteLoading.value = true;

    try {
        await deleteCommodity(deleteId.value);
        message.success('删除成功');
        deleteModalVisible.value = false;
        await fetchData();
    } catch (error) {
        message.error('删除失败');
    } finally {
        deleteLoading.value = false;
        deleteId.value = null;
    }
};

const cancelDelete = () => {
    deleteId.value = null;
    deleteModalVisible.value = false;
};

const handleOk = () => {
    formRef.value?.validate().then(async () => {
        submitLoading.value = true;
        try {
            if (editingId.value === null) {
                await createCommodity(formState);
                message.success('创建成功');
            } else {
                await updateCommodity(editingId.value, formState);
                message.success('更新成功');
            }
            visible.value = false;
            resetForm();
            await fetchData();
        } catch (error) {
            message.error(editingId.value === null ? '创建失败' : '更新失败');
        } finally {
            submitLoading.value = false;
        }
    });
};

const handleCancel = () => {
    visible.value = false;
    resetForm();
};

onMounted(() => {
    fetchData();
});
</script>

<style scoped>
.admin-container {
    padding: 24px;
    height: calc(100vh - 24px);
    width: calc(100vw - 24px -200px)
}

.operation-bar {
    margin-bottom: 16px;
}

.preview-image {
    margin-top: 8px;
}

.preview-image img {
    max-width: 200px;
    max-height: 200px;
    border: 1px solid #d9d9d9;
    border-radius: 4px;
}
</style>