<template>
    <div class="order-container">
        <!-- 搜索区域 -->
        <a-card class="search-card" :bordered="false">
            <a-form layout="inline" :model="searchForm">
                <a-form-item label="买家ID">
                    <a-input v-model:value="searchForm.buy_id" placeholder="请输入买家ID" allowClear />
                </a-form-item>
                <a-form-item label="卖家ID">
                    <a-input v-model:value="searchForm.sell_id" placeholder="请输入卖家ID" allowClear />
                </a-form-item>
                <a-form-item label="商品名称">
                    <a-input v-model:value="searchForm.commodity_name" placeholder="请输入商品名称" allowClear />
                </a-form-item>
                <a-form-item>
                    <a-space>
                        <a-button type="primary" @click="handleSearch">
                            <template #icon><search-outlined /></template>
                            搜索
                        </a-button>
                        <a-button @click="resetSearch">
                            <template #icon><reload-outlined /></template>
                            重置
                        </a-button>
                    </a-space>
                </a-form-item>
            </a-form>
        </a-card>

        <!-- 订单列表 -->

        <a-table :dataSource="orderList" :columns="columns" rowKey="id" :pagination="pagination" :loading="loading"
            @change="handleTableChange">
            <template #bodyCell="{ column, record }">
                <template v-if="column.key === 'created_at'">
                    {{ formatDate(record.created_at) }}
                </template>
                <template v-if="column.key === 'status'">
                    <a-tag :color="getStatusColor(record.status)">
                        {{ record.status }}
                    </a-tag>
                </template>
                <template v-if="column.key === 'action' && userInfo.role != 'buy'">
                    <a-space>
                        <a-tooltip v-if="record.status === '待发货'" title="发货">
                            <a-button type="primary" shape="circle" size="small" :icon="h(SendOutlined)"
                                @click="handleShip(record)" />
                        </a-tooltip>
                        <a-tooltip v-if="record.status === '待付款' || record.status === '待发货'" title="取消订单">
                            <a-button danger shape="circle" size="small" :icon="h(CloseOutlined)"
                                @click="handleCancel(record)" />
                        </a-tooltip>
                    </a-space>
                </template>
            </template>
        </a-table>


        <!-- 发货弹窗 -->
        <a-modal v-model:visible="shipModalVisible" title="填写快递单号" @ok="confirmShip" okText="确认" cancelText="取消">
            <a-form>
                <a-form-item label="快递单号">
                    <a-input v-model:value="expressNumber" placeholder="请输入快递单号" />
                </a-form-item>
            </a-form>
        </a-modal>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, reactive, h } from 'vue';
import { getOrderList, updateOrder, sendMessage } from '@/request/api';
import type { OrderI } from '@/interface';
import { message } from 'ant-design-vue';
import { formatDate } from '@/interface';
import { SearchOutlined, ReloadOutlined, SendOutlined, CloseOutlined } from '@ant-design/icons-vue';

const userInfo = ref({
    id: '',
    name: '',
    role: ''
});

const orderList = ref<OrderI[]>([]);
const currentOrder = ref<OrderI | null>(null);
const shipModalVisible = ref(false);
const expressNumber = ref('');
const loading = ref(false);

// 搜索表单数据
const searchForm = reactive({
    buy_id: '',
    sell_id: '',
    commodity_name: '' // 仅装饰，无实际功能
});

// 分页参数
const pagination = reactive({
    current: 1,
    pageSize: 10,
    total: 0,
    showSizeChanger: true,
    showQuickJumper: true,
    showTotal: (total: number) => `共 ${total} 条数据`
});

// 处理分页变化
const handleTableChange = (pag: any) => {
    pagination.current = pag.current;
    pagination.pageSize = pag.pageSize;
    fetchOrders();
};

// 搜索方法
const handleSearch = () => {
    fetchOrders();
};

// 重置搜索
const resetSearch = () => {
    searchForm.buy_id = '';
    searchForm.sell_id = '';
    searchForm.commodity_name = '';
    fetchOrders();
};

// 根据用户角色显示不同的列
const columns = computed(() => {
    const baseColumns = [
        { title: '订单ID', dataIndex: 'id', key: 'id', align: 'center' },
        { title: '买家ID', dataIndex: 'buy_id', key: 'buy_id', align: 'center' },
        { title: '卖家ID', dataIndex: 'sell_id', key: 'sell_id', align: 'center' },
        { title: '商品ID', dataIndex: 'commodity_id', key: 'commodity_id', align: 'center' },
        { title: '数量', dataIndex: 'number', key: 'number', align: 'center' },
        { title: '金额', dataIndex: 'amount', key: 'amount', align: 'center' },
        { title: '收货地址', dataIndex: 'address', key: 'address', align: 'center' },
        { title: '快递单号', dataIndex: 'express_number', key: 'express_number', align: 'center' },
        { title: '联系电话', dataIndex: 'phone', key: 'phone', align: 'center' },
        { title: '创建时间', dataIndex: 'created_at', key: 'created_at', align: 'center' },
        { title: '状态', dataIndex: 'status', key: 'status', align: 'center' },
    ];

    if (userInfo.value.role != 'buy') {
        baseColumns.push({ title: '操作', dataIndex: 'action', key: 'action', align: 'center' });
    }

    return baseColumns;
});

// 获取订单列表
const fetchOrders = async () => {
    loading.value = true;
    try {
        const params: Record<string, any> = {
            page: pagination.current,
            limit: pagination.pageSize
        };

        if (userInfo.value.role === 'buyer') {
            params.buy_id = userInfo.value.id;
        } else if (userInfo.value.role === 'seller') {
            params.sell_id = userInfo.value.id;
        } else {
            // 管理员可以搜索特定买家或卖家
            if (searchForm.buy_id) {
                params.buy_id = searchForm.buy_id;
            }
            if (searchForm.sell_id) {
                params.sell_id = searchForm.sell_id;
            }
        }

        const res = await getOrderList(params);
        orderList.value = res.data.data;
        pagination.total = res.data.total; // 更新总数
    } catch (error) {
        console.error('获取订单列表失败:', error);
        message.error('获取订单列表失败');
    } finally {
        loading.value = false;
    }
};

// 发货处理
const handleShip = (record: OrderI) => {
    currentOrder.value = record;
    shipModalVisible.value = true;
};

// 确认发货
const confirmShip = async () => {
    if (!expressNumber.value) {
        message.warning('请输入快递单号');
        return;
    }

    if (!currentOrder.value) return;

    try {
        await updateOrder(currentOrder.value.id, {
            status: '已发货', // 已发货
            express_number: expressNumber.value
        });
        await sendMessage({
            sender_id: currentOrder.value.buy_id,
            receiver_id: currentOrder.value.sell_id,
            content: `您的订单${currentOrder.value.id}已发货，快递单号为${expressNumber.value}`
        });
        message.success('发货成功');
        shipModalVisible.value = false;
        expressNumber.value = '';
        await fetchOrders(); // 刷新订单列表
    } catch (error) {
        console.error('发货失败:', error);
        message.error('发货失败');
    }
};

// 取消订单
const handleCancel = async (record: OrderI) => {
    try {
        await updateOrder(record.id, {
            status: '已取消' // 已取消
        });
        message.success('订单已取消');
        await fetchOrders(); // 刷新订单列表
    } catch (error) {
        console.error('取消订单失败:', error);
        message.error('取消订单失败');
    }
};

// 根据订单状态获取对应的标签颜色
const getStatusColor = (status: string) => {
    switch (status) {
        case '待付款':
            return 'orange';
        case '待发货':
            return 'blue';
        case '已发货':
            return 'green';
        case '已完成':
            return 'green';
        case '已取消':
            return 'gray';
        default:
            return '';
    }
};

onMounted(async () => {
    const localUserInfo = localStorage.getItem('userInfo');
    if (localUserInfo) {
        userInfo.value = JSON.parse(localUserInfo);
        await fetchOrders();
    } else {
        message.warning('请先登录');
    }
});
</script>

<style scoped>
.order-container {
    padding: 24px;
    background-color: #f0f2f5;
    min-height: 100vh;
}

.search-card {
    margin-bottom: 24px;
    border-radius: 8px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.table-card {
    border-radius: 8px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.ant-form-item {
    margin-bottom: 16px;
}

@media (max-width: 768px) {
    .ant-form-inline .ant-form-item {
        margin-right: 0;
        display: block;
    }
}
</style>
