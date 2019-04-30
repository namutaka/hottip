/* tslint:disable */
/* eslint-disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: createChannel
// ====================================================

export interface createChannel_createChannel_channel {
  __typename: "ChannelNode";
  /**
   * The ID of the object.
   */
  id: string;
}

export interface createChannel_createChannel_errors {
  __typename: "ErrorType";
  field: string;
  messages: string[];
}

export interface createChannel_createChannel {
  __typename: "CreateChannel";
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
