<template>
  <div class="card-container">
    <v-card class="mx-auto elevation-5 text-center pa-5 card"
    >
      <v-card-subtitle class="title black--text pa-1">
        Register
      </v-card-subtitle>
      <v-text-field color="black" label="Author ID" class="text-field" v-model="id"></v-text-field>
      <v-text-field color="black" label="Name" class="text-field" v-model="name"></v-text-field>
      <v-text-field color="black" label="Organization" class="text-field" v-model="org"></v-text-field>
      <v-text-field color="black" label="Gid" class="text-field" v-model="gid"></v-text-field>
      <v-text-field color="black" label="Oid" class="text-field" v-model="oid"></v-text-field>
      <v-text-field color="black" label="Organization ID" class="text-field" v-model="orgid"></v-text-field>
      <v-card-actions>
        <v-btn color="black" dark block rounded @click="register">
          Register
        </v-btn>
      </v-card-actions>
    </v-card>
    <div class="text-center register">
      <v-btn color="black" to="/login" nuxt>Login</v-btn>
    </div>
  </div>
</template>

<script>
import {Author} from "../../models/author";

export default {
  data() {
    return {
      id: '',
      name: '',
      org: '',
      gid: '',
      oid: '',
      orgid: ''
    }
  },
  methods: {
    async register() {
      const author = new Author(this._id, this.name, this.org, this.gid, this.oid, this.orgid)
      const config = useRuntimeConfig()
      const data = await $fetch(`${config.serverUrl}/database/author/create?author=${author}`,
          { method: 'POST'})
      console.log(data)
    }
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