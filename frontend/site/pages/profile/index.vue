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
export default {
  setup() {
    const router = useRouter()
    return {
      router
    }
  },
  beforeCreate() {
    if (process.client) {
      if (!localStorage.getItem('isAuthenticated')) {
        this.router.push({ path: "/login" });
      }
      else {
        this.user = JSON.parse(localStorage.getItem('user'))
      }
    }
  },
  data () {
    return {
      user: null
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('isAuthenticated')
      localStorage.removeItem('user')

      window.dispatchEvent(new CustomEvent('user-localstorage-changed', {
        detail: {
          isAuth: false,
          user: null
        }
      }));

      this.router.push({ path: "/login" });
    }
  }
}
</script>

<style scoped>

</style>