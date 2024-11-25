<template>
  <n-data-table :columns="columns" :data="data" />
</template>

<script setup lang="ts">
import { ref } from 'vue'

function createColumns() {
  return [
    {
      title: 'Name',
      key: 'name'
    },
    {
      title: 'Age',
      key: 'age'
    },
    {
      title: 'Address',
      key: 'address'
    },
    {
      title: 'Tags',
      key: 'tags'
    },
    {
      title: 'Action',
      key: 'actions'
    }
  ]
}

const data = ref([])
const columns = createColumns()
</script>