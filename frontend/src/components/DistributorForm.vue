<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-card>
        <v-card-title
          class="grey lighten-2 font-weight-bold"
        >Distributor: {{ editedDistributor.type }}</v-card-title>

        <v-divider></v-divider>

        <v-card-text>
          <v-text-field
            v-model="editedDistributor.tipsCount"
            label="# of Tips"
          />

          <label
            aria-hidden="true"
            class="v-label v-label--active theme--light"
            style="left: 0px; right: auto; font-size: 12px;">
                Schedule</label>
          <Schedule v-model="editedDistributor.schedule" />

          <div v-if="editedDistributor.type == 'SLACK'">
            <v-text-field
              :value="attribute.get('channel')"
              @input="v => attribute.set('channel', v)"
              label="Channel"
            />

            <v-text-field
              :value="attribute.get('username')"
              @input="v => attribute.set('username', v)"
              label="Username"
            />

            <v-text-field
              :value="attribute.get('icon')"
              @input="v => attribute.set('icon', v)"
              label="Icon"
            />

          </div>
        </v-card-text>

        <v-card-actions>
          <v-btn flat @click="close">Cancel</v-btn>
          <v-spacer />
          <v-btn flat color="primary"
            :disabled="!valid"
            @click="save">Save</v-btn>
        </v-card-actions>

      </v-card>
    </v-form>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Prop, Model, Emit, Watch, Vue } from 'vue-property-decorator';
import { CREATE_DISTRIBUTOR, UPDATE_DISTRIBUTOR } from '@/graphql/queries';
import Schedule from '@/components/Schedule.vue';

class Attribute {
  constructor(private attribute: {key: string, value: string}[]) {};

  get(key: string) {
    let kv = this.attribute.find(kv => kv.key == key);
    return kv ? kv.value : '';
  }

  set(key: string, value: string) {
    let kv = this.attribute.find(kv => kv.key == key);
    if (kv) {
      kv.value = value;
    }
  }
}

@Component({
  components: {
    Schedule
  }
})
export default class DistributorForm extends Vue {
  $refs!: {
    form: HTMLFormElement;
  };

  @Prop() private distributor!: any;
  @Prop() private channelId!: string;
  @Model('change', { type: Boolean, default: false}) private dialogValue!: boolean;
  private attribute!: Attribute;

  editedDistributor: any = {};
  valid = true;
  errors: { field: string; messages: string[] }[] = [];

  readonly rules = {
    title: []
  };

  // このタグの v-model を dialog プロパティに連動させる
  get dialog() { return this.dialogValue; }
  set dialog(newDialog) {this.$emit('change', newDialog);}

  @Watch('dialogValue')
  onDialogValueChanged(newVal: boolean) { 
    // dialogが開いたときに初期化
    if (newVal) {
      // deepcopy
      this.editedDistributor = JSON.parse(JSON.stringify(this.distributor));
      // graphql向けに不要フィールド除去
      for (let att of this.editedDistributor.attribute) {
        delete att.__typename
      }
      this.attribute = new Attribute(this.editedDistributor.attribute);
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
      let mutation;
      if (!this.editedDistributor.id) {
        mutation = this.$apollo
          .mutate({
            mutation: CREATE_DISTRIBUTOR,
            variables: {
              channelId: this.channelId,
              ...this.editedDistributor
            },
            fetchPolicy: "no-cache"
          });
      } else {
        mutation = this.$apollo
          .mutate({
            mutation: UPDATE_DISTRIBUTOR,
            variables: {
              ...this.editedDistributor
            },
            fetchPolicy: "no-cache"
          });
      }

      mutation
        .then(({ data: { result: { distributor, errors } } }) => {
          if (distributor) {
            this.close();
            this.changeDistributor(distributor);
          } else {
            this.valid = false;
            this.errors = errors;
            this.$refs.form.validate();
          }
        })
        .catch(error => {
          console.error(error);
          for (let e of error.networkError.result.errors) {
            console.error(e.message);
          }
        });
    }
  }

  @Emit()
  changeDistributor(distributor: any) {
    return distributor;
  }
}
</script>

<style></style>
