<script setup lang="ts">
import { post } from '@/utils/request'

async function debug() {
  const response = await post('/apps/8d62b2ef-391b-46d0-b851-e3e4165402e7/debug', {
    body: { query: '你好，你是谁' },
  })
  console.log(response)
}
</script>

<template>
  <a-button @click="debug">发起请求</a-button>
</template>

<style scoped></style>
