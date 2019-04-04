<template>
  <div class="channel_list">
    <ChannelList />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import ChannelList from "@/components/ChannelList.vue"; // @ is an alias to /src

@Component({
  components: {
    ChannelList
  }
})
export default class Channel extends Vue {}
</script>
