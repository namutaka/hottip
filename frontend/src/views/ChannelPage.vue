<template>
  <v-container grid-list-xl>
    <v-layout column>
      <v-flex>
        <Channel :channel="channel" />
      </v-flex>

      <v-flex>
        <v-tabs color="grey lighten-3">
          <v-tab ripple>Tips</v-tab>
          <v-tab ripple>Distributors</v-tab>

          <v-tab-item>
            <v-card flat class="pa-2">
              <v-btn>New Tip</v-btn>

              <v-layout column
                v-if="channel.tips.length"
              >
                <v-flex v-for="tip in channel.tips" :key="tip.id">
                  <v-card pa-2>
                    <v-flex absolute right>
                      <v-chip v-if="tip.enable" small label color="green" dark>ON</v-chip>
                      <v-chip v-else small label color="indigo" dark>OFF</v-chip>

                      <v-btn flat small icon>
                        <v-icon small color="grey lighten-1">edit</v-icon>
                      </v-btn>
                    </v-flex>

                    <v-card-text>
                      <h4>{{tip.title}}</h4>
                      <div>{{tip.text}}</div>
                    </v-card-text>
                  </v-card>
                </v-flex>
              </v-layout>

              <v-layout column v-else>
                <v-flex>
                  <v-card pa-2>
                    <v-card-text>
                      no-data
                    </v-card-text>
                  </v-card>
                </v-flex>
              </v-layout>

            </v-card>
          </v-tab-item>

          <v-tab-item>
            <v-card flat class="pa-2">
              <v-btn>New</v-btn>

              <v-layout column>
                <template v-for="dist in channel.distributors">
                  <v-flex :key="dist.id">
                    <v-card pa-2>
                      <v-flex absolute right>
                        <v-btn flat small icon>
                          <v-icon small color="grey lighten-1">edit</v-icon>
                        </v-btn>
                      </v-flex>

                      <v-list dense>
                        <v-list-tile>
                          <v-list-tile-content class="item-label font-weight-light gray">Type</v-list-tile-content>
                          <v-list-tile-content>{{dist.type}}</v-list-tile-content>
                        </v-list-tile>
                        <v-list-tile>
                          <v-list-tile-content class="item-label font-weight-light gray"># of Tips</v-list-tile-content>
                          <v-list-tile-content>{{dist.tipsCount}}</v-list-tile-content>
                        </v-list-tile>
                        <v-list-tile>
                          <v-list-tile-content class="item-label font-weight-light gray">schedule</v-list-tile-content>
                          <v-list-tile-content>{{dist.schedule}}</v-list-tile-content>
                        </v-list-tile>
                        <v-list-tile v-for="(item, index) in dist.attribute" :key="index">
                          <v-list-tile-content class="item-label font-weight-light gray">{{item.key}}</v-list-tile-content>
                          <v-list-tile-content>{{item.value}}</v-list-tile-content>
                        </v-list-tile>
                      </v-list>
                    </v-card>
                  </v-flex>
                </template>
              </v-layout>

            </v-card>
          </v-tab-item>

        </v-tabs>
      </v-flex>

    </v-layout>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Channel from '@/components/Channel.vue';
import { CHANNEL } from '@/graphql/queries';

@Component({
  apollo: {
    channel() {
      return {
        query: CHANNEL,
        variables: {
          id: this.$route.params.channelId
        }
      }
    }
  },
  components: {
    Channel
  }
})
export default class ChannelPage extends Vue {
  private channel!: any
}
</script>

<style>
.item-label  {
  max-width: 7em;
}
</style>