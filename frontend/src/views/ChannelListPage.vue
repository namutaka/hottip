<template>
  <v-container class="channel_list grid-list-xl">
    <ChannelForm ref="channelForm" @change-channel="openChannel" />

    <v-layout wrap>
      <v-flex xs12>
        <v-card dark color="indigo lighten-2">
          <v-card-title primary-title>
            <h1 class="mr-4">Hot Tip</h1>
            <div>
              Hot Tip はちょっとした情報を定期的に届けるルールです。<br />
              チャンネル に登録した Tips を指定した配信先に順番に送信します。<br />
              最初に チャンネル
              を作成し、その中にTipsや配信先をそれぞれ設定してください。
            </div>
          </v-card-title>
        </v-card>
      </v-flex>

      <v-flex>
        <v-btn color="primary" dark class="mb-2" @click="add">
          チャンネル作成
        </v-btn>

        <ChannelList
          :channels="allChannels"
          @click-channel="openChannel"
          :loading="loading"
        />
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import ChannelList from '@/components/ChannelList.vue';
import ChannelForm from '@/components/ChannelForm.vue';
import { Channel } from '@/types/models';
import { ALL_CHANNELS } from '@/graphql/queries';
import {
  allChannels_allChannels,
  allChannels,
} from '@/graphql/types/allChannels';

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
      },
    },
  },
})
export default class Channels extends Vue {
  $refs!: {
    channelForm: ChannelForm;
  };

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
