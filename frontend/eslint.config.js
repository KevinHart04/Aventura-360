import js from "@eslint/js";
import comments from "@eslint-community/eslint-plugin-eslint-comments";
import prettier from "eslint-config-prettier";
import jsxA11y from "eslint-plugin-jsx-a11y";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import vitest from "@vitest/eslint-plugin";
import globals from "globals";
import tseslint from "typescript-eslint";

export default tseslint.config(
  { ignores: ["dist", "coverage", "playwright-report", "test-results"] },

  js.configs.recommended,
  tseslint.configs.strictTypeChecked,
  tseslint.configs.stylisticTypeChecked,
  jsxA11y.flatConfigs.recommended,

  {
    languageOptions: {
      globals: globals.browser,
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    plugins: {
      "@eslint-community/eslint-comments": comments,
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
    },
    rules: {
      // Anti-trampa: ningún comentario eslint-* (disable, enable, etc.)
      "@eslint-community/eslint-comments/no-use": ["error", { allow: [] }],
      "@typescript-eslint/ban-ts-comment": [
        "error",
        {
          "ts-ignore": true,
          "ts-nocheck": true,
          "ts-check": false,
          "ts-expect-error": "allow-with-description",
          minimumDescriptionLength: 15,
        },
      ],

      // Calidad
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "error",
      "react-refresh/only-export-components": [
        "error",
        { allowConstantExport: true },
      ],
      "no-console": "error",
      eqeqeq: "error",
      complexity: ["error", 10],
      "max-lines": [
        "error",
        { max: 300, skipBlankLines: true, skipComments: true },
      ],
      "max-lines-per-function": [
        "error",
        { max: 60, skipBlankLines: true, skipComments: true },
      ],
      "@typescript-eslint/consistent-type-imports": "error",
    },
  },

  // Archivos JS de configuración: sin reglas que requieren tipos
  {
    files: ["**/*.js"],
    extends: [tseslint.configs.disableTypeChecked],
    languageOptions: { globals: globals.node },
  },

  // Tests unitarios
  {
    files: ["src/**/*.test.{ts,tsx}"],
    plugins: { vitest },
    rules: {
      "vitest/no-disabled-tests": "error",
      "vitest/no-focused-tests": "error",
      "vitest/expect-expect": "error",
      "vitest/no-conditional-expect": "error",
      "vitest/no-identical-title": "error",
      "vitest/valid-expect": "error",
      "max-lines-per-function": "off",
    },
  },

  // E2E (Playwright): prohibir skip/only/fixme
  {
    files: ["e2e/**/*.ts"],
    rules: {
      "no-restricted-properties": [
        "error",
        {
          object: "test",
          property: "skip",
          message: "Prohibido saltar tests.",
        },
        { object: "test", property: "only", message: "Prohibido test.only." },
        { object: "test", property: "fixme", message: "Prohibido test.fixme." },
      ],
    },
  },

  prettier, // siempre al final
);
