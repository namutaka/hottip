/* tslint:disable */
/* eslint-disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: allChannels
// ====================================================

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
}

export interface allChannels_allChannels_edges {
  /**
   * The item at the end of the edge
   */
  node: allChannels_allChannels_edges_node | null;
  /**
   * A cursor for use in pagination
   */
  cursor: string;
}

export interface allChannels_allChannels_pageInfo {
  /**
   * When paginating forwards, the cursor to continue.
   */
  endCursor: string | null;
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
