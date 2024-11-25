<template>

<n-form
    ref="formRef"
    :model="data"
    label-placement="left"
    label-width="auto"
    require-mark-placement="right-hanging"
>
    <n-form-item label="Input" path="inputValue">
        <n-input v-model:value="data.inputValue" placeholder="Input" />
    </n-form-item>

    <div style="display: flex; justify-content: flex-end">
    <n-button round type="primary" @click="onSubmit">
        验证
    </n-button>
    </div>
</n-form>


</template>
<script setup lang="ts">
import { ref,defineProps } from 'vue'
import type { FormInst, FormItemRule } from 'naive-ui'
import { useMessage } from 'naive-ui'

const prop = defineProps(['data','update'])
const formRef = ref<FormInst | null>(null)
const message = useMessage()


function onSubmit(e: MouseEvent) {
    e.preventDefault()
    formRef.value?.validate((errors) => {
        if (!errors) {
            prop.update(prop.data.value)
        } else {
            message.error('验证失败')
        }
    })
}

</script>