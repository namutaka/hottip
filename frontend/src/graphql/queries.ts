import gql from 'graphql-tag';

export const ALL_CHANNELS = gql`
  query allChannels {
    allChannels(first: 50) {
      edges {
        node {
          id
          rawId
          name
          description
          createdAt
          updatedAt
        }
        cursor
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
`;

export const CHANNEL = gql`
  query channel($id: ID!) {
    channel(id: $id) {
      id
      rawId
      name
      description
      createdAt
      updatedAt

      tips {
        id
        title
        text
        enable
      }

      distributors {
        id
        type
        schedule
        tipsCount
        attribute {
          key
          value
        }
      }
    }
  }
`;

export const CREATE_CHANNEL = gql`
  mutation createChannel($name: String!, $description: String) {
    createChannel(name: $name, description: $description) {
      channel {
        id
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const CREATE_TIP = gql`
  mutation createTip($channelId: ID!, $title: String!, $text: String, $enable: Boolean) {
    result: createTip(channelId: $channelId, title: $title, text: $text, enable: $enable) {
      tip {
        id
        title
        text
        enable
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const UPDATE_TIP = gql`
  mutation updateTip($id: ID!, $title: String, $text: String, $enable: Boolean) {
    result: updateTip(id: $id, title: $title, text: $text, enable: $enable) {
      tip {
        id
        title
        text
        enable
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const DELETE_TIP = gql`
  mutation deleteTip($id: ID!) {
    deleteTip(id: $id) {
      ok
    }
  }
`;

export const CREATE_DISTRIBUTOR = gql`
  mutation createDistributor(
      $channelId: ID!,
      $schedule: String,
      $type: String!,
      $attribute: [KeyValueInput!]!,
      $tipsCount: Int) {
    result: createDistributor(
        channelId: $channelId,
        schedule: $schedule,
        type:  $type,
        attribute: $attribute,
        tipsCount: $tipsCount
    ) {
      distributor {
        id
        type
        schedule
        tipsCount
        attribute {
          key
          value
        }
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const UPDATE_DISTRIBUTOR = gql`
  mutation updateDistributor(
      $id: ID!,
      $schedule: String,
      $type: String,
      $attribute: [KeyValueInput!],
      $tipsCount: Int) {
    result: updateDistributor(
        id: $id,
        schedule: $schedule,
        type: $type,
        attribute: $attribute,
        tipsCount: $tipsCount
    ) {
      distributor {
        id
        type
        schedule
        tipsCount
        attribute {
          key
          value
        }
      }
      errors {
        field
        messages
      }
    }
  }
`;

export const DELETE_DISTRIBUTOR = gql`
  mutation deleteDistributor($id: ID!) {
    deleteDistributor(id: $id) {
      ok
    }
  }
`;
