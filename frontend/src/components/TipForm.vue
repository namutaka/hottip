<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-form v-model="valid">
      <v-card>
        <v-card-title
          class="grey lighten-2 font-weight-bold"
        >Tip</v-card-title>

        <v-divider></v-divider>

        <v-text-field
          v-model="tip.title"
          label="Title"
          :rules="rules.title"
          full-width
          single-line
          hide-details
        />

        <v-divider></v-divider>

        <v-textarea
          v-model="tip.text"
          label="Text"
          full-width
          single-line
        ></v-textarea>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn flat>Cancel</v-btn>
          <v-spacer />
          <v-btn flat color="primary">Save</v-btn>
        </v-card-actions>

      </v-card>
    </v-form>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Prop, Model, Vue } from 'vue-property-decorator';
import { CHANNEL } from '@/graphql/queries';

@Component({})
export default class TipForm extends Vue {
  @Prop() private tip!: any;
  @Model('change', { type: Boolean, default: false}) private dialogValue!: boolean;
  valid = true;

  readonly rules = {
    title: []
  }

  // このタグの v-model を dialog プロパティに連動させる
  get dialog() { return this.dialogValue; }
  set dialog(newDialog) {this.$emit('input', newDialog);}

}
</script>

<style></style>
