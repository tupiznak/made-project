<template lang="pug">
v-container
  v-row
    v-col
      h3 {{ user?.name }}
  v-row
    v-col AuthorID: {{ user?._id }}
    v-col Organization: {{ user?.org }}
    v-col OrganizationID: {{ user?.orgid }}
  v-row
    v-col GID: {{ user?.gid }}
    v-col OID: {{ user?.oid }}
  v-spacer
  v-row
    v-btn(@click='logout') Logout
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