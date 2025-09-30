module.exports = {
  'packages/frontend/**/*.{js,jsx,ts,tsx}': [
    'eslint --fix',
    'prettier --write',
  ],
  'packages/backend/**/*.py': [
    'black',
    'isort',
  ],
  '**/*.{json,md,yml,yaml}': [
    'prettier --write',
  ],
}
