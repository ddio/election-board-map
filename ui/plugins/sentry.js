import Vue from 'vue';
import * as Sentry from '@sentry/browser'

const SentryPlugin = {
  install (Vue) {
    Sentry.init({
      dsn: process.env.sentry.publicDSN,
      integrations: [new Sentry.Integrations.Vue({ Vue })]
    })
    Vue.prototype.$sentry = {
      self: Sentry,
      setUser: (user) => {
        Sentry.configureScope(scope => {
          scope.setUser(user)
        })
      }
    }
  }
}

Vue.use(SentryPlugin)
