<template>
  <div class="channel_list">
    <ChannelForm ref="channelForm" @change-channel="openChannel" />

    <ChannelList
      :channels="channels"
      @click-channel="openChannel"
      :loading="loading"
      >
      <v-btn color="primary"
        dark
        class="mb-2"
        @click="add"
        >New Channel</v-btn>
    </ChannelList>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import ChannelList from '@/components/ChannelList.vue';
import ChannelForm from '@/components/ChannelForm.vue';
import { Channel } from '@/types/models';
import { ALL_CHANNELS } from '@/graphql/queries';
import { allChannels_allChannels } from '@/graphql/types/allChannels'

@Component({
  components: {
    ChannelList,
    ChannelForm,
  },
  apollo: {
    allChannels: {
      query: ALL_CHANNELS,
    },
  },
})
export default class Channels extends Vue {
  $refs!: {
    channelForm: ChannelForm
  }

  allChannels!: allChannels_allChannels | null;

  mounted() {
    // ページ遷移時に内容を確実に更新
    this.$apollo.queries.allChannels.refetch();
  }

  get loading(): boolean {
    return this.$apollo.queries.allChannels.loading;
  }

  get channels() {
    if (this.allChannels && this.allChannels.edges) {
      return this.allChannels.edges.map((edge: any) => edge.node);
    } else {
      return [];
    }
  }

  add() {
    this.$refs.channelForm.open();
  }

  openChannel(channel: Channel) {
    this.$router.push({ name: 'channel', params: { channelId: channel.id } });
  }
}
</script>
