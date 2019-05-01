/* tslint:disable */
/* eslint-disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: updateChannel
// ====================================================

export interface updateChannel_result_channel {
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

export interface updateChannel_result_errors {
  field: string;
  messages: string[];
}

export interface updateChannel_result {
  channel: updateChannel_result_channel | null;
  errors: updateChannel_result_errors[];
}

export interface updateChannel {
  result: updateChannel_result | null;
}

export interface updateChannelVariables {
  id: string;
  name?: string | null;
  description?: string | null;
}
