<template lang="pug">
v-container
  v-row
    v-col
      v-btn(@click="paperAmount") paper amount
    v-col
      v-btn(@click="authorAmount") author amount
    v-col
      v-btn(@click="venueAmount") venue amount
  v-row
    v-col
      v-chip {{paperCount}}
    v-col
      v-chip {{authorCount}}
    v-col
      v-chip {{venueCount}}

</template>

<script setup>
import { onMounted, ref } from "vue";
import {ConfigSetup} from "../services/ConfigSetup";
import {LocalStorage} from "../services/LocalStorage";
const paperCount = ref("---");
const authorCount = ref("---");
const venueCount = ref("---");
const localStorageService = new LocalStorage();
const serverUrl = ref("");

onMounted(() => {
  localStorageService.pushToLoginIfNotAuthenticated();
  const configSetup = new ConfigSetup();
  serverUrl.value = configSetup.getServerUrl();
});

const paperAmount = async () => {
    const data = await $fetch(`${serverUrl.value}/database/paper/total_size`)
    paperCount.value = data
};
const authorAmount = async () => {
    const data = await $fetch(`${serverUrl.value}/database/author/total_size`)
    authorCount.value = data
};
const venueAmount = async () => {
    const data = await $fetch(`${serverUrl.value}/database/venue/total_size`)
    venueCount.value = data
};

</script>