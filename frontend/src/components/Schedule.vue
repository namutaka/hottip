<template>
  <div class="schedule_input">
    <v-container v-for="([field, label], index) in SCHEDULE_TEXT" :key="field">
      <v-layout row align-center>
        <v-flex xs1 align-center>
          {{ label }}
        </v-flex>

        <v-flex xs10>
          <v-radio-group
            v-if="field != 'day_of_week'"
            v-model="values[field]"
            hide-details
            height="50px"
            row
            @change="input"
          >
            <v-radio :label="'毎' + label" value="every" />
            <v-radio value="spec">
              <template v-slot:label>
                <v-text-field
                  v-model="values[field + '_spec']"
                  :disabled="values[field] != 'spec'"
                  label="例) 1,2 2-5 */3"
                  hide-details
                  single-line
                  :rules="values[field] == 'spec' ? rules.spec : []"
                  @change="input"
                />
              </template>
            </v-radio>
          </v-radio-group>

          <v-layout row v-else>
            <v-flex
              v-for="(dow_label, index) in DAY_OF_WEEK_TEXT"
              :key="index"
              xs4
              class="pr-2"
            >
              <v-checkbox
                :label="dow_label"
                :value="index"
                v-model="values[field]"
                hide-details
                @change="input"
              ></v-checkbox>
            </v-flex>
          </v-layout>
        </v-flex>

        <v-flex xs1 align-right>
          <div v-if="index == 0">
            <v-tooltip bottom>
              <template v-slot:activator="{ on }">
                <v-icon color="primary" dark v-on="on">help</v-icon>
              </template>
              <table>
                <tr>
                  <td colspan="2">(表記例)</td>
                </tr>
                <tr>
                  <td>5</td>
                  <td>5日のみ</td>
                </tr>
                <tr>
                  <td>2-6</td>
                  <td>2日〜6日(両方含む)</td>
                </tr>
                <tr>
                  <td>*/3</td>
                  <td>3日間隔</td>
                </tr>
                <tr>
                  <td>10-30/5</td>
                  <td>10日〜30日の間で5日間隔</td>
                </tr>
                <tr>
                  <td>5,2-6,*/5</td>
                  <td>コンマで複数条件を列挙</td>
                </tr>
              </table>
            </v-tooltip>
          </div>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
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
import { SCHEDULE_TEXT, DAY_OF_WEEK_TEXT } from '@/utils/ScheduleUtils';

@Component({})
export default class Schedule extends Vue {
  readonly SCHEDULE_TEXT = SCHEDULE_TEXT;
  readonly DAY_OF_WEEK_TEXT = DAY_OF_WEEK_TEXT;

  @Model('input', { type: String }) private schedule!: string;

  readonly rules = {
    spec: [
      (value: string) =>
        (!!value &&
          value
            .split(/,/)
            .every(v =>
              /^(?:[0-9]+(?:-[0-9]+)?|\*)(?:\/[0-9]+)?$/.test(v.trim()),
            )) ||
        'invalid format',
    ],
  };

  get values(): any {
    if (!this.schedule) {
      return {};
    }

    let values: any = {};
    const schedule = JSON.parse(this.schedule);
    for (let [field, _] of SCHEDULE_TEXT) {
      if (field != 'day_of_week') {
        let value = (schedule[field] || '').toString();
        if (value == '*') {
          values[field] = 'every';
        } else {
          values[field] = 'spec';
          values[field + '_spec'] = value.replace(/ /g, '');
        }
      } else {
        if (schedule[field] == '*') {
          values[field] = Array.from({ length: 7 }, (_, i) => i);
        } else {
          values[field] = schedule[field]
            .split(',')
            .map((dow: string) => parseInt(dow, 10));
        }
      }
    }
    return values;
  }

  @Emit()
  input() {
    const values = this.values;
    let schedule: any = {};
    for (let [field, _] of SCHEDULE_TEXT) {
      let value = '';
      if (field != 'day_of_week') {
        if (values[field] == 'every') {
          value = '*';
        } else {
          value = (values[field + '_spec'] || '').trim();
        }
      } else {
        if (values[field].length == 7) {
          value = '*';
        } else {
          value = values[field].join(',');
        }
      }

      schedule[field] = value;
    }

    return JSON.stringify(schedule);
  }
}
</script>

<style>
.schedule_input {
  margin-bottom: 15px;
}
.schedule_input .container {
  padding: 0 8px;
}
.schedule_input .v-input--selection-controls {
  margin-top: 0;
}
.schedule_input .v-text-field {
  margin-top: 0;
  padding-top: 0;
}
</style>
