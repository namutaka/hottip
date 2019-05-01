<template>
  <div class="channel_list">
    <ChannelList @click-channel="openChannel">
      <v-btn color="primary"
        dark
        class="mb-2"
        @click="add"
        >New Channel</v-btn>

      <ChannelForm ref="channelForm" @change-channel="openChannel" />
    </ChannelList>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import ChannelList from '@/components/ChannelList.vue';
import ChannelForm from '@/components/ChannelForm.vue';
import { Channel } from '@/types/models';

@Component({
  components: {
    ChannelList,
    ChannelForm,
  },
})
export default class Channels extends Vue {
  $refs!: {
    channelForm: ChannelForm
  }

  add() {
    this.$refs.channelForm.open();
  }

  openChannel(channel: Channel) {
    this.$router.push({ name: 'channel', params: { channelId: channel.id } });
  }
}
</script>
