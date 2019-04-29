//
// vue.confg.js
//

module.exports = {
  devServer: {
    proxy: {
      '^/(graphql|admin|static)': {
        target: 'http://localhost:8080',
        changeOrigin: true
      }
    }
  },
  configureWebpack: {
    devtool: 'source-map'
  }
}