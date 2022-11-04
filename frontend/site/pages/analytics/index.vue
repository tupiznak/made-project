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
    .author(v-for='(id, index) in authorIds' :key='id._id')
      v-row
        v-col
          p.text-h6.text--primary
            | {{ index + 1 }}. {{ id._id }}
  .all-coauthors-graph
    h2 Graph of co-authors
    div
      .graph(slot='graph_html' slot-scope='{graph_html}' v-html='graph_html')
  .current-coauthors-graph
    h2 Graph of co-authors for {{ authorId }}
    div
      .graph(slot='graph_html' slot-scope='{graph_html}' v-html='graph_html')
</template>

<script setup>
import {onMounted, ref} from "vue";
import {ConfigSetup} from "../../services/ConfigSetup";
import {LocalStorage} from "../../services/LocalStorage";

const localStorageService = new LocalStorage();
const authorId= ref("");
const serverUrl = ref("");
const authorIds = ref([]);
const chuck_size = ref("");
const graph_html = ref("");

onMounted(async() => {
  localStorageService.pushToLoginIfNotAuthenticated();
  authorId.value = localStorageService.getUser()._id;
  const configSetup = new ConfigSetup();
  serverUrl.value = configSetup.getServerUrl();
  await loadAuthors();
  await loadAllUsersGraph();
  await loadCurrentUserGraph();
});

const loadAuthors = async (chunk_size=10) => {
  authorIds.value = await $fetch(`${serverUrl.value}/database/author?chunk_size=${chunk_size}`);
};

const loadAllUsersGraph = async () => {
  graph_html.value = await $fetch(`${serverUrl.value}/test`, {
    headers: {
      'accept': 'text/html',
      'Content-Type': 'text/html',
    },
  });
};

const loadCurrentUserGraph = async () => {
  graph_html.value = await $fetch(`${serverUrl.value}/test`, {
    headers: {
      'accept': 'text/html',
      'Content-Type': 'text/html',
    },
  });
};
</script>

<style scoped>
  .top-authors, .all-coauthors-graph {
    margin-bottom: 5rem;
  }
  .graph {
    max-width: 100vw;
  }
</style>