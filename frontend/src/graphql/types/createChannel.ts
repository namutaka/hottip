/* tslint:disable */
/* eslint-disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: createChannel
// ====================================================

export interface createChannel_createChannel_channel {
  /**
   * The ID of the object.
   */
  id: string;
}

export interface createChannel_createChannel_errors {
  field: string;
  messages: string[];
}

export interface createChannel_createChannel {
  channel: createChannel_createChannel_channel | null;
  errors: createChannel_createChannel_errors[];
}

export interface createChannel {
  createChannel: createChannel_createChannel | null;
}

export interface createChannelVariables {
  name: string;
  description?: string | null;
}
