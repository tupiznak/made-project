<template lang="pug">
v-container
  v-row
    v-col
      v-btn(@click="sendToDB") count
  v-row
    v-col
      v-chip {{count}}

</template>

<script setup>
import { ref } from "vue";
const count = ref("---")
const config = useRuntimeConfig()

const sendToDB = async () => {
    console.log(config.serverUrl)
    await $fetch(`${config.serverUrl}/db/create`)
    const data = await $fetch(`${config.serverUrl}/db/read`)
    count.value = data.message
}

</script>