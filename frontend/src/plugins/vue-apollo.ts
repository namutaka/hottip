import Vue from 'vue';
import VueApollo from 'vue-apollo';
import {
  createApolloClient,
  restartWebsockets,
} from 'vue-cli-plugin-apollo/graphql-client';
import Cookies from 'js-cookie';
import { setContext } from 'apollo-link-context';
import { onError } from "apollo-link-error";

// Install the vue plugin
Vue.use(VueApollo);

// Name of the localStorage item
const AUTH_TOKEN = 'hottip-token';

// Http endpoint
const httpEndpoint: string | undefined = process.env.VUE_APP_GRAPHQL_HTTP;

const LOGIN_URL = '/admin/login/';

const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors)
    graphQLErrors.map(({ message, locations, path }) =>
      console.log(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`
      )
    );
  if (networkError) {
    // @ts-ignore
    const statusCode = networkError.statusCode || -1;
    console.log(`[Network error]: status=${statusCode} ${networkError}`);

    if (statusCode == 403) {
      const url = window.location.pathname + window.location.search;
      window.location.href = `${LOGIN_URL}?next=${encodeURIComponent(url)}`;
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
  link: errorLink.concat(setContext((_, { headers }) => {
    return {
      headers: {
        ...headers,
        'X-CSRFToken': Cookies.get('csrftoken'),
        'X-Requested-With': 'XMLHttpRequest',
      },
    };
  })),

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
    errorHandler(error) {
      // eslint-disable-next-line no-console
      console.log(
        '%cError',
        'background: red; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;',
        error.message,
      );
    },
  });

  return apolloProvider;
}

// Manually call this when user log in
export async function onLogin(apolloClient: any, token: string) {
  if (typeof localStorage !== 'undefined' && token) {
    localStorage.setItem(AUTH_TOKEN, token);
  }
  if (apolloClient.wsClient) restartWebsockets(apolloClient.wsClient);
  try {
    await apolloClient.resetStore();
  } catch (e) {
    // eslint-disable-next-line no-console
    console.log('%cError on cache reset (login)', 'color: orange;', e.message);
  }
}

// Manually call this when user log out
export async function onLogout(apolloClient: any) {
  if (typeof localStorage !== 'undefined') {
    localStorage.removeItem(AUTH_TOKEN);
  }
  if (apolloClient.wsClient) restartWebsockets(apolloClient.wsClient);
  try {
    await apolloClient.resetStore();
  } catch (e) {
    // eslint-disable-next-line no-console
    console.log('%cError on cache reset (logout)', 'color: orange;', e.message);
  }
}
