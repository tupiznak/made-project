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
        v-row.mt-5(dense)
          v-col(cols=2)
            v-row
              v-col
                p Filters
            v-row.pt-5
              v-col
                v-btn(@click="findByFilters") find
          v-col
            v-row
              v-col(cols=1)
                p year
              v-col
                v-range-slider.align-center(
                  v-model="yearFilter",
                  :max="2030",
                  :min="1900",
                  :step="1",
                  thumb-label="always"
                )
            v-row
              v-col(cols=1)
                p venue
              v-col
                v-text-field(v-model="venueFilter")
            v-row
              v-col(cols=1)
                p author
              v-col
                v-text-field(v-model="authorFilter")

        v-row(dense)
          v-col(v-for="paper in filteredPapers", :key="paper", cols="12")
            v-card.mx-auto(variant="outlined")
              v-card-item
                div
                  v-container.pa-0(fluid)
                    v-row(dense)
                      v-col(cols=11)
                        .text-h6.mb-1
                          | {{ paper.title }}
                      v-col
                        .text-overline.mb-1 {{ paper.year }}
                  .text-caption {{ paper.abstract }}
                  v-row.pt-2
                    v-col(cols=1)
                      p paper id:
                    v-col
                      v-chip {{ paper._id }}
                  v-row.pt-2
                    v-col(cols=1)
                      p venue id:
                    v-col
                      v-chip(@click="venueFilter = paper.venue") {{ paper.venue }}
                  v-row.pt-2
                    v-col(cols=1)
                      p authors:
                    v-col(v-if="paper.authors != null")
                      v-chip(
                        v-for="author in paper.authors",
                        :key="author",
                        @click="authorFilter = author"
                      ) {{ author }}
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
import { ref, onMounted } from "vue";
const search = ref("");
const config = useRuntimeConfig();
const filteredPapers = ref([]);
const yearFilter = ref([1900, 2020]);
const authorFilter = ref("");
const venueFilter = ref("");
const router = useRouter();

onMounted(() => {
  if (process.client) {
    if (!localStorage.getItem('isAuthenticated')) {
      router.push({ path: "/login" });
    }
  }

  if (config.serverUrl.indexOf("vercel") !== -1) {
    const currURL = document.URL;
    const pathArray = currURL.split("/");
    const gitPath = pathArray[2].slice(8);
    config.serverUrl = `${pathArray[0]}//made22t4-back${gitPath}`;
  }
});

const paperAmount = async () => {
  const data = await $fetch(`${config.serverUrl}/database/paper/total_size`);
  paperCount.value = data;
};

const find = async () => {
  const data = await $fetch(
    `${config.serverUrl}/database/paper/abstract_substring?sub_string=${search.value}&chunk_size=10`,
    { method: "POST" }
  );
  filteredPapers.value = data;
};
const findByFilters = async () => {
  const data = await $fetch(
    `${config.serverUrl}/database/paper/filter?author=${authorFilter.value}&venue=${venueFilter.value}&year_start=${yearFilter.value[0]}&year_end=${yearFilter.value[1]}&chunk_size=10`,
    { method: "POST" }
  );
  filteredPapers.value = data;
  console.log(data);
};
</script>