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
