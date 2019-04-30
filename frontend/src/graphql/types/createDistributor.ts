/* tslint:disable */
/* eslint-disable */
// This file was automatically generated and should not be edited.

import { KeyValueInput, DistributorType } from "./../../../types/globalTypes";

// ====================================================
// GraphQL mutation operation: createDistributor
// ====================================================

export interface createDistributor_result_distributor_attribute {
  key: string;
  value: string | null;
}

export interface createDistributor_result_distributor {
  /**
   * The ID of the object.
   */
  id: string;
  type: DistributorType;
  schedule: string;
  tipsCount: number;
  attribute: createDistributor_result_distributor_attribute[];
}

export interface createDistributor_result_errors {
  field: string;
  messages: string[];
}

export interface createDistributor_result {
  distributor: createDistributor_result_distributor | null;
  errors: createDistributor_result_errors[];
}

export interface createDistributor {
  result: createDistributor_result | null;
}

export interface createDistributorVariables {
  channelId: string;
  schedule?: string | null;
  type: string;
  attribute: KeyValueInput[];
  tipsCount?: number | null;
}
