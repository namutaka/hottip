/* tslint:disable */
/* eslint-disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: createChannel
// ====================================================

export interface createChannel_result_channel {
  /**
   * The ID of the object.
   */
  id: string;
  rawId: number | null;
  name: string;
  description: string;
  createdAt: any;
  updatedAt: any;
}

export interface createChannel_result_errors {
  field: string;
  messages: string[];
}

export interface createChannel_result {
  channel: createChannel_result_channel | null;
  errors: createChannel_result_errors[];
}

export interface createChannel {
  result: createChannel_result | null;
}

export interface createChannelVariables {
  name: string;
  description?: string | null;
}
