<template>
  <v-dialog v-model="dialog" max-width="640px" persistent>
    <v-form ref="form" v-model="valid" lazy-validation>
      <v-card>
        <v-card-title>
          <span class="headline">{{ caption }}</span>
        </v-card-title>

        <v-card-text>
          <v-text-field
            v-model="editedDistributor.tipsCount"
            label="一度に送信するTips数"
            :rules="rules.tipsCount"
          />

          <label
            aria-hidden="true"
            class="v-label v-label--active theme--light"
            style="left: 0px; right: auto; font-size: 12px;"
          >
            配信タイミング
          </label>
          <Schedule v-model="editedDistributor.schedule" />

          <v-text-field
            v-for="field in ATTRIBUTE_FIELDS[editedDistributor.type]"
            :key="field.key"
            :value="attribute.get(field.key)"
            @input="v => attribute.set(field.key, v)"
            :rules="[rules.required]"
            :label="field.label"
            :placeholder="field.placeholder"
          />
        </v-card-text>

        <v-card-actions>
          <v-btn flat color="grey" @click="close">Cancel</v-btn>
          <v-spacer />
          <v-btn flat color="primary" @click="save">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Emit, Vue } from 'vue-property-decorator';
import { CREATE_DISTRIBUTOR, UPDATE_DISTRIBUTOR } from '@/graphql/queries';
import Schedule from '@/components/Schedule.vue';
import { QueryResult } from 'vue-apollo/types/vue-apollo';
import { createDistributor } from '@/graphql/types/createDistributor';
import { updateDistributor } from '@/graphql/types/updateDistributor';
import { Distributor, KeyValue } from '@/types/models';
import { DistributorType } from '../../types/globalTypes';
import { Attribute, ATTRIBUTE_FIELDS } from '@/utils/AttributeUtils';

// graphql向けオブジェクトで__typenameがあるとエラーになるため除去する
function normalize(obj: any): any {
  if (Array.isArray(obj)) {
    return obj.map(v => normalize(v));
  } else if (typeof obj == 'object') {
    let newObj: any = { ...obj };
    delete newObj['__typename'];
    for (let key of Object.keys(newObj)) {
      newObj[key] = normalize(newObj[key]);
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

  readonly ATTRIBUTE_FIELDS = ATTRIBUTE_FIELDS;

  readonly rules = {
    tipsCount: [
      (v: string) => !!v || '必須入力です',
      (v: string) => /^[0-9]*$/.test(v) || '数字を入力してください',
      () => this.validate_error('tipsCount'),
    ],
    required: (v: string) => !!v || '必須入力です',
  };

  readonly defaultDistributor: Distributor = {
    id: '',
    type: DistributorType.SLACK,
    schedule:
      '{"month": "*", "day": "*", "day_of_week": "*", "hour": "*", "minute": "0"}',
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

  get caption() {
    if (this.editedDistributor.id) {
      return `配信設定編集: ${this.editedDistributor.type}`;
    } else {
      return `配信設定作成: ${this.editedDistributor.type}`;
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
      let mutation: Promise<QueryResult<createDistributor | updateDistributor>>;
      if (!this.editedDistributor.id) {
        mutation = this.$apollo.mutate<createDistributor>({
          mutation: CREATE_DISTRIBUTOR,
          variables: {
            channelId: this.channelId,
            ...normalize(this.editedDistributor),
          },
          fetchPolicy: 'no-cache',
        });
      } else {
        mutation = this.$apollo.mutate<updateDistributor>({
          mutation: UPDATE_DISTRIBUTOR,
          variables: {
            ...normalize(this.editedDistributor),
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
