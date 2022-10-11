<template lang="pug">
v-card
  v-layout
    v-app-bar
      template(v-slot:prepend)
        v-app-bar-nav-icon
      v-app-bar-title Dashboard
      v-text-field(v-model="search", label="Search Abstract", single-line)
      v-btn(icon, @click="find")
        v-icon mdi-magnify
      v-btn(icon)
        v-icon mdi-dots-vertical
    v-main
      v-container(fluid)
        v-row(dense)
          v-col(v-for="n in filteredPapers", :key="n", cols="12")
            v-card.mx-auto(variant="outlined")
              v-card-item
                div
                  v-container.pa-0(fluid)
                    v-row(dense)
                      v-col(cols=11)
                        .text-h6.mb-1
                          | {{ n.title }}
                      v-col
                        .text-overline.mb-1 {{ n.year }}
                  .text-caption {{ n.abstract }}
              v-card-actions
                v-btn(variant="outlined")
                  | details
                v-spacer
                v-btn(
                  size="small",
                  color="surface-variant",
                  variant="text",
                  icon="mdi-heart"
                )
</template>


<script setup>
import { ref } from "vue";
const search = ref("");
const config = useRuntimeConfig();
const filteredPapers = ref([]);

const paperAmount = async () => {
  const data = await $fetch(`${config.serverUrl}/database/paper/total_size`);
  paperCount.value = data;
};

const find = async () => {
  if (config.serverUrl.indexOf("vercel") !== -1) {
    const currURL = document.URL
    const pathArray = currURL.split("/");
    const gitPath = pathArray[2].slice(8)
    config.serverUrl = `${pathArray[0]}//made22t4-back${gitPath}`;
  }
  const data = await $fetch(
    `${config.serverUrl}/database/paper/abstract_substring?sub_string=${search.value}&chunk_size=10`,
    { method: "POST" }
  );
  filteredPapers.value = data;
  console.log(data);
};
// watch(search, async (search) => {
//   console.log(search);
//   const data = await $fetch(
//     `${config.serverUrl}/database/paper/abstract_substring?sub_string=${search}&chunk_size=10`,
//     { method: "POST" }
//   );
//   console.log(data);
// });
</script>