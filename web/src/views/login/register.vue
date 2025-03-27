<template>
    <div class="view-content">
        <a-form :model="formState" @finish="handleFinish" @finishFailed="handleFinishFailed" layout="vertical"
            class="register-form">
            <img src="@/assets/images/logo.png" alt="" class="logo_img">
            <a-form-item name="username" :rules="[{ required: true, message: '请输入用户名' }]">
                <a-input v-model:value="formState.username" placeholder="用户名" size="large">
                    <template #prefix>
                        <UserOutlined style="color: rgba(0, 0, 0, 0.25)" />
                    </template>
                </a-input>
            </a-form-item>
            <a-form-item name="password" :rules="[{ required: true, message: '请输入密码' }]">
                <a-input v-model:value="formState.password" type="password" placeholder="密码" size="large">
                    <template #prefix>
                        <LockOutlined style="color: rgba(0, 0, 0, 0.25)" />
                    </template>
                </a-input>
            </a-form-item>
            <a-form-item name="confirmPassword"
                :rules="[{ required: true, message: '请确认密码' }, { validator: validateConfirmPassword }]">
                <a-input v-model:value="formState.confirmPassword" type="password" placeholder="确认密码" size="large">
                    <template #prefix>
                        <LockOutlined style="color: rgba(0, 0, 0, 0.25)" />
                    </template>
                </a-input>
            </a-form-item>
            <a-form-item name="role" :rules="[{ required: true, message: '请选择角色' }]">
                <a-select v-model:value="formState.role" placeholder="请选择角色" size="large">
                    <a-select-option value="buy">买家</a-select-option>
                    <a-select-option value="sell">卖家</a-select-option>
                </a-select>
            </a-form-item>
            <a-form-item name="name"
                :rules="[{ required: true, message: formState.role === 'buy' ? '请输入昵称' : '请输入公司名称' }]">
                <a-input v-model:value="formState.name" :placeholder="formState.role === 'buy' ? '昵称' : '公司名称'"
                    size="large">
                    <template #prefix>
                        <UserOutlined style="color: rgba(0, 0, 0, 0.25)" />
                    </template>
                </a-input>
            </a-form-item>
            <a-form-item name="phone"
                :rules="[{ required: true, message: '请输入电话' }, { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码' }]">
                <a-input v-model:value="formState.phone" placeholder="电话" size="large">
                    <template #prefix>
                        <PhoneOutlined style="color: rgba(0, 0, 0, 0.25)" />
                    </template>
                </a-input>
            </a-form-item>
            <a-form-item>
                <a-button type="primary" html-type="submit" block size="large" :loading="loading">
                    注册
                </a-button>
            </a-form-item>
            <div class="form-footer">
                已有账号？<router-link to="/login">立即登录</router-link>
            </div>
        </a-form>
    </div>
</template>

<style scoped>
.view-content {
    height: 100%;
    width: 100%;
    background-color: #f0f2f5;
    display: flex;
    justify-content: center;
    align-items: center;
}

.register-form {
    width: 400px;
    background-color: #fff;
    padding: 20px;
    border-radius: 10px;
}

.logo_img {
    width: 200px;
    display: block;
    margin: 0 auto 20px;
}

.form-footer {
    text-align: right;
}
</style>

<script lang="ts" setup>
import { reactive, ref } from 'vue';
import { UserOutlined, LockOutlined, PhoneOutlined } from '@ant-design/icons-vue';
import type { UnwrapRef } from 'vue';
import type { FormProps } from 'ant-design-vue';
import { message } from 'ant-design-vue';
import { useRouter } from 'vue-router';
import { createUser } from '@/request/api';

interface FormState {
    username: string;
    password: string;
    confirmPassword: string;
    name: string;
    phone: string;
    role: string;
}

const router = useRouter();
const loading = ref(false);

const formState: UnwrapRef<FormState> = reactive({
    username: '',
    password: '',
    confirmPassword: '',
    name: '',
    phone: '',
    role: 'buy'
});

const validateConfirmPassword = async (_rule: any, value: string) => {
    if (value !== formState.password) {
        throw new Error('两次输入的密码不一致');
    }
};

const handleFinish: FormProps['onFinish'] = async () => {
    try {
        loading.value = true;
        const { confirmPassword, ...userData } = formState;
        await createUser(userData);
        message.success('注册成功');
        router.push('/login');
    } catch (error: any) {
        message.error(error.response?.data?.detail || '注册失败');
    } finally {
        loading.value = false;
    }
};

const handleFinishFailed: FormProps['onFinishFailed'] = ({ errorFields }) => {
    message.error(errorFields[0].errors[0]);
};
</script>