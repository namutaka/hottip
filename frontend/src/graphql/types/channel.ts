/* tslint:disable */
/* eslint-disable */
// This file was automatically generated and should not be edited.

import { DistributorType } from "./../../../types/globalTypes";

// ====================================================
// GraphQL query operation: channel
// ====================================================

export interface channel_channel_tips {
  __typename: "TipNode";
  /**
   * The ID of the object.
   */
  id: string;
  title: string;
  text: string;
  enable: boolean;
}

export interface channel_channel_distributors_attribute {
  __typename: "KeyValue";
  key: string;
  value: string | null;
}

export interface channel_channel_distributors {
  __typename: "DistributorNode";
  /**
   * The ID of the object.
   */
  id: string;
  type: DistributorType;
  schedule: string;
  tipsCount: number;
  attribute: channel_channel_distributors_attribute[];
}

export interface channel_channel {
  __typename: "ChannelNode";
  /**
   * The ID of the object.
   */
  id: string;
  rawId: number | null;
  name: string;
  description: string;
  createdAt: any;
  updatedAt: any;
  tips: channel_channel_tips[];
  distributors: channel_channel_distributors[];
}

export interface channel {
  /**
   * The ID of the object
   */
  channel: channel_channel | null;
}

export interface channelVariables {
  id: string;
}
