<template>
  <v-dialog v-model="dialog" max-width="500px">
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-card>
        <v-card-title class="grey lighten-2 font-weight-bold"
          >Distributor: {{ editedDistributor.type }}</v-card-title
        >

        <v-divider></v-divider>

        <v-card-text>
          <v-text-field
            v-model="editedDistributor.tipsCount"
            label="# of Tips"
            :rules="rules.tipsCount"
          />

          <label
            aria-hidden="true"
            class="v-label v-label--active theme--light"
            style="left: 0px; right: auto; font-size: 12px;"
          >
            Schedule</label
          >
          <Schedule v-model="editedDistributor.schedule" />

          <div v-if="editedDistributor.type == 'SLACK'">
            <v-text-field
              :value="attribute.get('channel')"
              @input="v => attribute.set('channel', v)"
              :rules="[rules.required]"
              label="Channel"
            />

            <v-text-field
              :value="attribute.get('username')"
              @input="v => attribute.set('username', v)"
              :rules="[rules.required]"
              label="Username"
            />

            <v-text-field
              :value="attribute.get('icon')"
              @input="v => attribute.set('icon', v)"
              :rules="[rules.required]"
              label="Icon"
            />
          </div>
        </v-card-text>

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
import {
  Component,
  Prop,
  Model,
  Emit,
  Watch,
  Vue,
} from 'vue-property-decorator';
import { CREATE_DISTRIBUTOR, UPDATE_DISTRIBUTOR } from '@/graphql/queries';
import Schedule from '@/components/Schedule.vue';
import { QueryResult } from 'vue-apollo/types/vue-apollo';
import { createDistributor } from '@/graphql/types/createDistributor';
import { updateDistributor } from '@/graphql/types/updateDistributor';
import { Distributor, KeyValue } from '@/types/models';
import { DistributorType } from '../../types/globalTypes';

class Attribute {
  constructor(private attribute: KeyValue[]) {}

  get(key: string) {
    let kv = this.attribute.find(kv => kv.key == key);
    return kv ? kv.value : '';
  }

  set(key: string, value: string) {
    let kv = this.attribute.find(kv => kv.key == key);
    if (kv) {
      kv.value = value;
    } else {
      this.attribute.push({ key, value });
    }
  }
}

// graphql向けオブジェクトで__typenameがあるとエラーになるため除去する
function treat(obj: any): any {
  if (Array.isArray(obj)) {
    return obj.map(v => treat(v));
  } else if (typeof obj == 'object') {
    let newObj: any = { ...obj };
    delete newObj['__typename'];
    for (let key of Object.keys(newObj)) {
      newObj[key] = treat(newObj[key]);
    }
    return newObj;
  } else {
    return obj;
  }
}

@Component({
  components: {
    Schedule,
  },
})
export default class DistributorForm extends Vue {
  $refs!: {
    form: HTMLFormElement;
  };

  readonly rules = {
    tipsCount: [
      (v: string) => !!v || 'Required',
      (v: string) => /^[0-9]*$/.test(v) || 'Invalid number',
    ],
    required: (v: string) => !!v || 'Required',
  };

  readonly defaultDistributor: Distributor = {
    id: '',
    type: DistributorType.SLACK,
    schedule:
      '{"month": "*", "day": "*", "day_of_week": "*", "hour": "*", "minute": "*"}',
    tipsCount: 1,
    attribute: [],
  };

  private dialog: boolean = false;
  private valid = true;
  private errors: { field: string; messages: string[] }[] = [];

  private channelId: String = '';
  private editedDistributor: Distributor = { ...this.defaultDistributor };
  private attribute: Attribute = new Attribute([]);

  open(
    channelId: string,
    type: DistributorType,
    distributor: Distributor | null = null,
  ) {
    this.dialog = true;
    this.valid = true;
    this.errors = [];
    this.$refs.form.resetValidation();

    this.channelId = channelId;
    this.editedDistributor = {
      ...this.defaultDistributor,
      type,
      ...JSON.parse(JSON.stringify(distributor || {})), // deepcopy
    };
    this.attribute = new Attribute(this.editedDistributor.attribute);
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
      let mutation: Promise<QueryResult<createDistributor | updateDistributor>>;
      if (!this.editedDistributor.id) {
        mutation = this.$apollo.mutate<createDistributor>({
          mutation: CREATE_DISTRIBUTOR,
          variables: {
            channelId: this.channelId,
            ...treat(this.editedDistributor),
          },
          fetchPolicy: 'no-cache',
        });
      } else {
        mutation = this.$apollo.mutate<updateDistributor>({
          mutation: UPDATE_DISTRIBUTOR,
          variables: {
            ...treat(this.editedDistributor),
          },
          fetchPolicy: 'no-cache',
        });
      }

      mutation
        .then(({ data: { result } }) => {
          if (!result) {
            throw 'result is null';
          }
          return result;
        })
        .then(({ distributor, errors }) => {
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
        });
    }
  }

  @Emit()
  changeDistributor(distributor: Distributor) {
    return distributor;
  }
}
</script>

<style></style>
