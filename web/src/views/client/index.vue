<template>
    <a-layout class="layout">
        <a-layout-header class="app-header">
            <a-menu v-model:selectedKeys="selectedKeys" mode="horizontal" @select="selectMenu">
                <a-menu-item key="/"><img src="@/assets/images/logo.png" class="app-logo"></a-menu-item>
                <a-menu-item key="/market"><span class="app-menu-title">市场行情</span></a-menu-item>

                <a-menu-item key="/information" class="app-menu-title"><span
                        class="app-menu-title">知识资讯</span></a-menu-item>

                <a-menu-item key="/buy" class="app-menu-title"><span class="app-menu-title">我要买货</span></a-menu-item>

                <a-menu-item v-if="userInfo.role != 'buy'" key="/sell" class="app-menu-title"><span
                        class="app-menu-title">我要卖货</span></a-menu-item>

                <a-menu-item key="/chat" class="app-menu-title"><span class="app-menu-title">我要聊天</span></a-menu-item>

                <a-menu-item key="/order" class="app-menu-title"><span class="app-menu-title">我的订单</span></a-menu-item>

                <a-sub-menu key="/auth/login" class="app-menu-login" style="margin-left: auto;">
                    <template #title>
                        <span>
                            <UserOutlined />
                            {{ userInfo.name }}
                        </span>
                    </template>

                    <a-menu-item key="/set">修改信息</a-menu-item>
                    <a-menu-item v-if="userInfo.role == 'admin'" key="/admin">后台管理</a-menu-item>
                    <a-menu-item key="/login">退出登录</a-menu-item>
                </a-sub-menu>

            </a-menu>
        </a-layout-header>

        <a-layout-content class="app-content">
            <RouterView />
        </a-layout-content>

        <a-layout-footer style="text-align: center">
            文山三七交易平台 ©2024 Created by Zhang bing
        </a-layout-footer>
    </a-layout>
</template>
<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue';
import { UserOutlined } from '@ant-design/icons-vue';
import { RouterLink, RouterView } from 'vue-router'
import { useRouter, useRoute } from 'vue-router';
const router = useRouter();
const route = useRoute();

const selectedKeys = ref<string[]>(['/']);
selectedKeys.value[0] = sessionStorage.getItem('router') || '/';

// 从本地存储读取用户信息
const userInfo = ref({
    id: '',
    name: '',
    role: ''
})

// 选择菜单时
function selectMenu(item: any) {
    // 存储到本地，避免刷新丢失
    sessionStorage.setItem('router', item.key);
    router.push(item.key)
}

// 监听路由变化，更新菜单选中状态
watch(() => route.path, (newPath) => {
    selectedKeys.value = [newPath];
    sessionStorage.setItem('router', newPath);
}, { immediate: true });

onMounted(() => {
    const localUserInfo = localStorage.getItem('userInfo')
    if (localUserInfo) {
        userInfo.value = JSON.parse(localUserInfo)
    }

    if (userInfo.value.id == '') {
        router.push('/login')
    }
})


</script>

<style scoped>
.app-header {
    /* padding: 0px; */
    padding-left: 100px;
    position: fixed;
    z-index: 1;
    width: 100%;
    background-color: #fff;
    box-shadow: rgba(0, 0, 0, 0.03) 0px 8px 16px 0px;
}

.app-logo {
    float: left;
    padding-top: 10px;
    height: 60px;
    margin-right: 100px;
}

.app-content {
    height: calc(100vh - 67px - 70px);
    margin-top: 65px;
    overflow: auto;
}

.app-menu-title {
    font-size: 16px;
    font-weight: 600;
    font-family: 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
}
</style>
