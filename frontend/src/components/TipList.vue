<template>
  <v-card flat class="pa-2">
    <TipForm ref="tipForm" @change-tip="changeTip" />

    <v-btn @click="add">Tips作成</v-btn>

    <v-layout column v-if="tips.length">
      <v-flex v-for="tip in tips" :key="tip.id">
        <v-card>
          <v-flex absolute right>
            <v-chip v-if="tip.enable" small label color="green" dark>ON</v-chip>
            <v-chip v-else small label color="indigo" dark>OFF</v-chip>
          </v-flex>

          <v-card-text class="pt-4 px-4">
            <h4>{{ tip.title }}</h4>
            <div>
              <pre>{{ tip.text }}</pre>
            </div>
          </v-card-text>

          <v-card-actions>
            <v-btn flat small color="primary" @click="edit(tip)">EDIT</v-btn>
            <v-spacer />
            <v-btn flat small color="grey" @click="doDelete(tip)">DELETE</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>

    <v-layout column v-else>
      <v-flex>
        <v-card pa-2 class="elevation-0">
          <v-card-text>
            Tipsを作成してください
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Emit, Vue } from 'vue-property-decorator';
import TipForm from '@/components/TipForm.vue';
import { Tip } from '@/types/models';
import { DELETE_TIP } from '@/graphql/queries';
import { deleteTip } from '@/graphql/types/deleteTip';

@Component({
  components: {
    TipForm,
  },
})
export default class TipList extends Vue {
  $refs!: {
    tipForm: TipForm;
  };

  @Prop() private tips!: Tip[];
  @Prop() private channelId!: string;

  add() {
    this.$refs.tipForm.open(this.channelId);
  }

  edit(tip: Tip) {
    this.$refs.tipForm.open(this.channelId, tip);
  }

  async doDelete(tip: Tip) {
    if (
      await this.$root.$confirm(
        'Tips削除',
        `Tips "${tip.title}" を削除します`)
    ) {
      let mutation = this.$apollo
        .mutate<deleteTip>({
          mutation: DELETE_TIP,
          variables: {
            id: tip.id,
          },
          fetchPolicy: 'no-cache',
        })
        .then(({ data: { deleteTip } }) => {
          if (!deleteTip) {
            throw 'result is null';
          }
          if (deleteTip.ok) {
            this.deleteTip(tip);
          }
        })
        .catch(error => {
          console.error(error);
        });
    }
  }

  @Emit()
  changeTip(tip: Tip) {
    return tip;
  }

  @Emit()
  deleteTip(tip: Tip) {
    return tip;
  }
}
</script>

<style></style>
