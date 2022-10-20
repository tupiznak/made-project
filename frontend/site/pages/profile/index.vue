<template>
  <v-container>
    <v-row>
      <v-col>
        <h3>{{ user?.name }}</h3>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        AuthorID: {{ user?._id }}
      </v-col>
      <v-col>
        Organization: {{ user?.org }}
      </v-col>
      <v-col>
        OrganizationID: {{ user?.orgid }}
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        GID: {{ user?.gid }}
      </v-col>
      <v-col>
        OID: {{ user?.oid }}
      </v-col>
    </v-row>
    <v-spacer></v-spacer>
    <v-row>
      <v-btn @click="logout">Logout</v-btn>
    </v-row>
  </v-container>
</template>

<script>
import {LocalStorage} from "../../services/LocalStorage";

export default {
  setup() {
    const localStorageService = new LocalStorage()
    return {
      localStorageService
    }
  },
  beforeCreate() {
    this.localStorageService.pushToLoginIfNotAuthenticated()
  },
  mounted() {
    this.user = this.localStorageService.getUser()
  },
  data () {
    return {
      user: null
    }
  },
  methods: {
    logout() {
      this.localStorageService.removeUser()
      this.localStorageService.removeIsAuthenticated()
      this.localStorageService.raiseLocalstorageChangedEvent()
      this.localStorageService.pushToLoginIfNotAuthenticated()
    }
  }
}
</script>

<style scoped>

</style>