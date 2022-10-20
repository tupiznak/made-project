<template>
  <div class="card-container">
    <v-card class="mx-auto elevation-5 text-center pa-5 card"
    >
      <v-card-subtitle class="title black--text pa-1">
        Sign in
      </v-card-subtitle>
      <v-text-field color="black" label="AuthorId" class="author-id" v-model="authorId"></v-text-field>
      <v-card-actions>
        <v-btn color="black" dark block rounded @click="login">
          Sign in
        </v-btn>
      </v-card-actions>
    </v-card>
    <div class="text-center register">
      <v-btn color="black" to="/register" nuxt>Register</v-btn>
    </div>
  </div>
</template>

<script>
import { ConfigSetup } from "../../services/ConfigSetup";

export default {
  setup() {
    const configSetup = new ConfigSetup()
    const config = configSetup.setup()
    const router = useRouter();

    return {
      config,
      router
    }
  },
  data() {
    return {
      authorId: '',
    }
  },
  methods: {
    async login() {
      try {
        const data = await $fetch(
            `${this.config.serverUrl}/database/author/read?_id=${this.authorId}`,
            { method: "POST" })

        if (process.client) {
          localStorage.setItem('isAuthenticated', true)
          localStorage.setItem('user', JSON.stringify(data))

          window.dispatchEvent(new CustomEvent('user-localstorage-changed', {
            detail: {
              isAuth: localStorage.getItem('isAuthenticated'),
              user: localStorage.getItem('user')
            }
          }));
        }

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

.link {

}
</style>