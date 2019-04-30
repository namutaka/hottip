/* tslint:disable */
/* eslint-disable */
// This file was automatically generated and should not be edited.

import { KeyValueInput, DistributorType } from "./../../../types/globalTypes";

// ====================================================
// GraphQL mutation operation: updateDistributor
// ====================================================

export interface updateDistributor_result_distributor_attribute {
  __typename: "KeyValue";
  key: string;
  value: string | null;
}

export interface updateDistributor_result_distributor {
  __typename: "DistributorNode";
  /**
   * The ID of the object.
   */
  id: string;
  type: DistributorType;
  schedule: string;
  tipsCount: number;
  attribute: updateDistributor_result_distributor_attribute[];
}

export interface updateDistributor_result_errors {
  __typename: "ErrorType";
  field: string;
  messages: string[];
}

export interface updateDistributor_result {
  __typename: "UpdateDistributor";
  distributor: updateDistributor_result_distributor | null;
  errors: updateDistributor_result_errors[];
}

export interface updateDistributor {
  result: updateDistributor_result | null;
}

export interface updateDistributorVariables {
  id: string;
  schedule?: string | null;
  type?: string | null;
  attribute?: KeyValueInput[] | null;
  tipsCount?: number | null;
}
