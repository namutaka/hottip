import gql from 'graphql-tag';

export const ALL_CHANNELS = gql`
  query allChannels {
    allChannels(first: 10) {
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

export const CREATE_CHANNEL = gql`
  mutation createChannel($name: String!, $description: String) {
    createChannel(name: $name, description: $description) {
      channel {
        id
        name
        description
      }
      errors {
        field
        messages
      }
    }
  }
`;
