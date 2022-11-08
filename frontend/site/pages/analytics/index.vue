<template  lang="pug">
v-container
  .top-authors
    h2 Top authors over citation
    v-row
      v-col
        v-text-field(v-model="chuck_size", label="Amount of top authors", single-line)
      v-col
        v-btn(@click="loadAuthors(chuck_size)" color='accent-4')
          | Find
    .author(v-for='(id, index) in authorIds' :key='id')
      v-row
        v-col
          p.text-h6.text--primary
            | {{ index + 1 }}. {{ id }}
  .all-coauthors-graph
    h2 Graph of co-authors
    v-row
      v-col(cols="2")
        v-btn(@click="openAllUsersGraph()" color='accent-4') Show
      v-col(cols="4")
        v-text-field(v-model="maximum_papers", label="Amount of max papers", single-line)
  .current-coauthors-graph
    h2 Graph of co-authors for {{ authorId }}
    v-btn(@click="openCurrentUsersGraph()" color='accent-4') Show
</template>

<script setup>
import {onMounted, ref} from "vue";
import {ConfigSetup} from "../../services/ConfigSetup";
import {LocalStorage} from "../../services/LocalStorage";

const localStorageService = new LocalStorage();
const authorId = ref("");
const maximum_papers = ref(100);
const serverUrl = ref("");
const authorIds = ref([]);
const chuck_size = ref("");

onMounted(async() => {
  localStorageService.pushToLoginIfNotAuthenticated();
  authorId.value = localStorageService.getUser()._id;
  const configSetup = new ConfigSetup();
  serverUrl.value = configSetup.getServerUrl();
  await loadAuthors();
});

const loadAuthors = async (chunk_size=10) => {
  authorIds.value = await $fetch(`${serverUrl.value}/database/author/get_top_authors?chunk_size=${chunk_size}`);
};

const openAllUsersGraph = () => {
  window.open(`${serverUrl.value}/database/paper/coauthors_graph?maximum_papers=${maximum_papers.value}`, '_blank').focus();
};

const openCurrentUsersGraph = () => {
  window.open(`${serverUrl.value}/database/author/coauthors_graph?author_id=${authorId.value}`, '_blank').focus();
};
</script>

<style scoped>
  .top-authors, .all-coauthors-graph {
    margin-bottom: 3rem;
  }
</style>