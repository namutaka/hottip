<template>
  <v-container>
    <slot></slot>

    <v-data-table
      :headers="headers"
      :items="allChannels.edges"
      :loading="loading"
      no-data-text="no-data"
      class="elevation-1"
      hide-actions
    >
      <template v-slot:items="props">
        <tr span @click="clickChannel(props.item.node.id)">
          <td>{{ props.item.node.rawId }}</td>
          <td class="text-sm-left text-wrap">{{ props.item.node.name }}</td>
          <td class="text-sm-left text-wrap">
            {{ props.item.node.description }}
          </td>
          <td class="font-weight-light">
            <div>
              <v-icon small class="mx-1">create</v-icon>
              {{ props.item.node.createdAt | datetime }}
            </div>
            <div>
              <v-icon small class="mx-1">update</v-icon>
              {{ props.item.node.updatedAt | datetime }}
            </div>
          </td>
        </tr>
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import { Component, Prop, Emit, Vue } from 'vue-property-decorator';
import { ALL_CHANNELS } from '@/graphql/queries';

@Component({
  apollo: {
    allChannels: {
      query: ALL_CHANNELS,
    },
  },
})
export default class ChannelList extends Vue {
  $refs!: {
    form: HTMLFormElement;
  };

  allChannels: Object = {};

  readonly headers = [
    { text: 'ID', value: 'id', width: '30' },
    { text: '名前', value: 'name' },
    { text: '説明', value: 'description' },
    { text: '日付', value: 'createdAt', width: '180' },
  ];

  get loading(): boolean {
    return this.$apollo.queries.allChannels.loading;
  }

  @Emit()
  clickChannel(channelId: string) {
    return channelId;
  }
}
</script>

<style>
.text-wrap {
  word-break: break-all;
}
</style>
