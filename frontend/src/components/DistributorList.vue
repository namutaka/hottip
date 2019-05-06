<template>
  <v-card flat class="pa-2">
    <DistributorForm
      ref="distributorForm"
      @change-distributor="changeDistributor"
    />

    <v-btn @click="add(DistributorType.SLACK)">
      配信設定作成
    </v-btn>

    <v-layout column v-if="distributors.length">
      <template v-for="dist in distributors">
        <v-flex :key="dist.id">
          <v-card pa-2>
            <v-list dense>
              <v-list-tile>
                <v-list-tile-content
                  class="item-label font-weight-light grey--text text--darken-2"
                >
                  配信方法
                </v-list-tile-content>
                <v-list-tile-content>{{ dist.type }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content
                  class="item-label font-weight-light grey--text text--darken-2"
                >
                  一度に送信するTips数
                </v-list-tile-content>
                <v-list-tile-content
                  >{{ dist.tipsCount }} 件づつ</v-list-tile-content
                >
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content
                  class="item-label font-weight-light grey--text text--darken-2"
                >
                  配信タイミング
                </v-list-tile-content>
                <v-list-tile-content>{{
                  scheduleText(dist)
                }}</v-list-tile-content>
              </v-list-tile>
              <v-list-tile v-for="item in dist.attribute" :key="item.key">
                <v-list-tile-content
                  class="item-label font-weight-light grey--text text--darken-2"
                >
                  {{ fieldLabel(dist.type, item.key) }}
                </v-list-tile-content>
                <v-list-tile-content>{{ item.value }}</v-list-tile-content>
              </v-list-tile>
            </v-list>

            <v-card-actions>
              <v-btn flat small color="primary" @click="edit(dist)">EDIT</v-btn>
              <v-spacer />
              <v-btn flat small color="grey" @click="doDelete(dist)"
                >DELETE</v-btn
              >
            </v-card-actions>
          </v-card>
        </v-flex>
      </template>
    </v-layout>

    <v-layout column v-else>
      <v-flex>
        <v-card pa-2 class="elevation-0">
          <v-card-text>
            配信設定を作成してください
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
import { deleteDistributor } from '@/graphql/types/deleteDistributor';
import { ATTRIBUTE_FIELDS } from '@/utils/AttributeUtils';

@Component({
  components: {
    DistributorForm,
  },
})
export default class DistributorList extends Vue {
  $refs!: {
    distributorForm: DistributorForm;
  };

  readonly DistributorType = DistributorType;

  @Prop() private distributors!: Distributor[];
  @Prop() private channelId!: string;

  scheduleText(dist: Distributor) {
    return scheduleText(dist.schedule);
  }

  add(type: DistributorType) {
    this.$refs.distributorForm.open(this.channelId, type);
  }

  edit(distributor: Distributor) {
    this.$refs.distributorForm.open(
      this.channelId,
      distributor.type,
      distributor,
    );
  }

  fieldLabel(type: keyof typeof ATTRIBUTE_FIELDS, key: string) {
    const field = ATTRIBUTE_FIELDS[type].find(v => v.key === key);
    if (field) {
      return field.label;
    } else {
      return key;
    }
  }

  async doDelete(distributor: Distributor) {
    if (
      await this.$root.$confirm(
        '配信設定削除',
        `配信設定 "${distributor.type}" を削除します`,
      )
    ) {
      let mutation = this.$apollo
        .mutate<deleteDistributor>({
          mutation: DELETE_DISTRIBUTOR,
          variables: {
            id: distributor.id,
          },
          fetchPolicy: 'no-cache',
        })
        .then(({ data: { deleteDistributor } }) => {
          if (!deleteDistributor) {
            throw 'result is null';
          }
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
  max-width: 12em;
}
</style>
