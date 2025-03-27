<template>
  <div class="view-content">
    <a-form :model="formState" @finish="handleFinish" @finishFailed="handleFinishFailed" layout="vertical"
      class="login-form">
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
      <a-form-item>
        <a-button type="primary" html-type="submit" block size="large" :loading="loading">
          登录
        </a-button>
      </a-form-item>
      <div class="form-footer">
        没有账号？<router-link to="/register">立即注册</router-link>
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

.login-form {
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
import { UserOutlined, LockOutlined } from '@ant-design/icons-vue';
import type { UnwrapRef } from 'vue';
import type { FormProps } from 'ant-design-vue';
import { message } from 'ant-design-vue';
import { useRouter } from 'vue-router';
import { getUserByUsername } from '@/request/api';

interface FormState {
  username: string;
  password: string;
}

const router = useRouter();
const loading = ref(false);

const formState: UnwrapRef<FormState> = reactive({
  username: '',
  password: '',
});

const handleFinish: FormProps['onFinish'] = async () => {
  try {
    loading.value = true;
    const response = await getUserByUsername(formState.username);
    const user = response.data;

    if (!user) {
      throw new Error('用户不存在');
    }

    if (user.password !== formState.password) {
      console.log(user.password, formState.password);
      throw new Error('密码错误');
    }

    // 保存用户信息到本地存储
    localStorage.setItem('userInfo', JSON.stringify({
      id: user.id,
      name: user.name,
      role: user.role
    }));
    message.success('登录成功');
    router.push('/');
  } catch (error: any) {
    message.error(error.message || error.response?.data?.detail || '登录失败');
  } finally {
    loading.value = false;
  }
};

const handleFinishFailed: FormProps['onFinishFailed'] = ({ errorFields }) => {
  message.error(errorFields[0].errors[0]);
};
</script>

<style scoped>
.view-content {
  height: 100%;
  width: 100%;
  /* padding: 50px 100px; */
  background-color: #f0f2f5;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-form {
  width: 400px;
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
}
</style>