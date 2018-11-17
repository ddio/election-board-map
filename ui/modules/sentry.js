const path = require('path')

module.exports = function (options)  {
  const sentryOpt = this.options.env.sentry

  if (sentryOpt && sentryOpt.publicDSN) {
    const sentryPlugin = path.resolve(__dirname, '../plugins/sentry.js')
    this.addPlugin(sentryPlugin, {
      publicDSN: sentryOpt.publicDSN
    })
  }
}
