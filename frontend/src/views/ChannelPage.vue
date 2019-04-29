<template>
  <v-container grid-list-xl>
    <v-layout align-center justify-center fill-height mt-5 v-if="loading">
      <v-progress-circular
        :size="50"
        color="primary"
        indeterminate
      ></v-progress-circular>
    </v-layout>

    <v-layout column v-else>
      <v-flex>
        <Channel :channel="channel" />
      </v-flex>

      <v-flex>
        <v-tabs color="grey lighten-3">
          <v-tab ripple>Tips</v-tab>
          <v-tab ripple>Distributors</v-tab>

          <v-tab-item>
            <TipList
              :channelId="channel.id"
              :tips="channel.tips"
              @change-tip="changeTip" />
          </v-tab-item>

          <v-tab-item>
            <DistributorList :distributors="channel.distributors" />
          </v-tab-item>
        </v-tabs>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Channel from '@/components/Channel.vue';
import TipList from '@/components/TipList.vue';
import DistributorList from '@/components/DistributorList.vue';
import { CHANNEL } from '@/graphql/queries';

@Component({
  apollo: {
    channel() {
      return {
        query: CHANNEL,
        variables: {
          id: this.$route.params.channelId,
        },
      };
    },
  },
  components: {
    Channel,
    TipList,
    DistributorList,
  },
})
export default class ChannelPage extends Vue {
  private channel!: any;
  private editTipDialog = true;

  get loading() {
    return this.$apollo.queries.channel.loading;
  }

  changeTip(tip: any) {
    let index = this.channel.tips.findIndex((t: any) => t.id === tip.id);
    if (index >= 0) {
      this.channel.tips[index] = tip;
    } else {
      this.channel.tips.unshift(tip);
    }
  }
}
</script>

<style></style>
