<template>
  <v-container>
    <slot></slot>

    <v-data-table
      :headers="headers"
      :items="channels"
      :loading="loading"
      no-data-text="no-data"
      class="elevation-1"
      hide-actions
    >
      <template v-slot:items="props">
        <tr span @click="clickChannel(props.item)">
          <td>{{ props.item.rawId }}</td>
          <td class="text-sm-left text-wrap">{{ props.item.name }}</td>
          <td class="text-sm-left text-wrap">
            {{ props.item.description }}
          </td>
          <td class="font-weight-light">
            <v-icon small class="mx-1">update</v-icon>
            {{ props.item.updatedAt | datetime }}
          </td>
        </tr>
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import { Component, Prop, Emit, Vue } from 'vue-property-decorator';
import { Channel } from '@/types/models';

@Component({})
export default class ChannelList extends Vue {
  $refs!: {
    form: HTMLFormElement;
  };

  @Prop() channels!: Channel[];
  @Prop() loading!: boolean;

  readonly headers = [
    { text: 'ID', value: 'rawId', width: '30' },
    { text: '名前', value: 'name' },
    { text: '説明', value: 'description' },
    { text: '日付', value: 'createdAt', width: '180' },
  ];

  @Emit()
  clickChannel(channel: Channel) {
    return channel;
  }
}
</script>

<style>
.text-wrap {
  word-break: break-all;
}
</style>
