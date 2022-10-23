<template lang="pug">
  .card-container
    v-card.mx-auto.elevation-5.text-center.pa-5.card
      v-card-subtitle.title.black--text.pa-1 Sign in
      v-text-field.author-id(color='black' label='AuthorId' v-model='authorId')
      v-card-actions
        v-btn(color='black' dark='' block='' rounded='' @click='login') Sign in
    .text-center.register
      v-btn(color='black' to='/register' nuxt='') Register
</template>

<script>
import { ConfigSetup } from "../../services/ConfigSetup";
import { LocalStorage } from "../../services/LocalStorage";

export default {
  setup() {
    const localStorageService = new LocalStorage()
    const router = useRouter();

    return {
      localStorageService,
      router
    }
  },
  mounted() {
    const configSetup = new ConfigSetup()
    this.config = configSetup.setup()
  },
  data() {
    return {
      authorId: '',
      config: null
    }
  },
  methods: {
    async login() {
      try {
        const data = await $fetch(
            `${this.config.serverUrl}/database/author/read?_id=${this.authorId}`,
            { method: "POST" })

        this.localStorageService.setUser(data)
        this.localStorageService.setIsAuthenticated(true)
        this.localStorageService.raiseLocalstorageChangedEvent()
        this.router.push({ path: "/" });
      } catch (e) {
        console.error(e);
      }
    }
  }
}
</script>

<style scoped>

.card-container {
  max-height: 100vh;
  margin: 20vh;
}

.card {
  border-radius: 20px;
  max-width: 450px;
}

.author-id {
  margin: 5vh 2vh;
}

.register {
  margin-top: 2vh;
}
</style>