<template>
  <v-card flat class="pa-2">
    <DistributorForm v-model="editDialog"
      :channelId="channelId"
      :distributor="editingDistributor"
      :type="edittingType"
      @change-distributor="changeDistributor" />

    <v-btn primary @click="add(DistributorType.SLACK)">New</v-btn>

    <v-layout column v-if="distributors.length">
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
              <v-spacer/>
              <v-btn flat small @click="doDelete(dist)">DELETE</v-btn>
            </v-card-actions>

          </v-card>
        </v-flex>
      </template>
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
import { Component, Emit, Prop, Vue } from 'vue-property-decorator';
import { scheduleText } from '@/utils/ScheduleUtils';
import DistributorForm from '@/components/DistributorForm.vue';
import { Distributor } from '@/types/models';
import { DistributorType } from '../../types/globalTypes';
import { DELETE_DISTRIBUTOR } from '@/graphql/queries';
import { deleteDistributor } from '@/graphql/types/deleteDistributor'

@Component({
  components: {
    DistributorForm,
  },
})
export default class DistributorList extends Vue {
  readonly DistributorType = DistributorType;

  @Prop() private distributors!: Distributor[];
  @Prop() private channelId!: string;

  private editDialog = false;
  private editingDistributor: Distributor | null = null;
  private edittingType: DistributorType = DistributorType.SLACK;

  scheduleText(dist: Distributor) {
    return scheduleText(dist.schedule);
  }

  add(type: DistributorType) {
    this.editDialog = true;
    this.editingDistributor = null;
    this.edittingType = type;
  }

  edit(distributor: Distributor) {
    this.editDialog = true;
    this.editingDistributor = distributor;
    this.edittingType = distributor.type;
  }

  async doDelete(distributor: Distributor) {
    if(await this.$root.$confirm("Delete", "Delete this dist")) {
      let mutation = this.$apollo
        .mutate<deleteDistributor>({
          mutation: DELETE_DISTRIBUTOR,
          variables: {
            id: distributor.id
          },
          fetchPolicy: "no-cache"
        })
        .then(({ data: { deleteDistributor }}) => {
          if (!deleteDistributor) { throw "result is null"; }
          if (deleteDistributor.ok) {
            this.deleteDistributor(distributor);
          }
        })
        .catch(error => {
          console.error(error);
        });
    }
  }

  @Emit()
  changeDistributor(distributor: Distributor) {
    return distributor;
  }

  @Emit()
  deleteDistributor(distributor: Distributor) {
    return distributor;
  }
}
</script>

<style>
.item-label {
  max-width: 7em;
}
</style>
