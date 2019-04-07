<template>
  <v-card flat class="pa-2">
    <v-btn>New</v-btn>

    <v-layout column>
      <template v-for="dist in distributors">
        <v-flex :key="dist.id">
          <v-card pa-2>
            <v-flex absolute right>
              <v-btn flat small icon>
                <v-icon small color="grey lighten-1">edit</v-icon>
              </v-btn>
            </v-flex>

            <v-list dense>
              <v-list-tile>
                <v-list-tile-content class="item-label font-weight-light gray"
                  >Type</v-list-tile-content
                >
                <v-list-tile-content>{{ dist.type }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content class="item-label font-weight-light gray"
                  ># of Tips</v-list-tile-content
                >
                <v-list-tile-content>{{ dist.tipsCount }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content class="item-label font-weight-light gray"
                  >schedule</v-list-tile-content
                >
                <v-list-tile-content>{{ dist.schedule }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile v-for="(item, index) in dist.attribute" :key="index">
                <v-list-tile-content
                  class="item-label font-weight-light gray"
                  >{{ item.key }}</v-list-tile-content
                >
                <v-list-tile-content>{{ item.value }}</v-list-tile-content>
              </v-list-tile>
            </v-list>
          </v-card>
        </v-flex>
      </template>
    </v-layout>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component({})
export default class DistributorList extends Vue {
  @Prop() private distributors!: any[];
}
</script>

<style>
.item-label {
  max-width: 7em;
}
</style>
