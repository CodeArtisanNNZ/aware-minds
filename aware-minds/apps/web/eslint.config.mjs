import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
export default [
  {ignores:['dist/**','node_modules/**','test-results/**','screenshots/**']},
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  {files:['src/**/*.{ts,tsx}','e2e/**/*.ts','playwright.config.ts'],rules:{'no-undef':'off'}}
];
