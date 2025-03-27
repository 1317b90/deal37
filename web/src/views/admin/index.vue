<template>
    <a-layout class="admin-class">
        <a-layout-sider width="200" style="background: #fff">
            <div class="logo">
                <img src="@/assets/images/logo.png" alt="" class="logo_img">
            </div>

            <a-menu v-model:selectedKeys="menuKeys" v-model:openKeys="menuKey" mode="inline" @select="selectMenu"
                class="admin-menu">


                <a-menu-item key="/admin/information" class="app-menu-title"><span
                        class="app-menu-title">资讯管理</span></a-menu-item>

                <a-menu-item key="/admin/user" class="app-menu-title"><span
                        class="app-menu-title">用户管理</span></a-menu-item>

                <a-menu-item key="/admin/commodity" class="app-menu-title"><span
                        class="app-menu-title">商品管理</span></a-menu-item>


                <a-menu-item key="/" class="app-menu-title"><span class="app-menu-title">用户界面</span></a-menu-item>

                <a-menu-item key="/login" class="app-menu-title"><span class="app-menu-title">退出登录</span></a-menu-item>

            </a-menu>
        </a-layout-sider>

        <a-layout-content :style="{ padding: '0 24px', minHeight: '280px' }">
            <RouterView />
        </a-layout-content>
    </a-layout>

</template>

<script setup lang="ts">
import { ref } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import { useRouter } from 'vue-router';
const router = useRouter();

import { UserOutlined, LaptopOutlined, NotificationOutlined } from '@ant-design/icons-vue';
const menuKeys = ref<string[]>(['/admin/information']);
const menuKey = ref<string[]>(['/admin/information']);

menuKeys.value[0] = sessionStorage.getItem('admin_router') || '/';

// 选择菜单时
function selectMenu(item: any) {
    console.log(item)
    // 存储到本地，避免刷新丢失
    sessionStorage.setItem('admin_router', item.key);
    router.push(item.key)
}

</script>
<style scoped>
.admin-class {
    height: 100vh;
}

.logo {
    padding: 20px 10px;
}

.logo_img {
    width: 100%;
}
</style>