/* tslint:disable */
/* eslint-disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: updateTip
// ====================================================

export interface updateTip_result_tip {
  /**
   * The ID of the object.
   */
  id: string;
  title: string;
  text: string;
  enable: boolean;
}

export interface updateTip_result_errors {
  field: string;
  messages: string[];
}

export interface updateTip_result {
  tip: updateTip_result_tip | null;
  errors: updateTip_result_errors[];
}

export interface updateTip {
  result: updateTip_result | null;
}

export interface updateTipVariables {
  id: string;
  title?: string | null;
  text?: string | null;
  enable?: boolean | null;
}
