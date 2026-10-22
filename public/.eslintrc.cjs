// Existing scripts had no ESLint configuration. Start with syntax checks for
// legacy files and recommended correctness rules for the new rollover script.
module.exports = {
    root: true,
    env: { browser: true, es2021: true },
    parserOptions: { ecmaVersion: 2022, sourceType: 'module' },
    overrides: [
        {
            files: ['js/components/daily-refresh.js'],
            extends: ['eslint:recommended'],
        },
    ],
};
