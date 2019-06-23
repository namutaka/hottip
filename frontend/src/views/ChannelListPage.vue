<template>
  <v-container class="channel_list grid-list-xl">
    <ChannelForm ref="channelForm" @change-channel="openChannel" />

    <v-layout wrap>
      <v-flex xs12>
        <v-card dark color="indigo lighten-1">
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
        <v-layout justify-space-between>
          <v-flex xs12 sm4>
            <v-btn color="primary" dark class="mb-2" @click="add">
              チャンネル作成
            </v-btn>
          </v-flex>
          <v-flex xs12 sm4>
            <v-text-field
              v-model="searchText"
              label="Search..."
              single-line
              append-icon="search"
              hide-details
            />
          </v-flex>
        </v-layout>

        <ChannelList
          :channels="channels"
          @click-channel="openChannel"
          :loading="loading"
        />

        <v-layout v-if="hasMore">
          <v-flex sm12>
            <v-btn block @click="showMore">More</v-btn>
          </v-flex>
        </v-layout>
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
import { allChannels, allChannels_allChannels_pageInfo } from '@/graphql/types/allChannels';
import { notEmpty } from '@/utils/TypeUtils';
import { SmartQuery } from 'vue-apollo/types/vue-apollo';

@Component({
  components: {
    ChannelList,
    ChannelForm,
  },
  apollo: {
    allChannels: {
      query: ALL_CHANNELS,
      update(data: allChannels) {
        if (data.allChannels) {
          return {
            channels: data.allChannels.edges.map((edge: any) => edge.node),
            pageInfo: data.allChannels.pageInfo
          };
        } else {
          return {
            channels: [],
            pageInfo: {}
          };
        }
      },
      variables() {
        return {
          count: this.pageSize,
          search: this.searchText,
        };
      }
    },
  },
})
export default class ChannelListPage extends Vue {
  $refs!: {
    channelForm: ChannelForm;
  };

  allChannels!: {
    channels: Channel[];
    pageInfo: allChannels_allChannels_pageInfo;
  };
  pageSize = 20;

  searchText = "";

  mounted() {
    // ページ遷移時に内容を確実に更新
    this.$apollo.queries.allChannels.refetch();
  }

  get loading(): boolean {
    return this.$apollo.queries.allChannels.loading;
  }

  get hasMore() {
    return this.allChannels && this.allChannels.pageInfo.hasNextPage;
  }

  get channels(): Channel[] {
    return this.allChannels ? this.allChannels.channels : [];
  }

  add() {
    this.$refs.channelForm.open();
  }

  openChannel(channel: Channel) {
    this.$router.push({ name: 'channel', params: { channelId: channel.id } });
  }

  nextVariables() {
    return {
      count: this.pageSize,
      cursor: this.allChannels.pageInfo.endCursor,
      search: this.searchText,
    };
  }

  showMore() {
    if (!this.hasMore) {
      return;
    }

    this.$apollo.queries.allChannels.fetchMore({
      variables: this.nextVariables(),
      updateQuery(previousResult, { fetchMoreResult }) {
        return {
          allChannels: {
            __typename: previousResult.allChannels.__typename,
            edges: [
              ...previousResult.allChannels.edges,
              ...fetchMoreResult.allChannels.edges
            ],
            pageInfo: fetchMoreResult.allChannels.pageInfo,
          },
        }
      },
    });
  }
}
</script>