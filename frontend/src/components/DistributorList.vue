<template>
  <v-card flat class="pa-2">
    <DistributorForm v-model="editDialog"
      :channelId="channelId"
      :distributor="editingDistributor"
      @change-distributor="changeDistributor" />

    <v-btn>New</v-btn>

    <v-layout column>
      <template v-for="dist in distributors">
        <v-flex :key="dist.id">
          <v-card pa-2>
            <v-list dense>
              <v-list-tile>
                <v-list-tile-content class="item-label font-weight-light gray"
                  >Type</v-list-tile-content>
                <v-list-tile-content>{{ dist.type }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content class="item-label font-weight-light gray"
                  ># of Tips</v-list-tile-content>
                <v-list-tile-content>{{ dist.tipsCount }} 件づつ</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content class="item-label font-weight-light gray"
                  >schedule</v-list-tile-content>
                <v-list-tile-content>{{ scheduleText(dist) }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile v-for="(item, index) in dist.attribute" :key="index">
                <v-list-tile-content
                  class="item-label font-weight-light gray"
                  >{{ item.key }}</v-list-tile-content>
                <v-list-tile-content>{{ item.value }}</v-list-tile-content>
              </v-list-tile>
            </v-list>

            <v-card-actions>
              <v-btn flat small color="primary" @click="edit(dist)">EDIT</v-btn>
            </v-card-actions>

          </v-card>
        </v-flex>
      </template>
    </v-layout>
  </v-card>
</template>

<script lang="ts">
import { Component, Emit, Prop, Vue } from 'vue-property-decorator';
import { scheduleText } from '@/utils/ScheduleUtils';
import DistributorForm from '@/components/DistributorForm.vue';

@Component({
  components: {
    DistributorForm,
  },
})
export default class DistributorList extends Vue {
  @Prop() private distributors!: any[];
  @Prop() private channelId!: string;

  private editDialog = false;
  private editingDistributor = {};

  scheduleText(dist: any) {
    return scheduleText(dist.schedule);
  }

  add() {
    this.editDialog = true;
    this.editingDistributor = {};
  }

  edit(distributor: any) {
    this.editDialog = true;
    this.editingDistributor = distributor;
  }

  @Emit()
  changeDistributor(distributor: any) {
    return distributor;
  }
}
</script>

<style>
.item-label {
  max-width: 7em;
}
</style>
