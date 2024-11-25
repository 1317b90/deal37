<template>
  <n-message-provider>
  <n-modal-provider>
  <n-dialog-provider>
  <n-layout class="app-all">
    <n-layout has-sider>
      <n-layout-sider
          bordered
          show-trigger
          collapse-mode="width"
          :collapsed-width="64"
          :width="240"
          :native-scrollbar="false"
          :inverted="inverted"
          class="app-sider"
        >
          <n-menu
            :inverted="inverted"
            :collapsed-width="64"
            :collapsed-icon-size="22"
            :options="menuOptions"
        />
      </n-layout-sider>
     
        <n-layout-content class="app-content">
          <router-view />
        </n-layout-content>
      
    </n-layout>
      <n-layout-footer class="app-footer" :inverted="inverted" bordered>
        Footer Footer Footer
      </n-layout-footer>
  </n-layout>
</n-dialog-provider>
</n-modal-provider>
</n-message-provider>
</template>

<script setup lang="ts">
import type { Component } from 'vue'
import { h, ref } from 'vue'
import { NIcon } from 'naive-ui'
import {
  BookOutline as BookIcon,
  PersonOutline as PersonIcon,
  WineOutline as WineIcon
} from '@vicons/ionicons5'
import { RouterLink } from 'vue-router'


function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const menuOptions = [
  {
    label:  () =>
      h(
        RouterLink,
        {
          to: {
            name: 'information'
          }
        },
        { default: () => '资讯管理' }
      ),
    key: 'Information',
    icon: renderIcon(BookIcon)
  },

  {
    label:  () =>
      h(
        RouterLink,
        {
          to: {
            name: 'user'
          }
        },
        { default: () => '用户管理' }
      ),
    key: 'User',
    icon: renderIcon(BookIcon)
  },

  {
    label: '舞，舞，舞',
    key: 'dance-dance-dance',
    icon: renderIcon(BookIcon),
    children: [
      {
        type: 'group',
        label: '人物',
        key: 'people',
        children: [
          {
            label: '叙事者',
            key: 'narrator',
            icon: renderIcon(PersonIcon)
          },
          {
            label: '羊男',
            key: 'sheep-man',
            icon: renderIcon(PersonIcon)
          }
        ]
      },
      {
        label: '饮品',
        key: 'beverage',
        icon: renderIcon(WineIcon),
        children: [
          {
            label: '威士忌',
            key: 'whisky'
          }
        ]
      },
      {
        label: '食物',
        key: 'food',
        children: [
          {
            label: '三明治',
            key: 'sandwich'
          }
        ]
      },
      {
        label: '过去增多，未来减少',
        key: 'the-past-increases-the-future-recedes'
      }
    ]
  }
]

const inverted = ref(false)
</script>


<style scoped>
.app-all {
  height: 100vh;
  width: 100vw;
}
.app-sider {
  height: calc(100vh - 50px);
}

.app-content {
  height: calc(100vh - 50px);
}

.app-footer {
  height: 50px;
}
</style>
