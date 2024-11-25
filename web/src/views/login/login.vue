<template>
  <div class="view-content">
    <a-form
        :model="formState"
        @finish="handleFinish"
        @finishFailed="handleFinishFailed"
        layout="vertical"
        class="login-form"
      >
          <a-form-item>
            <a-input v-model:value="formState.username" placeholder="用户名" size="large">
              <template #prefix><UserOutlined style="color: rgba(0, 0, 0, 0.25)" /></template>
            </a-input>
          </a-form-item>
          <a-form-item>
            <a-input v-model:value="formState.password" type="password" placeholder="密码" size="large">
              <template #prefix><LockOutlined style="color: rgba(0, 0, 0, 0.25)" /></template>
            </a-input>
          </a-form-item>
          <a-form-item>
            <a-button
              type="primary"
              html-type="submit"
              block
              size="large"
            >
              登录
            </a-button>
          </a-form-item>
    </a-form>
  </div>
</template>
<script lang="ts" setup>
import { reactive } from 'vue';
import { UserOutlined, LockOutlined } from '@ant-design/icons-vue';
import type { UnwrapRef } from 'vue';
import type { FormProps } from 'ant-design-vue';

interface FormState {
  username: string;
  password: string;
}
const formState: UnwrapRef<FormState> = reactive({
  username: '',
  password: '',
});
const handleFinish: FormProps['onFinish'] = values => {
  console.log(values, formState);
};
const handleFinishFailed: FormProps['onFinishFailed'] = errors => {
  console.log(errors);
};
</script>

<style scoped>
.view-content{
  height: 100%;
  width: 100%;
  /* padding: 50px 100px; */
  background-color: #f0f2f5;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-form{
  width: 400px;
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
}

</style>