const fs = require('fs')
const path = require('path')

let env = {}

if (process.env.NODE_ENV) {
  configPath = path.join(__dirname, 'envs', `${process.env.NODE_ENV}.json`)
  if (fs.existsSync(configPath)) {
    env = JSON.parse(fs.readFileSync(configPath))
  }
}

module.exports = {
  mode: 'universal',
  router: {
    base: '/election-board-map/'
  },
  env,
  /*
  ** Headers of the page
  */
  head: {
    title: '看板追追追地圖',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '看板追追追地圖' }
    ],
    link: []
  },

  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },

  /*
  ** Global CSS
  */
  css: [
    'tachyons/css/tachyons.css',
    'leaflet/dist/leaflet.css',
  ],

  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    { src: '~/plugins/hexbin', ssr: false },
    '~/plugins/routeParams',
  ],

  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://github.com/nuxt-community/axios-module#usage
    '@nuxtjs/axios',
    '@nuxtjs/font-awesome',
    [
      '@nuxtjs/google-analytics',
      {
        id: 'UA-129581083-1'
      }
    ],
    '@/modules/sentry',
    'nuxt-leaflet'
  ],
  /*
  ** Axios module configuration
  */
  axios: {
    // See https://github.com/nuxt-community/axios-module#options
  },

  /*
  ** Build configuration
  */
  build: {
    /*
    ** You can extend webpack config here
    */
    extend(config, ctx) {
      // Run ESLint on save
      if (ctx.isDev && ctx.isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        })

        config.devtool = '#source-map'
      }
    }
  }
}
