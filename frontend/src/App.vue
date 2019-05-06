<template>
  <v-app>
    <v-toolbar app dark color="indigo lighten-1">
      <v-btn icon flat to="/">
        <v-icon>home</v-icon>
      </v-btn>
      <v-toolbar-title class="headline">
        Hot Tips
      </v-toolbar-title>
      <v-spacer></v-spacer>

      <v-spacer></v-spacer>
      <v-btn icon large>
        <v-avatar size="32px" tile>
          <v-icon>account_circle</v-icon>
        </v-avatar>
      </v-btn>
    </v-toolbar>

    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>
