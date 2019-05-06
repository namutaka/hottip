<template>
  <v-card>
    <ChannelForm ref="channelForm" @change-channel="changeChannel" />

    <v-container class="px-0 py-1">
      <v-layout row>
        <v-flex xs11>
          <v-card-title>
            <h3 class="font-weight-medium channel-title">{{ channel.name }}</h3>
          </v-card-title>
          <v-card-text class="pt-0">
            <pre>{{ channel.description }}</pre>
          </v-card-text>
        </v-flex>

        <v-flex xs1>
          <v-menu offset-y>
            <template v-slot:activator="{ on }">
              <v-btn flat small icon v-on="on">
                <v-icon color="grey lighten-1">more_vert</v-icon>
              </v-btn>
            </template>

            <v-list>
              <v-list-tile @click="edit">
                <v-list-tile-title>
                  <v-icon color="grey lighten-1" class="mr-2">edit</v-icon>
                  変更
                </v-list-tile-title>
              </v-list-tile>

              <v-divider class="my-2" />

              <v-list-tile @click="doDelete">
                <v-list-tile-title>
                  <v-icon color="grey lighten-1" class="mr-2">delete</v-icon>
                  削除
                </v-list-tile-title>
              </v-list-tile>
            </v-list>
          </v-menu>
        </v-flex>
      </v-layout>
    </v-container>

    <v-divider class="mx-3" />

    <v-card-actions class="font-weight-light mx-3 px-0 py-2">
      #{{ channel.rawId }}
      <v-divider vertical class="mx-2" />
      <span>
        <v-icon small class="mx-1">create</v-icon>
        {{ channel.createdAt | datetime }}
      </span>
      <span class="mx-1">
        <v-icon small class="mx-1">update</v-icon>
        {{ channel.updatedAt | datetime }}
      </span>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Emit, Vue } from 'vue-property-decorator';
import { Channel as ChannelType } from '@/types/models';
import ChannelForm from '@/components/ChannelForm.vue';
import { deleteChannel } from '@/graphql/types/deleteChannel';
import { DELETE_CHANNEL } from '@/graphql/queries';

@Component({
  components: {
    ChannelForm,
  },
})
export default class Channel extends Vue {
  $refs!: {
    channelForm: ChannelForm;
  };

  @Prop() private channel!: ChannelType;

  edit() {
    this.$refs.channelForm.open(this.channel);
  }

  async doDelete() {
    if (
      await this.$root.$confirm(
        'チャンネル削除',
        'チャンネルを削除します。' +
          '登録されているTipsや配信先設定もあわせて削除されます',
      )
    ) {
      let mutation = this.$apollo
        .mutate<deleteChannel>({
          mutation: DELETE_CHANNEL,
          variables: {
            id: this.channel.id,
          },
          fetchPolicy: 'no-cache',
        })
        .then(({ data: { deleteChannel } }) => {
          if (!deleteChannel) {
            throw 'result is null';
          }
          if (deleteChannel.ok) {
            this.deleteChannel(this.channel);
          }
        })
        .catch(error => {
          console.error(error);
        });
    }
  }

  @Emit()
  deleteChannel(channel: ChannelType) {
    return channel;
  }

  @Emit()
  changeChannel(channel: ChannelType) {
    return channel;
  }
}
</script>

<style>
.channel-title {
  word-break: break-all;
}
</style>
