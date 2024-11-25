<template>
  <div class="content-box">
    <n-data-table :columns="columns" :data="data"  :pagination="10"/>
  </div>

  <n-modal v-model:show="showModal" class="modal-box" :trap-focus="false"   preset="dialog" >
    <Form v-if="showModal" :data="formData" :update="update"/>
  </n-modal>

</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { getAllInformation,createInformation,deleteInformation,searchInformation,updateInformation } from '@/request/api'
import { useMessage,NButton ,useDialog} from 'naive-ui'
import { h } from 'vue'
import type { informationI } from '@/interface'

import Form from '../form.vue'

const showModal = ref(false)
const dialog = useDialog()
const message = useMessage()

function getAllInformationFunc(){
  getAllInformation().then((res) => {
    data.value = res.data
  }).catch((err) => {
    console.log(err)
    message.error("获取失败")
  })
}

function createInformationFunc(data:informationI){

  createInformation(data).then((res) => {
    message.success('创建成功')
  }).catch((err) => {
    message.error('创建失败')
  })
}

function updateInformationFunc(id:number,data:informationI){
  updateInformation(id,data).then((res) => {
    message.success('更新成功')
  }).catch((err) => {
    message.error('更新失败')
  })
}

function deleteInformationFunc(id:number|undefined){
  if(!id){
    message.error('id不存在')
    return
  }


// deleteInformation(id)
dialog.error({
        title: '错误',
        content: '错了',
        positiveText: '啊',
        onPositiveClick: () => {
          message.success('我就知道')
        }
      })

}

const formData: informationI = reactive({
  id: 0,
  title: "",
  src_url: "",
  img_url: "",
  created_at: new Date()
})

function test(){
  showModal.value = true
}

function update(data:informationI){
  if (data.id==0){
    createInformationFunc(data)
  }else{
    if (!data.id){
      message.error('id不存在')
      return
    }
    updateInformationFunc(data.id,data)
  }
}
const data = ref([])

const columns = [
    {
      title: 'ID',
      key: 'id',
      align: 'center'
    },
    {
      title: '标题',
      key: 'title',
      align: 'center'
    },
    {
      title: '文章链接',
      key: 'src_url',
      align: 'center'
    },
    {
      title: '图片链接',
      key: 'img_url',
      align: 'center'
    },
    {
      title: '创建时间',
      key: 'created_at',
      align: 'center'
    },
    {
      title: '操作',
      key: 'actions',
      align: 'center',
      render(row:informationI) {
        return [
        h(
          NButton,

          {
            size: 'small',
            quaternary  : true,
            
            type:"primary",
            style: {
              marginRight: '5px'
            },
            onClick: () => test()
          },
          { default: () => '编辑' }
        ),
        h(
          NButton,
          {
            size: 'small',
            quaternary  : true,
            type:"error",
            onClick: () => deleteInformationFunc(row.id)
          },
          { default: () => '删除' }
        )
      ]
      }
    }
  ]




onMounted(() => {
  getAllInformationFunc()
})
</script>