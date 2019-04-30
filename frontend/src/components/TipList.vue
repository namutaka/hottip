<template>
  <v-card flat class="pa-2">
    <TipForm v-model="editDialog"
      :channelId="channelId"
      :tip="editingTip"
      @change-tip="changeTip" />

    <v-btn color="primary" @click="add">New Tip</v-btn>

    <v-layout column v-if="tips.length">
      <v-flex v-for="tip in tips" :key="tip.id">
        <v-card>
          <v-flex absolute right>
            <v-chip v-if="tip.enable" small label color="green" dark>ON</v-chip>
            <v-chip v-else small label color="indigo" dark>OFF</v-chip>

          </v-flex>

          <v-card-text class="pt-4 px-4">
            <h4>{{ tip.title }}</h4>
            <div><pre>{{ tip.text }}</pre></div>
          </v-card-text>

          <v-card-actions>
            <v-btn flat small color="primary" @click="edit(tip)">EDIT</v-btn>
          </v-card-actions>
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
import { Component, Prop, Emit, Vue } from 'vue-property-decorator';
import TipForm from '@/components/TipForm.vue';
import { Tip } from '@/types/models';

@Component({
  components: {
    TipForm,
  },
})
export default class TipList extends Vue {
  @Prop() private tips!: Tip[];
  @Prop() private channelId!: string;

  private editDialog = false;
  private editingTip: Tip | null = null;

  add() {
    this.editDialog = true;
    this.editingTip = null;
  }

  edit(tip: Tip) {
    this.editDialog = true;
    this.editingTip = tip;
  }

  @Emit()
  changeTip(tip: Tip) {
    return tip;
  }
}
</script>

<style></style>
