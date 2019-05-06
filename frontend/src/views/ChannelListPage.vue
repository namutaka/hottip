<template>
  <div class="channel_list">
    <ChannelForm ref="channelForm" @change-channel="openChannel" />

    <ChannelList
      :channels="allChannels"
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
import { allChannels_allChannels, allChannels } from '@/graphql/types/allChannels'

@Component({
  components: {
    ChannelList,
    ChannelForm,
  },
  apollo: {
    allChannels: {
      query: ALL_CHANNELS,
      update: (data: allChannels) => {
        if (data.allChannels && data.allChannels.edges) {
          return data.allChannels.edges.map((edge: any) => edge.node);
        } else {
          return [];
        }
      }
    },
  },
})
export default class Channels extends Vue {
  $refs!: {
    channelForm: ChannelForm
  }

  allChannels!: Channel[];

  mounted() {
    // ページ遷移時に内容を確実に更新
    this.$apollo.queries.allChannels.refetch();
  }

  get loading(): boolean {
    return this.$apollo.queries.allChannels.loading;
  }

  add() {
    this.$refs.channelForm.open();
  }

  openChannel(channel: Channel) {
    this.$router.push({ name: 'channel', params: { channelId: channel.id } });
  }
}
</script>
