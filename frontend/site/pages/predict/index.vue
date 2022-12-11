<template  lang="pug">
v-container
  .top-authors
    h2 Prediction
    v-row
      v-col
        v-text-field(v-model="title", label="title", single-line)
    v-row
      v-col
        v-textarea(v-model="abstract", label="abstract", single-line)
    v-row
      v-col
        v-btn(@click="predictByTitle", color="accent-4") Predict by paper
      v-col
        v-btn(@click="predictByAuthor", color="accent-4") Predict by author
    v-row
      v-col
        h2 Recomended coauthors:
    v-row(v-for="author in predictedAuthors", :key="author")
      v-col
        v-chip {{ author }}
</template>

<script setup>
import { onMounted, ref } from "vue";
import { ConfigSetup } from "../../services/ConfigSetup";
import { LocalStorage } from "../../services/LocalStorage";

const localStorageService = new LocalStorage();
const authorId = ref("");
const serverUrl = ref("");
const title = ref("");
const abstract = ref("");
const predictedAuthors = ref(["diwujwd", "kdwenmdkw"]);

onMounted(async () => {
  localStorageService.pushToLoginIfNotAuthenticated();
  authorId.value = localStorageService.getUser()._id;
  const configSetup = new ConfigSetup();
  serverUrl.value = configSetup.getServerUrl();
});

const predictByAuthor = async () => {
  predictedAuthors.value = await $fetch(
    `${serverUrl.value}/model/predict_by_author?coauthors_count=10&_id=${authorId.value}`,
    { method: "POST" }
  );
};
const predictByTitle = async () => {
  predictedAuthors.value = await $fetch(
    `${serverUrl.value}/model/predict_by_paper?coauthors_count=10&title=${title.value}`,
    { method: "POST" }
  );
};
</script>

<style scoped>
.top-authors,
.all-coauthors-graph {
  margin-bottom: 3rem;
}
</style>