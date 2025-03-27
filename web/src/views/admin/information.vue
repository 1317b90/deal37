<template>
    <div class="admin-container">
        <div class="operation-bar">
            <a-space>
                <a-button type="primary" @click="showModal">新增资讯</a-button>
                <a-input-search v-model:value="searchText" placeholder="搜索资讯标题" @search="onSearch"
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
                        <a-tooltip title="编辑资讯">
                            <a-button type="primary" size="small" :icon="h(FormOutlined)"
                                @click="handleEdit(record)">编辑</a-button>
                        </a-tooltip>
                        <a-tooltip title="删除资讯">
                            <a-button type="primary" danger size="small" :icon="h(DeleteOutlined)"
                                @click="handleDelete(record.id)">删除</a-button>
                        </a-tooltip>
                    </a-space>
                </template>
                <template v-if="column.dataIndex === 'img_url'">
                    <a-image :src="record.img_url" :width="50" />
                </template>
                <template v-if="column.dataIndex === 'content'">
                    <a-typography-paragraph :ellipsis="{ rows: 2 }">{{ record.content }}</a-typography-paragraph>
                </template>
            </template>
        </a-table>

        <a-modal v-model:visible="visible" :title="modalTitle" @ok="handleOk" @cancel="handleCancel"
            :confirmLoading="submitLoading" :maskClosable="false">
            <a-form :model="formState" :rules="rules" ref="formRef" layout="vertical">
                <a-form-item label="标题" name="title">
                    <a-input v-model:value="formState.title" placeholder="请输入资讯标题" :maxLength="100" show-count />
                </a-form-item>
                <a-form-item label="作者" name="author">
                    <a-input v-model:value="formState.author" placeholder="请输入作者" :maxLength="50" show-count />
                </a-form-item>
                <a-form-item label="图片链接" name="img_url">
                    <a-input v-model:value="formState.img_url" placeholder="请输入图片链接" />
                    <div class="preview-image" v-if="formState.img_url">
                        <a-image :src="formState.img_url" :width="200" />
                    </div>
                </a-form-item>
                <a-form-item label="内容" name="content">
                    <a-textarea v-model:value="formState.content" placeholder="请输入资讯内容" :rows="6" show-count />
                </a-form-item>
            </a-form>
        </a-modal>

        <a-modal v-model:visible="deleteModalVisible" title="确认删除" @ok="confirmDelete" @cancel="cancelDelete"
            :confirmLoading="deleteLoading" :maskClosable="false">
            <template #icon>
                <ExclamationCircleOutlined style="color: #ff4d4f" />
            </template>
            <p>确定要删除这条资讯吗？此操作不可恢复。</p>
        </a-modal>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, h } from 'vue';
import { message } from 'ant-design-vue';
import { FormOutlined, DeleteOutlined, ExclamationCircleOutlined } from '@ant-design/icons-vue';
import type { FormInstance } from 'ant-design-vue';
import { createInformation, getAllInformation, updateInformation, deleteInformation } from '@/request/api';
import type { informationI } from '@/interface';

const dataSource = ref<informationI[]>([]);
const visible = ref<boolean>(false);
const deleteModalVisible = ref<boolean>(false);
const modalTitle = ref<string>('新增资讯');
const editingId = ref<number | null>(null);
const deleteId = ref<number | null>(null);
const formRef = ref<FormInstance>();
const loading = ref<boolean>(false);
const submitLoading = ref<boolean>(false);
const deleteLoading = ref<boolean>(false);
const searchText = ref<string>('');
const pageSize = ref<number>(10);

const formState = reactive<Omit<informationI, 'id'>>({
    title: '',
    author: '',
    img_url: '',
    content: '',
});

const filteredDataSource = computed(() => {
    if (!searchText.value) return dataSource.value;
    return dataSource.value.filter(item =>
        item.title.toLowerCase().includes(searchText.value.toLowerCase())
    );
});

const rules = {
    title: [
        { required: true, message: '请输入标题' },
        { max: 100, message: '标题长度不能超过100个字符' }
    ],
    author: [
        { required: true, message: '请输入作者' },
        { max: 50, message: '作者长度不能超过50个字符' }
    ],
    img_url: [
        { required: true, message: '请输入图片链接' },
        { type: 'url', message: '请输入有效的URL地址' }
    ],
    content: [
        { required: true, message: '请输入内容' },
        { max: 2000, message: '内容长度不能超过2000个字符' }
    ],
};

const columns = [
    {
        title: '标题',
        dataIndex: 'title',
        key: 'title',
        ellipsis: true,
        width: '20%',
    },
    {
        title: '作者',
        dataIndex: 'author',
        key: 'author',
        width: '10%',
    },
    {
        title: '预览图',
        dataIndex: 'img_url',
        key: 'img_url',
        width: 80,
    },
    {
        title: '内容',
        dataIndex: 'content',
        key: 'content',
        width: '30%',
    },
    {
        title: '创建时间',
        dataIndex: 'created_at',
        key: 'created_at',
        width: '15%',
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
        const res = await getAllInformation();
        dataSource.value = res.data;
    } catch (error) {
        message.error('获取资讯列表失败');
    } finally {
        loading.value = false;
    }
};

const onSearch = (value: string) => {
    searchText.value = value;
};

const resetForm = () => {
    formState.title = '';
    formState.author = '';
    formState.img_url = '';
    formState.content = '';
    formRef.value?.resetFields();
};

const showModal = () => {
    editingId.value = null;
    modalTitle.value = '新增资讯';
    resetForm();
    visible.value = true;
};

const handleEdit = (record: informationI) => {
    editingId.value = record.id ?? null;
    modalTitle.value = '编辑资讯';
    Object.assign(formState, {
        title: record.title,
        author: record.author,
        img_url: record.img_url,
        content: record.content,
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
        await deleteInformation(deleteId.value);
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
                await createInformation(formState);
                message.success('创建成功');
            } else {
                await updateInformation(editingId.value, formState);
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