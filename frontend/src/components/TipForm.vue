<template>
  <v-dialog v-model="dialog" max-width="500px">

    <v-form ref="form" v-model="valid" lazy-validation>
      <v-card>
        <v-card-title
          class="grey lighten-2 font-weight-bold"
        >Tip</v-card-title>

        <v-divider></v-divider>

        <v-text-field
          v-model="editedTip.title"
          label="Title"
          :rules="rules.title"
          full-width
          single-line
          hide-details
        />

        <v-divider></v-divider>

        <v-textarea
          v-model="editedTip.text"
          label="Text"
          full-width
          single-line
        ></v-textarea>

        <v-divider></v-divider>

        <div class="ma-2">
          <v-switch 
            value 
            label="Use"
            v-model="editedTip.enable"></v-switch>
        </div>

        <v-card-actions>
          <v-btn flat @click="close">Cancel</v-btn>
          <v-spacer />
          <v-btn flat color="primary" @click="save">Save</v-btn>
        </v-card-actions>

      </v-card>
    </v-form>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Prop, Model, Emit, Watch, Vue } from 'vue-property-decorator';
import { CREATE_TIP, UPDATE_TIP } from '@/graphql/queries';
import { Tip } from '@/types/models';
import { QueryResult } from 'vue-apollo/types/vue-apollo';
import { createTip } from '@/graphql/types/createTip'
import { updateTip } from '@/graphql/types/updateTip'

@Component({})
export default class TipForm extends Vue {
  $refs!: {
    form: HTMLFormElement;
  };

  @Prop() private tip!: Tip;
  @Prop() private channelId!: string;
  @Model('change', { type: Boolean, default: false}) private dialogValue!: boolean;

  defaultTip: Tip = {
    id: "",
    title: "",
    text: "",
    enable: true
  };
  editedTip: Tip = {...this.defaultTip};
  valid = true;
  errors: { field: string; messages: string[] }[] = [];

  readonly rules = {
    title: []
  }

  // このタグの v-model を dialog プロパティに連動させる
  get dialog() { return this.dialogValue; }
  set dialog(newDialog) {this.$emit('change', newDialog);}

  @Watch('dialogValue')
  onDialogValueChanged(newVal: boolean) { 
    // dialogが開いたときに初期化
    if (newVal) {
      this.editedTip = {...this.defaultTip, ...this.tip};
    }
  }

  validate_error(field: string): string | boolean {
    let error = this.errors.find(i => i.field == field);
    if (error) {
      return error.messages.join('\n');
    } else {
      return true;
    }
  }

  close() {
    this.dialog = false;
  }

  save() {
    this.errors = [];
    if (this.$refs.form.validate()) {
      let mutation: Promise<QueryResult<createTip | updateTip>>;
      if (!this.editedTip.id) {
        mutation = this.$apollo
          .mutate<createTip>({
            mutation: CREATE_TIP,
            variables: {
              channelId: this.channelId,
              ...this.editedTip
            },
            fetchPolicy: "no-cache"
          });
      } else {
        mutation = this.$apollo
          .mutate<updateTip>({
            mutation: UPDATE_TIP,
            variables: {
              ...this.editedTip
            },
            fetchPolicy: "no-cache"
          });
      }

      mutation
        .then(({ data: { result }}) => {
          if (!result) { throw "result is null"; }
          return result;
        })
        .then(({ tip, errors }) => {
          if (tip) {
            this.close();
            this.changeTip(tip);
          } else {
            this.valid = false;
            this.errors = errors;
            this.$refs.form.validate();
          }
        })
        .catch(error => {
          console.error(error);
        });
    }
  }

  @Emit()
  changeTip(tip: Tip) {
    return tip;
  }
}
</script>

<style></style>
