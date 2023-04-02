<template>
  <v-app>
    <v-app-bar
      app
      color= #FA8072
      dark
    >
      <div class="d-flex align-center">
        <router-link to="/" class="mr-5" style="color:white">
          <h1 >CV Score</h1>
        </router-link>
      </div>
      <div class="d-flex align-center">
        <router-link to="/" class="mr-5" style="color:white">
          <span class="mr-2">Sélection annonce</span>
          <v-icon>mdi-cursor-default-click</v-icon>
        </router-link>

      <v-spacer></v-spacer>

      <router-link to="/new" class="mr-5" style="color:white">
        <span class="mr-2" >Nouvelle annonce</span>
        <v-icon>mdi-new-box</v-icon>
      </router-link>
      </div>
    </v-app-bar>

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    //
  }),
};
</script>
