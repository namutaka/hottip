import Vue from 'vue';
import VueApollo from 'vue-apollo';
import { createApolloClient } from 'vue-cli-plugin-apollo/graphql-client';
import Cookies from 'js-cookie';
import { setContext } from 'apollo-link-context';
import { onError } from 'apollo-link-error';
import router from '@/router';

// Install the vue plugin
Vue.use(VueApollo);

// Name of the localStorage item
const AUTH_TOKEN = 'hottip-token';

// Http endpoint
const httpEndpoint = '/graphql';

// error handling
const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors)
    graphQLErrors.map(({ message, locations, path }) =>
      console.log(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`,
      ),
    );
  if (networkError) {
    // @ts-ignore
    const statusCode = networkError.statusCode || -1;
    console.log(`[Network error]: status=${statusCode} ${networkError}`);

    if (statusCode == 403) {
      const url = window.location.pathname + window.location.search;
      router.push({ name: 'login', query: { next: url } });
    }
  }
});

// Config
const defaultOptions = {
  // You can use `https` for secure connection (recommended in production)
  httpEndpoint,
  // You can use `wss` for secure connection (recommended in production)
  // Use `null` to disable subscriptions
  wsEndpoint: process.env.VUE_APP_GRAPHQL_WS,
  // LocalStorage token
  tokenName: AUTH_TOKEN,
  // Enable Automatic Query persisting with Apollo Engine
  persisting: false,
  // Use websockets for everything (no HTTP)
  // You need to pass a `wsEndpoint` for this to work
  websocketsOnly: false,
  // Is being rendered on the server?
  ssr: false,

  // Override default apollo link
  // note: don't override httpLink here, specify httpLink options in the
  // httpLinkOptions property of defaultOptions.
  // Djangoのcsrftoken認証対応
  link: errorLink.concat(
    setContext((_, { headers }) => {
      return {
        headers: {
          ...headers,
          'X-CSRFToken': Cookies.get('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest',
        },
      };
    }),
  ),

  // Override default cache
  // cache: myCache

  // Override the way the Authorization header is set
  // getAuth: (tokenName: string) => { }

  // Additional ApolloClient options
  // apollo: { }

  // Client local data (see apollo-link-state)
  // clientState: { resolvers: { ... }, defaults: { ... } }
};

// Call this in the Vue app file
export function createProvider(options = {}) {
  // Create apollo client
  const { apolloClient, wsClient } = createApolloClient({
    ...defaultOptions,
    ...options,
  });
  apolloClient.wsClient = wsClient;

  // Create vue apollo provider
  const apolloProvider = new VueApollo({
    defaultClient: apolloClient,
    defaultOptions: {
      $query: {
        // fetchPolicy: 'cache-and-network',
      },
    },
  });

  return apolloProvider;
}
