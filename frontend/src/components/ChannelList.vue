<template>
  <v-container>
    <CreateChannelDialog />

    <v-data-table
      :headers="headers"
      :items="allChannels.edges"
      :pagination.sync="pagination"
      :loading="loading"
      no-data-text="no-data"
      class="elevation-1"
    >
      <template v-slot:items="props">
        <td>{{ props.item.node.rawId }}</td>
        <td class="text-sm-left text-wrap">{{ props.item.node.name }}</td>
        <td class="text-sm-left text-wrap">
          {{ props.item.node.description }}
        </td>
        <td class="">
          {{ props.item.node.createdAt | datetime }}<br />
          {{ props.item.node.updatedAt | datetime }}
        </td>
      </template>
    </v-data-table>

    <v-btn @click="run">DO</v-btn>
  </v-container>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { ALL_CHANNELS } from '@/graphql/queries';
import CreateChannelDialog from '@/components/CreateChannelDialog.vue';

@Component({
  apollo: {
    allChannels: {
      query: ALL_CHANNELS,
    },
  },
  components: {
    CreateChannelDialog,
  },
})
export default class ChannelList extends Vue {
  $refs!: {
    form: HTMLFormElement;
  };

  allChannels: Object = {};

  readonly headers = [
    { text: 'ID', value: 'id' },
    { text: '名前', value: 'name' },
    { text: '説明', value: 'description' },
    { text: '日付', value: 'createdAt', width: '180' },
  ];

  readonly pagination = {
    descending: true,
    rowsPerPage: 10,
  };

  get loading(): boolean {
    return this.$apollo.queries.allChannels.loading;
  }

  run(): void {
    console.log(this.$apollo.queries.channels);
  }
}
</script>

<style>
.text-wrap {
  word-break: break-all;
}
</style>
