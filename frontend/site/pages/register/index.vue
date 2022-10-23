<template lang="pug">
  .card-container
    v-card.mx-auto.elevation-5.text-center.pa-5.card
      v-card-subtitle.title.black--text.pa-1 Register
      v-text-field.text-field(color='black' label='Author ID' v-model='author._id')
      v-text-field.text-field(color='black' label='Name' v-model='author.name')
      v-text-field.text-field(color='black' label='Organization' v-model='author.org')
      v-text-field.text-field(color='black' label='Gid' v-model='author.gid')
      v-text-field.text-field(color='black' label='Oid' v-model='author.oid')
      v-text-field.text-field(color='black' label='Organization ID' v-model='author.orgid')
      v-card-actions
        v-btn(color='black' dark='' block='' rounded='' @click='register') Register
    .text-center.register
      v-btn(color='black' to='/login' nuxt='') Login
</template>

<script>
import {Author} from "../../models/author";
import {ConfigSetup} from "../../services/ConfigSetup";
import {LocalStorage} from "../../services/LocalStorage";

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
      author: new Author('', '', '', '', '', ''),
      config: null
    }
  },
  methods: {
    async register() {
      try {
        const data = await $fetch(`${this.config.serverUrl}/database/author/create`, {
          headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json',
          },
          method: 'POST',
          body: JSON.stringify(this.author)
        })

        this.localStorageService.setUser(data)
        this.localStorageService.setIsAuthenticated(true)
        this.localStorageService.raiseLocalstorageChangedEvent()
        this.router.push({ path: "/" });
      } catch (e) {
        console.error(e);
      }
    },
  }
}
</script>

<style scoped>

.card-container {
  max-height: 100vh;
  margin: 3vh;
}

.card {
  border-radius: 20px;
  max-width: 450px;
}

.text-field {
  margin: 0.5vh 2vh;
}

.register {
  margin-top: 2vh;
}
</style>