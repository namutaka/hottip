/* tslint:disable */
/* eslint-disable */
// This file was automatically generated and should not be edited.

import { DistributorType } from "./../../../types/globalTypes";

// ====================================================
// GraphQL query operation: allChannels
// ====================================================

export interface allChannels_allChannels_edges_node_distributors_attribute {
  key: string;
  value: string | null;
}

export interface allChannels_allChannels_edges_node_distributors {
  type: DistributorType;
  attribute: allChannels_allChannels_edges_node_distributors_attribute[];
}

export interface allChannels_allChannels_edges_node {
  /**
   * The ID of the object.
   */
  id: string;
  rawId: number | null;
  name: string;
  description: string;
  createdAt: any;
  updatedAt: any;
  distributors: allChannels_allChannels_edges_node_distributors[];
}

export interface allChannels_allChannels_edges {
  /**
   * The item at the end of the edge
   */
  node: allChannels_allChannels_edges_node | null;
}

export interface allChannels_allChannels_pageInfo {
  /**
   * When paginating backwards, the cursor to continue.
   */
  startCursor: string | null;
  /**
   * When paginating forwards, the cursor to continue.
   */
  endCursor: string | null;
  /**
   * When paginating backwards, are there more items?
   */
  hasPreviousPage: boolean;
  /**
   * When paginating forwards, are there more items?
   */
  hasNextPage: boolean;
}

export interface allChannels_allChannels {
  edges: (allChannels_allChannels_edges | null)[];
  pageInfo: allChannels_allChannels_pageInfo;
}

export interface allChannels {
  allChannels: allChannels_allChannels | null;
}

export interface allChannelsVariables {
  count?: number | null;
  cursor?: string | null;
  name?: string | null;
}
