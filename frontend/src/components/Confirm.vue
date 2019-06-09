<template>
  <v-dialog
    v-model="dialog"
    :max-width="options.width"
    @keydown.esc="cancel"
    v-bind:style="{ zIndex: options.zIndex }"
    persistent
  >
    <v-card>
      <v-toolbar dark :color="options.color" dense flat>
        <v-toolbar-title class="white--text">{{ title }}</v-toolbar-title>
      </v-toolbar>
      <v-card-text v-show="!!message">{{ message }}</v-card-text>
      <v-card-actions class="pt-0">
        <v-spacer></v-spacer>
        <v-btn color="primary darken-1" flat="flat" @click.native="agree"
          >Yes</v-btn
        >
        <v-btn color="grey" flat="flat" @click.native="cancel">Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import Vue from 'vue';
import { Component, Prop } from 'vue-property-decorator';

/**
 * Vuetify Confirm Dialog component
 *
 * Call it:
 * if (await this.$root.$confirm('Delete', 'Are you sure?', { color: 'red' })) {
 *   // yes
 * } else {
 *   // cancel
 * }
 */
@Component({})
export default class Confirm extends Vue {
  dialog = false;
  @Prop() resolve!: (result: boolean) => void;
  @Prop() message!: string;
  @Prop() title!: string;
  @Prop() options!: { color: string; width: number; zIndex: number };

  static open(title: string, message: string, options?: any) {
    options = {
      color: 'primary',
      width: 290,
      zIndex: 200,
      ...options,
    };

    return new Promise(resolve => {
      new Confirm({
        propsData: {
          title,
          message,
          options,
          resolve,
        },
      });
    });
  }

  created() {
    const el = document.createElement('div');
    document.getElementsByTagName('body')[0].appendChild(el);
    this.$mount(el);

    this.dialog = true;
  }

  agree() {
    this.resolve(true);
    this.destroy();
  }

  cancel() {
    this.resolve(false);
    this.destroy();
  }

  destroy() {
    this.dialog = false;

    // 即座にdomを削除するとtransitionする前に消えてしまうので、200ms待つ
    setTimeout(() => {
      if (this.$el && this.$el.parentNode) {
        this.$el.parentNode.removeChild(this.$el);
      }
      this.$destroy();
    }, 200);
  }
}
</script>
