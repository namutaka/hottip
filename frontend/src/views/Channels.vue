<template>
  <div class="channel_list">
    <ChannelList @click-channel="openChannel">
      <CreateChannelDialog @create-channel="openChannel" />
    </ChannelList>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import ChannelList from '@/components/ChannelList.vue';
import CreateChannelDialog from '@/components/CreateChannelDialog.vue';

@Component({
  components: {
    ChannelList,
    CreateChannelDialog,
  },
})
export default class Channel extends Vue {
  openChannel(channelId: string) {
    this.$router.push({ name: 'channel', params: { channelId } });
  }
}
</script>
