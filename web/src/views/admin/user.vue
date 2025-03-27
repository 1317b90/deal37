<template>
    <div class="admin-container">
        <div class="operation-bar">
            <a-space>
                <a-button type="primary" @click="showModal">新增用户</a-button>
                <a-input-search v-model:value="searchText" placeholder="搜索用户名" @search="onSearch"
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
                        <a-tooltip title="编辑用户">
                            <a-button type="primary" size="small" :icon="h(FormOutlined)"
                                @click="handleEdit(record)">编辑</a-button>
                        </a-tooltip>
                        <a-tooltip title="删除用户">
                            <a-button type="primary" danger size="small" :icon="h(DeleteOutlined)"
                                @click="handleDelete(record.id)">删除</a-button>
                        </a-tooltip>
                    </a-space>
                </template>
            </template>
        </a-table>

        <a-modal v-model:visible="visible" :title="modalTitle" @ok="handleOk" @cancel="handleCancel"
            :confirmLoading="submitLoading" :maskClosable="false">
            <a-form :model="formState" :rules="rules" ref="formRef" layout="vertical">
                <a-form-item label="用户名" name="username">
                    <a-input v-model:value="formState.username" placeholder="请输入用户名" :maxLength="50" show-count
                        :disabled="!!editingId" />
                </a-form-item>
                <a-form-item label="密码" name="password">
                    <a-input-password v-model:value="formState.password" placeholder="请输入密码" />
                </a-form-item>
                <a-form-item label="昵称或公司名称" name="name">
                    <a-input v-model:value="formState.name" placeholder="昵称或公司名称" />
                </a-form-item>
                <a-form-item label="手机号" name="phone">
                    <a-input v-model:value="formState.phone" placeholder="请输入手机号" />
                </a-form-item>
                <a-form-item label="角色" name="role">
                    <a-select v-model:value="formState.role" placeholder="请选择角色">
                        <a-select-option value="admin">管理员</a-select-option>
                        <a-select-option value="buy">买家</a-select-option>
                        <a-select-option value="sell">卖家</a-select-option>
                    </a-select>
                </a-form-item>
            </a-form>
        </a-modal>

        <a-modal v-model:visible="deleteModalVisible" title="确认删除" @ok="confirmDelete" @cancel="cancelDelete"
            :confirmLoading="deleteLoading" :maskClosable="false">
            <template #icon>
                <ExclamationCircleOutlined style="color: #ff4d4f" />
            </template>
            <p>确定要删除这个用户吗？此操作不可恢复。</p>
        </a-modal>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, h } from 'vue';
import { message } from 'ant-design-vue';
import { FormOutlined, DeleteOutlined, ExclamationCircleOutlined } from '@ant-design/icons-vue';
import type { FormInstance } from 'ant-design-vue';
import { createUser, getAllUsers, updateUser, deleteUser } from '@/request/api';
import type { UserI } from '@/interface';

const dataSource = ref<UserI[]>([]);
const visible = ref<boolean>(false);
const deleteModalVisible = ref<boolean>(false);
const modalTitle = ref<string>('新增用户');
const editingId = ref<number | null>(null);
const deleteId = ref<number | null>(null);
const formRef = ref<FormInstance>();
const loading = ref<boolean>(false);
const submitLoading = ref<boolean>(false);
const deleteLoading = ref<boolean>(false);
const searchText = ref<string>('');
const pageSize = ref<number>(10);

const formState = reactive<Omit<UserI, 'id' | 'created_at' | 'updated_at'>>({
    username: '',
    password: '',
    name: '',
    phone: '',
    role: 'buy'
});

const filteredDataSource = computed(() => {
    if (!searchText.value) return dataSource.value;
    return dataSource.value.filter(item =>
        item.username.toLowerCase().includes(searchText.value.toLowerCase())
    );
});

const rules = {
    username: [
        { required: true, message: '请输入用户名' },
        { max: 50, message: '用户名长度不能超过50个字符' }
    ],
    password: [
        { required: !editingId.value, message: '请输入密码' },
        { min: 6, message: '密码长度不能少于6个字符', trigger: 'change' }
    ],
    name: [
        { required: true, message: '请输入昵称或公司名称' }
    ],
    phone: [
        { required: true, message: '请输入手机号' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号' }
    ],
    role: [
        { required: true, message: '请选择角色' }
    ]
};

const columns = [
    {
        title: 'ID',
        dataIndex: 'id',
        key: 'id',
        width: '5%',
        align: 'center'
    },
    {
        title: '用户名',
        dataIndex: 'username',
        key: 'username',
        align: 'center'
    },
    {
        title: '名称',
        dataIndex: 'name',
        key: 'name',
        align: 'center'
    },
    {
        title: '手机号',
        dataIndex: 'phone',
        key: 'phone',
        align: 'center'
    },
    {
        title: '角色',
        dataIndex: 'role',
        key: 'role',
        align: 'center',
        customRender: ({ text }: { text: string }) => {
            const roleMap = {
                admin: '管理员',
                buy: '买家',
                sell: '卖家'
            };
            return roleMap[text as keyof typeof roleMap] || text;
        }
    },
    {
        title: '创建时间',
        dataIndex: 'created_at',
        key: 'created_at',
        align: 'center'
    },
    {
        title: '修改时间',
        dataIndex: 'updated_at',
        key: 'updated_at',
        align: 'center'
    },
    {
        title: '操作',
        key: 'action',
        dataIndex: 'action',
        width: 150,
        fixed: 'right',
        align: 'center'
    },
];

const fetchData = async () => {
    loading.value = true;
    try {
        const res = await getAllUsers();
        dataSource.value = res.data;
    } catch (error) {
        message.error('获取用户列表失败');
    } finally {
        loading.value = false;
    }
};

const onSearch = (value: string) => {
    searchText.value = value;
};

const resetForm = () => {
    formState.username = '';
    formState.password = '';
    formState.name = '';
    formState.phone = '';
    formState.role = 'buy';
    formRef.value?.resetFields();
};

const showModal = () => {
    editingId.value = null;
    modalTitle.value = '新增用户';
    resetForm();
    visible.value = true;
};

const handleEdit = (record: UserI) => {
    editingId.value = record.id;
    modalTitle.value = '编辑用户';
    Object.assign(formState, {
        username: record.username,
        name: record.name,
        password: record.password, // 编辑时密码置空
        phone: record.phone,
        role: record.role
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
        await deleteUser(deleteId.value);
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
                await createUser(formState);
                message.success('创建成功');
            } else {
                // 编辑时，如果密码为空，则不修改密码
                // const updateData = { ...formState };
                // if (!updateData.password) {
                //     delete updateData.password;
                // }
                await updateUser(editingId.value, formState);
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
</style>