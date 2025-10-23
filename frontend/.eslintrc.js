module.exports = {
  extends: [
    'react-app',
    'react-app/jest'
  ],
  rules: {
    'jsx-a11y/anchor-is-valid': 'warn',
    'no-unused-vars': 'warn'
  },
  env: {
    browser: true,
    es6: true,
    node: true
  }
};
