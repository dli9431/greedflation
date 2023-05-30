const config = require('./webpack.config.js');

module.exports = (env, argv) => {
  const modifiedConfig = {
    ...config(env, argv),
    // Additional development-specific config goes here
  };

  return modifiedConfig;
};