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
              @change-tip="changeTip"
              @delete-tip="deleteTip"
              />
          </v-tab-item>

          <v-tab-item>
            <DistributorList
              :channelId="channel.id"
              :distributors="channel.distributors"
              @change-distributor="changeDistributor"
              @delete-distributor="deleteDistributor"
              />
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
import { channel_channel } from '@/graphql/types/channel'
import { Tip, Distributor } from '@/types/models'

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
  private channel!: channel_channel;

  get loading() {
    return this.$apollo.queries.channel.loading;
  }

  changeTip(tip: Tip) {
    let index = this.channel.tips.findIndex((t: Tip) => t.id === tip.id);
    if (index >= 0) {
      this.channel.tips[index] = tip;
    } else {
      this.channel.tips.unshift(tip);
    }
  }

  deleteTip(tip: Tip) {
    let index = this.channel.tips.findIndex((t: Tip) => t.id === tip.id);
    this.channel.tips.splice(index, 1);
  }

  changeDistributor(distributor: Distributor) {
    let index = this.channel.distributors.findIndex((d: Distributor) => d.id === distributor.id);
    if (index >= 0) {
      this.channel.distributors[index] = distributor;
    } else {
      this.channel.distributors.unshift(distributor);
    }
  }

  deleteDistributor(distributor: Distributor) {
    let index = this.channel.distributors.findIndex((d: Distributor) => d.id === distributor.id);
    this.channel.distributors.splice(index, 1);
  }
}
</script>

<style></style>
