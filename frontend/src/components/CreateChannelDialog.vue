<template>
  <v-dialog v-model="dialog" max-width="500px">
    <template v-slot:activator="{ on }">
      <v-btn color="primary" dark class="mb-2" v-on="on">New Channel</v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="headline">新規作成</span>
      </v-card-title>

      <v-form ref="form" v-model="valid" lazy-validation>
        <v-card-text>
          <v-container grid-list-md>
            <v-text-field
              :rules="rules.name"
              v-model="editedChannel.name"
              label="名前"
            ></v-text-field>
            <v-text-field
              v-model="editedChannel.description"
              label="説明"
            ></v-text-field>
          </v-container>
        </v-card-text>
      </v-form>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" flat @click="close">Cancel</v-btn>
        <v-btn color="blue darken-1" flat @click="save">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { CREATE_CHANNEL } from '@/graphql/queries';

@Component({})
export default class CreateChannelDialog extends Vue {
  $refs!: {
    form: HTMLFormElement;
  };

  dialog = false;
  defaultEditedChannel = { name: '', description: '' };
  editedChannel = Object.assign({}, this.defaultEditedChannel);
  valid = true;
  errors: { field: string; messages: string[] }[] = [];

  validate_error(field: string): string | boolean {
    var error = this.errors.find(i => i.field == field);
    if (error) {
      return error.messages.join('\n');
    } else {
      return true;
    }
  }

  readonly rules = {
    name: [
      (value: string) => !!value || 'Required.',
      () => this.validate_error('name'),
    ],
  };

  close() {
    this.dialog = false;
    setTimeout(() => {
      this.editedChannel = Object.assign({}, this.defaultEditedChannel);
    }, 300);
  }

  save() {
    this.errors = [];
    if (this.$refs.form.validate()) {
      this.$apollo
        .mutate({
          mutation: CREATE_CHANNEL,
          variables: {
            name: this.editedChannel.name,
            description: this.editedChannel.description,
          },
        })
        .then(({ data: { createChannel: { channel, errors } } }) => {
          if (channel) {
            this.close();
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
}
</script>

<style></style>
