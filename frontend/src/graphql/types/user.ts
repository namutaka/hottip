/* tslint:disable */
/* eslint-disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: user
// ====================================================

export interface user_user {
  id: string;
  /**
   * この項目は必須です。半角アルファベット、半角数字、@/./+/-/_ で150文字以下にしてください。
   */
  username: string;
  email: string;
}

export interface user {
  user: user_user | null;
}
