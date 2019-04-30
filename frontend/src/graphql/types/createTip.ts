/* tslint:disable */
/* eslint-disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: createTip
// ====================================================

export interface createTip_result_tip {
  /**
   * The ID of the object.
   */
  id: string;
  title: string;
  text: string;
  enable: boolean;
}

export interface createTip_result_errors {
  field: string;
  messages: string[];
}

export interface createTip_result {
  tip: createTip_result_tip | null;
  errors: createTip_result_errors[];
}

export interface createTip {
  result: createTip_result | null;
}

export interface createTipVariables {
  channelId: string;
  title: string;
  text?: string | null;
  enable?: boolean | null;
}
