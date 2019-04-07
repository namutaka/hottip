<template>
  <v-card flat class="pa-2">
    <v-btn>New Tip</v-btn>

    <v-layout column v-if="tips.length">
      <v-flex v-for="tip in tips" :key="tip.id">
        <v-card pa-2>
          <v-flex absolute right>
            <v-chip v-if="tip.enable" small label color="green" dark>ON</v-chip>
            <v-chip v-else small label color="indigo" dark>OFF</v-chip>

            <v-btn flat small icon>
              <v-icon small color="grey lighten-1">edit</v-icon>
            </v-btn>
          </v-flex>

          <v-card-text>
            <h4>{{ tip.title }}</h4>
            <div>{{ tip.text }}</div>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>

    <v-layout column v-else>
      <v-flex>
        <v-card pa-2>
          <v-card-text>
            no-data
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({})
export default class TipList extends Vue {
  @Prop() private tips!: any[];
}
</script>

<style></style>
