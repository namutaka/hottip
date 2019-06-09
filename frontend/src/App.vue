<template>
  <v-app>
    <v-toolbar app dark color="indigo lighten-1">
      <v-btn icon flat to="/">
        <v-icon>home</v-icon>
      </v-btn>
      <v-toolbar-title class="headline">
        HOT TIP
      </v-toolbar-title>
      <v-spacer></v-spacer>

      <v-spacer></v-spacer>

      <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn icon large v-on="on">
            <v-avatar size="32px" tile>
              <v-icon>more_vert</v-icon>
            </v-avatar>
          </v-btn>
        </template>

        <v-list>
          <v-list-tile avatar v-if="user">
            <v-list-tile-avatar>
              <v-icon size="40px">account_circle</v-icon>
            </v-list-tile-avatar>
            <v-list-tile-content>
              <v-list-tile-title>{{ user.username }}</v-list-tile-title>
              <v-list-tile-sub-title>{{ user.email }}</v-list-tile-sub-title>
            </v-list-tile-content>
          </v-list-tile>

          <v-divider class="my-2" />

          <v-list-tile avatar :to="{ name: 'logout' }">
            <v-list-tile-avatar />
            <v-list-tile-content>
              <v-list-tile-title>Logout</v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list>
      </v-menu>
    </v-toolbar>

    <v-content>
      <router-view />
    </v-content>
  </v-app>
</template>

<script lang="ts">
import { Component, Prop, Emit, Vue } from 'vue-property-decorator';
import { user, user_user } from '@/graphql/types/user';
import { USER } from '@/graphql/queries';

@Component({
  apollo: {
    user: {
      query: USER,
    },
  },
})
export default class App extends Vue {
  private user: user_user = {
    id: '',
    username: '',
    email: '',
  };
}
</script>
