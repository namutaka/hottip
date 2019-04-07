<template>
  <v-card>
    <v-flex absolute right>
      <v-btn flat small icon>
        <v-icon small color="grey lighten-1">edit</v-icon>
      </v-btn>
    </v-flex>

    <v-card-text>
      <h4 class="font-weight-medium">{{channel.name}}</h4>
      <p>{{channel.description}}</p>
    </v-card-text>
    <v-divider class="mx-3" />
    <v-card-actions class="font-weight-light mx-3 px-0 py-2">
      #{{channel.rawId}}
      <v-divider vertical class="mx-2" />
      <span>
        <v-icon small class="mx-1">create</v-icon>
        {{channel.createdAt | datetime}}
      </span>
      <span class="mx-1">
        <v-icon small class="mx-1">update</v-icon>
        {{channel.updatedAt | datetime}}
      </span>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({})
export default class Channel extends Vue {
    @Prop() private channel!: any
}
</script>

<style></style>
