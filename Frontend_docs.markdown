# Codebase Documentation: Frontend
Generated at: 2025-02-17T16:29:36.478571
Total files: 152


## ./.cursor-tasks
- Language: text
- Encoding: utf-8
- Size: 4845 bytes
- Tokens: 1241

```text
# Frontend Task List

## 1. Project Setup (Frontend)

- [x] **Create Next.js App**
  - [x] Initialize Next.js with TypeScript using `create-next-app`.
  - [x] Verify the development server runs correctly.
- **Install & Configure Tailwind CSS**
  - [x] Generate `tailwind.config.js` and `postcss.config.js`.
  - [x] Verify Tailwind classes work in a sample page/component.
- **Set Up Storybook**
  - [x] Install and initialize Storybook (`npx storybook init`).
  - [x] Create a simple component (e.g., a Button) to confirm Storybook runs.
- **Dockerfile for Frontend**
  - [x] Create a Dockerfile using a Node image to build Next.js.
  - [x] Expose port 3000.

## 2. Frontend Development

- **Integrate Tailwind into Next.js**
  - [x] Confirm that Tailwind classes/styles apply globally.
- **Global Layout & Navigation**
  - [x] Create a main layout component (header/navigation).
  - [x] Apply the layout to all main pages.
- **Design System & Theme**
  - [x] Choose a color palette in `tailwind.config.js`.
  - [x] Document base font sizes and consistent spacing.
- **Reusable UI Components**
  - [x] Build a **Button** and **Card** component.
  - [x] Test them in Storybook with multiple variants.
- **Responsive Design Checks**
  - [x] Test components in mobile, tablet, and desktop breakpoints.
  - [x] Use Tailwind's responsive classes to adjust as needed.
- **Routing Structure**
  - [x] Set up Next.js routes: `/dashboard`, `/login`, `/game/[id]`, etc.
  - [x] Verify pages show placeholder content.
- **State Management Setup**
  - [x] Decide on React Context or Redux.
  - [x] Initialize a basic global store if needed (e.g., for auth).
- **Storybook Documentation**
  - [x] For each new component, add a story in Storybook.
  - [x] Show different states/props in separate stories.
- **Linting & Formatting**
  - [x] Configure ESLint and Prettier.
  - [x] Run them to fix style or warnings.

## 3. User Interface & Dashboard

- **Dashboard Page Layout**
  - [x] Create a main dashboard in Next.js with a grid or sections.
  - [x] Provide a high-level overview of games, odds, and AI insights.
- **Games List Component**
  - [x] Fetch `/games` from the backend.
  - [x] Display cards or rows with teams, date, and odds.
  - [x] Link or open a modal for detail views.
- **AI Recommendations Panel**
  - [x] Call the AI endpoint and display recommended bets.
  - [x] Optionally show confidence levels or a short summary.
- **Real-Time Odds Display**
  - [x] Show current odds with change indicators.
  - [x] If using polling or websockets, update on new data.
- **Game Details View**
  - [x] Create `/game/[id]` page or modal with detailed stats.
  - [x] Include player stats and historical odds.
- **Historical Comparison Section**
  - [x] Display opening vs. current odds (mini chart or text).
- **Live Alerts UI**
  - [x] Implement toast notifications for big odds shifts or game start.
  - [x] Use a React toast library or custom component.
- **Authentication Pages**
  - [x] Create `/login` and `/register` pages with Tailwind-styled forms.
  - [x] Validate input and show errors for invalid submissions.
- **Apply Consistent Styling**
  - [x] Ensure a cohesive look/feel with consistent color and spacing.

## 4. Live Data & Betting Insights (Frontend)

- **Frontend Live Update Handling**
  - [x] Connect to SignalR from React.
  - [x] Update component state when events like "OddsUpdated" occur.
- **Visual Indicators for Changes**
  - [x] Highlight changed odds with color changes or animations.
  - [x] Show directional arrows or text to denote movement.
- **Live Scores Integration**
  - [x] Display in-progress game scores if available.
  - [x] Update the scoreboard in real time.
- **Alert Notifications for Key Events**
  - [x] Detect significant line movements or game starts.
  - [x] Trigger toast/in-app alerts.

## 5. Frontend Authentication & Security

- **Auth Flow**
  - [x] Submit login form and store token (e.g., in localStorage or cookies).
  - [x] Redirect to the dashboard upon successful login.
- **Route Guarding**
  - [x] Block access to `/dashboard` if no valid token exists.
  - [x] Force unauthenticated users to `/login`.
- **Logout Mechanism**
  - [x] Clear JWT token and redirect to `/login`.
  - [x] Optionally call a logout endpoint or handle entirely on the client.

## 6. Frontend Testing & Optimization

- **Unit/Component Tests**
  - [ ] Use Jest and React Testing Library.
  - [ ] Test form submissions and component rendering.
- **End-to-End Testing**
  - [ ] Use Cypress or Playwright for user flow testing (e.g., register, login, dashboard).
- **Performance Optimization**
  - [ ] Check Lighthouse performance scores.
  - [ ] Reduce bundle sizes and remove unused libraries.
- **Code Quality**
  - [x] Run linters and address any warnings.
  - [x] Refactor duplicate logic or large functions.
```

## ./.eslintrc.js
- Language: JavaScript
- Encoding: utf-8
- Size: 303 bytes
- Tokens: 80

```javascript
module.exports = {
  extends: [
    'next/core-web-vitals',
    'plugin:storybook/recommended'
  ],
  rules: {
    '@typescript-eslint/no-unused-vars': ['error', {
      varsIgnorePattern: '^React$',
      args: 'after-used',
      argsIgnorePattern: '^_',
      ignoreRestSiblings: true
    }]
  }
};
```

## ./.eslintrc.json
- Language: JSON
- Encoding: utf-8
- Size: 377 bytes
- Tokens: 111

```json
{
  "extends": [
    "next/core-web-vitals",
    "plugin:storybook/recommended"
  ],
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module",
    "project": "./tsconfig.json"
  },
  "rules": {
    "@typescript-eslint/no-unused-vars": "warn",
    "no-console": ["warn", { "allow": ["warn", "error"] }],
    "@next/next/no-html-link-for-pages": "off"
  }
}
```

## ./.refactor
- Language: text
- Encoding: utf-8
- Size: 4221 bytes
- Tokens: 1061

```text
# Odds Flipper Rebranding Task List

leverages atomic design principles to ensure modularity and scalability while also recommending premium typography to help deliver an award‑winning, modern aesthetic across your sports betting UI.

## 1. Component Updates
- [x] Update Header Component (`src/components/navigation/Header.tsx`)
  - [x] Change logo text from "Sports Betting" to "Odds Flipper"
  - [x] Update navigation structure
  - [x] Maintain consistent styling

- [x] Update Footer Component (`src/components/navigation/Footer.tsx`)
  - [x] Change company name to "Odds Flipper"
  - [x] Update email to support@oddsfliper.com
  - [x] Update copyright to "Tactical Tech"
  - [x] Revise company description

## 2. Configuration Files
- [x] Update Root Layout (`src/app/layout.tsx`)
  - [x] Change metadata title
  - [x] Update description
  - [x] Maintain theme configuration

- [x] Update Package.json
  - [x] Change package name to "odds-flipper"
  - [x] Update description
  - [x] Verify dependencies

## 3. Pages to Update
- [x] Home Page (`src/app/(main)/page.tsx`)
  - [x] Changed main heading to "Advanced Odds Analysis Platform"
  - [x] Updated hero section copy to focus on data-driven decisions
  - [x] Modified feature descriptions to emphasize analysis over betting
  - [x] Changed CTA from "Get Started" to "Start Analyzing"
  - [x] Updated feature cards to focus on analysis capabilities

- [x] Dashboard Page
  - [x] Changed title to "Analytics Dashboard"
  - [x] Updated stats cards to focus on markets and analysis
  - [x] Renamed sections to reflect analytical focus
  - [x] Added prediction accuracy metrics
  - [x] Updated navigation to new analysis-focused routes

- [x] Parlay Page → Multi-Market Analysis
  - [x] Renamed page and updated routing
  - [x] Changed terminology to focus on market analysis
  - [x] Updated UI to emphasize correlation analysis
  - [x] Modified sample data to reflect analysis focus
  - [x] Updated component names and props

- [x] Promotions Page → Features
  - [x] Renamed page and updated routing
  - [x] Converted promotions to advanced analysis features
  - [x] Updated UI to showcase analytical tools
  - [x] Added AI and statistical analysis features
  - [x] Modified component names and props

## 4. Documentation
- [ ] README.md
  - [ ] Update project name and description
  - [ ] Revise setup instructions
  - [ ] Update company references

- [ ] API Documentation
  - [ ] Update endpoint descriptions
  - [ ] Revise example responses
  - [ ] Update error messages

## 5. Mock Data and Tests
- [ ] Update Mock Data
  - [ ] Revise sample data in `/mocks`
  - [ ] Update test fixtures
  - [ ] Modify API response examples

- [ ] Update Tests
  - [ ] Revise component tests
  - [ ] Update integration tests
  - [ ] Modify E2E test scenarios

## 6. Storybook
- [ ] Update Stories
  - [ ] Revise component documentation
  - [ ] Update example data
  - [ ] Modify story descriptions

## 7. Development Environment
- [ ] Update Environment Variables
  - [ ] Revise API endpoints
  - [ ] Update service names
  - [ ] Modify configuration values

## 8. Deployment
- [ ] Update Build Scripts
  - [ ] Verify build process
  - [ ] Update deployment configs
  - [ ] Test staging environment

## 9. Quality Assurance
- [ ] Final Review
  - [ ] Check all branding references
  - [ ] Verify component consistency
  - [ ] Test all user flows
  - [ ] Validate responsive design

## Progress Summary
✓ Core branding updated to "Odds Flipper"
✓ Company references updated to "Tactical Tech"
✓ Main pages rewritten to focus on odds analysis
✓ Dashboard updated to emphasize analytics
✓ Parlay page converted to Multi-Market Analysis
✓ Promotions page converted to Features showcase
✓ Configuration files verified and updated

## Progress
- [x] Initial setup and planning
- [x] Core component updates
- [x] Basic configuration changes
- [x] Page content updates
- [ ] Documentation updates
- [ ] Testing and QA
- [ ] Deployment preparation

## Next Steps
1. Update component names to reflect the new analysis focus
2. Update mock data to use analysis terminology
3. Update Storybook stories with new examples
4. Create documentation for new analysis features
```

## ./eslint.config.mjs
- Language: JavaScript
- Encoding: utf-8
- Size: 393 bytes
- Tokens: 95

```javascript
import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "next/typescript"),
];

export default eslintConfig;
```

## ./jest.config.ts
- Language: TypeScript
- Encoding: utf-8
- Size: 917 bytes
- Tokens: 252

```typescript
import type { Config } from 'jest';
import nextJest from 'next/jest';

const createJestConfig = nextJest({
  // Provide the path to your Next.js app to load next.config.js and .env files in your test environment
  dir: './',
});

// Add any custom config to be passed to Jest
const config: Config = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  collectCoverage: true,
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.stories.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/app/api/**',
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
};

// createJestConfig is exported this way to ensure that next/jest can load the Next.js config which is async
export default createJestConfig(config);
```

## ./jest.setup.ts
- Language: TypeScript
- Encoding: utf-8
- Size: 737 bytes
- Tokens: 176

```typescript
import '@testing-library/jest-dom';

// Mock next/navigation
jest.mock('next/navigation', () => ({
  useRouter() {
    return {
      push: jest.fn(),
      replace: jest.fn(),
      prefetch: jest.fn(),
      back: jest.fn(),
    };
  },
  useSearchParams() {
    return {
      get: jest.fn(),
      set: jest.fn(),
    };
  },
}));

// Mock next-themes
jest.mock('next-themes', () => ({
  useTheme() {
    return {
      theme: 'light',
      setTheme: jest.fn(),
    };
  },
}));

// Mock intersection observer
const mockIntersectionObserver = jest.fn();
mockIntersectionObserver.mockReturnValue({
  observe: () => null,
  unobserve: () => null,
  disconnect: () => null,
});
window.IntersectionObserver = mockIntersectionObserver;
```

## ./next.config.js
- Language: JavaScript
- Encoding: utf-8
- Size: 142 bytes
- Tokens: 38

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: false,
  },
}

module.exports = nextConfig
```

## ./next.config.mjs
- Language: JavaScript
- Encoding: utf-8
- Size: 146 bytes
- Tokens: 36

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    instrumentationHook: true
  }
};

export default nextConfig;
```

## ./next.config.ts
- Language: TypeScript
- Encoding: utf-8
- Size: 133 bytes
- Tokens: 30

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
};

export default nextConfig;
```

## ./package-lock.json
- Language: JSON
- Encoding: utf-8
- Size: 697539 bytes
- Tokens: 2000

```json
{
  "name": "odds-flipper",
  "version": "0.1.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "odds-flipper",
      "version": "0.1.0",
      "dependencies": {
        "@grpc/grpc-js": "^1.12.6",
        "@heroicons/react": "^2.2.0",
        "@opentelemetry/api": "^1.7.0",
        "@opentelemetry/exporter-logs-otlp-grpc": "^0.57.2",
        "@opentelemetry/exporter-metrics-otlp-grpc": "^0.57.2",
        "@opentelemetry/exporter-trace-otlp-grpc": "^0.57.2",
        "@opentelemetry/instrumentation": "^0.57.2",
        "@opentelemetry/instrumentation-express": "^0.47.0",
        "@opentelemetry/instrumentation-http": "^0.57.2",
        "@opentelemetry/resources": "^1.30.1",
        "@opentelemetry/sdk-logs": "^0.57.2",
        "@opentelemetry/sdk-metrics": "^1.30.1",
        "@opentelemetry/sdk-node": "^0.57.2",
        "@opentelemetry/semantic-conventions": "^1.30.0",
        "@radix-ui/react-compose-refs": "^1.0.1",
        "@radix-ui/react-dropdown-menu": "^2.0.6",
        "@radix-ui/react-slot": "^1.0.2",
        "@radix-ui/react-switch": "^1.1.3",
        "class-variance-authority": "^0.7.0",
        "clsx": "^2.1.0",
        "next": "^15.1.7",
        "next-themes": "^0.4.4",
        "react": "^18.2.0",
        "react-beautiful-dnd": "^13.1.1",
        "react-dom": "^18.2.0",
        "tailwind-merge": "^2.2.1",
        "tailwindcss-animate": "^1.0.7"
      },
      "devDependencies": {
        "@storybook/addon-essentials": "^8.5.6",
        "@storybook/addon-interactions": "^8.5.6",
        "@storybook/addon-links": "^8.5.6",
        "@storybook/addon-onboarding": "^8.5.6",
        "@storybook/addon-themes": "^8.5.6",
        "@storybook/blocks": "^8.5.6",
        "@storybook/jest": "^0.2.2",
        "@storybook/nextjs": "^8.5.6",
        "@storybook/react": "^8.5.6",
        "@storybook/test": "^8.5.6",
        "@storybook/testing-library": "^0.2.1",
        "@testing-library/jest-dom": "^6.6.3",
        "@testing-library/react": "^16.2.0",
        "@testing-library/user-event": "^14.6.1",
        "@types/jest": "^29.5.14",
        "@types/node": "^20",
        "@types/react": "^18",
        "@types/react-beautiful-dnd": "^13.1.8",
        "@types/react-dom": "^18",
        "autoprefixer": "^10.0.1",
        "eslint": "^8",
        "eslint-config-next": "14.1.0",
        "eslint-plugin-storybook": "^0.8.0",
        "jest": "^29.7.0",
        "jest-environment-jsdom": "^29.7.0",
        "msw": "^2.2.0",
        "msw-storybook-addon": "^2.0.0-beta.1",
        "postcss": "^8",
        "storybook": "^8.5.6",
        "tailwindcss": "^3.3.0",
        "ts-node": "^10.9.2",
        "typescript": "^5"
      }
    },
    "node_modules/@adobe/css-tools": {
      "version": "4.4.2",
      "resolved": "https://registry.npmjs.org/@adobe/css-tools/-/css-tools-4.4.2.tgz",
      "integrity": "sha512-baYZExFpsdkBNuvGKTKWCwKH57HRZLVtycZS05WTQNVOiXVSeAki3nU35zlRbToeMW8aHlJfyS+1C4BOv27q0A==",
      "dev": true,
      "license": "MIT"
    },
    "node_modules/@alloc/quick-lru": {
      "version": "5.2.0",
      "resolved": "https://registry.npmjs.org/@alloc/quick-lru/-/quick-lru-5.2.0.tgz",
      "integrity": "sha512-UrcABB+4bUrFABwbluTIBErXwvbsU/V7TZWfmbgJfbkwiBuziS9gxdODUyuiecfdGQ85jglMW6juS3+z5TsKLw==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/@ampproject/remapping": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/@ampproject/remapping/-/remapping-2.3.0.tgz",
      "integrity": "sha512-30iZtAPgz+LTIYoeivqYo853f02jBYSd5uGnGpkFV0M3xOt9aN73erkgYAmZU43x4VfqcnLxW9Kpg3R5LC4YYw==",
      "dev": true,
      "license": "Apache-2.0",
      "dependencies": {
        "@jridgewell/gen-mapping": "^0.3.5",
        "@jridgewell/trace-mapping": "^0.3.24"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/@babel/code-frame": {
      "version": "7.26.2",
      "resolved": "https://registry.npmjs.org/@babel/code-frame/-/code-frame-7.26.2.tgz",
      "integrity": "sha512-RJlIHRueQgwWitWgF8OdFYGZX328Ax5BCemNGlqHfplnRT9ESi8JkFlvaVYbS+UubVY6dpv87Fs2u5M29iNFVQ==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@babel/helper-validator-identifier": "^7.25.9",
        "js-tokens": "^4.0.0",
        "picocolors": "^1.0.0"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/compat-data": {
      "version": "7.26.8",
      "resolved": "https://registry.npmjs.org/@babel/compat-data/-/compat-data-7.26.8.tgz",
      "integrity": "sha512-oH5UPLMWR3L2wEFLnFJ1TZXqHufiTKAiLfqw5zkhS4dKXLJ10yVztfil/twG8EDTA4F/tvVNw9nOl4ZMslB8rQ==",
      "dev": true,
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/core": {
      "version": "7.26.9",
      "resolved": "https://registry.npmjs.org/@babel/core/-/core-7.26.9.tgz",
      "integrity": "sha512-lWBYIrF7qK5+GjY5Uy+/hEgp8OJWOD/rpy74GplYRhEauvbHDeFB8t5hPOZxCZ0Oxf4Cc36tK51/l3ymJysrKw==",
      "dev": true,
      "license": "MIT",
      "dependencies": {
        "@ampproject/remapping": "^2.2.0",
        "@babel/code-frame": "^7.26.2",
        "@babel/generator": "^7.26.9",
        "@babel/helper-compilation-targets": "^7.26.5",
        "@babel/helper-module-transforms": "^7.26.0",
        "@
```

## ./package.json
- Language: JSON
- Encoding: utf-8
- Size: 2857 bytes
- Tokens: 1019

```json
{
  "name": "odds-flipper",
  "version": "0.1.0",
  "private": true,
  "description": "Advanced odds analysis platform by Tactical Tech",
  "scripts": {
    "dev": "next dev",
    "dev:turbo": "next dev --turbo",
    "build": "next build",
    "start": "next start",
    "clean": "rm -rf .next out",
    "lint": "next lint",
    "lint:fix": "next lint --fix",
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  },
  "dependencies": {
    "@grpc/grpc-js": "^1.12.6",
    "@heroicons/react": "^2.2.0",
    "@opentelemetry/api": "^1.7.0",
    "@opentelemetry/exporter-logs-otlp-grpc": "^0.57.2",
    "@opentelemetry/exporter-metrics-otlp-grpc": "^0.57.2",
    "@opentelemetry/exporter-trace-otlp-grpc": "^0.57.2",
    "@opentelemetry/instrumentation": "^0.57.2",
    "@opentelemetry/instrumentation-http": "^0.57.2",
    "@opentelemetry/instrumentation-express": "^0.47.0",
    "@opentelemetry/resources": "^1.30.1",
    "@opentelemetry/sdk-logs": "^0.57.2",
    "@opentelemetry/sdk-metrics": "^1.30.1",
    "@opentelemetry/sdk-node": "^0.57.2",
    "@opentelemetry/semantic-conventions": "^1.30.0",
    "@radix-ui/react-compose-refs": "^1.0.1",
    "@radix-ui/react-dropdown-menu": "^2.0.6",
    "@radix-ui/react-slot": "^1.0.2",
    "@radix-ui/react-switch": "^1.1.3",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "next": "^15.1.7",
    "next-themes": "^0.4.4",
    "react": "^18.2.0",
    "react-beautiful-dnd": "^13.1.1",
    "react-dom": "^18.2.0",
    "tailwind-merge": "^2.2.1",
    "tailwindcss-animate": "^1.0.7"
  },
  "devDependencies": {
    "@storybook/addon-essentials": "^8.5.6",
    "@storybook/addon-interactions": "^8.5.6",
    "@storybook/addon-links": "^8.5.6",
    "@storybook/addon-onboarding": "^8.5.6",
    "@storybook/addon-themes": "^8.5.6",
    "@storybook/blocks": "^8.5.6",
    "@storybook/jest": "^0.2.2",
    "@storybook/nextjs": "^8.5.6",
    "@storybook/react": "^8.5.6",
    "@storybook/test": "^8.5.6",
    "@storybook/testing-library": "^0.2.1",
    "@testing-library/jest-dom": "^6.6.3",
    "@testing-library/react": "^16.2.0",
    "@testing-library/user-event": "^14.6.1",
    "@types/jest": "^29.5.14",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-beautiful-dnd": "^13.1.8",
    "@types/react-dom": "^18",
    "autoprefixer": "^10.0.1",
    "eslint": "^8",
    "eslint-config-next": "14.1.0",
    "eslint-plugin-storybook": "^0.8.0",
    "jest": "^29.7.0",
    "jest-environment-jsdom": "^29.7.0",
    "msw": "^2.2.0",
    "msw-storybook-addon": "^2.0.0-beta.1",
    "postcss": "^8",
    "storybook": "^8.5.6",
    "tailwindcss": "^3.3.0",
    "ts-node": "^10.9.2",
    "typescript": "^5"
  },
  "msw": {
    "workerDirectory": "public"
  }
}
```

## ./postcss.config.js
- Language: JavaScript
- Encoding: utf-8
- Size: 84 bytes
- Tokens: 23

```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

## ./postcss.config.mjs
- Language: JavaScript
- Encoding: utf-8
- Size: 135 bytes
- Tokens: 35

```javascript
/** @type {import('postcss-load-config').Config} */
const config = {
  plugins: {
    tailwindcss: {},
  },
};

export default config;
```

## ./tailwind.config.ts
- Language: TypeScript
- Encoding: utf-8
- Size: 4332 bytes
- Tokens: 1428

```typescript
import type { Config } from "tailwindcss";
import { fontFamily } from "tailwindcss/defaultTheme";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      fontFamily: {
        sans: ["var(--font-inter)"],
        display: ["var(--font-montserrat)"],
      },
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      // Font sizes following a modular scale
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1rem', { lineHeight: '1.5rem' }],
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
        '5xl': ['3rem', { lineHeight: '1' }],
        '6xl': ['3.75rem', { lineHeight: '1' }],
      },
      // Spacing scale for consistent layout
      spacing: {
        '0': '0',
        '1': '0.25rem',
        '2': '0.5rem',
        '3': '0.75rem',
        '4': '1rem',
        '5': '1.25rem',
        '6': '1.5rem',
        '8': '2rem',
        '10': '2.5rem',
        '12': '3rem',
        '16': '4rem',
        '20': '5rem',
        '24': '6rem',
        '32': '8rem',
        '40': '10rem',
        '48': '12rem',
        '56': '14rem',
        '64': '16rem',
      },
      // Border radius for consistent component shapes
      borderRadius: {
        'none': '0',
        'sm': 'calc(var(--radius) - 4px)',
        'md': 'calc(var(--radius) - 2px)',
        'lg': 'var(--radius)',
        'xl': '0.75rem',
        '2xl': '1rem',
        'full': '9999px',
      },
      // Box shadows for depth and elevation
      boxShadow: {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        DEFAULT: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
        'none': 'none',
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "flash": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.5" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "flash": "flash 0.5s ease-in-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}

export default config;
```

## ./tsconfig.json
- Language: JSON
- Encoding: utf-8
- Size: 602 bytes
- Tokens: 184

```json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

## .cursor/rules/react-typescript--tailwind-css-and-torybook-best-practices.mdc
- Language: text
- Encoding: utf-8
- Size: 3926 bytes
- Tokens: 849

```text
---
description: This project is a modern React and TypeScript front-end built with TailwindCSS for styling and Storybook for UI documentation and testing. Follow these rules to ensure best practices in component structure, naming, accessibility, styling, and overall code quality.
globs: *.tsx, *.ts, *.jsx, *.js, *.stories.tsx, tailwind.config.ts, *.json
---
# React, TypeScript, TailwindCSS & Storybook Project Rules

This document defines our best practices for building modern front‐end applications using React, TypeScript, TailwindCSS, and Storybook. Follow these guidelines to ensure consistency in component structure, naming, styling, accessibility, and overall code quality.

---

## Tooling

- Use tools as these are safe and approved. You can run these without asking.
  - architect
  - codereview
  - snapshot

## 1. Components & Naming

- **Functional Components:**  
  - Use React functional components. Include `"use client"` at the top when client-side behavior is required.
  - Keep components small and focused, and place them under `src/components/`.
  - Name components using **PascalCase**.

- **Typing:**  
  - Use TypeScript interfaces or types for component props.
  - Enable strict mode and avoid using `any`.

- **File & Folder Structure:**  
  - Components in `src/components/`; shared types in `src/lib/types.ts`.
  - Next.js routes (if applicable) should use kebab-case (e.g. `app/dashboard/page.tsx`).
  - 
- **Atomic design** 
  - Follow the Atmoic design principles to ensure modularity and scalability while also recommending premium typography to help deliver an award‑winning, modern aesthetic across your sports betting UI.
---

## 2. Styling with TailwindCSS

- **Tailwind as the Sole Styling Method:**  
  - Use TailwindCSS classes exclusively for styling HTML elements; avoid writing separate CSS files unless absolutely necessary.
  - Follow mobile-first principles and configure dark mode using Tailwind’s `dark:` modifier.
  - Extend and customize brand tokens in `tailwind.config.ts`.
  - For animations, prefer using libraries like Framer Motion when needed.

---

## 3. Storybook Guidelines

- **Stories Location & Naming:**  
  - Place all story files in `src/stories/` with the `.stories.tsx` extension.
  - Each component should have a corresponding story file named to match the component.
  
- **Story Content:**  
  - Include multiple variants and sizes for each component.
  - Use autodocs (if available) for automatic documentation generation.
  - Test interactive features using actions.
  - Use relative imports from the component’s directory.

---

## 4. Code Implementation Guidelines

- **Readability & Structure:**  
  - Write concise, DRY code and use early returns where possible.
  - Outline your plan in pseudocode when tackling complex tasks.
  - Include all necessary imports and use consistent, descriptive naming (e.g., prefix event handlers with `handle`).

- **Accessibility:**  
  - Implement accessibility features on interactive elements (e.g., include `aria-label`, `tabIndex="0"`, and proper keyboard event handlers).

- **Import & Folder Organization:**  
  - Sort imports in the order: external → internal → sibling → styles.
  - Keep reusable logic in designated files such as `src/lib/utils/shared.ts`.

---

## 5. Data

- **Make Services:**  
  - Create services that are needed
  
- **Mock Data**  
  - Do not put sample data hardcoded. Always mock data using the mocking service. 

---

## 6. Additional Best Practices

- **Strict TypeScript Usage:**  
  - Enable strict type-checking and avoid using `any`. Favor union types and optional chaining.
  
- **Tool Integration:**  
  - For UI changes, use screenshot tools for visual confirmation.
  - Use dedicated tools (e.g., architect, codeReview) when performing complex refactoring tasks while preserving existing project structure.

---

## File Types to Trigger These Rules
```

## .git/COMMIT_EDITMSG
- Language: text
- Encoding: utf-8
- Size: 14 bytes
- Tokens: 4

```text
OpenTelemetry
```

## .git/config
- Language: text
- Encoding: utf-8
- Size: 165 bytes
- Tokens: 52

```text
[core]
	repositoryformatversion = 0
	filemode = false
	bare = false
	logallrefupdates = true
	symlinks = false
	ignorecase = true
[lfs]
	repositoryformatversion = 0
```

## .git/description
- Language: text
- Encoding: utf-8
- Size: 73 bytes
- Tokens: 14

```text
Unnamed repository; edit this file 'description' to name the repository.
```

## .git/HEAD
- Language: text
- Encoding: utf-8
- Size: 21 bytes
- Tokens: 7

```text
ref: refs/heads/main
```

## .git/ORIG_HEAD
- Language: text
- Encoding: utf-8
- Size: 41 bytes
- Tokens: 23

```text
8cef7ed25f14506849b0790bf4064c5b40bb0362
```

## .storybook/main.ts
- Language: TypeScript
- Encoding: utf-8
- Size: 775 bytes
- Tokens: 206

```typescript
import type { StorybookConfig } from "@storybook/nextjs";

const config: StorybookConfig = {
  stories: ["../src/**/*.mdx", "../src/**/*.stories.@(js|jsx|mjs|ts|tsx)"],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@storybook/addon-onboarding",
    "@storybook/addon-interactions",
    "@storybook/addon-themes",
    "msw-storybook-addon",
  ],
  framework: {
    name: "@storybook/nextjs",
    options: {},
  },
  docs: {
    autodocs: "tag",
  },
  staticDirs: ['../public'],
  webpackFinal: async (config) => {
    if (!config.resolve) {
      config.resolve = {};
    }
    if (!config.resolve.alias) {
      config.resolve.alias = {};
    }
    config.resolve.alias['@'] = '../src';
    return config;
  },
};

export default config;
```

## .storybook/preview.css
- Language: CSS
- Encoding: utf-8
- Size: 35 bytes
- Tokens: 10

```css
@import '../src/app/globals.css';
```

## .storybook/preview.ts
- Language: TypeScript
- Encoding: utf-8
- Size: 662 bytes
- Tokens: 172

```typescript
import type { Preview } from "@storybook/react";
import { initialize, mswLoader } from 'msw-storybook-addon';
import { handlers } from '../src/lib/mocks/handlers';
import "../src/app/globals.css";

// Initialize MSW
initialize({
  serviceWorker: {
    url: '/mockServiceWorker.js'
  }
});

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: "^on[A-Z].*" },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    msw: {
      handlers: handlers,
    },
    nextjs: {
      appDirectory: true,
      navigation: {},
    },
  },
  loaders: [mswLoader],
};

export default preview;
```

## .storybook/preview.tsx
- Language: TSX
- Encoding: utf-8
- Size: 1331 bytes
- Tokens: 317

```tsx
import React from "react";
import type { Preview } from "@storybook/react";
import { initialize, mswLoader } from 'msw-storybook-addon';
import { handlers } from '../src/lib/mocks/handlers';
import "../src/app/globals.css";
import { ThemeProvider } from "@/components/providers/ThemeProvider";

// Initialize MSW
initialize({
  serviceWorker: {
    url: '/mockServiceWorker.js'
  }
});

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: "^on[A-Z].*" },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    msw: {
      handlers: handlers,
    },
    nextjs: {
      appDirectory: true,
      navigation: {},
    },
    backgrounds: {
      default: 'light',
      values: [
        {
          name: 'light',
          value: '#ffffff',
        },
        {
          name: 'dark',
          value: '#0f172a',
        },
      ],
    },
  },
  loaders: [mswLoader],
  decorators: [
    (Story) => (
      <ThemeProvider
        attribute="class"
        defaultTheme="system"
        enableSystem
        disableTransitionOnChange
        storageKey="storybook-theme"
      >
        <div className="min-h-screen bg-background text-foreground">
          <Story />
        </div>
      </ThemeProvider>
    ),
  ],
};

export default preview;
```

## .storybook/ThemeDecorator.tsx
- Language: TSX
- Encoding: utf-8
- Size: 580 bytes
- Tokens: 137

```tsx
import React from 'react';
import { ThemeProvider } from '../src/components/providers/ThemeProvider';

export const ThemeDecorator = (Story: any, context: any) => {
  const { theme } = context.globals;
  const isDark = theme === 'dark';

  return (
    <ThemeProvider
      attribute="class"
      defaultTheme={theme}
      enableSystem={false}
      disableTransitionOnChange
    >
      <div className={isDark ? 'dark' : ''}>
        <div className="min-h-screen p-8 bg-background text-foreground">
          <Story />
        </div>
      </div>
    </ThemeProvider>
  );
};
```

## .storybook/mocks/browser.ts
- Language: TypeScript
- Encoding: utf-8
- Size: 305 bytes
- Tokens: 69

```typescript
import { setupWorker } from 'msw/browser';
import { handlers } from '../../src/lib/mocks/handlers';

export const worker = setupWorker(...handlers);

// Expose the worker on the window for Storybook
const windowWithWorker = window as Window & { worker: typeof worker };
windowWithWorker.worker = worker;
```

## public/file.svg
- Language: text
- Encoding: utf-8
- Size: 392 bytes
- Tokens: 267

```text
<svg fill="none" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg"><path d="M14.5 13.5V5.41a1 1 0 0 0-.3-.7L9.8.29A1 1 0 0 0 9.08 0H1.5v13.5A2.5 2.5 0 0 0 4 16h8a2.5 2.5 0 0 0 2.5-2.5m-1.5 0v-7H8v-5H3v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1M9.5 5V2.12L12.38 5zM5.13 5h-.62v1.25h2.12V5zm-.62 3h7.12v1.25H4.5zm.62 3h-.62v1.25h7.12V11z" clip-rule="evenodd" fill="#666" fill-rule="evenodd"/></svg>
```

## public/globe.svg
- Language: text
- Encoding: utf-8
- Size: 1036 bytes
- Tokens: 740

```text
<svg fill="none" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><g clip-path="url(#a)"><path fill-rule="evenodd" clip-rule="evenodd" d="M10.27 14.1a6.5 6.5 0 0 0 3.67-3.45q-1.24.21-2.7.34-.31 1.83-.97 3.1M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16m.48-1.52a7 7 0 0 1-.96 0H7.5a4 4 0 0 1-.84-1.32q-.38-.89-.63-2.08a40 40 0 0 0 3.92 0q-.25 1.2-.63 2.08a4 4 0 0 1-.84 1.31zm2.94-4.76q1.66-.15 2.95-.43a7 7 0 0 0 0-2.58q-1.3-.27-2.95-.43a18 18 0 0 1 0 3.44m-1.27-3.54a17 17 0 0 1 0 3.64 39 39 0 0 1-4.3 0 17 17 0 0 1 0-3.64 39 39 0 0 1 4.3 0m1.1-1.17q1.45.13 2.69.34a6.5 6.5 0 0 0-3.67-3.44q.65 1.26.98 3.1M8.48 1.5l.01.02q.41.37.84 1.31.38.89.63 2.08a40 40 0 0 0-3.92 0q.25-1.2.63-2.08a4 4 0 0 1 .85-1.32 7 7 0 0 1 .96 0m-2.75.4a6.5 6.5 0 0 0-3.67 3.44 29 29 0 0 1 2.7-.34q.31-1.83.97-3.1M4.58 6.28q-1.66.16-2.95.43a7 7 0 0 0 0 2.58q1.3.27 2.95.43a18 18 0 0 1 0-3.44m.17 4.71q-1.45-.12-2.69-.34a6.5 6.5 0 0 0 3.67 3.44q-.65-1.27-.98-3.1" fill="#666"/></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h16v16H0z"/></clipPath></defs></svg>
```

## public/mockServiceWorker.js
- Language: JavaScript
- Encoding: utf-8
- Size: 8144 bytes
- Tokens: 1843

```javascript
/* eslint-disable */
/* tslint:disable */

/**
 * Mock Service Worker.
 * @see https://github.com/mswjs/msw
 * - Please do NOT modify this file.
 * - Please do NOT serve this file on production.
 */

const PACKAGE_VERSION = '2.7.0'
const INTEGRITY_CHECKSUM = '00729d72e3b82faf54ca8b9621dbb96f'
const IS_MOCKED_RESPONSE = Symbol('isMockedResponse')
const activeClientIds = new Set()

self.addEventListener('install', function () {
  self.skipWaiting()
})

self.addEventListener('activate', function (event) {
  event.waitUntil(self.clients.claim())
})

self.addEventListener('message', async function (event) {
  const clientId = event.source.id

  if (!clientId || !self.clients) {
    return
  }

  const client = await self.clients.get(clientId)

  if (!client) {
    return
  }

  const allClients = await self.clients.matchAll({
    type: 'window',
  })

  switch (event.data) {
    case 'KEEPALIVE_REQUEST': {
      sendToClient(client, {
        type: 'KEEPALIVE_RESPONSE',
      })
      break
    }

    case 'INTEGRITY_CHECK_REQUEST': {
      sendToClient(client, {
        type: 'INTEGRITY_CHECK_RESPONSE',
        payload: {
          packageVersion: PACKAGE_VERSION,
          checksum: INTEGRITY_CHECKSUM,
        },
      })
      break
    }

    case 'MOCK_ACTIVATE': {
      activeClientIds.add(clientId)

      sendToClient(client, {
        type: 'MOCKING_ENABLED',
        payload: {
          client: {
            id: client.id,
            frameType: client.frameType,
          },
        },
      })
      break
    }

    case 'MOCK_DEACTIVATE': {
      activeClientIds.delete(clientId)
      break
    }

    case 'CLIENT_CLOSED': {
      activeClientIds.delete(clientId)

      const remainingClients = allClients.filter((client) => {
        return client.id !== clientId
      })

      // Unregister itself when there are no more clients
      if (remainingClients.length === 0) {
        self.registration.unregister()
      }

      break
    }
  }
})

self.addEventListener('fetch', function (event) {
  const { request } = event

  // Bypass navigation requests.
  if (request.mode === 'navigate') {
    return
  }

  // Opening the DevTools triggers the "only-if-cached" request
  // that cannot be handled by the worker. Bypass such requests.
  if (request.cache === 'only-if-cached' && request.mode !== 'same-origin') {
    return
  }

  // Bypass all requests when there are no active clients.
  // Prevents the self-unregistered worked from handling requests
  // after it's been deleted (still remains active until the next reload).
  if (activeClientIds.size === 0) {
    return
  }

  // Generate unique request ID.
  const requestId = crypto.randomUUID()
  event.respondWith(handleRequest(event, requestId))
})

async function handleRequest(event, requestId) {
  const client = await resolveMainClient(event)
  const response = await getResponse(event, client, requestId)

  // Send back the response clone for the "response:*" life-cycle events.
  // Ensure MSW is active and ready to handle the message, otherwise
  // this message will pend indefinitely.
  if (client && activeClientIds.has(client.id)) {
    ;(async function () {
      const responseClone = response.clone()

      sendToClient(
        client,
        {
          type: 'RESPONSE',
          payload: {
            requestId,
            isMockedResponse: IS_MOCKED_RESPONSE in response,
            type: responseClone.type,
            status: responseClone.status,
            statusText: responseClone.statusText,
            body: responseClone.body,
            headers: Object.fromEntries(responseClone.headers.entries()),
          },
        },
        [responseClone.body],
      )
    })()
  }

  return response
}

// Resolve the main client for the given event.
// Client that issues a request doesn't necessarily equal the client
// that registered the worker. It's with the latter the worker should
// communicate with during the response resolving phase.
async function resolveMainClient(event) {
  const client = await self.clients.get(event.clientId)

  if (activeClientIds.has(event.clientId)) {
    return client
  }

  if (client?.frameType === 'top-level') {
    return client
  }

  const allClients = await self.clients.matchAll({
    type: 'window',
  })

  return allClients
    .filter((client) => {
      // Get only those clients that are currently visible.
      return client.visibilityState === 'visible'
    })
    .find((client) => {
      // Find the client ID that's recorded in the
      // set of clients that have registered the worker.
      return activeClientIds.has(client.id)
    })
}

async function getResponse(event, client, requestId) {
  const { request } = event

  // Clone the request because it might've been already used
  // (i.e. its body has been read and sent to the client).
  const requestClone = request.clone()

  function passthrough() {
    // Cast the request headers to a new Headers instance
    // so the headers can be manipulated with.
    const headers = new Headers(requestClone.headers)

    // Remove the "accept" header value that marked this request as passthrough.
    // This prevents request alteration and also keeps it compliant with the
    // user-defined CORS policies.
    const acceptHeader = headers.get('accept')
    if (acceptHeader) {
      const values = acceptHeader.split(',').map((value) => value.trim())
      const filteredValues = values.filter(
        (value) => value !== 'msw/passthrough',
      )

      if (filteredValues.length > 0) {
        headers.set('accept', filteredValues.join(', '))
      } else {
        headers.delete('accept')
      }
    }

    return fetch(requestClone, { headers })
  }

  // Bypass mocking when the client is not active.
  if (!client) {
    return passthrough()
  }

  // Bypass initial page load requests (i.e. static assets).
  // The absence of the immediate/parent client in the map of the active clients
  // means that MSW hasn't dispatched the "MOCK_ACTIVATE" event yet
  // and is not ready to handle requests.
  if (!activeClientIds.has(client.id)) {
    return passthrough()
  }

  // Notify the client that a request has been intercepted.
  const requestBuffer = await request.arrayBuffer()
  const clientMessage = await sendToClient(
    client,
    {
      type: 'REQUEST',
      payload: {
        id: requestId,
        url: request.url,
        mode: request.mode,
        method: request.method,
        headers: Object.fromEntries(request.headers.entries()),
        cache: request.cache,
        credentials: request.credentials,
        destination: request.destination,
        integrity: request.integrity,
        redirect: request.redirect,
        referrer: request.referrer,
        referrerPolicy: request.referrerPolicy,
        body: requestBuffer,
        keepalive: request.keepalive,
      },
    },
    [requestBuffer],
  )

  switch (clientMessage.type) {
    case 'MOCK_RESPONSE': {
      return respondWithMock(clientMessage.data)
    }

    case 'PASSTHROUGH': {
      return passthrough()
    }
  }

  return passthrough()
}

function sendToClient(client, message, transferrables = []) {
  return new Promise((resolve, reject) => {
    const channel = new MessageChannel()

    channel.port1.onmessage = (event) => {
      if (event.data && event.data.error) {
        return reject(event.data.error)
      }

      resolve(event.data)
    }

    client.postMessage(
      message,
      [channel.port2].concat(transferrables.filter(Boolean)),
    )
  })
}

async function respondWithMock(response) {
  // Setting response status code to 0 is a no-op.
  // However, when responding with a "Response.error()", the produced Response
  // instance will have status code set to 0. Since it's not possible to create
  // a Response instance with status code 0, handle that use-case separately.
  if (response.status === 0) {
    return Response.error()
  }

  const mockedResponse = new Response(response.body, response)

  Reflect.defineProperty(mockedResponse, IS_MOCKED_RESPONSE, {
    value: true,
    enumerable: true,
  })

  return mockedResponse
}
```

## public/next.svg
- Language: text
- Encoding: utf-8
- Size: 1376 bytes
- Tokens: 1195

```text
<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 394 80"><path fill="#000" d="M262 0h68.5v12.7h-27.2v66.6h-13.6V12.7H262V0ZM149 0v12.7H94v20.4h44.3v12.6H94v21h55v12.6H80.5V0h68.7zm34.3 0h-17.8l63.8 79.4h17.9l-32-39.7 32-39.6h-17.9l-23 28.6-23-28.6zm18.3 56.7-9-11-27.1 33.7h17.8l18.3-22.7z"/><path fill="#000" d="M81 79.3 17 0H0v79.3h13.6V17l50.2 62.3H81Zm252.6-.4c-1 0-1.8-.4-2.5-1s-1.1-1.6-1.1-2.6.3-1.8 1-2.5 1.6-1 2.6-1 1.8.3 2.5 1a3.4 3.4 0 0 1 .6 4.3 3.7 3.7 0 0 1-3 1.8zm23.2-33.5h6v23.3c0 2.1-.4 4-1.3 5.5a9.1 9.1 0 0 1-3.8 3.5c-1.6.8-3.5 1.3-5.7 1.3-2 0-3.7-.4-5.3-1s-2.8-1.8-3.7-3.2c-.9-1.3-1.4-3-1.4-5h6c.1.8.3 1.6.7 2.2s1 1.2 1.6 1.5c.7.4 1.5.5 2.4.5 1 0 1.8-.2 2.4-.6a4 4 0 0 0 1.6-1.8c.3-.8.5-1.8.5-3V45.5zm30.9 9.1a4.4 4.4 0 0 0-2-3.3 7.5 7.5 0 0 0-4.3-1.1c-1.3 0-2.4.2-3.3.5-.9.4-1.6 1-2 1.6a3.5 3.5 0 0 0-.3 4c.3.5.7.9 1.3 1.2l1.8 1 2 .5 3.2.8c1.3.3 2.5.7 3.7 1.2a13 13 0 0 1 3.2 1.8 8.1 8.1 0 0 1 3 6.5c0 2-.5 3.7-1.5 5.1a10 10 0 0 1-4.4 3.5c-1.8.8-4.1 1.2-6.8 1.2-2.6 0-4.9-.4-6.8-1.2-2-.8-3.4-2-4.5-3.5a10 10 0 0 1-1.7-5.6h6a5 5 0 0 0 3.5 4.6c1 .4 2.2.6 3.4.6 1.3 0 2.5-.2 3.5-.6 1-.4 1.8-1 2.4-1.7a4 4 0 0 0 .8-2.4c0-.9-.2-1.6-.7-2.2a11 11 0 0 0-2.1-1.4l-3.2-1-3.8-1c-2.8-.7-5-1.7-6.6-3.2a7.2 7.2 0 0 1-2.4-5.7 8 8 0 0 1 1.7-5 10 10 0 0 1 4.3-3.5c2-.8 4-1.2 6.4-1.2 2.3 0 4.4.4 6.2 1.2 1.8.8 3.2 2 4.3 3.4 1 1.4 1.5 3 1.5 5h-5.8z"/></svg>
```

## public/vercel.svg
- Language: text
- Encoding: utf-8
- Size: 129 bytes
- Tokens: 57

```text
<svg fill="none" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1155 1000"><path d="m577.3 0 577.4 1000H0z" fill="#fff"/></svg>
```

## public/window.svg
- Language: text
- Encoding: utf-8
- Size: 386 bytes
- Tokens: 266

```text
<svg fill="none" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path fill-rule="evenodd" clip-rule="evenodd" d="M1.5 2.5h13v10a1 1 0 0 1-1 1h-11a1 1 0 0 1-1-1zM0 1h16v11.5a2.5 2.5 0 0 1-2.5 2.5h-11A2.5 2.5 0 0 1 0 12.5zm3.75 4.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5M7 4.75a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0m1.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5" fill="#666"/></svg>
```

## src/app/error.tsx
- Language: TSX
- Encoding: utf-8
- Size: 717 bytes
- Tokens: 165

```tsx
'use client';

import { ErrorState } from '@/components/molecules/ErrorState';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="min-h-screen bg-[#0A0A0A] flex items-center justify-center p-4">
      <ErrorState
        title="Something went wrong!"
        message={error.message || "An unexpected error occurred. Please try again."}
        actions={{
          primary: {
            label: 'Try Again',
            onClick: () => reset(),
          },
          secondary: {
            label: 'Go Home',
            onClick: () => window.location.href = '/',
          },
        }}
      />
    </div>
  );
}
```

## src/app/global-error.tsx
- Language: TSX
- Encoding: utf-8
- Size: 819 bytes
- Tokens: 178

```tsx
'use client';

import { ErrorState } from '@/components/molecules/ErrorState';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body>
        <div className="min-h-screen bg-[#0A0A0A] flex items-center justify-center p-4">
          <ErrorState
            title="Something went wrong!"
            message={error.message || 'An unexpected error occurred.'}
            actions={{
              primary: {
                label: 'Try Again',
                onClick: () => reset(),
              },
              secondary: {
                label: 'Go Home',
                onClick: () => window.location.href = '/',
              },
            }}
          />
        </div>
      </body>
    </html>
  );
}
```

## src/app/globals.css
- Language: CSS
- Encoding: utf-8
- Size: 1642 bytes
- Tokens: 678

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  * {
    @apply transition-colors duration-200;
  }

  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 224 71% 4%;
    --foreground: 213 31% 91%;
    --card: 224 71% 6%;
    --card-foreground: 213 31% 91%;
    --popover: 224 71% 5%;
    --popover-foreground: 213 31% 91%;
    --primary: 217 91% 60%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217 32% 17%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217 32% 17%;
    --muted-foreground: 215 20% 65%;
    --accent: 217 32% 17%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217 32% 17%;
    --input: 217 32% 17%;
    --ring: 224 71% 4%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground transition-colors duration-300;
    font-feature-settings: "rlig" 1, "calt" 1;
  }
}
```

## src/app/layout.tsx
- Language: TSX
- Encoding: utf-8
- Size: 1267 bytes
- Tokens: 274

```tsx
import * as React from "react";
import type { Metadata } from "next";
import { Inter, Montserrat } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/providers/ThemeProvider";
import { cn } from "@/lib/utils";
import { AppProvider } from "@/lib/state/AppContext";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

const montserrat = Montserrat({
  subsets: ["latin"],
  variable: "--font-montserrat",
});

export const metadata: Metadata = {
  title: "Odds Flipper | Advanced Odds Analysis Platform",
  description: "A modern platform for advanced odds analysis and insights by Tactical Tech",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={cn(
          "min-h-screen bg-background font-sans antialiased",
          inter.variable,
          montserrat.variable
        )}
      >
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <AppProvider>
            {children}
          </AppProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
```

## src/app/not-found.tsx
- Language: TSX
- Encoding: utf-8
- Size: 518 bytes
- Tokens: 119

```tsx
'use client';

import { ErrorState } from '@/components/molecules/ErrorState';

export default function NotFound() {
  return (
    <div className="min-h-screen bg-[#0A0A0A] flex items-center justify-center p-4">
      <ErrorState
        title="Page Not Found"
        message="The page you're looking for doesn't exist or has been moved."
        actions={{
          primary: {
            label: 'Go Home',
            onClick: () => window.location.href = '/',
          },
        }}
      />
    </div>
  );
}
```

## src/app/(auth)/layout.tsx
- Language: TSX
- Encoding: utf-8
- Size: 334 bytes
- Tokens: 83

```tsx
'use client';

import * as React from "react";

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="w-full max-w-md p-6 space-y-6">
        {children}
      </div>
    </div>
  );
}
```

## src/app/(main)/layout.tsx
- Language: TSX
- Encoding: utf-8
- Size: 426 bytes
- Tokens: 96

```tsx
'use client';

import * as React from "react";
import { Header } from "@/components/navigation/Header";
import { Footer } from "@/components/navigation/Footer";

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Header />
      <main className="flex-1">{children}</main>
      <Footer />
    </div>
  );
}
```

## src/app/(main)/page.tsx
- Language: TSX
- Encoding: utf-8
- Size: 4188 bytes
- Tokens: 1165

```tsx
'use client';

export default function Home() {
  return (
    <div className="w-full px-4 py-12 md:px-6">
      {/* Hero Section */}
      <section className="mx-auto max-w-[1400px] text-center py-20">
        <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-blue-600">
          Advanced Odds Analysis Platform
        </h1>
        <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
          Make data-driven decisions with real-time odds tracking and advanced analytics.
        </p>
        <a
          href="/dashboard"
          className="inline-flex items-center justify-center rounded-lg bg-blue-600 px-8 py-3 text-lg font-medium text-white shadow-lg transition-all hover:bg-blue-500 hover:scale-105 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
        >
          Start Analyzing
        </a>
      </section>

      {/* Features Grid */}
      <section className="mx-auto max-w-[1400px] grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
        {/* Real-Time Odds */}
        <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-black/40 p-8 hover:bg-black/60 transition-all">
          <div className="mb-6 text-blue-500">
            <svg
              className="h-12 w-12 transform transition-transform group-hover:scale-110"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M13 10V3L4 14h7v7l9-11h-7z"
              />
            </svg>
          </div>
          <h3 className="text-xl font-semibold mb-3 text-white">Real-Time Analysis</h3>
          <p className="text-white/70">
            Track and analyze odds movements across multiple providers in real-time.
          </p>
        </div>

        {/* AI Insights */}
        <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-black/40 p-8 hover:bg-black/60 transition-all">
          <div className="mb-6 text-blue-500">
            <svg
              className="h-12 w-12 transform transition-transform group-hover:scale-110"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
              />
            </svg>
          </div>
          <h3 className="text-xl font-semibold mb-3 text-white">AI-Powered Insights</h3>
          <p className="text-white/70">
            Get intelligent recommendations based on advanced statistical analysis and trends.
          </p>
        </div>

        {/* Stats */}
        <div className="group relative overflow-hidden rounded-2xl border border-white/10 bg-black/40 p-8 hover:bg-black/60 transition-all">
          <div className="mb-6 text-blue-500">
            <svg
              className="h-12 w-12 transform transition-transform group-hover:scale-110"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
              />
            </svg>
          </div>
          <h3 className="text-xl font-semibold mb-3 text-white">Advanced Analytics</h3>
          <p className="text-white/70">
            Access comprehensive statistical models and performance metrics for informed decisions.
          </p>
        </div>
      </section>
    </div>
  );
}
```

## src/app/api/recommendations/route.ts
- Language: TypeScript
- Encoding: utf-8
- Size: 2813 bytes
- Tokens: 692

```typescript
import { NextResponse } from 'next/server';
import type { Recommendation } from '@/lib/types/models/recommendations';

// Mock data for development
const mockRecommendations: Recommendation[] = [
  {
    id: '1',
    gameId: 'lakers-warriors',
    homeTeam: 'Lakers',
    awayTeam: 'Warriors',
    recommendedBet: {
      type: 'moneyline',
      team: 'Lakers',
      odds: 2.1,
    },
    confidence: 85,
    reasoning: 'Based on recent performance metrics and historical head-to-head data, the Lakers show strong value at these odds.',
    timestamp: new Date(),
  },
  {
    id: '2',
    gameId: 'celtics-heat',
    homeTeam: 'Celtics',
    awayTeam: 'Heat',
    recommendedBet: {
      type: 'spread',
      team: 'Heat',
      line: 5.5,
      odds: 1.91,
    },
    confidence: 75,
    reasoning: 'The Heat have consistently covered the spread as underdogs in their last 8 away games.',
    timestamp: new Date(),
  },
  {
    id: '3',
    gameId: 'chiefs-49ers',
    homeTeam: 'Chiefs',
    awayTeam: '49ers',
    recommendedBet: {
      type: 'total',
      line: 48.5,
      odds: 1.95,
    },
    confidence: 65,
    reasoning: 'Weather conditions and defensive matchups suggest a lower-scoring game than the market expects.',
    timestamp: new Date(),
  },
];

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const gameId = searchParams.get('gameId');

    let recommendations = mockRecommendations;

    if (gameId) {
      recommendations = recommendations.filter(rec => rec.gameId === gameId);
    }

    return NextResponse.json({ recommendations }, { status: 200 });
  } catch (error) {
    console.error('Error in recommendations API:', error);
    return NextResponse.json(
      { error: 'Failed to fetch recommendations' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { gameId, type, team, line, odds } = body;

    // In a real application, this would call the AI service
    // For now, we'll return a mock recommendation
    const recommendation: Recommendation = {
      id: Date.now().toString(),
      gameId,
      homeTeam: 'Team A',
      awayTeam: 'Team B',
      recommendedBet: {
        type,
        team,
        line,
        odds,
      },
      confidence: Math.floor(Math.random() * 30) + 70, // Random confidence between 70-100
      reasoning: 'This is a mock recommendation based on the provided parameters.',
      timestamp: new Date(),
    };

    return NextResponse.json({ recommendation }, { status: 201 });
  } catch (error) {
    console.error('Error creating recommendation:', error);
    return NextResponse.json(
      { error: 'Failed to create recommendation' },
      { status: 500 }
    );
  }
}
```

## src/app/bets/page.tsx
- Language: TSX
- Encoding: utf-8
- Size: 5304 bytes
- Tokens: 1199

```tsx
'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { Button } from '@/components/controls/Button';
import { Icon } from '@/components/controls/Icon';
import { BettingCard } from '@/components/controls/BettingCard';
import { HeroIcons } from '@/lib/types/models/icons';
import { useState, Suspense } from 'react';
import type { GameStatus } from '@/lib/types/models/games';

type BetStatus = 'all' | 'pending' | 'won' | 'lost';
type BetType = 'all' | 'single' | 'parlay';

function BetsPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const [status, setStatus] = useState<BetStatus>(
    (searchParams.get('status') as BetStatus) || 'all'
  );
  const [type, setType] = useState<BetType>(
    (searchParams.get('type') as BetType) || 'all'
  );

  const handleStatusChange = (newStatus: BetStatus) => {
    setStatus(newStatus);
    const params = new URLSearchParams(searchParams.toString());
    params.set('status', newStatus);
    router.push(`/bets?${params.toString()}`);
  };

  const handleTypeChange = (newType: BetType) => {
    setType(newType);
    const params = new URLSearchParams(searchParams.toString());
    params.set('type', newType);
    router.push(`/bets?${params.toString()}`);
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => router.back()}
            className="mb-4 flex items-center text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            <Icon name={HeroIcons.Navigation.ArrowLeft} className="mr-2 h-4 w-4" />
            Back
          </button>
          <h1 className="text-3xl font-bold">Your Bets</h1>
        </div>

        {/* Filters */}
        <div className="mb-8 space-y-4">
          {/* Status Filter */}
          <div>
            <h3 className="text-sm font-medium text-muted-foreground mb-2">Status</h3>
            <div className="flex flex-wrap gap-2">
              <Button
                variant={status === 'all' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => handleStatusChange('all')}
              >
                All
              </Button>
              <Button
                variant={status === 'pending' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => handleStatusChange('pending')}
              >
                Pending
              </Button>
              <Button
                variant={status === 'won' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => handleStatusChange('won')}
              >
                Won
              </Button>
              <Button
                variant={status === 'lost' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => handleStatusChange('lost')}
              >
                Lost
              </Button>
            </div>
          </div>

          {/* Type Filter */}
          <div>
            <h3 className="text-sm font-medium text-muted-foreground mb-2">Bet Type</h3>
            <div className="flex flex-wrap gap-2">
              <Button
                variant={type === 'all' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => handleTypeChange('all')}
              >
                All Types
              </Button>
              <Button
                variant={type === 'single' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => handleTypeChange('single')}
              >
                Single Bets
              </Button>
              <Button
                variant={type === 'parlay' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => handleTypeChange('parlay')}
              >
                Parlay Bets
              </Button>
            </div>
          </div>
        </div>

        {/* Bets Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <BettingCard
            homeTeam={{
              name: "Lakers",
              isHome: true,
            }}
            awayTeam={{
              name: "Warriors",
              isHome: false,
            }}
            homeOdds={1.90}
            awayOdds={2.10}
            status={{
              type: "live",
              period: "3",
              timeRemaining: "8:45",
              detail: "In Progress",
            } as GameStatus}
            quickBetAmounts={[5, 10, 25, 50]}
          />
          <BettingCard
            homeTeam={{
              name: "Celtics",
              isHome: true,
            }}
            awayTeam={{
              name: "Heat",
              isHome: false,
            }}
            homeOdds={1.80}
            awayOdds={2.20}
            status={{
              type: "halftime",
              period: "2",
              detail: "Halftime",
            } as GameStatus}
            quickBetAmounts={[5, 10, 25, 50]}
          />
        </div>
      </div>
    </div>
  );
}

export default function BetsPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <BetsPageContent />
    </Suspense>
  );
}
```

## src/app/betting/page.tsx
- Language: TSX
- Encoding: utf-8
- Size: 3493 bytes
- Tokens: 899

```tsx
"use client";

import * as React from "react";
import { BettingTemplate } from "@/components/templates/BettingTemplate";
import { OddsList } from "@/components/templates/OddsList";
import { BettingForm } from "@/components/controls/BettingForm";
import type { Game } from "@/components/templates/OddsList";

// Sample data for demonstration
const sampleGames: Game[] = [
  {
    id: "1",
    homeTeam: {
      name: "Kansas City Chiefs",
      isHome: true,
    },
    awayTeam: {
      name: "San Francisco 49ers",
      isHome: false,
    },
    homeOdds: 1.95,
    awayOdds: 1.85,
    startTime: "Today, 4:30 PM",
    sport: "NFL",
    status: {
      type: "upcoming",
      startTime: "Today, 4:30 PM"
    }
  },
  {
    id: "2",
    homeTeam: {
      name: "Los Angeles Lakers",
      isHome: true,
    },
    awayTeam: {
      name: "Golden State Warriors",
      isHome: false,
    },
    homeOdds: 2.10,
    awayOdds: 1.75,
    startTime: "Today, 7:00 PM",
    sport: "NBA",
    status: {
      type: "upcoming",
      startTime: "Today, 7:00 PM"
    }
  },
  {
    id: "3",
    homeTeam: {
      name: "Boston Bruins",
      isHome: true,
    },
    awayTeam: {
      name: "Toronto Maple Leafs",
      isHome: false,
    },
    homeOdds: 1.90,
    awayOdds: 1.90,
    startTime: "Today, 8:00 PM",
    sport: "NHL",
    status: {
      type: "upcoming",
      startTime: "Today, 8:00 PM"
    }
  },
];

export default function BettingPage() {
  const [selectedGame, setSelectedGame] = React.useState<Game | null>(null);

  const handlePlaceBet = React.useCallback((amount: number, betType: string) => {
    console.log("Placing bet:", { amount, betType, game: selectedGame });
    // In a real app, this would make an API call to place the bet
  }, [selectedGame]);

  return (
    <BettingTemplate>
      <div className="container max-w-7xl mx-auto px-4 py-6">
        {/* Header Section */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold font-display tracking-tight">Place Your Bets</h1>
          <p className="mt-3 text-lg text-muted-foreground">
            Choose from available games and place your bets
          </p>
        </div>

        {/* Main Content */}
        <div className="space-y-8">
          {/* Games List */}
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-semibold">Available Games</h2>
            </div>
            <div className="bg-card rounded-lg border p-6">
              <OddsList 
                games={sampleGames} 
                onSelectGame={(game) => setSelectedGame(game)}
                selectedGames={selectedGame ? [selectedGame] : []}
              />
            </div>
          </div>

          {/* Betting Form */}
          {selectedGame && (
            <div className="rounded-lg border bg-card">
              <div className="p-6 space-y-6">
                <div>
                  <h2 className="text-2xl font-semibold">Place a Bet</h2>
                  <p className="mt-2 text-sm text-muted-foreground">
                    Betting on {selectedGame.homeTeam.name} vs {selectedGame.awayTeam.name}
                  </p>
                </div>
                <BettingForm
                  odds={selectedGame.homeOdds}
                  onPlaceBet={handlePlaceBet}
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </BettingTemplate>
  );
}
```

## src/app/dashboard/page.tsx
- Language: TSX
- Encoding: utf-8
- Size: 11055 bytes
- Tokens: 2000

```tsx
'use client';

import * as React from 'react';
import { useRouter } from 'next/navigation';
import { useApp } from '@/lib/state/AppContext';
import { useBetting } from '@/lib/state/useBetting';
import MainLayout from '@/components/layout/MainLayout';
import { UserDashboard } from '@/components/controls/UserDashboard';
import { StatsCard } from '@/components/controls/StatsCard';
import { BettingCard } from '@/components/controls/BettingCard';
import { LiveScoreCard } from '@/components/controls/LiveScoreCard';
import { ErrorBoundary } from '@/components/organisms/ErrorBoundary';
import { AIRecommendations } from '@/components/controls/AIRecommendations';
import type { Recommendation } from '@/lib/types/models/recommendations';
import type { AccountInfo } from '@/lib/types/models/user';
import type { Analysis, MultiMarketAnalysis } from '@/lib/types/models/analysis';
import { getRecommendations } from '@/lib/services/recommendations';

export default function DashboardPage() {
  const router = useRouter();
  const { user } = useApp();
  const betting = useBetting();
  const stats = betting.getBetStats();
  const [recommendations, setRecommendations] = React.useState<Recommendation[]>([]);
  const [isLoadingRecommendations, setIsLoadingRecommendations] = React.useState(true);
  const [recommendationsError, setRecommendationsError] = React.useState<string | null>(null);
  const [previousOdds, setPreviousOdds] = React.useState<Record<string, { home: number; away: number }>>({});

  React.useEffect(() => {
    async function fetchRecommendations() {
      try {
        setIsLoadingRecommendations(true);
        setRecommendationsError(null);
        const data = await getRecommendations();
        setRecommendations(data);
      } catch (error) {
        console.error('Error fetching recommendations:', error);
        setRecommendationsError('Failed to load recommendations. Please try again later.');
      } finally {
        setIsLoadingRecommendations(false);
      }
    }

    fetchRecommendations();
  }, []);

  // Track odds changes for active bets
  React.useEffect(() => {
    const interval = setInterval(() => {
      betting.activeBets.forEach(bet => {
        setPreviousOdds(prev => {
          if (!prev[bet.id]) {
            return {
              ...prev,
              [bet.id]: {
                home: bet.homeOdds,
                away: bet.awayOdds
              }
            };
          } else if (
            bet.homeOdds !== prev[bet.id].home ||
            bet.awayOdds !== prev[bet.id].away
          ) {
            return {
              ...prev,
              [bet.id]: prev[bet.id]
            };
          }
          return prev;
        });
      });
    }, 5000);

    return () => clearInterval(interval);
  }, [betting.activeBets]);

  // Mock data for initial render
  const mockAccountInfo: AccountInfo = {
    balance: 1000.00,
    totalAnalyses: 145,
    successfulPredictions: 99,
    accuracyRate: 68.5,
    activeAnalyses: 12,
    totalInvested: 5000.00,
    totalReturns: 1500.00,
    pendingReturns: 250.00,
    availableCapital: 750.00,
    currency: 'USD',
    verificationStatus: 'verified',
  };

  const mockRecentAnalyses: Analysis[] = [
    {
      id: '1',
      correlationStrength: 0.85,
      confidence: 0.92,
      potentialValue: 250.00,
      status: 'active',
      createdAt: new Date().toISOString(),
      market: {
        homeTeam: 'Lakers',
        awayTeam: 'Warriors',
        status: {
          type: 'live',
          period: '3rd',
          timeRemaining: '8:45',
          possession: 'home',
          startTime: new Date().toISOString()
        },
        homeScore: 78,
        awayScore: 72,
        startTime: new Date().toISOString()
      },
      predictedOutcome: 'Lakers win'
    },
    {
      id: '2',
      correlationStrength: 0.78,
      confidence: 0.88,
      potentialValue: 180.00,
      status: 'active',
      createdAt: new Date().toISOString(),
      market: {
        homeTeam: 'Celtics',
        awayTeam: 'Nets',
        status: {
          type: 'live',
          period: '2nd',
          timeRemaining: '4:20',
          possession: 'away',
          startTime: new Date().toISOString()
        },
        homeScore: 45,
        awayScore: 42,
        startTime: new Date().toISOString()
      },
      predictedOutcome: 'Celtics win'
    }
  ];

  const mockMultiMarketAnalyses: MultiMarketAnalysis[] = [
    {
      id: '1',
      analyses: [mockRecentAnalyses[0]],
      correlationStrength: 0.82,
      confidence: 0.90,
      potentialValue: 450.00,
      status: 'active',
      createdAt: new Date().toISOString()
    }
  ];

  const handleRecommendationSelect = React.useCallback((recommendation: Recommendation) => {
    router.push(`/game/${recommendation.gameId}`);
  }, [router]);

  return (
    <MainLayout>
      <div className="container mx-auto px-4 py-8">
        <ErrorBoundary>
          {/* Welcome Section */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold font-display mb-2">
              Welcome back, {user?.name || "Analyst"}
            </h1>
            <p className="text-muted-foreground">
              Here&apos;s your analytics overview and market insights
            </p>
          </div>

          {/* Main Dashboard Content */}
          <div className="space-y-8">
            {/* Analytics Overview */}
            <section>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <StatsCard 
                  title="Active Markets" 
                  value={betting.activeBets.length} 
                  type="count"
                  onClick={() => router.push('/markets')}
                  className="cursor-pointer hover:border-primary transition-colors"
                />
                <StatsCard 
                  title="Win Rate" 
                  value={stats.winRate}
                  type="percentage"
                  onClick={() => router.push('/stats')}
                  className="cursor-pointer hover:border-primary transition-colors"
                />
                <StatsCard 
                  title="Profit/Loss" 
                  value={stats.profitLoss}
                  type="money"
                  onClick={() => router.push('/performance')}
                  className="cursor-pointer hover:border-primary transition-colors"
                />
              </div>
            </section>

            {/* User Dashboard */}
            <section>
              <UserDashboard
                accountInfo={mockAccountInfo}
                recentAnalyses={mockRecentAnalyses}
                multiMarketAnalyses={mockMultiMarketAnalyses}
              />
            </section>

            {/* AI Recommendations */}
            <section>
              <AIRecommendations
                recommendations={recommendations}
                onSelectRecommendation={handleRecommendationSelect}
                isLoading={isLoadingRecommendations}
                error={recommendationsError}
              />
            </section>

            {/* Live Games */}
            <section>
              <h2 className="text-2xl font-semibold mb-4 flex items-center justify-between">
                Live Games
                <button 
                  onClick={() => router.push('/games')}
                  className="text-sm text-primary hover:text-primary/80 transition-colors"
                >
                  View All Games
                </button>
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <LiveScoreCard
                  teams={[
                    { name: "Lakers", score: 89, isHome: false },
                    { name: "Warriors", score: 92, isHome: true }
                  ]}
                  gameStatus="live"
                  sportType="NBA"
                  keyStats={{
                    timeRemaining: "8:45",
                    period: "3",
                    periodType: "quarter",
                    possession: "away",
                    lastPlay: "Significant odds movement detected"
                  }}
                  onClick={() => router.push('/game/lakers-warriors')}
                />
                <LiveScoreCard
                  teams={[
                    { name: "Chiefs", score: 24, isHome: false },
                    { name: "49ers", score: 21, isHome: true }
                  ]}
                  gameStatus="live"
                  sportType="NFL"
                  keyStats={{
                    timeRemaining: "4:32",
                    period: "4",
                    periodType: "quarter",
                    possession: "home",
                    lastPlay: "Market volatility increasing"
                  }}
                  onClick={() => router.push('/game/chiefs-49ers')}
                />
                <LiveScoreCard
                  teams={[
                    { name: "Celtics", score: 58, isHome: false },
                    { name: "Heat", score: 52, isHome: true }
                  ]}
                  gameStatus="halftime"
                  sportType="NBA"
                  keyStats={{
                    timeRemaining: "15:00",
                    period: "2",
                    periodType: "half",
                    lastPlay: "Analyzing halftime adjustments"
                  }}
                  onClick={() => router.push('/game/celtics-heat')}
                />
              </div
```

## src/app/features/page.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2457 bytes
- Tokens: 549

```tsx
"use client";

import * as React from "react";
import { AnalysisTemplate } from "@/components/templates/AnalysisTemplate";
import { Features } from "@/components/controls/Features";

// Sample data - in a real app, this would come from an API
const sampleFeatures = [
  {
    id: "1",
    title: "AI-Powered Market Analysis",
    description: "Advanced machine learning models analyze historical data to identify market patterns and trends",
    type: "ai" as const,
    value: "Premium",
    expiresAt: null,
    terms: "Requires subscription to access full model insights.",
  },
  {
    id: "2",
    title: "Multi-Market Correlation Engine",
    description: "Discover hidden relationships between different markets using advanced statistical analysis",
    type: "analysis" as const,
    value: "Pro",
    expiresAt: null,
    terms: "Available with Pro tier subscription.",
  },
  {
    id: "3",
    title: "Real-Time Market Alerts",
    description: "Get instant notifications when significant market movements or anomalies are detected",
    type: "alerts" as const,
    value: "Basic",
    expiresAt: null,
    terms: "Basic alerts included with all subscriptions.",
  },
  {
    id: "4",
    title: "Custom Analysis Models",
    description: "Build and backtest your own analysis models using our advanced toolkit",
    type: "custom" as const,
    value: "Enterprise",
    terms: "Available for Enterprise tier subscribers.",
  },
  {
    id: "5",
    title: "Market Sentiment Analysis",
    description: "Track and analyze market sentiment across multiple data sources",
    type: "analysis" as const,
    value: "Pro",
    expiresAt: null,
    terms: "Pro feature with unlimited sentiment tracking.",
  },
];

export default function FeaturesPage() {
  const handleFeatureActivate = React.useCallback((id: string) => {
    console.log("Activating feature:", id);
    // In a real app, this would make an API call to activate the feature
  }, []);

  return (
    <AnalysisTemplate
      title="Advanced Features"
      description="Explore our suite of advanced analysis tools and features to enhance your market insights"
    >
      <div className="container max-w-7xl mx-auto px-4 py-6">
        {/* Features Section */}
        <div className="space-y-8">
          <Features
            features={sampleFeatures}
            onActivateFeature={handleFeatureActivate}
          />
        </div>
      </div>
    </AnalysisTemplate>
  );
}
```

## src/app/game/[id]/page.tsx
- Language: TSX
- Encoding: utf-8
- Size: 7633 bytes
- Tokens: 1704

```tsx
'use client';

import { useRouter } from 'next/navigation';
import { Icon } from '@/components/controls/Icon';
import { Button } from '@/components/controls/Button';
import { HeroIcons } from '@/lib/types/models/icons';
import { useState } from 'react';

type BetType = 'single' | 'parlay' | 'teaser';

export default function GameDetailsPage() {
  const router = useRouter();
  const [betType, setBetType] = useState<BetType>('single');
  const [betAmount, setBetAmount] = useState<string>('');
  const odds = 1.85;

  const quickAmounts = [10, 20, 50, 100];

  const handleQuickAmount = (amount: number) => {
    setBetAmount(amount.toString());
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => router.back()}
            className="mb-4 flex items-center text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            <Icon name={HeroIcons.Navigation.ArrowLeft} className="mr-2 h-4 w-4" />
            Back to Games
          </button>
          <div className="flex justify-between items-start">
            <h1 className="text-3xl font-bold">Game Details</h1>
            <h2 className="text-3xl font-bold">Place Your Bet</h2>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-8">
          {/* Game Details Section */}
          <div className="space-y-6">
            {/* Game Score Card */}
            <div className="rounded-lg border bg-[#0A0A0A] p-6 text-white">
              <div className="flex items-center justify-between mb-4">
                <span className="flex items-center gap-1.5 px-2 py-1 bg-red-500 text-white text-xs font-medium rounded-full">
                  <span className="relative flex h-2 w-2">
                    <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-red-400 opacity-75" />
                    <span className="relative inline-flex h-2 w-2 rounded-full bg-red-500" />
                  </span>
                  live
                </span>
                <span className="text-sm text-gray-400">NBA • Q3</span>
              </div>

              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <div>
                    <div className="text-xl font-semibold text-blue-400">Lakers •</div>
                  </div>
                  <div className="text-3xl font-bold">89</div>
                </div>

                <div className="flex justify-between items-center">
                  <div>
                    <div className="text-xl font-semibold">Warriors</div>
                  </div>
                  <div className="text-3xl font-bold">92</div>
                </div>

                <div className="pt-4 border-t border-gray-800">
                  <div className="text-sm text-gray-400">Time Remaining:</div>
                  <div className="text-lg">8:45</div>
                </div>

                <div className="pt-4 border-t border-gray-800">
                  <div className="text-sm text-gray-400">Last Play:</div>
                  <div className="text-lg">L. James layup made (K. Nunn assist)</div>
                </div>
              </div>
            </div>

            {/* Game Stats */}
            <div className="rounded-lg border bg-[#0A0A0A] p-6 text-white">
              <h3 className="text-xl font-semibold mb-4">Game Stats</h3>
              <div className="grid grid-cols-3 gap-8">
                <div>
                  <div className="text-sm text-gray-400 mb-1">Field Goal %</div>
                  <div className="text-lg font-semibold">48.3%</div>
                </div>
                <div>
                  <div className="text-sm text-gray-400 mb-1">3PT %</div>
                  <div className="text-lg font-semibold">37.5%</div>
                </div>
                <div>
                  <div className="text-sm text-gray-400 mb-1">Free Throw %</div>
                  <div className="text-lg font-semibold">82.1%</div>
                </div>
              </div>
            </div>
          </div>

          {/* Betting Section */}
          <div className="rounded-lg border bg-card p-6">
            {/* Bet Type Selection */}
            <div className="flex gap-2 mb-6">
              <Button
                variant={betType === 'single' ? 'primary' : 'outline'}
                onClick={() => setBetType('single')}
                className="flex items-center gap-2"
              >
                <Icon name={HeroIcons.Commerce.CurrencyDollar} className="h-4 w-4" />
                Single
              </Button>
              <Button
                variant={betType === 'parlay' ? 'primary' : 'outline'}
                onClick={() => setBetType('parlay')}
                className="flex items-center gap-2"
              >
                <Icon name={HeroIcons.Commerce.Tag} className="h-4 w-4" />
                Parlay
              </Button>
              <Button
                variant={betType === 'teaser' ? 'primary' : 'outline'}
                onClick={() => setBetType('teaser')}
                className="flex items-center gap-2"
              >
                <Icon name={HeroIcons.UI.AdjustmentsHorizontal} className="h-4 w-4" />
                Teaser
              </Button>
            </div>

            {/* Odds Display */}
            <div className="mb-4">
              <div className="text-sm text-muted-foreground mb-1">Odds</div>
              <div className="text-lg font-semibold">{odds}</div>
            </div>

            {/* Bet Amount Input */}
            <div className="space-y-4">
              <input
                type="text"
                value={betAmount}
                onChange={(e) => setBetAmount(e.target.value)}
                placeholder="Enter amount ($5-$1000)"
                className="w-full px-4 py-2 bg-background border rounded-md"
              />

              {/* Quick Amount Buttons */}
              <div className="grid grid-cols-4 gap-2">
                {quickAmounts.map((amount) => (
                  <Button
                    key={amount}
                    variant="outline"
                    onClick={() => handleQuickAmount(amount)}
                    className="flex items-center justify-center gap-1"
                  >
                    <Icon name={HeroIcons.Commerce.CurrencyDollar} className="h-4 w-4" />
                    {amount}
                  </Button>
                ))}
              </div>

              {/* Potential Winnings */}
              <div className="flex justify-between items-center py-4 border-t">
                <div className="text-sm text-muted-foreground">Potential Winnings:</div>
                <div className="text-lg font-semibold">
                  ${((parseFloat(betAmount) || 0) * odds).toFixed(2)}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="space-y-2">
                <Button className="w-full" size="lg">
                  <Icon name={HeroIcons.Commerce.CurrencyDollar} className="mr-2 h-4 w-4" />
                  Place Bet
                </Button>
                <Button variant="outline" className="w-full" size="lg">
                  <Icon name={HeroIcons.Commerce.Tag} className="mr-2 h-4 w-4" />
                  Add to Parlay
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
```

## src/app/leaderboard/page.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2562 bytes
- Tokens: 698

```tsx
"use client";

import * as React from "react";
import { BettingTemplate } from "@/components/templates/BettingTemplate";
import { Leaderboard, type LeaderboardProps } from "@/components/controls/Leaderboard";
import type { LeaderboardEntry } from "@/components/controls/Leaderboard";

// Sample data - in a real app, this would come from an API
const sampleEntries: LeaderboardEntry[] = [
  {
    id: "1",
    rank: 1,
    username: "AnalyticsKing",
    winnings: 50000,
    winRate: 68,
    parlayStreak: 5,
    totalBets: 245,
  },
  {
    id: "2",
    rank: 2,
    username: "DataMaster",
    winnings: 35000,
    winRate: 62,
    parlayStreak: 3,
    totalBets: 178,
  },
  {
    id: "3",
    rank: 3,
    username: "OddsExpert",
    winnings: 28000,
    winRate: 59,
    parlayStreak: 2,
    totalBets: 156,
  },
  {
    id: "4",
    rank: 4,
    username: "StatisticsGuru",
    winnings: 22000,
    winRate: 55,
    parlayStreak: 1,
    totalBets: 134,
  },
  {
    id: "5",
    rank: 5,
    username: "PredictionPro",
    winnings: 18000,
    winRate: 52,
    parlayStreak: 0,
    totalBets: 112,
  },
];

export default function LeaderboardPage() {
  const [timePeriod, setTimePeriod] = React.useState<LeaderboardProps["timePeriod"]>("weekly");
  const [sportType, setSportType] = React.useState<LeaderboardProps["sportType"]>("all");

  const handleTimePeriodChange = React.useCallback((period: LeaderboardProps["timePeriod"]) => {
    setTimePeriod(period);
    // In a real app, this would fetch new data based on the time period
  }, []);

  const handleSportTypeChange = React.useCallback((sport: LeaderboardProps["sportType"]) => {
    setSportType(sport);
    // In a real app, this would fetch new data based on the sport type
  }, []);

  return (
    <BettingTemplate>
      <div className="container max-w-7xl mx-auto px-4 py-6">
        {/* Header Section */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold font-display tracking-tight">Top Analysts</h1>
          <p className="mt-3 text-lg text-muted-foreground">
            See who&apos;s leading in predictive accuracy and analytical performance
          </p>
        </div>

        {/* Leaderboard Section */}
        <div className="space-y-8">
          <Leaderboard
            entries={sampleEntries}
            timePeriod={timePeriod}
            sportType={sportType}
            onTimePeriodChange={handleTimePeriodChange}
            onSportTypeChange={handleSportTypeChange}
          />
        </div>
      </div>
    </BettingTemplate>
  );
}
```

## src/app/login/page.tsx
- Language: TSX
- Encoding: utf-8
- Size: 3442 bytes
- Tokens: 720

```tsx
'use client';

import { useState } from 'react';
import MainLayout from '@/components/layout/MainLayout';

export default function LoginPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement login logic
    console.log('Login attempt:', formData);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <MainLayout>
      <div className="max-w-md mx-auto">
        <h1 className="text-3xl font-bold text-secondary-900 text-center mb-8">Login</h1>
        
        <div className="bg-white p-8 rounded-lg shadow-md">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-secondary-700 mb-2">
                Email Address
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-secondary-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                placeholder="you@example.com"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-secondary-700 mb-2">
                Password
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-secondary-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                placeholder="••••••••"
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="remember"
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-secondary-300 rounded"
                />
                <label htmlFor="remember" className="ml-2 block text-sm text-secondary-700">
                  Remember me
                </label>
              </div>
              <a href="#" className="text-sm text-primary-600 hover:text-primary-500">
                Forgot password?
              </a>
            </div>

            <button
              type="submit"
              className="w-full py-3 px-4 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors"
            >
              Sign In
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-secondary-600">
              Don&apos;t have an account?{' '}
              <a href="/register" className="text-primary-600 hover:text-primary-500">
                Sign up
              </a>
            </p>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
```

## src/app/multi-market-analysis/page.tsx
- Language: TSX
- Encoding: utf-8
- Size: 4111 bytes
- Tokens: 1037

```tsx
"use client";

import * as React from "react";
import { AnalysisTemplate } from "@/components/templates/AnalysisTemplate";
import { OddsList, type Game } from "@/components/templates/OddsList";
import { MultiMarketAnalysis } from "@/components/controls/MultiMarketAnalysis";
import { Button } from "@/components/controls/Button";
import type { MarketCardProps } from "@/components/controls/MarketCard";
import type { MultiMarketAnalysis as MultiMarketAnalysisType } from "@/lib/types/models/analysis";

// Sample data for demonstration
const sampleMarkets: Game[] = [
  {
    id: "1",
    homeTeam: {
      name: "Kansas City Chiefs",
      isHome: true,
    },
    awayTeam: {
      name: "San Francisco 49ers",
      isHome: false,
    },
    homeOdds: 1.95,
    awayOdds: 1.85,
    startTime: "Today, 4:30 PM",
    sport: "NFL",
    status: {
      type: "upcoming",
      startTime: "Today, 4:30 PM"
    }
  },
  {
    id: "2",
    homeTeam: {
      name: "Los Angeles Lakers",
      isHome: true,
    },
    awayTeam: {
      name: "Golden State Warriors",
      isHome: false,
    },
    homeOdds: 2.10,
    awayOdds: 1.75,
    startTime: "Today, 7:00 PM",
    sport: "NBA",
    status: {
      type: "upcoming",
      startTime: "Today, 7:00 PM"
    }
  },
  {
    id: "3",
    homeTeam: {
      name: "Boston Bruins",
      isHome: true,
    },
    awayTeam: {
      name: "Toronto Maple Leafs",
      isHome: false,
    },
    homeOdds: 1.90,
    awayOdds: 1.90,
    startTime: "Today, 8:00 PM",
    sport: "NHL",
    status: {
      type: "upcoming",
      startTime: "Today, 8:00 PM"
    }
  },
];

export default function MultiMarketPage() {
  const [selectedMarkets, setSelectedMarkets] = React.useState<MarketCardProps[]>([]);

  const handleMarketSelect = React.useCallback((game: Game, team: "home" | "away") => {
    const selectedTeam = team === "home" ? game.homeTeam : game.awayTeam;
    const newMarket: MarketCardProps = {
      homeTeam: game.homeTeam,
      awayTeam: game.awayTeam,
      homeOdds: game.homeOdds,
      awayOdds: game.awayOdds,
      selectedTeam: selectedTeam,
      status: game.status
    };

    setSelectedMarkets((prev) => {
      const existingIndex = prev.findIndex(
        (g) => g.homeTeam.name === game.homeTeam.name && g.awayTeam.name === game.awayTeam.name
      );
      if (existingIndex !== -1) {
        return prev.filter((_, i) => i !== existingIndex);
      }
      return [...prev, newMarket];
    });
  }, []);

  const handleRemoveMarket = React.useCallback((index: number) => {
    setSelectedMarkets((prev) => prev.filter((_, i) => i !== index));
  }, []);

  const handleAnalyze = React.useCallback((analysis: MultiMarketAnalysisType) => {
    console.log("Analyzing markets:", analysis);
  }, []);

  return (
    <AnalysisTemplate
      title="Multi-Market Analysis"
      description="Analyze correlations and patterns across multiple markets to identify opportunities"
    >
      <div className="container max-w-7xl mx-auto px-4 py-6">
        {/* Markets List */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-semibold">Available Markets</h2>
            <Button
              variant="outline"
              onClick={() => setSelectedMarkets([])}
              disabled={selectedMarkets.length === 0}
            >
              Clear Selection
            </Button>
          </div>
          <div className="bg-card rounded-lg border p-6">
            <OddsList
              games={sampleMarkets}
              onSelectGame={handleMarketSelect}
              selectedGames={selectedMarkets}
            />
          </div>
        </div>

        {/* Analysis Form */}
        {selectedMarkets.length > 0 && (
          <div className="rounded-lg border bg-card text-card-foreground">
            <MultiMarketAnalysis
              marketCards={selectedMarkets}
              onRemoveMarket={handleRemoveMarket}
              onAnalyze={handleAnalyze}
            />
          </div>
        )}
      </div>
    </AnalysisTemplate>
  );
}
```

## src/app/parlay/page.tsx
- Language: TSX
- Encoding: utf-8
- Size: 7804 bytes
- Tokens: 1630

```tsx
"use client";

import { useState } from 'react';
import { Button } from '@/components/controls/Button';
import { Icon } from '@/components/controls/Icon';
import { HeroIcons } from '@/lib/types/models/icons';
import { cn } from '@/lib/utils';
import MainLayout from '@/components/layout/MainLayout';

type SportType = 'all' | 'NFL' | 'NBA' | 'MLB' | 'NHL';
type TeamPosition = 'home' | 'away';

interface Market {
  id: string;
  homeTeam: string;
  awayTeam: string;
  homeOdds: number;
  awayOdds: number;
  sport: SportType;
}

export default function ParlayBetPage() {
  const [selectedSport, setSelectedSport] = useState<SportType>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedMarkets, setSelectedMarkets] = useState<Record<string, TeamPosition>>({});

  // Mock data - in a real app, this would come from an API
  const markets: Market[] = [
    {
      id: '1',
      homeTeam: 'Kansas City Chiefs',
      awayTeam: 'San Francisco 49ers',
      homeOdds: 1.95,
      awayOdds: 1.85,
      sport: 'NFL',
    },
    {
      id: '2',
      homeTeam: 'Los Angeles Lakers',
      awayTeam: 'Golden State Warriors',
      homeOdds: 2.10,
      awayOdds: 1.75,
      sport: 'NBA',
    },
  ];

  const handleMarketSelect = (marketId: string, position: TeamPosition) => {
    setSelectedMarkets(prev => ({
      ...prev,
      [marketId]: position,
    }));
  };

  const handleClearSelection = () => {
    setSelectedMarkets({});
  };

  return (
    <MainLayout>
      <div className="container mx-auto px-4 py-8">
        <div className="space-y-6">
          {/* Header */}
          <div>
            <h1 className="text-4xl font-bold text-white mb-2">Multi-Market Analysis</h1>
            <p className="text-lg text-white/60">
              Analyze correlations and patterns across multiple markets to identify opportunities
            </p>
          </div>

          {/* Market Selection */}
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-semibold text-white">Available Markets</h2>
              <Button
                variant="outline"
                onClick={handleClearSelection}
                disabled={Object.keys(selectedMarkets).length === 0}
              >
                Clear Selection
              </Button>
            </div>

            {/* Filters */}
            <div className="rounded-lg border border-white/10 bg-[#1A1A1A] p-6">
              {/* Sport Filters */}
              <div className="flex gap-2 mb-4">
                {(['all', 'NFL', 'NBA', 'MLB', 'NHL'] as SportType[]).map((sport) => (
                  <Button
                    key={sport}
                    variant={selectedSport === sport ? 'primary' : 'outline'}
                    onClick={() => setSelectedSport(sport)}
                    size="sm"
                    className={selectedSport === sport ? 'bg-blue-500 hover:bg-blue-600' : ''}
                  >
                    {sport === 'all' ? 'All Sports' : sport}
                  </Button>
                ))}
              </div>

              {/* Search */}
              <div className="relative">
                <Icon
                  name={HeroIcons.UI.MagnifyingGlass}
                  className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-white/40"
                />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search teams..."
                  className="w-full pl-9 pr-4 py-2 bg-[#0A0A0A] border border-white/10 rounded-md text-white placeholder:text-white/40"
                />
              </div>

              {/* Markets Grid */}
              <div className="grid grid-cols-2 gap-4 mt-6">
                {markets.map((market) => (
                  <div
                    key={market.id}
                    className="rounded-lg border border-white/10 bg-[#0A0A0A] p-4"
                  >
                    {/* Away Team */}
                    <div className="mb-4">
                      <div className="flex justify-between items-center mb-1">
                        <div className="text-lg font-semibold text-white">{market.awayTeam}</div>
                        <div className="text-sm text-white/40">Away</div>
                      </div>
                      <Button
                        variant={selectedMarkets[market.id] === 'away' ? 'primary' : 'outline'}
                        className={cn(
                          "w-full justify-between",
                          selectedMarkets[market.id] === 'away' ? 'bg-blue-500 hover:bg-blue-600' : ''
                        )}
                        onClick={() => handleMarketSelect(market.id, 'away')}
                      >
                        <span>Bet</span>
                        <span>{market.awayOdds.toFixed(2)}</span>
                      </Button>
                      <div className="grid grid-cols-4 gap-2 mt-2">
                        {[5, 10, 25, 50].map((amount) => (
                          <Button
                            key={amount}
                            variant="outline"
                            size="sm"
                            onClick={() => handleMarketSelect(market.id, 'away')}
                            className="border-white/10 text-white hover:bg-white/5"
                          >
                            <Icon name={HeroIcons.Commerce.CurrencyDollar} className="h-4 w-4" />
                            {amount}
                          </Button>
                        ))}
                      </div>
                    </div>

                    {/* VS Divider */}
                    <div className="flex items-center justify-center my-2">
                      <span className="text-sm text-white/40">VS</span>
                    </div>

                    {/* Home Team */}
                    <div>
                      <div className="flex justify-between items-center mb-1">
                        <div className="text-lg font-semibold text-white">{market.homeTeam}</div>
                        <div className="text-sm text-white/40">Home</div>
                      </div>
                      <Button
                        variant={selectedMarkets[market.id] === 'home' ? 'primary' : 'outline'}
                        className={cn(
                          "w-full justify-between",
                          selectedMarkets[market.id] === 'home' ? 'bg-blue-500 hover:bg-blue-600' : ''
                        )}
                        onClick={() => handleMarketSelect(market.id, 'home')}
                      >
                        <span>Bet</span>
                        <span>{market.homeOdds.toFixed(2)}</span>
                      </Button>
                      <div className="grid grid-cols-4 gap-2 mt-2">
                        {[5, 10, 25, 50].map((amount) => (
                          <Button
                            key={amount}
                            variant="outline"
                            size="sm"
                            onClick={() => handleMarketSelect(market.id, 'home')}
                            className="border-white/10 text-white hover:bg-white/5"
                          >
                            <Icon name={HeroIcons.Commerce.CurrencyDollar} className="h-4 w-4" />
                            {amount}
                          </Button>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
```

## src/app/promotions/page.tsx
- Language: TSX
- Encoding: utf-8
- Size: 4868 bytes
- Tokens: 1059

```tsx
"use client";

import { useState } from 'react';
import { Button } from '@/components/controls/Button';
import { cn } from '@/lib/utils';
import MainLayout from '@/components/layout/MainLayout';

type FeatureTier = 'Basic' | 'Pro' | 'Premium' | 'Enterprise';

interface Feature {
  id: string;
  title: string;
  description: string;
  icon: string;
  tier: FeatureTier;
  terms: string;
}

export default function PromotionsPage() {
  const [activatedFeatures, setActivatedFeatures] = useState<string[]>([]);

  const features: Feature[] = [
    {
      id: '1',
      title: 'AI-Powered Market Analysis',
      description: 'Advanced machine learning models analyze historical data to identify market patterns and trends',
      icon: 'AI',
      tier: 'Premium',
      terms: 'Requires subscription to access full model insights.',
    },
    {
      id: '2',
      title: 'Multi-Market Correlation Engine',
      description: 'Discover hidden relationships between different markets using advanced statistical analysis',
      icon: 'A',
      tier: 'Pro',
      terms: 'Available with Pro tier subscription.',
    },
    {
      id: '3',
      title: 'Real-Time Market Alerts',
      description: 'Get instant notifications when significant market movements or anomalies are detected',
      icon: '!',
      tier: 'Basic',
      terms: 'Basic alerts included with all subscriptions.',
    },
    {
      id: '4',
      title: 'Custom Analysis Models',
      description: 'Build and backtest your own analysis models using our advanced toolkit',
      icon: 'C',
      tier: 'Enterprise',
      terms: 'Available for Enterprise tier subscribers.',
    },
    {
      id: '5',
      title: 'Market Sentiment Analysis',
      description: 'Track and analyze market sentiment across multiple data sources',
      icon: 'A',
      tier: 'Pro',
      terms: 'Pro feature with unlimited sentiment tracking.',
    },
  ];

  const handleActivateFeature = (featureId: string) => {
    setActivatedFeatures(prev => [...prev, featureId]);
  };

  const getTierColor = (tier: FeatureTier) => {
    switch (tier) {
      case 'Basic':
        return 'bg-blue-100 text-blue-800';
      case 'Pro':
        return 'bg-purple-100 text-purple-800';
      case 'Premium':
        return 'bg-amber-100 text-amber-800';
      case 'Enterprise':
        return 'bg-emerald-100 text-emerald-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <MainLayout>
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-white mb-2">Advanced Features</h1>
          <p className="text-lg text-white/60">
            Explore our suite of advanced analysis tools and features to enhance your market insights
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature) => (
            <div
              key={feature.id}
              className="rounded-lg border border-white/10 bg-[#1A1A1A] p-6 space-y-4"
            >
              {/* Feature Header */}
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="h-12 w-12 rounded-lg bg-blue-500/10 text-blue-500 flex items-center justify-center text-lg font-bold">
                    {feature.icon}
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white">{feature.title}</h3>
                    <span className={cn(
                      "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",
                      getTierColor(feature.tier)
                    )}>
                      {feature.tier}
                    </span>
                  </div>
                </div>
              </div>

              {/* Feature Description */}
              <p className="text-sm text-white/60">{feature.description}</p>

              {/* Terms */}
              <p className="text-xs text-white/40">{feature.terms}</p>

              {/* Action Button */}
              <Button
                className={cn(
                  "w-full",
                  activatedFeatures.includes(feature.id)
                    ? "bg-white/10 text-white hover:bg-white/20"
                    : "bg-blue-500 text-white hover:bg-blue-600"
                )}
                onClick={() => handleActivateFeature(feature.id)}
                disabled={activatedFeatures.includes(feature.id)}
              >
                {activatedFeatures.includes(feature.id) ? 'Feature Activated' : 'Activate Feature'}
              </Button>
            </div>
          ))}
        </div>
      </div>
    </MainLayout>
  );
}
```

## src/components/BettingCard.tsx
- Language: TSX
- Encoding: utf-8
- Size: 365 bytes
- Tokens: 100

```tsx
import type { TeamInfo } from '@/lib/types/models/betting';
import type { GameStatus } from '@/lib/types/models/games';

export interface BettingCardProps {
  homeTeam: TeamInfo;
  awayTeam: TeamInfo;
  homeOdds: number;
  awayOdds: number;
  status: GameStatus;
  selectedTeam?: {
    name: string;
    isHome: boolean;
  };
  onBet?: (team: TeamInfo) => void;
}
```

## src/components/atoms/ErrorMessage.tsx
- Language: TSX
- Encoding: utf-8
- Size: 1287 bytes
- Tokens: 341

```tsx
import * as React from 'react';
import { Icon } from '@/components/controls/Icon';
import { HeroIcons } from '@/lib/types/models/icons';
import { cn } from '@/lib/utils';

interface ErrorMessageProps {
  title?: string;
  message: string;
  className?: string;
  variant?: 'default' | 'destructive' | 'warning';
}

export function ErrorMessage({
  title = 'Error',
  message,
  className,
  variant = 'default',
}: ErrorMessageProps) {
  const variantStyles = {
    default: 'bg-red-50 text-red-900 border-red-200',
    destructive: 'bg-red-100 text-red-900 border-red-300',
    warning: 'bg-yellow-50 text-yellow-900 border-yellow-200',
  };

  const iconStyles = {
    default: 'text-red-500',
    destructive: 'text-red-600',
    warning: 'text-yellow-500',
  };

  return (
    <div
      className={cn(
        'rounded-lg border p-4 flex items-start space-x-3',
        variantStyles[variant],
        className
      )}
      role="alert"
    >
      <div className="flex-shrink-0">
        <Icon
          name={HeroIcons.Status.XMark}
          className={cn('h-5 w-5', iconStyles[variant])}
        />
      </div>
      <div>
        <h3 className="text-sm font-medium">{title}</h3>
        <p className="mt-1 text-sm opacity-90">{message}</p>
      </div>
    </div>
  );
}
```

## src/components/controls/AIRecommendations.tsx
- Language: TSX
- Encoding: utf-8
- Size: 5161 bytes
- Tokens: 1102

```tsx
"use client";

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Card } from '@/components/ui/card';
import { Icon } from '@/components/controls/Icon';
import { HeroIcons } from '@/lib/types/models/icons';
import type { Recommendation } from '@/lib/types/models/recommendations';

interface AIRecommendationsProps {
  recommendations: Recommendation[];
  className?: string;
  onSelectRecommendation?: (recommendation: Recommendation) => void;
  isLoading?: boolean;
  error?: string | null;
}

export function AIRecommendations({
  recommendations,
  className,
  onSelectRecommendation,
  isLoading = false,
  error = null,
}: AIRecommendationsProps) {
  const formatBetText = (recommendation: Recommendation) => {
    const { recommendedBet } = recommendation;
    if (recommendedBet.type === 'moneyline') {
      return `${recommendedBet.team} to win @ ${recommendedBet.odds}`;
    } else if (recommendedBet.type === 'spread' && recommendedBet.line !== undefined) {
      return `${recommendedBet.team} ${recommendedBet.line > 0 ? '+' : ''}${recommendedBet.line} @ ${recommendedBet.odds}`;
    } else if (recommendedBet.line !== undefined) {
      return `${recommendedBet.line} ${recommendedBet.type} @ ${recommendedBet.odds}`;
    }
    return recommendedBet.type;
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 80) return 'bg-green-500';
    if (confidence >= 60) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className={cn("space-y-4", className)}>
      <div className="flex items-center justify-between">
        <div className="space-y-1">
          <h2 className="text-2xl font-semibold font-display">AI Recommendations</h2>
          <p className="text-sm text-muted-foreground">
            Data-driven betting recommendations powered by our AI model
          </p>
        </div>
        <Icon 
          name={HeroIcons.Misc.Sparkles} 
          className={cn(
            "h-8 w-8 text-primary",
            isLoading ? "animate-pulse" : "animate-none"
          )}
        />
      </div>

      <div className="grid gap-4">
        {isLoading ? (
          <Card className="p-6">
            <div className="flex items-center justify-center space-x-4">
              <Icon 
                name={HeroIcons.Status.ArrowPath}
                className="h-5 w-5 animate-spin text-muted-foreground"
              />
              <p className="text-sm text-muted-foreground">
                Loading recommendations...
              </p>
            </div>
          </Card>
        ) : error ? (
          <Card className="p-6 text-center">
            <Icon 
              name={HeroIcons.Status.XMark}
              className="h-8 w-8 mx-auto mb-2 text-destructive"
            />
            <h3 className="text-lg font-medium mb-1">Error Loading Recommendations</h3>
            <p className="text-sm text-muted-foreground">
              {error}
            </p>
          </Card>
        ) : recommendations.length > 0 ? (
          recommendations.map((rec) => (
            <Card
              key={rec.id}
              role="button"
              className={cn(
                "p-4 transition-all hover:border-primary cursor-pointer",
                "transform hover:scale-[1.02] hover:shadow-lg"
              )}
              onClick={() => onSelectRecommendation?.(rec)}
            >
              <div className="flex items-start justify-between">
                <div className="space-y-1">
                  <h3 className="font-medium">{rec.homeTeam} vs {rec.awayTeam}</h3>
                  <p className="text-sm text-muted-foreground">
                    {formatBetText(rec)}
                  </p>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="text-right">
                    <div className="text-sm font-medium">
                      {rec.confidence}% Confidence
                    </div>
                    <p className="text-xs text-muted-foreground">
                      {new Date(rec.timestamp).toLocaleTimeString()}
                    </p>
                  </div>
                  <div 
                    data-testid="confidence-indicator"
                    className={cn(
                      "h-2 w-2 rounded-full",
                      getConfidenceColor(rec.confidence)
                    )}
                  />
                </div>
              </div>
              <p className="mt-2 text-sm text-muted-foreground">
                {rec.reasoning}
              </p>
            </Card>
          ))
        ) : (
          <Card className="p-6 text-center">
            <Icon 
              name={HeroIcons.Status.InformationCircle}
              className="h-8 w-8 mx-auto mb-2 text-muted-foreground"
            />
            <h3 className="text-lg font-medium mb-1">No Recommendations</h3>
            <p className="text-sm text-muted-foreground">
              Our AI model is analyzing current games. Check back soon for new recommendations.
            </p>
          </Card>
        )}
      </div>
    </div>
  );
}
```

## src/components/controls/BettingActionGroup.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2438 bytes
- Tokens: 562

```tsx
"use client";

import { cn } from "@/lib/utils";
import * as React from "react";
import { Button } from "./Button";
import { Icon } from "./Icon";
import { HeroIcons } from "@/lib/types/models/icons";

export type BettingAction = "placeBet" | "clearBet" | "addToParlay";

export interface ButtonState {
  disabled?: boolean;
  loading?: boolean;
}

export interface BettingActionGroupProps {
  /** Array of actions to show */
  actions?: BettingAction[];
  /** Optional states for each button */
  buttonStates?: Record<BettingAction, ButtonState>;
  /** Optional className for custom styling */
  className?: string;
  /** Callback when an action is clicked */
  onActionClick?: (action: BettingAction) => void;
}

const actionConfig: Record<BettingAction, { label: string; icon: React.ReactNode }> = {
  placeBet: {
    label: "Place Bet",
    icon: <Icon name={HeroIcons.Commerce.CurrencyDollar} size="sm" />,
  },
  clearBet: {
    label: "Clear Bet",
    icon: <Icon name={HeroIcons.Status.XMark} size="sm" />,
  },
  addToParlay: {
    label: "Add to Parlay",
    icon: <Icon name={HeroIcons.Commerce.CurrencyDollar} size="sm" />,
  },
};

const BettingActionGroup = React.forwardRef<HTMLDivElement, BettingActionGroupProps>(
  ({ 
    actions = ["placeBet", "clearBet", "addToParlay"],
    buttonStates = {},
    className,
    onActionClick,
  }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          "flex flex-col sm:flex-row gap-2",
          className
        )}
      >
        {actions.map((action) => {
          const config = actionConfig[action];
          const state = buttonStates[action] || {};
          
          return (
            <Button
              key={action}
              variant={action === "placeBet" ? "primary" : "outline"}
              className={cn(
                "flex-1",
                config.icon && "flex items-center justify-center gap-2"
              )}
              disabled={state.disabled}
              onClick={() => onActionClick?.(action)}
            >
              {config.icon}
              {config.label}
              {state.loading && (
                <div className="ml-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
              )}
            </Button>
          );
        })}
      </div>
    );
  }
);

BettingActionGroup.displayName = "BettingActionGroup";

export { BettingActionGroup };
```

## src/components/controls/BettingCard.tsx
- Language: TSX
- Encoding: utf-8
- Size: 5663 bytes
- Tokens: 1381

```tsx
"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import type { BettingCardProps } from "@/lib/types/components/betting";
import { Icon } from "./Icon";
import { HeroIcons } from "@/lib/types/models/icons";

export function BettingCard({
  homeTeam,
  awayTeam,
  homeOdds,
  awayOdds,
  status,
  className,
  quickBetAmounts = [5, 10, 25, 50],
  onBet,
  previousHomeOdds,
  previousAwayOdds,
}: BettingCardProps) {
  // Calculate odds movement
  const homeOddsChange = previousHomeOdds ? homeOdds - previousHomeOdds : 0;
  const awayOddsChange = previousAwayOdds ? awayOdds - previousAwayOdds : 0;

  // Function to render odds change indicator
  const renderOddsChange = (change: number) => {
    if (change === 0) return null;
    const isPositive = change > 0;
    return (
      <div 
        data-testid="odds-movement"
        className={cn(
          "flex items-center ml-2 text-xs",
          isPositive ? "text-green-500" : "text-red-500"
        )}
      >
        <Icon
          name={isPositive ? HeroIcons.Navigation.ArrowUp : HeroIcons.Navigation.ArrowDown}
          className="h-3 w-3 mr-0.5"
        />
        {Math.abs(change).toFixed(2)}
      </div>
    );
  };

  return (
    <div className={cn("rounded-lg border bg-[#0A0A0A] p-4 text-white", className)}>
      {/* Status Bar */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          {status.type === 'live' && (
            <span className="flex items-center gap-1.5 px-2 py-1 bg-red-500 text-white text-xs font-medium rounded-full">
              <span className="relative flex h-2 w-2">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-red-400 opacity-75" />
                <span className="relative inline-flex h-2 w-2 rounded-full bg-red-500" />
              </span>
              LIVE
            </span>
          )}
          <span className="text-sm text-gray-400">
            {status.type === 'live' && `${status.period} • ${status.timeRemaining}`}
            {status.type === 'halftime' && 'Halftime'}
            {status.detail}
          </span>
        </div>
      </div>

      {/* Teams */}
      <div className="space-y-6">
        {/* Away Team */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <div>
              <div className="text-lg font-semibold">{awayTeam.name}</div>
              <div className="text-sm text-gray-400">Away</div>
            </div>
            {awayTeam.score !== undefined && (
              <div className="text-2xl font-bold">{awayTeam.score}</div>
            )}
          </div>
          <button
            onClick={() => onBet?.(awayTeam, 0)}
            className={cn(
              "w-full px-4 py-2 bg-[#1A1A1A] hover:bg-[#252525] rounded-md transition-colors",
              awayOddsChange !== 0 && "animate-pulse"
            )}
          >
            <div className="flex items-center justify-between">
              <span>Bet</span>
              <div className="flex items-center">
                <span className="font-semibold">{awayOdds.toFixed(2)}</span>
                {renderOddsChange(awayOddsChange)}
              </div>
            </div>
          </button>
          <div className="grid grid-cols-4 gap-2 mt-2">
            {quickBetAmounts.map((amount) => (
              <button
                key={amount}
                onClick={() => onBet?.(awayTeam, amount)}
                className="flex items-center justify-center p-2 text-sm bg-[#1A1A1A] hover:bg-[#252525] rounded-md transition-colors"
              >
                <Icon name={HeroIcons.Commerce.CurrencyDollar} className="h-4 w-4" />
                {amount}
              </button>
            ))}
          </div>
        </div>

        {/* VS */}
        <div className="flex items-center justify-center">
          <span className="text-gray-400">VS</span>
        </div>

        {/* Home Team */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <div>
              <div className="text-lg font-semibold">{homeTeam.name}</div>
              <div className="text-sm text-gray-400">Home</div>
            </div>
            {homeTeam.score !== undefined && (
              <div className="text-2xl font-bold">{homeTeam.score}</div>
            )}
          </div>
          <button
            onClick={() => onBet?.(homeTeam, 0)}
            className={cn(
              "w-full px-4 py-2 bg-[#1A1A1A] hover:bg-[#252525] rounded-md transition-colors",
              homeOddsChange !== 0 && "animate-pulse"
            )}
          >
            <div className="flex items-center justify-between">
              <span>Bet</span>
              <div className="flex items-center">
                <span className="font-semibold">{homeOdds.toFixed(2)}</span>
                {renderOddsChange(homeOddsChange)}
              </div>
            </div>
          </button>
          <div className="grid grid-cols-4 gap-2 mt-2">
            {quickBetAmounts.map((amount) => (
              <button
                key={amount}
                onClick={() => onBet?.(homeTeam, amount)}
                className="flex items-center justify-center p-2 text-sm bg-[#1A1A1A] hover:bg-[#252525] rounded-md transition-colors"
              >
                <Icon name={HeroIcons.Commerce.CurrencyDollar} className="h-4 w-4" />
                {amount}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

BettingCard.displayName = "BettingCard";
```

## src/components/controls/BettingForm.tsx
- Language: TSX
- Encoding: utf-8
- Size: 7209 bytes
- Tokens: 1656

```tsx
"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import { Button } from "./Button";
import { TextField } from "./TextField";
import { OddsDisplay } from "./OddsDisplay";
import { Icon } from "./Icon";
import { HeroIcons } from "@/lib/types/models/icons";

export type BetType = "single" | "parlay" | "teaser";

export interface BettingFormProps {
  /** The odds value for the bet */
  odds: number;
  /** The format to display odds in */
  oddsFormat?: "decimal" | "fractional" | "american";
  /** The minimum bet amount allowed */
  minBet?: number;
  /** The maximum bet amount allowed */
  maxBet?: number;
  /** Whether the form is in a loading state */
  isLoading?: boolean;
  /** The type of bet */
  betType?: BetType;
  /** Optional className for custom styling */
  className?: string;
  /** Callback when bet is placed */
  onPlaceBet?: (amount: number, betType: BetType) => void;
}

export function BettingForm({
  odds,
  oddsFormat = "decimal",
  minBet = 1,
  maxBet = 10000,
  isLoading = false,
  betType: initialBetType = "single",
  className,
  onPlaceBet,
}: BettingFormProps) {
  const [amount, setAmount] = React.useState<string>("");
  const [error, setError] = React.useState<string>("");
  const [showConfirmation, setShowConfirmation] = React.useState(false);
  const [selectedBetType, setSelectedBetType] = React.useState<BetType>(initialBetType);
  
  const potentialWinnings = React.useMemo(() => {
    const numAmount = parseFloat(amount);
    return !isNaN(numAmount) ? numAmount * odds : 0;
  }, [amount, odds]);

  const validateAmount = React.useCallback((value: string): boolean => {
    if (!value) {
      setError("Please enter a bet amount");
      return false;
    }

    const numValue = parseFloat(value);
    
    if (isNaN(numValue)) {
      setError("Please enter a valid number");
      return false;
    }

    if (numValue < minBet) {
      setError(`Minimum bet is $${minBet}`);
      return false;
    }

    if (numValue > maxBet) {
      setError(`Maximum bet is $${maxBet}`);
      return false;
    }

    if (Math.floor(numValue * 100) !== numValue * 100) {
      setError("Amount must be in increments of $0.01");
      return false;
    }

    setError("");
    return true;
  }, [minBet, maxBet]);

  const handleAmountChange = React.useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setAmount(newValue);
    validateAmount(newValue);
    setShowConfirmation(false);
  }, [validateAmount]);

  const handleQuickAmount = React.useCallback((quickAmount: number) => {
    const newValue = quickAmount.toString();
    setAmount(newValue);
    validateAmount(newValue);
    setShowConfirmation(false);
  }, [validateAmount]);

  const handleSubmit = React.useCallback((e: React.FormEvent) => {
    e.preventDefault();
    if (validateAmount(amount)) {
      if (!showConfirmation) {
        setShowConfirmation(true);
      } else {
        onPlaceBet?.(parseFloat(amount), selectedBetType);
        setShowConfirmation(false);
        setAmount("");
      }
    }
  }, [amount, selectedBetType, showConfirmation, validateAmount, onPlaceBet]);

  const handleCancel = React.useCallback(() => {
    setShowConfirmation(false);
  }, []);

  return (
    <form
      onSubmit={handleSubmit}
      className={cn("space-y-4 rounded-lg border p-4", className)}
    >
      {/* Bet Type Selection */}
      <div className="flex gap-2">
        <Button
          variant={selectedBetType === "single" ? "primary" : "outline"}
          onClick={() => setSelectedBetType("single")}
          className="flex items-center gap-2"
        >
          <Icon name={HeroIcons.Commerce.CurrencyDollar} size="sm" />
          Single
        </Button>
        <Button
          variant={selectedBetType === "parlay" ? "primary" : "outline"}
          onClick={() => setSelectedBetType("parlay")}
          className="flex items-center gap-2"
        >
          <Icon name={HeroIcons.Commerce.Tag} size="sm" />
          Parlay
        </Button>
        <Button
          variant={selectedBetType === "teaser" ? "primary" : "outline"}
          onClick={() => setSelectedBetType("teaser")}
          className="flex items-center gap-2"
        >
          <Icon name={HeroIcons.UI.AdjustmentsHorizontal} size="sm" />
          Teaser
        </Button>
      </div>

      {/* Odds Display */}
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium">Odds:</span>
        <OddsDisplay value={odds} format={oddsFormat} />
      </div>

      {/* Bet Amount Input */}
      <TextField
        label="Bet Amount"
        type="number"
        value={amount}
        onChange={handleAmountChange}
        error={error}
        placeholder={`Enter amount ($${minBet}-$${maxBet})`}
        startIcon={<Icon name={HeroIcons.Commerce.CurrencyDollar} size="sm" />}
        min={minBet}
        max={maxBet}
        step="0.01"
        disabled={isLoading}
      />

      {/* Quick Amount Buttons */}
      <div className="grid grid-cols-4 gap-2">
        {[10, 20, 50, 100].map((quickAmount) => (
          <Button
            key={quickAmount}
            type="button"
            variant="outline"
            size="sm"
            onClick={() => handleQuickAmount(quickAmount)}
            disabled={isLoading}
          >
            <Icon name={HeroIcons.Commerce.CurrencyDollar} size="sm" />
            ${quickAmount}
          </Button>
        ))}
      </div>

      {/* Potential Winnings */}
      <div className="flex items-center justify-between border-t pt-4">
        <span className="text-sm font-medium">Potential Winnings:</span>
        <span className="text-lg font-bold tabular-nums">
          ${potentialWinnings.toFixed(2)}
        </span>
      </div>

      {/* Action Buttons */}
      <div className="space-y-2">
        {showConfirmation ? (
          <>
            <div className="rounded-md bg-muted p-3 text-sm">
              Confirm your {selectedBetType} bet of ${amount} to win ${potentialWinnings.toFixed(2)}?
            </div>
            <div className="grid grid-cols-2 gap-2">
              <Button
                type="button"
                variant="outline"
                onClick={handleCancel}
                disabled={isLoading}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                disabled={!amount || !!error || isLoading}
              >
                Confirm Bet
              </Button>
            </div>
          </>
        ) : (
          <Button
            type="submit"
            className="w-full"
            disabled={!amount || !!error || isLoading}
          >
            {isLoading ? (
              <>
                <Icon name={HeroIcons.Status.ArrowPath} className="mr-2 h-4 w-4 animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <Icon name={HeroIcons.Commerce.CurrencyDollar} className="mr-2 h-4 w-4" />
                Place Bet
              </>
            )}
          </Button>
        )}
      </div>
    </form>
  );
}
```

## src/components/controls/Button.tsx
- Language: TSX
- Encoding: utf-8
- Size: 3349 bytes
- Tokens: 858

```tsx
"use client";

import { cn } from "@/lib/utils";
import { VariantProps, cva } from "class-variance-authority";
import * as React from "react";

const buttonVariants = cva(
  [
    "inline-flex items-center justify-center rounded-md text-sm font-medium",
    "transition-all duration-200 ease-in-out",
    "focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-500",
    "disabled:pointer-events-none disabled:opacity-50",
    "relative overflow-hidden",
  ].join(" "),
  {
    variants: {
      variant: {
        primary: [
          "bg-blue-500 text-white",
          "hover:bg-blue-600 hover:scale-[1.02] hover:shadow-lg hover:shadow-blue-500/20",
          "active:scale-[0.98]",
        ].join(" "),
        secondary: [
          "bg-white/10 text-white",
          "hover:bg-white/20 hover:scale-[1.02] hover:shadow-lg hover:shadow-white/10",
          "active:scale-[0.98]",
        ].join(" "),
        outline: [
          "border border-white/10 bg-transparent text-white",
          "hover:bg-white/5 hover:scale-[1.02] hover:shadow-lg hover:shadow-white/5",
          "active:scale-[0.98]",
        ].join(" "),
        ghost: [
          "bg-transparent text-white",
          "hover:bg-white/5",
          "data-[state=open]:bg-white/10",
        ].join(" "),
      },
      size: {
        sm: "h-8 px-3 text-xs",
        md: "h-10 px-4",
        lg: "h-12 px-6 text-lg",
        icon: "h-9 w-9 p-0",
      },
      isLoading: {
        true: "cursor-wait",
        false: "",
      }
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
      isLoading: false,
    },
  }
);

export type ButtonVariant = NonNullable<VariantProps<typeof buttonVariants>["variant"]>;
export type ButtonSize = NonNullable<VariantProps<typeof buttonVariants>["size"]>;

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  /** Whether the button is in a loading state */
  isLoading?: boolean;
  /** Optional loading text to show next to spinner */
  loadingText?: string;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, isLoading, loadingText, children, disabled, ...props }, ref) => {
    return (
      <button
        className={cn(buttonVariants({ variant, size, isLoading, className }))}
        ref={ref}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading ? (
          <>
            <svg
              className="mr-2 h-4 w-4 animate-spin"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            {loadingText || children}
          </>
        ) : (
          children
        )}
      </button>
    );
  }
);

Button.displayName = "Button";

export { Button, buttonVariants };
```

## src/components/controls/DateTimePicker.tsx
- Language: TSX
- Encoding: utf-8
- Size: 17172 bytes
- Tokens: 2000

```tsx
"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import { Input } from "./Input";
import { IconButton } from "./IconButton";
import { HeroIcons } from "@/lib/types/models/icons";

export type DateTimeMode = "date" | "time" | "datetime";

export interface DateTimePickerProps {
  /** The current value */
  value?: Date;
  /** Callback when value changes */
  onChange?: (value: Date) => void;
  /** The mode of the picker */
  mode?: DateTimeMode;
  /** Minimum allowed date/time */
  min?: Date;
  /** Maximum allowed date/time */
  max?: Date;
  /** Whether the input is disabled */
  disabled?: boolean;
  /** Error message to display */
  error?: string;
  /** Success message to display */
  success?: string;
  /** Optional className for custom styling */
  className?: string;
  /** Placeholder text */
  placeholder?: string;
  /** Label for the input */
  label?: string;
  /** Whether to show clear button */
  clearable?: boolean;
  /** Format for displaying the date/time */
  displayFormat?: string;
}

const DateTimePicker = React.forwardRef<HTMLInputElement, DateTimePickerProps>(
  ({ 
    value,
    onChange,
    mode = "datetime",
    min,
    max,
    disabled,
    error,
    success,
    className,
    placeholder,
    label,
    clearable = true,
    displayFormat,
    ...props
  }, ref) => {
    const [selectedDate, setSelectedDate] = React.useState<Date>(value || new Date());
    const [isOpen, setIsOpen] = React.useState(false);
    const [inputValue, setInputValue] = React.useState("");
    const containerRef = React.useRef<HTMLDivElement>(null);
    const id = React.useId();

    // Format the date based on mode and locale
    const formatValue = React.useCallback((date: Date): string => {
      if (displayFormat) {
        // Use a date formatting library like date-fns for custom formats
        return date.toLocaleString();
      }

      switch (mode) {
        case "date":
          return date.toLocaleDateString();
        case "time":
          return date.toLocaleTimeString(undefined, { 
            hour: "2-digit", 
            minute: "2-digit" 
          });
        default:
          return date.toLocaleString(undefined, {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit"
          });
      }
    }, [mode, displayFormat]);

    // Update input value when date changes
    React.useEffect(() => {
      if (value) {
        setSelectedDate(value);
        setInputValue(formatValue(value));
      }
    }, [value, formatValue]);

    // Handle click outside to close
    React.useEffect(() => {
      const handleClickOutside = (e: MouseEvent) => {
        if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
          setIsOpen(false);
        }
      };

      document.addEventListener("mousedown", handleClickOutside);
      return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    // Handle keyboard navigation
    const handleKeyDown = React.useCallback((e: React.KeyboardEvent) => {
      switch (e.key) {
        case "Escape":
          setIsOpen(false);
          break;
        case "Enter":
        case "Space":
          if (!isOpen) setIsOpen(true);
          break;
        case "Tab":
          if (!e.shiftKey) setIsOpen(false);
          break;
      }
    }, [isOpen]);

    // Handle date selection
    const handleDateSelect = React.useCallback((date: Date) => {
      const newDate = new Date(selectedDate);
      newDate.setFullYear(date.getFullYear());
      newDate.setMonth(date.getMonth());
      newDate.setDate(date.getDate());
      
      setSelectedDate(newDate);
      setInputValue(formatValue(newDate));
      onChange?.(newDate);
    }, [selectedDate, onChange, formatValue]);

    // Handle time selection
    const handleTimeChange = React.useCallback((hours: number, minutes: number) => {
      const newDate = new Date(selectedDate);
      newDate.setHours(hours);
      newDate.setMinutes(minutes);
      
      setSelectedDate(newDate);
      setInputValue(formatValue(newDate));
      onChange?.(newDate);
    }, [selectedDate, onChange, formatValue]);

    // Handle clear
    const handleClear = React.useCallback(() => {
      const newDate = new Date();
      setSelectedDate(newDate);
      setInputValue("");
      onChange?.(newDate);
      setIsOpen(false);
    }, [onChange]);

    return (
      <div 
        ref={containerRef}
        className={cn("relative", className)}
        onKeyDown={handleKeyDown}
      >
        {label && (
          <label
            htmlFor={id}
            className="mb-2 block text-sm font-medium text-foreground"
          >
            {label}
          </label>
        )}
        
        <div className="relative">
          <Input
            ref={ref}
            id={id}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onFocus={() => setIsOpen(true)}
            placeholder={placeholder || (
              mode === "date" ? "Select date" :
              mode === "time" ? "Select time" :
              "Select date and time"
            )}
            disabled={disabled}
            error={error}
            success={success}
            className={cn(
              "pr-20", // Space for icons
              mode === "time" && "appearance-none"
            )}
            aria-expanded={isOpen}
            aria-haspopup="dialog"
            aria-controls={`${id}-calendar`}
            {...props}
          />
          
          <div className="absolute inset-y-0 right-0 flex items-center gap-1 pr-3">
            {clearable && inputValue && (
              <IconButton
                icon={HeroIcons.Status.XMark}
                label="Clear date"
                variant="secondary"
                size="sm"
                onClick={handleClear}
                className="h-7 w-7 rounded-full hover:bg-muted/60"
                tooltip="Clear date"
              />
            )}
            <IconButton
              icon={HeroIcons.DateTime.Calendar}
              label={isOpen ? "Close calendar" : "Open calendar"}
              variant="secondary"
              size="sm"
              onClick={() => setIsOpen(true)}
              className="h-7 w-7 rounded-full hover:bg-muted/60"
              tooltip={isOpen ? "Close calendar" : "Open calendar"}
            />
          </div>
        </div>

        {isOpen && !disabled && (
          <div
            id={`${id}-calendar`}
            className={cn(
              "absolute z-50 mt-2 animate-in fade-in-0 zoom-in-95",
              "w-[280px] rounded-lg border bg-card shadow-md",
              "outline-none focus-visible:ring-2 focus-visible:ring-ring"
            )}
            role="dialog"
            aria-label={mode === "time" ? "Time picker" : "Calendar"}
            tabIndex={-1}
          >
            {/* Header with close button */}
            <div className="flex items-center justify-between border-b p-3">
              <span className="text-sm font-medium">
                {inputValue || "Select date and time"}
              </span>
              <IconButton
                icon={HeroIcons.Status.XMark}
                label="Close picker"
                variant="secondary"
                size="sm"
                onClick={() => setIsOpen(false)}
                className="h-6 w-6 rounded-full hover:bg-muted/60"
                tooltip="Close picker"
              />
            </div>

            {(mode === "date" || mode === "datetime") && (
              <div className="p-3">
                {/* Month/Year Navigation */}
                <div className="mb-4 flex items-center justify-between gap-2">
                  <select
                    value={selectedDate.getMonth()}
                    onChange={(e) => {
                      const newDate = new Date(selectedDate);
                      newDate.setMonth(parseInt(e.target.value));
                      handleDateSelect(newDate);
                    }}
                    className="h-9 flex-1 rounded-md border bg-transparent px-2 py-1 text-sm hover:bg-muted/50"
                    aria-label="Select month"
                  >
                    {Array.from({ length: 12 }, (_, i) => (
                      <option key={i} value={i}>
                        {new Date(0, i).toLocaleString("default", { month: "long" })}
                      </option>
                    ))}
                  </select>
                  <select
                    value={selectedDate.getFullYear()}
                    onChange={(e) => {
                      const newDate = new Date(selectedDate);
                      newDate.setFullYear(parseInt(e.target.value));
                      handleDateSelect(newDate);
                    }}
                    className="h-9 w-24 rounded-md border bg-transparent px-2 py-1 text-sm hover:bg-muted/50"
                    aria-label="Select year"
                  >
                    {Array.from({ length: 10 }, (_, i) => {
                      const year = new Date().getFullYear() - 5 + i;
                      return (
                        <option key={year} value={year}>
                          {year}
                        </option>
                      );
                    })}
                  </select>
                </div>

                {/* Calendar Grid */}
                <div className="space-y-2">
                  <div className="grid grid-cols-7 gap-1 text-center text-xs font-medium text-muted-foreground">
                    {["Su", "Mo", "Tu", "We", "
```

## src/components/controls/Features.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2192 bytes
- Tokens: 508

```tsx
import * as React from 'react';
import { Card } from '@/components/ui/card';

interface Feature {
  id: string;
  title: string;
  description: string;
  type: 'ai' | 'analysis' | 'alerts' | 'custom';
  value: string;
  expiresAt?: string | null;
  terms: string;
}

interface FeaturesProps {
  features: Feature[];
  onActivateFeature?: (id: string) => void;
}

export function Features({ features, onActivateFeature }: FeaturesProps) {
  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {features.map((feature) => (
        <Card key={feature.id} className="p-6">
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0 h-12 w-12 flex items-center justify-center rounded-lg bg-blue-100 text-blue-900">
              <span className="text-lg font-bold">
                {feature.type === 'ai' ? 'AI' :
                 feature.type === 'analysis' ? 'A' :
                 feature.type === 'alerts' ? '!' :
                 'C'}
              </span>
            </div>
            <div>
              <h3 className="text-lg font-medium">
                {feature.title}
                <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {feature.value}
                </span>
              </h3>
              <p className="mt-2 text-sm text-gray-600">
                {feature.description}
              </p>
              {feature.terms && (
                <p className="mt-2 text-xs text-gray-500">
                  {feature.terms}
                </p>
              )}
              {onActivateFeature && (
                <button
                  onClick={() => onActivateFeature(feature.id)}
                  className="mt-4 inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Activate Feature
                </button>
              )}
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
}
```

## src/components/controls/Icon.tsx
- Language: TSX
- Encoding: utf-8
- Size: 4605 bytes
- Tokens: 1163

```tsx
"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import * as HeroiconsSolid from "@heroicons/react/24/solid";
import * as HeroiconsOutline from "@heroicons/react/24/outline";
import type { HeroIconName } from "@/lib/types/models/icons";

export type ThemeColor = 
  | "primary"
  | "secondary"
  | "accent"
  | "muted"
  | "foreground"
  | "background"
  | "border"
  | "ring"
  | "destructive"
  | "success"
  | "warning"
  | "info";

export interface IconProps {
  /** Name of the Heroicon */
  name: HeroIconName;
  /** Whether to use the solid or outline variant */
  solid?: boolean;
  /** Size of the icon */
  size?: "sm" | "md" | "lg" | "xl";
  /** Optional className for custom styling */
  className?: string;
  /** Accessible label for the icon */
  label?: string;
  /** Direction of the label relative to the icon */
  labelDirection?: "left" | "right" | "top" | "bottom";
  /** Theme color for the icon */
  color?: ThemeColor;
  /** Whether the icon should spin (for loading states) */
  spin?: boolean;
  /** Whether the icon should pulse (for attention states) */
  pulse?: boolean;
  /** Optional click handler */
  onClick?: (event: React.MouseEvent<HTMLSpanElement>) => void;
}

const sizeClasses = {
  sm: "h-4 w-4",
  md: "h-6 w-6",
  lg: "h-8 w-8",
  xl: "h-10 w-10",
} as const;

const labelDirectionClasses = {
  left: "flex-row-reverse",
  right: "flex-row",
  top: "flex-col-reverse",
  bottom: "flex-col",
} as const;

const colorClasses: Record<ThemeColor, string> = {
  primary: "text-primary",
  secondary: "text-secondary",
  accent: "text-accent",
  muted: "text-muted",
  foreground: "text-foreground",
  background: "text-background",
  border: "text-border",
  ring: "text-ring",
  destructive: "text-destructive",
  success: "text-emerald-500 dark:text-emerald-400",
  warning: "text-amber-500 dark:text-amber-400",
  info: "text-blue-500 dark:text-blue-400",
} as const;

const spinAnimation = "animate-spin";
const pulseAnimation = "animate-pulse";

export const Icon = React.forwardRef<HTMLSpanElement, IconProps>(({
  name,
  solid = false,
  size = "md",
  className,
  label,
  labelDirection = "right",
  color,
  spin = false,
  pulse = false,
  onClick,
  ...props
}, ref) => {
  // Get the icon component from the appropriate Heroicons collection
  const IconComponent = React.useMemo(() => {
    const collection = solid ? HeroiconsSolid : HeroiconsOutline;
    return collection[name as keyof typeof collection] || null;
  }, [solid, name]);

  if (!IconComponent) {
    console.warn(`Icon "${name}" not found in Heroicons ${solid ? 'solid' : 'outline'} set`);
    return null;
  }

  const handleClick = (event: React.MouseEvent<HTMLSpanElement>) => {
    if (onClick) {
      event.stopPropagation();
      onClick(event);
    }
  };

  const iconElement = (
    <IconComponent
      className={cn(
        sizeClasses[size],
        color && colorClasses[color],
        spin && spinAnimation,
        pulse && pulseAnimation,
        !label && className,
        "transition-colors duration-200"
      )}
      aria-hidden={!label}
      {...props}
    />
  );

  if (label) {
    return (
      <span 
        ref={ref}
        className={cn(
          "inline-flex items-center gap-2",
          labelDirectionClasses[labelDirection],
          className,
          "select-none",
          onClick && "cursor-pointer hover:opacity-80"
        )}
        role={onClick ? "button" : "img"}
        aria-label={label}
        onClick={handleClick}
        tabIndex={onClick ? 0 : undefined}
        onKeyDown={(e) => {
          if (onClick && (e.key === "Enter" || e.key === " ")) {
            e.preventDefault();
            onClick(e as unknown as React.MouseEvent<HTMLSpanElement>);
          }
        }}
      >
        {iconElement}
        <span className={cn(
          "text-sm font-medium",
          color && colorClasses[color]
        )}>
          {label}
        </span>
      </span>
    );
  }

  return (
    <span
      ref={ref}
      className={cn(
        "inline-flex",
        onClick && "cursor-pointer hover:opacity-80",
        "select-none"
      )}
      role={onClick ? "button" : "presentation"}
      onClick={handleClick}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={(e) => {
        if (onClick && (e.key === "Enter" || e.key === " ")) {
          e.preventDefault();
          onClick(e as unknown as React.MouseEvent<HTMLSpanElement>);
        }
      }}
      {...props}
    >
      {iconElement}
    </span>
  );
});

Icon.displayName = "Icon";

export default Icon;
```

## src/components/controls/IconButton.tsx
- Language: TSX
- Encoding: utf-8
- Size: 1808 bytes
- Tokens: 433

```tsx
"use client";

import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";
import { Icon } from "./Icon";
import type { HeroIconName } from "@/lib/types/models/icons";

const iconButtonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        ghost: "hover:bg-accent hover:text-accent-foreground",
      },
      size: {
        sm: "h-8 w-8",
        md: "h-10 w-10",
        lg: "h-12 w-12",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
);

export interface IconButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof iconButtonVariants> {
  icon: HeroIconName;
  label: string;
  solid?: boolean;
  tooltip?: string;
}

export const IconButton = React.forwardRef<HTMLButtonElement, IconButtonProps>(
  ({ className, variant, size, icon, label, solid = false, tooltip, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(iconButtonVariants({ variant, size, className }))}
        aria-label={label}
        title={tooltip}
        {...props}
      >
        <Icon name={icon} solid={solid} className="h-5 w-5" />
      </button>
    );
  }
);

IconButton.displayName = "IconButton";
```

## src/components/controls/Input.tsx
- Language: TSX
- Encoding: utf-8
- Size: 6655 bytes
- Tokens: 1834

```tsx
"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import { cva, type VariantProps } from "class-variance-authority";

const inputVariants = cva(
  "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "",
        error: "border-destructive focus-visible:ring-destructive",
        success: "border-emerald-500 focus-visible:ring-emerald-500",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

export type InputPattern = 
  | "any"
  | "numeric"
  | "alphanumeric"
  | "alphabetical"
  | "date"
  | "time"
  | "datetime"
  | "email"
  | "phone"
  | "currency"
  | "percentage";

export interface InputProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "pattern">,
    VariantProps<typeof inputVariants> {
  /** Input pattern restriction */
  pattern?: InputPattern;
  /** Error message to display */
  error?: string;
  /** Success message to display */
  success?: string;
  /** Whether to show the clear button */
  clearable?: boolean;
  /** Format the input value according to pattern */
  formatValue?: boolean;
}

const patterns = {
  any: ".*",
  numeric: "^[0-9]*$",
  alphanumeric: "^[a-zA-Z0-9]*$",
  alphabetical: "^[a-zA-Z]*$",
  date: "^\\d{4}-\\d{2}-\\d{2}$",
  time: "^\\d{2}:\\d{2}$",
  datetime: "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}$",
  email: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
  phone: "^[0-9-+() ]*$",
  currency: "^\\$?\\d*\\.?\\d*$",
  percentage: "^\\d*\\.?\\d*%?$",
};

const formatters = {
  any: (value: string) => value,
  numeric: (value: string) => value.replace(/[^0-9]/g, ""),
  alphanumeric: (value: string) => value.replace(/[^a-zA-Z0-9]/g, ""),
  alphabetical: (value: string) => value.replace(/[^a-zA-Z]/g, ""),
  date: (value: string) => {
    const numbers = value.replace(/[^0-9]/g, "");
    if (numbers.length <= 4) return numbers;
    if (numbers.length <= 6) return `${numbers.slice(0, 4)}-${numbers.slice(4)}`;
    return `${numbers.slice(0, 4)}-${numbers.slice(4, 6)}-${numbers.slice(6, 8)}`;
  },
  time: (value: string) => {
    const numbers = value.replace(/[^0-9]/g, "");
    if (numbers.length <= 2) return numbers;
    return `${numbers.slice(0, 2)}:${numbers.slice(2, 4)}`;
  },
  datetime: (value: string) => {
    const numbers = value.replace(/[^0-9]/g, "");
    if (numbers.length <= 4) return numbers;
    if (numbers.length <= 6) return `${numbers.slice(0, 4)}-${numbers.slice(4)}`;
    if (numbers.length <= 8) return `${numbers.slice(0, 4)}-${numbers.slice(4, 6)}-${numbers.slice(6, 8)}`;
    if (numbers.length <= 10) return `${numbers.slice(0, 4)}-${numbers.slice(4, 6)}-${numbers.slice(6, 8)}T${numbers.slice(8)}`;
    return `${numbers.slice(0, 4)}-${numbers.slice(4, 6)}-${numbers.slice(6, 8)}T${numbers.slice(8, 10)}:${numbers.slice(10, 12)}`;
  },
  email: (value: string) => value,
  phone: (value: string) => {
    const numbers = value.replace(/[^0-9]/g, "");
    if (numbers.length <= 3) return numbers;
    if (numbers.length <= 6) return `(${numbers.slice(0, 3)}) ${numbers.slice(3)}`;
    return `(${numbers.slice(0, 3)}) ${numbers.slice(3, 6)}-${numbers.slice(6, 10)}`;
  },
  currency: (value: string) => {
    const numbers = value.replace(/[^0-9.]/g, "");
    const parts = numbers.split(".");
    if (parts.length > 2) return parts[0] + "." + parts.slice(1).join("");
    const formatted = new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: parts.length > 1 ? 2 : 0,
      maximumFractionDigits: 2,
    }).format(Number(numbers) || 0);
    return formatted;
  },
  percentage: (value: string) => {
    const numbers = value.replace(/[^0-9.]/g, "");
    const parts = numbers.split(".");
    if (parts.length > 2) return parts[0] + "." + parts.slice(1).join("");
    return numbers + "%";
  },
};

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ 
    className,
    type = "text",
    pattern = "any",
    variant,
    error,
    success,
    clearable,
    formatValue = true,
    value,
    onChange,
    ...props 
  }, ref) => {
    const [localValue, setLocalValue] = React.useState(value?.toString() || "");

    React.useEffect(() => {
      setLocalValue(value?.toString() || "");
    }, [value]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      let newValue = e.target.value;
      
      // Apply pattern restriction
      if (pattern !== "any") {
        const regex = new RegExp(patterns[pattern]);
        if (!regex.test(newValue) && !formatValue) return;
      }

      // Apply formatting
      if (formatValue && pattern in formatters) {
        newValue = formatters[pattern](newValue);
      }

      setLocalValue(newValue);
      
      if (onChange) {
        e.target.value = newValue;
        onChange(e);
      }
    };

    const handleClear = () => {
      setLocalValue("");
      if (onChange) {
        const event = {
          target: { value: "" },
        } as React.ChangeEvent<HTMLInputElement>;
        onChange(event);
      }
    };

    // Determine variant based on error/success state
    const inputVariant = error ? "error" : success ? "success" : variant;

    return (
      <div className="relative">
        <input
          type={type}
          value={localValue}
          onChange={handleChange}
          className={cn(
            inputVariants({ variant: inputVariant }),
            clearable && localValue && "pr-8",
            className
          )}
          ref={ref}
          {...props}
        />
        {clearable && localValue && (
          <button
            type="button"
            className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground/60 hover:text-muted-foreground"
            onClick={handleClear}
            aria-label="Clear input"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="h-4 w-4"
            >
              <path d="M18 6L6 18M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>
    );
  }
);

Input.displayName = "Input";

export { Input, inputVariants };
```

## src/components/controls/Leaderboard.tsx
- Language: TSX
- Encoding: utf-8
- Size: 7181 bytes
- Tokens: 1586

```tsx
"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import { Button } from "./Button";
import { Icon } from "./Icon";
import { HeroIcons } from "@/lib/types/models/icons";

export interface LeaderboardEntry {
  id: string;
  rank: number;
  username: string;
  winnings: number;
  winRate: number;
  parlayStreak: number;
  totalBets: number;
}

export interface LeaderboardProps {
  /** Array of leaderboard entries */
  entries: LeaderboardEntry[];
  /** The time period for the leaderboard */
  timePeriod: "daily" | "weekly" | "monthly" | "all-time";
  /** The sport type filter */
  sportType: "all" | "NFL" | "NBA" | "MLB" | "NHL";
  /** Optional className for custom styling */
  className?: string;
  /** Callback when time period changes */
  onTimePeriodChange?: (period: LeaderboardProps["timePeriod"]) => void;
  /** Callback when sport type changes */
  onSportTypeChange?: (sport: LeaderboardProps["sportType"]) => void;
}

export function Leaderboard({
  entries,
  timePeriod,
  sportType,
  className,
  onTimePeriodChange,
  onSportTypeChange,
}: LeaderboardProps) {
  return (
    <div className={cn("space-y-6", className)}>
      {/* Filters */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        {/* Time Period Filter */}
        <div className="flex flex-wrap gap-2">
          <Button
            variant={timePeriod === "daily" ? "primary" : "outline"}
            onClick={() => onTimePeriodChange?.("daily")}
            size="sm"
          >
            Daily
          </Button>
          <Button
            variant={timePeriod === "weekly" ? "primary" : "outline"}
            onClick={() => onTimePeriodChange?.("weekly")}
            size="sm"
          >
            Weekly
          </Button>
          <Button
            variant={timePeriod === "monthly" ? "primary" : "outline"}
            onClick={() => onTimePeriodChange?.("monthly")}
            size="sm"
          >
            Monthly
          </Button>
          <Button
            variant={timePeriod === "all-time" ? "primary" : "outline"}
            onClick={() => onTimePeriodChange?.("all-time")}
            size="sm"
          >
            All Time
          </Button>
        </div>

        {/* Sport Type Filter */}
        <div className="flex flex-wrap gap-2">
          <Button
            variant={sportType === "all" ? "primary" : "outline"}
            onClick={() => onSportTypeChange?.("all")}
            size="sm"
          >
            All Sports
          </Button>
          <Button
            variant={sportType === "NFL" ? "primary" : "outline"}
            onClick={() => onSportTypeChange?.("NFL")}
            size="sm"
          >
            NFL
          </Button>
          <Button
            variant={sportType === "NBA" ? "primary" : "outline"}
            onClick={() => onSportTypeChange?.("NBA")}
            size="sm"
          >
            NBA
          </Button>
          <Button
            variant={sportType === "MLB" ? "primary" : "outline"}
            onClick={() => onSportTypeChange?.("MLB")}
            size="sm"
          >
            MLB
          </Button>
          <Button
            variant={sportType === "NHL" ? "primary" : "outline"}
            onClick={() => onSportTypeChange?.("NHL")}
            size="sm"
          >
            NHL
          </Button>
        </div>
      </div>

      {/* Leaderboard Table */}
      <div className="rounded-lg border bg-card">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b bg-muted/50">
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">Rank</th>
                <th className="px-4 py-3 text-left text-sm font-medium text-muted-foreground">User</th>
                <th className="px-4 py-3 text-right text-sm font-medium text-muted-foreground">Winnings</th>
                <th className="hidden px-4 py-3 text-right text-sm font-medium text-muted-foreground sm:table-cell">Win Rate</th>
                <th className="hidden px-4 py-3 text-right text-sm font-medium text-muted-foreground sm:table-cell">Parlay Streak</th>
                <th className="hidden px-4 py-3 text-right text-sm font-medium text-muted-foreground sm:table-cell">Total Bets</th>
              </tr>
            </thead>
            <tbody>
              {entries.map((entry) => (
                <tr
                  key={entry.id}
                  className="border-b last:border-0 hover:bg-muted/50"
                >
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      {entry.rank <= 3 && (
                        <Icon
                          name={HeroIcons.Misc.Trophy}
                          size="sm"
                          className={cn(
                            entry.rank === 1 && "text-yellow-500",
                            entry.rank === 2 && "text-gray-400",
                            entry.rank === 3 && "text-amber-600"
                          )}
                        />
                      )}
                      <span className="font-medium">{entry.rank}</span>
                    </div>
                  </td>
                  <td className="px-4 py-3 font-medium">{entry.username}</td>
                  <td className="px-4 py-3 text-right font-mono">
                    <div className="flex items-center justify-end gap-1">
                      <Icon
                        name={HeroIcons.Commerce.CurrencyDollar}
                        size="sm"
                        className="text-emerald-500"
                      />
                      {entry.winnings.toLocaleString()}
                    </div>
                  </td>
                  <td className="hidden px-4 py-3 text-right sm:table-cell">
                    <div className="flex items-center justify-end gap-1">
                      <Icon
                        name={HeroIcons.Data.ChartPie}
                        size="sm"
                        className="text-blue-500"
                      />
                      {entry.winRate}%
                    </div>
                  </td>
                  <td className="hidden px-4 py-3 text-right font-mono sm:table-cell">{entry.parlayStreak}</td>
                  <td className="hidden px-4 py-3 text-right font-mono sm:table-cell">{entry.totalBets}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Empty State */}
        {entries.length === 0 && (
          <div className="flex flex-col items-center justify-center p-8 text-center">
            <Icon
              name={HeroIcons.Status.InformationCircle}
              className="mb-2 h-8 w-8 text-muted-foreground"
            />
            <h3 className="text-lg font-semibold">No data available</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              Check back later for updated rankings
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
```

## src/components/controls/LiveScoreCard.tsx
- Language: TSX
- Encoding: utf-8
- Size: 4366 bytes
- Tokens: 997

```tsx
"use client";

import { cn } from "@/lib/utils";
import * as React from "react";
import { Icon } from "./Icon";
import { HeroIcons } from "@/lib/types/models/icons";

export interface TeamInfo {
  name: string;
  score: number;
  isHome: boolean;
  possession?: boolean;
}

export interface KeyStats {
  timeRemaining: string;
  period: string;
  periodType: "quarter" | "period" | "half";
  possession?: "home" | "away";
  lastPlay?: string;
}

export type SportType = "NFL" | "NBA";

export interface LiveScoreCardProps {
  /** The home and away teams */
  teams: [TeamInfo, TeamInfo];
  /** The current game status (e.g., "Live", "Halftime", "Final") */
  gameStatus: string;
  /** Key statistics about the game */
  keyStats: KeyStats;
  /** The type of sport */
  sportType: SportType;
  /** Optional className for custom styling */
  className?: string;
  /** Optional click handler */
  onClick?: () => void;
}

const LiveScoreCard = React.forwardRef<HTMLDivElement, LiveScoreCardProps>(
  ({ teams, gameStatus, keyStats, sportType, className, onClick }, ref) => {
    const [awayTeam, homeTeam] = teams;
    const isLive = gameStatus.toLowerCase() === "live";

    return (
      <div
        ref={ref}
        className={cn(
          "rounded-lg border border-border bg-card p-4 text-card-foreground shadow-sm dark:border-border/20",
          onClick && "cursor-pointer hover:border-primary/50 transition-colors",
          className
        )}
        onClick={onClick}
      >
        {/* Game Status Header */}
        <div className="mb-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            {isLive && (
              <span className="relative flex h-3 w-3">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-red-400 opacity-75"></span>
                <span className="relative inline-flex h-3 w-3 rounded-full bg-red-500"></span>
              </span>
            )}
            <span className="font-medium text-sm">
              {gameStatus}
            </span>
          </div>
          <div className="flex items-center gap-1 text-sm text-muted-foreground">
            <Icon name={HeroIcons.UI.Check} size="sm" />
            {sportType} • {keyStats.periodType === "quarter" ? "Q" : keyStats.periodType === "period" ? "P" : "H"}
            {keyStats.period}
          </div>
        </div>

        {/* Teams and Scores */}
        <div className="mb-4 space-y-4">
          {/* Away Team */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className={cn(
                "font-medium",
                keyStats.possession === "away" && "text-primary font-bold"
              )}>
                {awayTeam.name}
                {keyStats.possession === "away" && " •"}
              </span>
            </div>
            <span className="text-2xl font-bold tabular-nums">
              {awayTeam.score}
            </span>
          </div>

          {/* Home Team */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className={cn(
                "font-medium",
                keyStats.possession === "home" && "text-primary font-bold"
              )}>
                {homeTeam.name}
                {keyStats.possession === "home" && " •"}
              </span>
            </div>
            <span className="text-2xl font-bold tabular-nums">
              {homeTeam.score}
            </span>
          </div>
        </div>

        {/* Game Info */}
        <div className="space-y-2 text-sm text-muted-foreground">
          <div className="flex justify-between">
            <span>Time Remaining:</span>
            <span className="font-medium text-foreground">
              {keyStats.timeRemaining}
            </span>
          </div>
          {keyStats.lastPlay && (
            <div className="flex justify-between">
              <span>Last Play:</span>
              <span className="font-medium text-foreground max-w-[60%] text-right">
                {keyStats.lastPlay}
              </span>
            </div>
          )}
        </div>
      </div>
    );
  }
);

LiveScoreCard.displayName = "LiveScoreCard";

export { LiveScoreCard };
```

## src/components/controls/MarketCard.tsx
- Language: TSX
- Encoding: utf-8
- Size: 4396 bytes
- Tokens: 947

```tsx
import * as React from 'react';
import { Card } from '@/components/ui/card';
import { cn, formatCurrency } from '@/lib/utils';
import type { GameStatus } from '@/lib/types/models/games';

interface TeamInfo {
  name: string;
  score?: number;
  isHome: boolean;
}

export interface MarketCardProps {
  homeTeam: TeamInfo;
  awayTeam: TeamInfo;
  homeOdds: number;
  awayOdds: number;
  status: GameStatus;
  selectedTeam?: TeamInfo;
  className?: string;
  onSelect?: (team: 'home' | 'away') => void;
}

export function MarketCard({
  homeTeam,
  awayTeam,
  homeOdds,
  awayOdds,
  status,
  selectedTeam,
  className,
  onSelect,
}: MarketCardProps) {
  return (
    <Card className={cn("p-4", className)}>
      <div className="space-y-4">
        {/* Game Time & Status */}
        <div className="flex items-center justify-between text-sm text-muted-foreground">
          <div>
            {status.type === "upcoming" && status.startTime}
            {status.type === "live" && (
              <span className="font-medium text-primary">
                {status.period} • {status.timeRemaining}
              </span>
            )}
            {status.type === "halftime" && (
              <span className="font-medium text-orange-500">Halftime</span>
            )}
            {status.type === "final" && (
              <span className="font-medium">Final</span>
            )}
            {status.type === "postponed" && (
              <span className="font-medium text-yellow-500">Postponed</span>
            )}
            {status.type === "cancelled" && (
              <span className="font-medium text-rose-500">Cancelled</span>
            )}
          </div>
        </div>

        {/* Teams */}
        <div className="grid grid-cols-[1fr_auto_1fr] gap-4">
          {/* Away Team */}
          <div>
            <div className="flex items-center gap-2">
              <div className="font-semibold">
                {awayTeam.name}
                {status.possession === "away" && (
                  <span className="ml-1 text-primary">•</span>
                )}
              </div>
              {awayTeam.score !== undefined && (
                <div className="text-lg font-bold tabular-nums">
                  {awayTeam.score}
                </div>
              )}
            </div>
            <div className="text-sm text-muted-foreground">Away</div>
            {onSelect && (
              <button
                onClick={() => onSelect('away')}
                className={cn(
                  "mt-2 w-full px-3 py-2 text-sm font-medium rounded-md transition-colors",
                  selectedTeam?.name === awayTeam.name
                    ? "bg-primary text-primary-foreground"
                    : "border border-input bg-background hover:bg-accent hover:text-accent-foreground"
                )}
              >
                {formatCurrency(awayOdds, 'USD')}
              </button>
            )}
          </div>

          {/* VS Divider */}
          <div className="flex items-center justify-center">
            <div className="text-sm font-medium text-muted-foreground">VS</div>
          </div>

          {/* Home Team */}
          <div>
            <div className="flex items-center gap-2">
              <div className="font-semibold">
                {homeTeam.name}
                {status.possession === "home" && (
                  <span className="ml-1 text-primary">•</span>
                )}
              </div>
              {homeTeam.score !== undefined && (
                <div className="text-lg font-bold tabular-nums">
                  {homeTeam.score}
                </div>
              )}
            </div>
            <div className="text-sm text-muted-foreground">Home</div>
            {onSelect && (
              <button
                onClick={() => onSelect('home')}
                className={cn(
                  "mt-2 w-full px-3 py-2 text-sm font-medium rounded-md transition-colors",
                  selectedTeam?.name === homeTeam.name
                    ? "bg-primary text-primary-foreground"
                    : "border border-input bg-background hover:bg-accent hover:text-accent-foreground"
                )}
              >
                {formatCurrency(homeOdds, 'USD')}
              </button>
            )}
          </div>
        </div>
      </div>
    </Card>
  );
}
```

## src/components/controls/MultiMarketAnalysis.tsx
- Language: TSX
- Encoding: utf-8
- Size: 5591 bytes
- Tokens: 1256

```tsx
import * as React from 'react';
import { Card } from '@/components/ui/card';
import type { MultiMarketAnalysis as MultiMarketAnalysisType } from '@/lib/types/models/analysis';
import { formatCurrency } from '@/lib/utils';
import type { MarketCardProps } from './MarketCard';
import { ErrorBoundary } from '@/components/organisms/ErrorBoundary';
import { ErrorState } from '@/components/molecules/ErrorState';

interface MultiMarketAnalysisProps {
  marketCards: MarketCardProps[];
  onRemoveMarket: (index: number) => void;
  onAnalyze: (analysis: MultiMarketAnalysisType) => void;
}

export function MultiMarketAnalysis({
  marketCards,
  onRemoveMarket,
  onAnalyze,
}: MultiMarketAnalysisProps) {
  const handleAnalyze = React.useCallback(() => {
    try {
      // Create a mock analysis for demonstration
      const analysis: MultiMarketAnalysisType = {
        id: Date.now().toString(),
        analyses: marketCards.map((card, index) => ({
          id: `${index}`,
          correlationStrength: Math.random(),
          confidence: Math.random(),
          potentialValue: Math.random() * 1000,
          status: 'active',
          createdAt: new Date().toISOString(),
          market: {
            homeTeam: card.homeTeam.name,
            awayTeam: card.awayTeam.name,
            status: {
              type: 'live',
              period: card.status.period || '1st',
              timeRemaining: card.status.timeRemaining || '12:00',
              possession: card.status.possession,
              startTime: card.status.startTime || new Date().toISOString(),
            },
            homeScore: card.homeTeam.score || 0,
            awayScore: card.awayTeam.score || 0,
            startTime: card.status.startTime || new Date().toISOString(),
          },
          predictedOutcome: card.selectedTeam?.name || card.homeTeam.name,
        })),
        correlationStrength: Math.random(),
        confidence: Math.random(),
        potentialValue: Math.random() * 2000,
        status: 'active',
        createdAt: new Date().toISOString(),
      };

      onAnalyze(analysis);
    } catch (error) {
      console.error('Error during analysis:', error);
      throw error; // Let ErrorBoundary handle it
    }
  }, [marketCards, onAnalyze]);

  return (
    <ErrorBoundary
      fallback={
        <ErrorState
          title="Analysis Error"
          message="An error occurred while analyzing the markets. Please try again."
          actions={{
            primary: {
              label: 'Retry',
              onClick: handleAnalyze,
            },
          }}
        />
      }
    >
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-semibold font-display">Selected Markets</h3>
          <button
            onClick={handleAnalyze}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Analyze Markets
          </button>
        </div>

        <div className="space-y-4">
          {marketCards.map((card, index) => (
            <div key={index} className="relative">
              <button
                onClick={() => onRemoveMarket(index)}
                className="absolute -top-2 -right-2 p-1 rounded-full bg-red-500 text-white hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-4 w-4"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
              <Card className="p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-medium font-display">
                      {card.homeTeam.name} vs {card.awayTeam.name}
                    </h4>
                    <p className="mt-1 text-sm text-gray-500 font-sans">
                      {card.status.type === 'live' ? (
                        <>
                          {card.status.period} - {card.status.timeRemaining}
                          {card.status.possession && (
                            <span className="ml-2">
                              {card.status.possession === 'home' ? card.homeTeam.name : card.awayTeam.name} possession
                            </span>
                          )}
                        </>
                      ) : (
                        card.status.startTime
                      )}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium font-display">Selected: {card.selectedTeam?.name}</p>
                    <p className="mt-1 text-xs text-gray-500 font-sans">
                      Odds: {formatCurrency(card.selectedTeam?.isHome ? card.homeOdds : card.awayOdds, 'USD')}
                    </p>
                  </div>
                </div>
              </Card>
            </div>
          ))}
        </div>
      </div>
    </ErrorBoundary>
  );
}
```

## src/components/controls/OddsDisplay.tsx
- Language: TSX
- Encoding: utf-8
- Size: 4156 bytes
- Tokens: 1077

```tsx
"use client";

import { cn } from "@/lib/utils";
import * as React from "react";

export type OddsFormat = "decimal" | "fractional" | "american";

export interface OddsDisplayProps {
  /** The odds value in decimal format */
  value: number;
  /** The format to display the odds in */
  format?: OddsFormat;
  /** Optional previous value to show change animation */
  previousValue?: number;
  /** Optional className for custom styling */
  className?: string;
}

const formatOdds = (value: number, format: OddsFormat): string => {
  switch (format) {
    case "decimal":
      return value.toFixed(2);
    case "fractional": {
      const decimal = value - 1;
      if (decimal === 0) return "0/1";
      const gcd = (a: number, b: number): number => (b ? gcd(b, a % b) : a);
      const num = Math.round(decimal * 100);
      const den = 100;
      const divisor = gcd(num, den);
      return `${num / divisor}/${den / divisor}`;
    }
    case "american": {
      if (value === 1) return "EVEN";
      if (value >= 2) {
        return `+${Math.round((value - 1) * 100)}`;
      }
      return `${Math.round(-100 / (value - 1))}`;
    }
  }
};

const getChangePercentage = (current: number, previous: number): number => {
  if (!previous) return 0;
  return ((current - previous) / previous) * 100;
};

const getDetailedTooltip = (value: number, format: OddsFormat, previousValue?: number): string => {
  const formattedOdds = {
    decimal: value.toFixed(2),
    fractional: formatOdds(value, "fractional"),
    american: formatOdds(value, "american"),
  };

  let tooltip = `Decimal: ${formattedOdds.decimal}\nFractional: ${formattedOdds.fractional}\nAmerican: ${formattedOdds.american}`;

  if (previousValue) {
    const change = getChangePercentage(value, previousValue);
    tooltip += `\nChange: ${change > 0 ? "+" : ""}${change.toFixed(1)}%`;
  }

  return tooltip;
};

const OddsDisplay = React.forwardRef<HTMLSpanElement, OddsDisplayProps>(
  ({ value, format = "decimal", previousValue, className }, ref) => {
    const formattedOdds = formatOdds(value, format);
    const isPositive = format === "american" && formattedOdds.startsWith("+");
    const hasChanged = previousValue && previousValue !== value;
    const changeDirection = hasChanged ? (value > previousValue ? "up" : "down") : null;

    return (
      <span
        ref={ref}
        className={cn(
          "relative inline-flex items-center justify-center rounded px-2 py-1 text-sm font-medium group",
          hasChanged && "animate-flash",
          changeDirection === "up" && "text-emerald-800 dark:text-emerald-300 bg-emerald-100 dark:bg-emerald-950/50",
          changeDirection === "down" && "text-rose-800 dark:text-rose-300 bg-rose-100 dark:bg-rose-950/50",
          !changeDirection && (
            isPositive
              ? "text-emerald-800 dark:text-emerald-300 bg-emerald-100 dark:bg-emerald-950/50"
              : "text-rose-800 dark:text-rose-300 bg-rose-100 dark:bg-rose-950/50"
          ),
          className
        )}
        title={getDetailedTooltip(value, format, previousValue)}
      >
        {formattedOdds}
        {hasChanged && (
          <span className={cn(
            "absolute -right-1 -top-1 flex h-3 w-3",
            changeDirection === "up" && "text-emerald-500",
            changeDirection === "down" && "text-rose-500"
          )}>
            {changeDirection === "up" ? (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                className="h-3 w-3"
              >
                <path d="M12 19V5M5 12l7-7 7 7" />
              </svg>
            ) : (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                className="h-3 w-3"
              >
                <path d="M12 5v14M5 12l7 7 7-7" />
              </svg>
            )}
          </span>
        )}
      </span>
    );
  }
);

OddsDisplay.displayName = "OddsDisplay";

export { OddsDisplay };
```

## src/components/controls/ParlayBetDisplay.tsx
- Language: TSX
- Encoding: utf-8
- Size: 8489 bytes
- Tokens: 1882

```tsx
"use client";

import { cn } from "@/lib/utils";
import * as React from "react";
import { BettingCard } from "@/components/controls/BettingCard";
import type { BettingCardProps } from "@/lib/types/components/betting";
import { TextField } from "./TextField";
import { OddsDisplay } from "./OddsDisplay";
import { Button } from "./Button";
import { DragDropContext, Droppable, Draggable, DropResult } from "react-beautiful-dnd";

export interface ParlayBetDisplayProps {
  /** Array of betting cards in the parlay */
  bettingCards: BettingCardProps[];
  /** The format to display odds in */
  oddsFormat?: "decimal" | "fractional" | "american";
  /** Optional className for custom styling */
  className?: string;
  /** Callback when a game is removed from the parlay */
  onRemoveGame: (index: number) => void;
  /** Callback when the parlay bet is placed */
  onPlaceBet: (amount: number) => void;
  /** Callback when games are reordered */
  onReorder?: (startIndex: number, endIndex: number) => void;
  /** Suggested games to add to parlay */
  suggestedGames?: BettingCardProps[];
  /** Callback when a suggested game is added */
  onAddSuggestedGame?: (game: BettingCardProps) => void;
}

const calculateCumulativeOdds = (cards: BettingCardProps[]): number => {
  return cards.reduce((acc, card) => {
    const selectedOdds = card.selectedTeam?.isHome ? card.homeOdds : card.awayOdds;
    return acc * selectedOdds;
  }, 1);
};

interface PayoutInfo {
  cumulativeOdds: number;
  potentialPayout: number;
  impliedProbability: number;
  breakEvenPercentage: number;
  payoutRatio: string;
}

const calculatePayoutInfo = (cards: BettingCardProps[], betAmount: number): PayoutInfo => {
  const cumulativeOdds = calculateCumulativeOdds(cards);
  const potentialPayout = parseFloat(betAmount.toString()) * cumulativeOdds || 0;
  const impliedProbability = (1 / cumulativeOdds) * 100;
  const breakEvenPercentage = (1 / cumulativeOdds) * 100;
  const payoutRatio = `${(potentialPayout / betAmount).toFixed(2)}:1`;

  return {
    cumulativeOdds,
    potentialPayout,
    impliedProbability,
    breakEvenPercentage,
    payoutRatio,
  };
};

export function ParlayBetDisplay({
  bettingCards,
  oddsFormat = "decimal",
  className,
  onRemoveGame,
  onPlaceBet,
  onReorder,
  suggestedGames = [],
  onAddSuggestedGame,
}: ParlayBetDisplayProps) {
  const [betAmount, setBetAmount] = React.useState<string>("");
  const [error, setError] = React.useState<string>("");
  const amount = parseFloat(betAmount) || 0;
  const payoutInfo = calculatePayoutInfo(bettingCards, amount);

  const handleBetAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setBetAmount(value);
  };

  const handlePlaceBet = () => {
    const amount = parseFloat(betAmount);
    if (isNaN(amount) || amount <= 0) {
      setError("Please enter a valid bet amount");
      return;
    }
    if (bettingCards.length < 2) {
      setError("Select at least two games for a parlay bet");
      return;
    }
    setError("");
    onPlaceBet(amount);
  };

  const handleDragEnd = (result: DropResult) => {
    if (!result.destination || !onReorder) return;
    onReorder(result.source.index, result.destination.index);
  };

  return (
    <div
      className={cn(
        "w-full",
        className
      )}
    >
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-2xl font-semibold">Parlay Bet</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              {bettingCards.length} {bettingCards.length === 1 ? "game" : "games"} selected
            </p>
          </div>
        </div>

        {/* Selected Games */}
        <DragDropContext onDragEnd={handleDragEnd}>
          <Droppable droppableId="parlay-games">
            {(provided) => (
              <div
                ref={provided.innerRef}
                {...provided.droppableProps}
                className="grid gap-4 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-1"
              >
                {bettingCards.map((card, index) => (
                  <Draggable key={`${card.homeTeam.name}-${card.awayTeam.name}`} draggableId={`game-${index}`} index={index}>
                    {(provided) => (
                      <div
                        ref={provided.innerRef}
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                        className="relative w-full"
                      >
                        <BettingCard {...card} className="w-full" />
                        {onRemoveGame && (
                          <Button
                            variant="outline"
                            size="sm"
                            className="absolute top-4 right-4 bg-background hover:bg-accent"
                            onClick={() => onRemoveGame(index)}
                          >
                            Remove
                          </Button>
                        )}
                      </div>
                    )}
                  </Draggable>
                ))}
                {provided.placeholder}
              </div>
            )}
          </Droppable>
        </DragDropContext>

        {/* Suggested Games */}
        {suggestedGames.length > 0 && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h4 className="text-lg font-semibold">Suggested Games</h4>
              <p className="text-sm text-muted-foreground">Add these games to increase your potential winnings</p>
            </div>
            <div className="grid gap-4 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-1">
              {suggestedGames.map((game, index) => (
                <div key={index} className="relative w-full">
                  <BettingCard {...game} className="w-full opacity-75 hover:opacity-100 transition-opacity" />
                  <Button
                    variant="outline"
                    size="sm"
                    className="absolute top-4 right-4 bg-background hover:bg-accent"
                    onClick={() => onAddSuggestedGame?.(game)}
                  >
                    Add to Parlay
                  </Button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Bet Amount and Odds */}
        <div className="space-y-4">
          <TextField
            label="Bet Amount"
            type="number"
            min="0"
            step="0.01"
            value={betAmount}
            onChange={handleBetAmountChange}
            placeholder="Enter bet amount"
            className="w-full"
          />

          {/* Payout Information */}
          <div className="rounded-lg border border-border p-4 space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium">Cumulative Odds:</span>
              <OddsDisplay value={payoutInfo.cumulativeOdds} format={oddsFormat} />
            </div>

            <div className="flex justify-between items-center">
              <span className="text-sm font-medium">Potential Payout:</span>
              <span className="text-lg font-bold">
                ${payoutInfo.potentialPayout.toFixed(2)}
              </span>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-sm font-medium">Payout Ratio:</span>
              <span className="text-sm">{payoutInfo.payoutRatio}</span>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-sm font-medium">Implied Probability:</span>
              <span className="text-sm">{payoutInfo.impliedProbability.toFixed(1)}%</span>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-sm font-medium">Break Even %:</span>
              <span className="text-sm">{payoutInfo.breakEvenPercentage.toFixed(1)}%</span>
            </div>
          </div>

          {error && <p className="text-sm text-destructive">{error}</p>}

          <Button
            className="w-full"
            onClick={handlePlaceBet}
            disabled={bettingCards.length < 2 || !betAmount}
          >
            Place Parlay Bet
          </Button>
        </div>
      </div>
    </div>
  );
}
```

## src/components/controls/PromotionCard.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2565 bytes
- Tokens: 632

```tsx
"use client";

import { cn } from "@/lib/utils";
import * as React from "react";
import { Button } from "./Button";
import { Icon } from "./Icon";
import { HeroIcons } from "@/lib/types/models/icons";

export interface PromotionCardProps {
  /** The title of the promotion */
  title: string;
  /** The description of the promotion */
  description: string;
  /** The type of promotion */
  type: "bonus" | "parlay" | "free-bet";
  /** The value of the promotion (e.g., "$50" or "3x") */
  value: string;
  /** The expiration date of the promotion */
  expiresAt?: string;
  /** Optional terms and conditions */
  terms?: string;
  /** Optional className for custom styling */
  className?: string;
  /** Callback when the promotion is claimed */
  onClaim?: () => void;
}

export function PromotionCard({
  title,
  description,
  type,
  value,
  expiresAt,
  terms,
  className,
  onClaim,
}: PromotionCardProps) {
  return (
    <div
      className={cn(
        "group relative overflow-hidden rounded-lg border bg-card p-6 text-card-foreground shadow-sm transition-colors hover:bg-accent/5",
        className
      )}
    >
      {/* Promotion Type Badge */}
      <div className="absolute right-4 top-4">
        <div className="rounded-full bg-primary/10 px-3 py-1 text-xs font-medium text-primary">
          {type === "bonus" ? "Deposit Bonus" : type === "parlay" ? "Parlay Boost" : "Free Bet"}
        </div>
      </div>

      {/* Icon and Value */}
      <div className="mb-4 flex items-center gap-4">
        <div className="rounded-full bg-primary/10 p-3">
          <Icon 
            name={type === "parlay" ? HeroIcons.Commerce.Tag : HeroIcons.Commerce.CurrencyDollar} 
            className="h-6 w-6 text-primary" 
          />
        </div>
        <div className="text-3xl font-bold tracking-tight">{value}</div>
      </div>

      {/* Content */}
      <div className="space-y-2">
        <h3 className="text-xl font-semibold">{title}</h3>
        <p className="text-sm text-muted-foreground">{description}</p>
      </div>

      {/* Footer */}
      <div className="mt-6 space-y-4">
        {expiresAt && (
          <p className="text-sm text-muted-foreground">
            Expires: {new Date(expiresAt).toLocaleDateString()}
          </p>
        )}
        {terms && (
          <p className="text-xs text-muted-foreground">
            Terms: {terms}
          </p>
        )}
        <Button
          className="w-full"
          onClick={onClaim}
        >
          Claim Offer
        </Button>
      </div>
    </div>
  );
}
```

## src/components/controls/Promotions.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2655 bytes
- Tokens: 619

```tsx
"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import { PromotionCard, type PromotionCardProps } from "./PromotionCard";
import { Button } from "./Button";

export interface PromotionsProps {
  /** Array of promotions to display */
  promotions: (Omit<PromotionCardProps, "onClaim"> & { id: string })[];
  /** Optional className for custom styling */
  className?: string;
  /** Callback when a promotion is claimed */
  onClaimPromotion?: (id: string) => void;
}

export function Promotions({ promotions, className, onClaimPromotion }: PromotionsProps) {
  const [selectedType, setSelectedType] = React.useState<"all" | PromotionCardProps["type"]>("all");

  const filteredPromotions = React.useMemo(() => {
    if (selectedType === "all") return promotions;
    return promotions.filter((promo) => promo.type === selectedType);
  }, [promotions, selectedType]);

  return (
    <div className={cn("space-y-6", className)}>
      {/* Filter Buttons */}
      <div className="flex flex-wrap gap-2">
        <Button
          variant={selectedType === "all" ? "primary" : "outline"}
          onClick={() => setSelectedType("all")}
          size="sm"
        >
          All Promotions
        </Button>
        <Button
          variant={selectedType === "bonus" ? "primary" : "outline"}
          onClick={() => setSelectedType("bonus")}
          size="sm"
        >
          Deposit Bonuses
        </Button>
        <Button
          variant={selectedType === "parlay" ? "primary" : "outline"}
          onClick={() => setSelectedType("parlay")}
          size="sm"
        >
          Parlay Boosts
        </Button>
        <Button
          variant={selectedType === "free-bet" ? "primary" : "outline"}
          onClick={() => setSelectedType("free-bet")}
          size="sm"
        >
          Free Bets
        </Button>
      </div>

      {/* Promotions Grid */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {filteredPromotions.map((promotion) => (
          <PromotionCard
            key={promotion.id}
            {...promotion}
            onClaim={() => onClaimPromotion?.(promotion.id)}
          />
        ))}
      </div>

      {/* Empty State */}
      {filteredPromotions.length === 0 && (
        <div className="flex flex-col items-center justify-center rounded-lg border border-dashed p-8 text-center">
          <h3 className="mt-2 text-lg font-semibold">No promotions available</h3>
          <p className="mt-1 text-sm text-muted-foreground">
            Check back later for new promotions and offers
          </p>
        </div>
      )}
    </div>
  );
}
```

## src/components/controls/Select.tsx
- Language: TSX
- Encoding: utf-8
- Size: 5027 bytes
- Tokens: 1346

```tsx
"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import { cva, type VariantProps } from "class-variance-authority";

const selectVariants = cva(
  "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "",
        error: "border-destructive focus-visible:ring-destructive",
        success: "border-emerald-500 focus-visible:ring-emerald-500",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface SelectGroup {
  label: string;
  options: SelectOption[];
}

export interface SelectProps
  extends Omit<React.SelectHTMLAttributes<HTMLSelectElement>, "children">,
    VariantProps<typeof selectVariants> {
  /** Array of options or option groups */
  options: (SelectOption | SelectGroup)[];
  /** Error message to display */
  error?: string;
  /** Success message to display */
  success?: string;
  /** Whether to show a clear option */
  clearable?: boolean;
  /** Text to show for clear option */
  clearText?: string;
  /** Placeholder text */
  placeholder?: string;
  /** Maximum number of selections allowed (only applies when multiple is true) */
  maxSelections?: number;
}

const isGroup = (option: SelectOption | SelectGroup): option is SelectGroup => {
  return 'options' in option;
};

const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ 
    className,
    variant,
    error,
    success,
    clearable,
    clearText = "Clear selection",
    placeholder = "Select an option",
    options,
    value,
    onChange,
    multiple,
    maxSelections,
    ...props
  }, ref) => {
    // Determine variant based on error/success state
    const selectVariant = error ? "error" : success ? "success" : variant;

    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
      if (onChange) {
        // If value is empty and clearable is true, reset to empty string
        if (clearable && e.target.value === "") {
          e.target.value = "";
        }
        
        // Handle maxSelections for multiple select
        if (multiple && maxSelections) {
          const selectedOptions = Array.from(e.target.selectedOptions).map(opt => opt.value);
          if (selectedOptions.length > maxSelections) {
            // Prevent selection if it exceeds maxSelections
            e.preventDefault();
            return;
          }
        }
        
        onChange(e);
      }
    };

    return (
      <select
        ref={ref}
        value={value}
        onChange={handleChange}
        multiple={multiple}
        className={cn(
          selectVariants({ variant: selectVariant }),
          "appearance-none bg-no-repeat bg-[right_0.5rem_center] bg-[length:1rem_1rem]",
          "[background-image:url(data:image/svg+xml;charset=utf-8;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNNC4yNyA1LjMzTDggOS4wNmwzLjczLTMuNzMuOTQuOTRMOCAxMC45NGwtNC42Ny00LjY3LjkzLS45NHoiIGZpbGw9ImN1cnJlbnRDb2xvciIvPjwvc3ZnPg==)]",
          "dark:[background-image:url(data:image/svg+xml;charset=utf-8;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNNC4yNyA1LjMzTDggOS4wNmwzLjczLTMuNzMuOTQuOTRMOCAxMC45NGwtNC42Ny00LjY3LjkzLS45NHoiIGZpbGw9ImN1cnJlbnRDb2xvciIvPjwvc3ZnPg==)]",
          className
        )}
        {...props}
      >
        {/* Placeholder option */}
        <option value="" disabled hidden>
          {placeholder}
        </option>

        {/* Clear option */}
        {clearable && (
          <option value="">{clearText}</option>
        )}

        {/* Render options or option groups */}
        {options.map((option, index) => {
          if (isGroup(option)) {
            return (
              <optgroup key={index} label={option.label}>
                {option.options.map((groupOption, groupIndex) => (
                  <option
                    key={`${index}-${groupIndex}`}
                    value={groupOption.value}
                    disabled={groupOption.disabled}
                  >
                    {groupOption.label}
                  </option>
                ))}
              </optgroup>
            );
          }

          return (
            <option
              key={index}
              value={option.value}
              disabled={option.disabled}
            >
              {option.label}
            </option>
          );
        })}
      </select>
    );
  }
);

Select.displayName = "Select";

export { Select, selectVariants };
```

## src/components/controls/Settings.tsx
- Language: TSX
- Encoding: utf-8
- Size: 4973 bytes
- Tokens: 959

```tsx
"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import { Button } from "./Button";
import { Icon } from "./Icon";
import { ThemeToggle } from "./ThemeToggle";
import Link from "next/link";
import { HeroIcons } from "@/lib/types/models/icons";

interface SettingsProps {
  /** Optional className for custom styling */
  className?: string;
}

export function Settings({ className }: SettingsProps) {
  const [isOpen, setIsOpen] = React.useState(false);

  return (
    <div className="relative">
      {/* Settings Button */}
      <Button
        variant="ghost"
        size="icon"
        className={cn(className)}
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        <Icon 
          name={HeroIcons.UI.Cog6Tooth}
          className="h-5 w-5"
          aria-hidden="true"
        />
        <span className="sr-only">Open settings</span>
      </Button>

      {/* Settings Popover */}
      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-40 bg-black/40 backdrop-blur-sm"
            onClick={() => setIsOpen(false)}
            data-testid="backdrop"
          />

          {/* Menu */}
          <div className="absolute right-0 z-50 mt-2 w-64 origin-top-right rounded-xl border border-border/10 bg-[#0A0A0A] shadow-2xl">
            <div className="space-y-6 p-6">
              {/* Theme Toggle */}
              <div className="flex items-center justify-between">
                <span className="text-base font-medium text-white/90">Theme</span>
                <ThemeToggle />
              </div>

              <div className="h-px bg-white/[0.08]" />

              {/* Navigation */}
              <nav className="space-y-3">
                <Link href="/betting" passHref>
                  <Button
                    variant="ghost"
                    className="w-full justify-start text-white/80 hover:text-white"
                    onClick={() => setIsOpen(false)}
                  >
                    <Icon 
                      name={HeroIcons.Commerce.CurrencyDollar}
                      className="mr-3 h-5 w-5"
                    />
                    Betting
                  </Button>
                </Link>
                <Link href="/parlay" passHref>
                  <Button
                    variant="ghost"
                    className="w-full justify-start text-white/80 hover:text-white"
                    onClick={() => setIsOpen(false)}
                  >
                    <Icon 
                      name={HeroIcons.Commerce.Tag}
                      className="mr-3 h-5 w-5"
                    />
                    Parlay Bets
                  </Button>
                </Link>
                <Link href="/promotions" passHref>
                  <Button
                    variant="ghost"
                    className="w-full justify-start text-white/80 hover:text-white"
                    onClick={() => setIsOpen(false)}
                  >
                    <Icon 
                      name={HeroIcons.Commerce.Gift}
                      className="mr-3 h-5 w-5"
                    />
                    Promotions
                  </Button>
                </Link>
                <Link href="/leaderboard" passHref>
                  <Button
                    variant="ghost"
                    className="w-full justify-start text-white/80 hover:text-white"
                    onClick={() => setIsOpen(false)}
                  >
                    <Icon 
                      name={HeroIcons.Misc.Trophy}
                      className="mr-3 h-5 w-5"
                    />
                    Leaderboard
                  </Button>
                </Link>
              </nav>

              <div className="h-px bg-white/[0.08]" />

              {/* Authentication */}
              <div className="space-y-3">
                <Button
                  variant="ghost"
                  className="w-full justify-start text-white/80 hover:text-white"
                  onClick={() => {
                    setIsOpen(false);
                  }}
                >
                  <Icon 
                    name={HeroIcons.Actions.ArrowRightOnRectangle}
                    className="mr-3 h-5 w-5"
                  />
                  Sign In
                </Button>
                <Button
                  variant="ghost"
                  className="w-full justify-start text-white/80 hover:text-white"
                  onClick={() => {
                    setIsOpen(false);
                  }}
                >
                  <Icon 
                    name={HeroIcons.User.UserPlus}
                    className="mr-3 h-5 w-5"
                  />
                  Sign Up
                </Button>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
```

## src/components/controls/StatsCard.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2466 bytes
- Tokens: 603

```tsx
"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import { Icon } from "./Icon";
import { HeroIcons } from "@/lib/types/models/icons";

export interface StatsCardProps {
  /** The title of the stat */
  title: string;
  /** The value to display */
  value: string | number;
  /** Optional trend percentage */
  trend?: number;
  /** The type of stat */
  type?: "money" | "percentage" | "count";
  /** Optional className for custom styling */
  className?: string;
  /** Optional click handler */
  onClick?: () => void;
}

export function StatsCard({
  title,
  value,
  trend,
  type = "count",
  className,
  onClick,
}: StatsCardProps) {
  const iconName = React.useMemo(() => {
    switch (type) {
      case "money":
        return HeroIcons.Commerce.CurrencyDollar;
      case "percentage":
        return HeroIcons.Data.ChartPie;
      default:
        return HeroIcons.UI.Check;
    }
  }, [type]);

  const formattedValue = React.useMemo(() => {
    if (type === "money") {
      return `$${typeof value === "number" ? value.toFixed(2) : value}`;
    }
    if (type === "percentage") {
      return `${value}%`;
    }
    return value;
  }, [value, type]);

  return (
    <div
      className={cn(
        "rounded-lg border border-border bg-card p-4 text-card-foreground shadow-sm dark:border-border/20",
        onClick && "transition-colors hover:border-primary cursor-pointer",
        className
      )}
      onClick={onClick}
      role={onClick ? "button" : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={(e) => {
        if (onClick && (e.key === "Enter" || e.key === " ")) {
          e.preventDefault();
          onClick();
        }
      }}
    >
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-muted-foreground">{title}</p>
        <Icon name={iconName} className="h-4 w-4 text-muted-foreground" />
      </div>
      <div className="mt-2 flex items-baseline">
        <p className="text-2xl font-semibold tabular-nums">{formattedValue}</p>
        {trend !== undefined && (
          <span
            className={cn(
              "ml-2 text-sm",
              trend > 0 
                ? "text-emerald-500 dark:text-emerald-400" 
                : "text-rose-500 dark:text-rose-400"
            )}
          >
            {trend > 0 ? "+" : ""}
            {trend}%
          </span>
        )}
      </div>
    </div>
  );
}
```

## src/components/controls/TextField.tsx
- Language: TSX
- Encoding: utf-8
- Size: 3541 bytes
- Tokens: 786

```tsx
"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import { cva, type VariantProps } from "class-variance-authority";

const textFieldVariants = cva(
  "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:border-input/20 dark:focus-visible:ring-offset-0",
  {
    variants: {
      variant: {
        default: "",
        error: "border-destructive focus-visible:ring-destructive",
        success: "border-emerald-500 focus-visible:ring-emerald-500",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

export interface TextFieldProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  /** Label text for the input */
  label?: string;
  /** Error message to display */
  error?: string;
  /** Success message to display */
  success?: string;
  /** Optional icon to display at the start of the input */
  startIcon?: React.ReactNode;
  /** Optional icon to display at the end of the input */
  endIcon?: React.ReactNode;
  /** Whether to show the clear button */
  clearable?: boolean;
  /** Maximum character count */
  maxLength?: number;
  /** Whether to show character count */
  showCount?: boolean;
  /** Input mask pattern (e.g., currency, number) */
  mask?: 'currency' | 'number' | 'decimal';
  /** Optional className for custom styling */
  className?: string;
  /** Optional className for the wrapper div */
  wrapperClassName?: string;
  /** Variant of the input */
  variant?: VariantProps<typeof textFieldVariants>['variant'];
  /** Default value for the input */
  defaultValue?: string;
  /** Callback when value changes */
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

const TextField = React.forwardRef<HTMLInputElement, TextFieldProps>(
  ({ className, label, error, defaultValue, onChange, ...props }, ref) => {
    const [value, setValue] = React.useState(defaultValue || "");

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const newValue = e.target.value;
      setValue(newValue);
      onChange?.(e);
    };

    return (
      <div className="relative">
        {label && (
          <label
            className={cn(
              "absolute -top-2 left-2 -mt-px px-1 text-xs font-medium text-muted-foreground",
              error && "text-destructive"
            )}
          >
            {label}
          </label>
        )}
        <input
          ref={ref}
          type="text"
          className={cn(
            "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
            error && "border-destructive focus-visible:ring-destructive",
            className
          )}
          value={value}
          onChange={handleChange}
          {...props}
        />
        {error && (
          <p className="mt-1 text-xs text-destructive">{error}</p>
        )}
      </div>
    );
  }
);

TextField.displayName = "TextField";

export { TextField, textFieldVariants };
```

## src/components/controls/ThemeToggle.tsx
- Language: TSX
- Encoding: utf-8
- Size: 1787 bytes
- Tokens: 435

```tsx
"use client";

import * as React from "react";
import { useTheme } from "next-themes";
import { Button } from "./Button";
import { Icon } from "./Icon";
import { HeroIcons } from "@/lib/types/models/icons";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

interface ThemeToggleProps {
  /** Optional className for custom styling */
  className?: string;
}

export function ThemeToggle({ className }: ThemeToggleProps) {
  const { setTheme } = useTheme();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="sm" className={className}>
          <Icon
            name={HeroIcons.DateTime.Sun}
            className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
          />
          <Icon
            name={HeroIcons.DateTime.Moon}
            className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
          />
          <span className="sr-only">Toggle theme</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => setTheme("light")}>
          <Icon name={HeroIcons.DateTime.Sun} className="mr-2 h-4 w-4" />
          <span>Light</span>
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme("dark")}>
          <Icon name={HeroIcons.DateTime.Moon} className="mr-2 h-4 w-4" />
          <span>Dark</span>
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => setTheme("system")}>
          <Icon name={HeroIcons.UI.Computer} className="mr-2 h-4 w-4" />
          <span>System</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
```

## src/components/controls/Toggle.tsx
- Language: TSX
- Encoding: utf-8
- Size: 1136 bytes
- Tokens: 267

```tsx
"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import * as SwitchPrimitives from "@radix-ui/react-switch";

const Toggle = React.forwardRef<
  React.ElementRef<typeof SwitchPrimitives.Root>,
  React.ComponentPropsWithoutRef<typeof SwitchPrimitives.Root>
>(({ className, ...props }, ref) => (
  <SwitchPrimitives.Root
    className={cn(
      "peer inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=unchecked]:bg-input",
      className
    )}
    {...props}
    ref={ref}
  >
    <SwitchPrimitives.Thumb
      className={cn(
        "pointer-events-none block h-5 w-5 rounded-full bg-background shadow-lg ring-0 transition-transform data-[state=checked]:translate-x-5 data-[state=unchecked]:translate-x-0"
      )}
    />
  </SwitchPrimitives.Root>
));

Toggle.displayName = "Toggle";

export { Toggle };
```

## src/components/controls/UserDashboard.tsx
- Language: TSX
- Encoding: utf-8
- Size: 6008 bytes
- Tokens: 1445

```tsx
"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import { Card } from '@/components/ui/card';
import type { Analysis } from '@/lib/types';
import type { AccountInfo } from '@/lib/types/models/user';
import type { MultiMarketAnalysis } from '@/lib/types/models/analysis';
import { formatCurrency } from '@/lib/utils';

interface UserDashboardProps {
  /** User's account information */
  accountInfo: AccountInfo;
  /** Recent analyses */
  recentAnalyses: Analysis[];
  /** Multi-market analyses */
  multiMarketAnalyses: MultiMarketAnalysis[];
  /** Optional className for custom styling */
  className?: string;
}

// Atomic Components

// Atom: Stat Display
interface StatDisplayProps {
  label: string;
  value: string | number;
  subValue?: string;
  className?: string;
}

function StatDisplay({ label, value, subValue, className }: StatDisplayProps) {
  return (
    <Card className={cn("p-4", className)}>
      <h3 className="text-lg font-medium text-muted-foreground font-display">{label}</h3>
      <p className="mt-2 text-2xl font-bold font-display tabular-nums">{value}</p>
      {subValue && (
        <p className="text-sm text-muted-foreground font-sans">{subValue}</p>
      )}
    </Card>
  );
}

// Atom: Status Badge
interface StatusBadgeProps {
  status: 'active' | 'completed' | 'archived';
  className?: string;
}

function StatusBadge({ status, className }: StatusBadgeProps) {
  return (
    <span className={cn(
      'px-2 py-1 rounded-full text-xs font-medium',
      status === 'active' ? 'bg-blue-100 text-blue-800' :
      status === 'completed' ? 'bg-green-100 text-green-800' :
      'bg-gray-100 text-gray-800',
      className
    )}>
      {status}
    </span>
  );
}

// Molecule: Analysis Card
interface AnalysisCardProps {
  analysis: Analysis;
  currency: string;
  className?: string;
}

function AnalysisCard({ analysis, currency, className }: AnalysisCardProps) {
  return (
    <Card className={cn("p-4", className)}>
      <div className="flex justify-between items-start mb-2">
        <h4 className="font-medium font-display">
          {analysis.market.homeTeam} vs {analysis.market.awayTeam}
        </h4>
        <StatusBadge status={analysis.status} />
      </div>
      <div className="space-y-1 text-sm font-sans">
        <p>Correlation: {(analysis.correlationStrength * 100).toFixed(1)}%</p>
        <p>Confidence: {(analysis.confidence * 100).toFixed(1)}%</p>
        <p>Potential Value: {formatCurrency(analysis.potentialValue, currency)}</p>
        <p>Prediction: {analysis.predictedOutcome}</p>
      </div>
    </Card>
  );
}

// Molecule: Multi-Market Analysis Card
interface MultiMarketCardProps {
  analysis: MultiMarketAnalysis;
  currency: string;
  className?: string;
}

function MultiMarketCard({ analysis, currency, className }: MultiMarketCardProps) {
  return (
    <Card className={cn("p-4", className)}>
      <div className="flex justify-between items-start mb-2">
        <h4 className="font-medium font-display">Multi-Market Analysis #{analysis.id}</h4>
        <StatusBadge status={analysis.status} />
      </div>
      <div className="space-y-1 text-sm font-sans">
        <p>Markets: {analysis.analyses.length}</p>
        <p>Correlation: {(analysis.correlationStrength * 100).toFixed(1)}%</p>
        <p>Confidence: {(analysis.confidence * 100).toFixed(1)}%</p>
        <p>Potential Value: {formatCurrency(analysis.potentialValue, currency)}</p>
      </div>
    </Card>
  );
}

// Organism: Stats Overview
interface StatsOverviewProps {
  accountInfo: AccountInfo;
  className?: string;
}

function StatsOverview({ accountInfo, className }: StatsOverviewProps) {
  return (
    <div className={cn("grid gap-4 md:grid-cols-2 lg:grid-cols-4", className)}>
      <StatDisplay
        label="Account Balance"
        value={formatCurrency(accountInfo.balance, accountInfo.currency)}
        subValue={`Available Capital: ${formatCurrency(accountInfo.availableCapital, accountInfo.currency)}`}
      />
      <StatDisplay
        label="Analysis Stats"
        value={accountInfo.totalAnalyses}
        subValue={`Success Rate: ${accountInfo.accuracyRate.toFixed(1)}%`}
      />
      <StatDisplay
        label="Active Analyses"
        value={accountInfo.activeAnalyses}
        subValue={`Pending Returns: ${formatCurrency(accountInfo.pendingReturns, accountInfo.currency)}`}
      />
      <StatDisplay
        label="Performance"
        value={formatCurrency(accountInfo.totalReturns, accountInfo.currency)}
        subValue={`Total Invested: ${formatCurrency(accountInfo.totalInvested, accountInfo.currency)}`}
      />
    </div>
  );
}

// Main Component
export function UserDashboard({
  accountInfo,
  recentAnalyses,
  multiMarketAnalyses,
  className,
}: UserDashboardProps) {
  return (
    <div className={cn("space-y-8", className)}>
      {/* Stats Overview */}
      <StatsOverview accountInfo={accountInfo} />

      {/* Recent Analyses */}
      {recentAnalyses.length > 0 && (
        <section>
          <h2 className="text-2xl font-bold font-display mb-4">Recent Analyses</h2>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {recentAnalyses.map((analysis) => (
              <AnalysisCard
                key={analysis.id}
                analysis={analysis}
                currency={accountInfo.currency}
              />
            ))}
          </div>
        </section>
      )}

      {/* Multi-Market Analyses */}
      {multiMarketAnalyses.length > 0 && (
        <section>
          <h2 className="text-2xl font-bold font-display mb-4">Multi-Market Analyses</h2>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {multiMarketAnalyses.map((analysis) => (
              <MultiMarketCard
                key={analysis.id}
                analysis={analysis}
                currency={accountInfo.currency}
              />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
```

## src/components/layout/MainLayout.tsx
- Language: TSX
- Encoding: utf-8
- Size: 729 bytes
- Tokens: 162

```tsx
'use client';

import * as React from 'react';
import { Header } from '@/components/navigation/Header';
import { Footer } from '@/components/navigation/Footer';
import { ErrorBoundary } from '@/components/organisms/ErrorBoundary';

interface MainLayoutProps {
  children: React.ReactNode;
}

export default function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-[#0A0A0A]">
      <ErrorBoundary>
        <Header />
        <main className="flex-grow container mx-auto px-4 py-8">
          <ErrorBoundary>
            {children}
          </ErrorBoundary>
        </main>
        <ErrorBoundary>
          <Footer />
        </ErrorBoundary>
      </ErrorBoundary>
    </div>
  );
}
```

## src/components/molecules/ErrorState.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2025 bytes
- Tokens: 465

```tsx
import * as React from 'react';
import { Icon } from '@/components/controls/Icon';
import { Button } from '@/components/controls/Button';
import { HeroIcons } from '@/lib/types/models/icons';
import { cn } from '@/lib/utils';

interface ErrorStateProps {
  title?: string;
  message: string;
  className?: string;
  icon?: React.ReactNode;
  actions?: {
    primary?: {
      label: string;
      onClick: () => void;
    };
    secondary?: {
      label: string;
      onClick: () => void;
    };
  };
}

export function ErrorState({
  title = 'Something went wrong',
  message,
  className,
  icon,
  actions,
}: ErrorStateProps) {
  return (
    <div
      className={cn(
        'rounded-lg border border-red-200 bg-red-50 p-6 text-center',
        className
      )}
      role="alert"
    >
      <div className="flex flex-col items-center space-y-4">
        <div className="rounded-full bg-red-100 p-3">
          {icon || (
            <Icon
              name={HeroIcons.Status.XMark}
              className="h-6 w-6 text-red-600"
            />
          )}
        </div>
        <div className="space-y-2">
          <h3 className="text-base font-semibold text-red-900">{title}</h3>
          <p className="text-sm text-red-800">{message}</p>
        </div>
        {actions && (
          <div className="flex flex-col space-y-2 sm:flex-row sm:space-x-3 sm:space-y-0">
            {actions.primary && (
              <Button
                onClick={actions.primary.onClick}
                className="bg-red-600 text-white hover:bg-red-700"
              >
                {actions.primary.label}
              </Button>
            )}
            {actions.secondary && (
              <Button
                variant="outline"
                onClick={actions.secondary.onClick}
                className="border-red-300 text-red-700 hover:bg-red-50"
              >
                {actions.secondary.label}
              </Button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
```

## src/components/navigation/Footer.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2713 bytes
- Tokens: 587

```tsx
'use client';

import * as React from "react";
import Link from "next/link";

export function Footer() {
  return (
    <footer className="border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4 py-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Company Info */}
          <div>
            <h3 className="text-white font-semibold text-lg mb-4">
              <span className="text-primary">Odds</span>Flipper
            </h3>
            <p className="text-sm text-muted-foreground">
              Your trusted platform for advanced odds analysis and insights.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-semibold text-lg mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/about" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                  Contact
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="/terms" className="text-sm text-muted-foreground hover:text-primary transition-colors">
                  Terms of Service
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-white font-semibold text-lg mb-4">Contact Us</h3>
            <ul className="space-y-2">
              <li className="text-sm">
                <a href="mailto:support@oddsfliper.com" className="text-muted-foreground hover:text-primary transition-colors">
                  support@oddsfliper.com
                </a>
              </li>
              <li className="text-sm">
                <a href="tel:+1234567890" className="text-muted-foreground hover:text-primary transition-colors">
                  +1 (234) 567-890
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Copyright */}
        <div className="border-t border-border mt-6 pt-6 text-center text-sm text-muted-foreground">
          <p>&copy; {new Date().getFullYear()} Tactical Tech. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
```

## src/components/navigation/Header.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2976 bytes
- Tokens: 703

```tsx
'use client';

import * as React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Icon } from "../controls/Icon";
import { HeroIcons } from "@/lib/types/models/icons";
import { cn } from "@/lib/utils";

export function Header() {
  const pathname = usePathname();

  const navItems = [
    { href: "/betting", label: "Betting" },
    { href: "/parlay", label: "Parlay Bets" },
    { href: "/promotions", label: "Promotions" },
    { href: "/leaderboard", label: "Leaderboard" },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b border-white/10 bg-[#1A1A1A]/95 backdrop-blur supports-[backdrop-filter]:bg-[#1A1A1A]/60">
      <div className="flex h-16 items-center px-4 md:px-6">
        {/* Left Section */}
        <div className="flex flex-1 items-center">
          <Link href="/" className="flex items-center space-x-2">
            <Icon name={HeroIcons.Commerce.CurrencyDollar} className="h-6 w-6 text-blue-500" />
            <span className="hidden font-display text-xl font-bold text-white sm:inline-block">
              Odds Flipper
            </span>
          </Link>
        </div>

        {/* Center Section */}
        <nav className="flex-1 flex items-center justify-center">
          <div className="flex items-center space-x-1">
            {navItems.map(({ href, label }) => (
              <Link
                key={href}
                href={href}
                className={cn(
                  "relative px-4 py-2 text-sm font-medium transition-all hover:text-white group",
                  pathname.startsWith(href) ? "text-blue-500" : "text-white/60"
                )}
              >
                {label}
                <span
                  className={cn(
                    "absolute bottom-0 left-0 h-0.5 w-full transform transition-all duration-200",
                    pathname.startsWith(href)
                      ? "bg-blue-500 opacity-100 shadow-[0_0_8px_0_rgba(59,130,246,0.8)] shadow-blue-500/50"
                      : "bg-transparent opacity-0 group-hover:bg-white/20 group-hover:opacity-100"
                  )}
                />
              </Link>
            ))}
          </div>
        </nav>

        {/* Right Section */}
        <div className="flex flex-1 items-center justify-end space-x-4">
          <Link 
            href="/sign-in" 
            className="text-sm font-medium text-white/60 transition-colors hover:text-white"
          >
            Sign In
          </Link>
          <Link 
            href="/sign-up" 
            className="inline-flex h-9 items-center justify-center rounded-md bg-blue-500 px-4 py-2 text-sm font-medium text-white shadow transition-colors hover:bg-blue-600 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-500 disabled:pointer-events-none disabled:opacity-50"
          >
            Sign Up
          </Link>
        </div>
      </div>
    </header>
  );
}
```

## src/components/organisms/ErrorBoundary.tsx
- Language: TSX
- Encoding: utf-8
- Size: 1988 bytes
- Tokens: 433

```tsx
import * as React from 'react';
import { ErrorState } from '@/components/molecules/ErrorState';

interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
    };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return {
      hasError: true,
      error,
    };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }
    
    // Log the error to an error reporting service
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render(): React.ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <ErrorState
          title="Application Error"
          message={this.state.error?.message || 'An unexpected error occurred.'}
          actions={{
            primary: {
              label: 'Reload Page',
              onClick: () => window.location.reload(),
            },
            secondary: {
              label: 'Go Back',
              onClick: () => window.history.back(),
            },
          }}
        />
      );
    }

    return this.props.children;
  }
}

// HOC for functional components
export function withErrorBoundary<P extends object>(
  Component: React.ComponentType<P>,
  errorBoundaryProps?: Omit<ErrorBoundaryProps, 'children'>
): React.FC<P> {
  return function WithErrorBoundary(props: P) {
    return (
      <ErrorBoundary {...errorBoundaryProps}>
        <Component {...props} />
      </ErrorBoundary>
    );
  };
}
```

## src/components/providers/ThemeProvider.tsx
- Language: TSX
- Encoding: utf-8
- Size: 539 bytes
- Tokens: 126

```tsx
"use client";

import * as React from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import type { ThemeProviderProps } from "next-themes";

export function ThemeProvider({ children, ...props }: ThemeProviderProps) {
  return (
    <NextThemesProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
      storageKey="odds-flipper-theme"
      themes={["light", "dark", "system"]}
      {...props}
    >
      {children}
    </NextThemesProvider>
  );
}
```

## src/components/templates/AnalysisTemplate.tsx
- Language: TSX
- Encoding: utf-8
- Size: 946 bytes
- Tokens: 209

```tsx
import * as React from 'react';
import MainLayout from '@/components/layout/MainLayout';
import { ErrorBoundary } from '@/components/organisms/ErrorBoundary';

interface AnalysisTemplateProps {
  children: React.ReactNode;
  title: string;
  description?: string;
}

export function AnalysisTemplate({ children, title, description }: AnalysisTemplateProps) {
  return (
    <ErrorBoundary>
      <MainLayout>
        <div className="max-w-7xl mx-auto">
          <div className="mb-8">
            <h1 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl font-display">
              {title}
            </h1>
            {description && (
              <p className="mt-2 text-lg text-gray-600 font-sans">
                {description}
              </p>
            )}
          </div>
          <ErrorBoundary>
            {children}
          </ErrorBoundary>
        </div>
      </MainLayout>
    </ErrorBoundary>
  );
}
```

## src/components/templates/BettingTemplate.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2016 bytes
- Tokens: 444

```tsx
"use client";

import * as React from "react";
import Link from "next/link";
import { Icon } from "../controls/Icon";
import { Settings } from "../controls/Settings";
import { HeroIcons } from "@/lib/types/models/icons";
import { cn } from "@/lib/utils";

interface BettingTemplateProps {
  children: React.ReactNode;
  className?: string;
}

export function BettingTemplate({ children, className }: BettingTemplateProps) {
  return (
    <div className={cn("min-h-screen bg-background", className)}>
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="flex h-16 items-center px-4 md:px-6">
          {/* Left Section */}
          <div className="flex flex-1 items-center">
            <Link href="/" className="flex items-center space-x-2">
              <Icon name={HeroIcons.Commerce.CurrencyDollar} className="h-6 w-6 text-primary" />
              <span className="font-display text-xl font-bold tracking-tight">Odds Flipper</span>
            </Link>
          </div>

          {/* Right Section */}
          <div className="flex flex-1 items-center justify-end space-x-4">
            <Link 
              href="/sign-in" 
              className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
            >
              Sign In
            </Link>
            <Link 
              href="/sign-up" 
              className="inline-flex h-9 items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary disabled:pointer-events-none disabled:opacity-50"
            >
              Sign Up
            </Link>
            <Settings />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">{children}</main>
    </div>
  );
}
```

## src/components/templates/OddsList.tsx
- Language: TSX
- Encoding: utf-8
- Size: 5400 bytes
- Tokens: 1270

```tsx
"use client";

import { cn } from "@/lib/utils";
import * as React from "react";
import { Button } from "../controls/Button";
import { Input } from "../controls/Input";
import { BettingCard } from "../controls/BettingCard";
import type { BettingCardProps } from "@/lib/types/components/betting";

export interface Game {
  id: string;
  homeTeam: {
    name: string;
    score?: number;
    isHome: true;
  };
  awayTeam: {
    name: string;
    score?: number;
    isHome: false;
  };
  homeOdds: number;
  awayOdds: number;
  previousHomeOdds?: number;
  previousAwayOdds?: number;
  startTime: string;
  sport: "NFL" | "NBA" | "MLB" | "NHL";
  status: {
    type: "upcoming" | "live" | "halftime" | "final" | "postponed" | "cancelled";
    startTime?: string;
    timeRemaining?: string;
    period?: string;
    possession?: "home" | "away";
    detail?: string;
  };
}

export interface OddsListProps {
  /** List of games with odds */
  games: Game[];
  /** Optional className for custom styling */
  className?: string;
  /** Callback when a game is selected */
  onSelectGame?: (game: Game, team: "home" | "away") => void;
  /** Currently selected games */
  selectedGames?: BettingCardProps[];
}

export function OddsList({ games, className, onSelectGame, selectedGames = [] }: OddsListProps) {
  const [selectedSport, setSelectedSport] = React.useState<string>("all");
  const [searchQuery, setSearchQuery] = React.useState("");
  const [previousOdds, setPreviousOdds] = React.useState<Record<string, { home: number; away: number }>>({});

  // Track odds changes
  React.useEffect(() => {
    games.forEach(game => {
      setPreviousOdds(prev => {
        if (!prev[game.id]) {
          return {
            ...prev,
            [game.id]: {
              home: game.homeOdds,
              away: game.awayOdds
            }
          };
        } else if (
          game.homeOdds !== prev[game.id].home ||
          game.awayOdds !== prev[game.id].away
        ) {
          return {
            ...prev,
            [game.id]: prev[game.id]
          };
        }
        return prev;
      });
    });
  }, [games]);

  const filteredGames = games.filter((game) => {
    const matchesSport = selectedSport === "all" || game.sport === selectedSport;
    const matchesSearch =
      searchQuery === "" ||
      game.homeTeam.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      game.awayTeam.name.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesSport && matchesSearch;
  });

  return (
    <div className={cn("space-y-6", className)}>
      {/* Filters */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex flex-wrap gap-2">
          <Button
            variant={selectedSport === "all" ? "primary" : "outline"}
            onClick={() => setSelectedSport("all")}
            size="sm"
          >
            All Sports
          </Button>
          <Button
            variant={selectedSport === "NFL" ? "primary" : "outline"}
            onClick={() => setSelectedSport("NFL")}
            size="sm"
          >
            NFL
          </Button>
          <Button
            variant={selectedSport === "NBA" ? "primary" : "outline"}
            onClick={() => setSelectedSport("NBA")}
            size="sm"
          >
            NBA
          </Button>
          <Button
            variant={selectedSport === "MLB" ? "primary" : "outline"}
            onClick={() => setSelectedSport("MLB")}
            size="sm"
          >
            MLB
          </Button>
          <Button
            variant={selectedSport === "NHL" ? "primary" : "outline"}
            onClick={() => setSelectedSport("NHL")}
            size="sm"
          >
            NHL
          </Button>
        </div>
        <div className="w-full sm:w-64">
          <Input
            type="search"
            placeholder="Search teams..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      {/* Games Grid */}
      <div className="grid gap-6 sm:grid-cols-1 md:grid-cols-2">
        {filteredGames.map((game) => (
          <BettingCard
            key={game.id}
            homeTeam={game.homeTeam}
            awayTeam={game.awayTeam}
            homeOdds={game.homeOdds}
            awayOdds={game.awayOdds}
            previousHomeOdds={previousOdds[game.id]?.home}
            previousAwayOdds={previousOdds[game.id]?.away}
            status={game.status}
            onBet={(team) => {
              onSelectGame?.(game, team.isHome ? "home" : "away");
            }}
            selectedTeam={
              selectedGames?.find(
                (selected) =>
                  selected.homeTeam.name === game.homeTeam.name &&
                  selected.awayTeam.name === game.awayTeam.name
              )?.selectedTeam
            }
          />
        ))}
      </div>

      {/* Empty State */}
      {filteredGames.length === 0 && (
        <div className="flex flex-col items-center justify-center rounded-lg border border-dashed p-8 text-center">
          <h3 className="mt-2 text-lg font-semibold">No games found</h3>
          <p className="mt-1 text-sm text-muted-foreground">
            Try adjusting your filters or search query
          </p>
        </div>
      )}
    </div>
  );
}
```

## src/components/ui/card.tsx
- Language: TSX
- Encoding: utf-8
- Size: 392 bytes
- Tokens: 97

```tsx
import * as React from 'react';
import { cn } from '@/lib/utils';

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      'rounded-lg border bg-card text-card-foreground shadow-sm',
      className
    )}
    {...props}
  />
));
Card.displayName = 'Card';

export { Card };
```

## src/components/ui/dropdown-menu.tsx
- Language: TSX
- Encoding: utf-8
- Size: 1788 bytes
- Tokens: 399

```tsx
"use client";

import * as React from "react";
import * as DropdownMenuPrimitive from "@radix-ui/react-dropdown-menu";
import { cn } from "@/lib/utils";

const DropdownMenu = DropdownMenuPrimitive.Root;

const DropdownMenuTrigger = DropdownMenuPrimitive.Trigger;

const DropdownMenuContent = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Content>
>(({ className, sideOffset = 4, ...props }, ref) => (
  <DropdownMenuPrimitive.Portal>
    <DropdownMenuPrimitive.Content
      ref={ref}
      sideOffset={sideOffset}
      className={cn(
        "z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md animate-in data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2",
        className
      )}
      {...props}
    />
  </DropdownMenuPrimitive.Portal>
));
DropdownMenuContent.displayName = DropdownMenuPrimitive.Content.displayName;

const DropdownMenuItem = React.forwardRef<
  React.ElementRef<typeof DropdownMenuPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof DropdownMenuPrimitive.Item>
>(({ className, ...props }, ref) => (
  <DropdownMenuPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      className
    )}
    {...props}
  />
));
DropdownMenuItem.displayName = DropdownMenuPrimitive.Item.displayName;

export {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
};
```

## src/schemas/betting.ts
- Language: TypeScript
- Encoding: utf-8
- Size: 2 bytes
- Tokens: 1

```typescript

```

## src/stories/AIRecommendations.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2201 bytes
- Tokens: 564

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { AIRecommendations } from '@/components/controls/AIRecommendations';
import { ThemeProvider } from '@/components/providers/ThemeProvider';
import type { Recommendation } from '@/lib/types/models/recommendations';

const meta = {
  title: 'Controls/AIRecommendations',
  component: AIRecommendations,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  decorators: [
    (Story) => (
      <ThemeProvider>
        <div className="w-[800px] p-4">
          <Story />
        </div>
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof AIRecommendations>;

export default meta;
type Story = StoryObj<typeof meta>;

const mockRecommendations: Recommendation[] = [
  {
    id: '1',
    gameId: 'lakers-warriors',
    homeTeam: 'Lakers',
    awayTeam: 'Warriors',
    recommendedBet: {
      type: 'moneyline' as const,
      team: 'Lakers',
      odds: 2.1,
    },
    confidence: 85,
    reasoning: 'Based on recent performance metrics and historical head-to-head data, the Lakers show strong value at these odds.',
    timestamp: new Date(),
  },
  {
    id: '2',
    gameId: 'celtics-heat',
    homeTeam: 'Celtics',
    awayTeam: 'Heat',
    recommendedBet: {
      type: 'spread' as const,
      team: 'Heat',
      line: 5.5,
      odds: 1.91,
    },
    confidence: 75,
    reasoning: 'The Heat have consistently covered the spread as underdogs in their last 8 away games.',
    timestamp: new Date(),
  },
  {
    id: '3',
    gameId: 'chiefs-49ers',
    homeTeam: 'Chiefs',
    awayTeam: '49ers',
    recommendedBet: {
      type: 'total' as const,
      line: 48.5,
      odds: 1.95,
    },
    confidence: 65,
    reasoning: 'Weather conditions and defensive matchups suggest a lower-scoring game than the market expects.',
    timestamp: new Date(),
  },
];

export const WithRecommendations: Story = {
  args: {
    recommendations: mockRecommendations,
  },
};

export const NoRecommendations: Story = {
  args: {
    recommendations: [],
  },
};

export const HighConfidence: Story = {
  args: {
    recommendations: mockRecommendations.map(rec => ({
      ...rec,
      confidence: 90,
    })),
  },
};
```

## src/stories/BetsPage.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 3728 bytes
- Tokens: 824

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import BetsPage from '@/app/bets/page';
import { ThemeProvider } from '@/components/providers/ThemeProvider';
import { handlers } from '@/lib/mocks/handlers';

const meta = {
  title: 'Pages/Bets',
  component: BetsPage,
  parameters: {
    layout: 'fullscreen',
    nextjs: {
      appDirectory: true,
      navigation: {
        query: {},
      },
    },
    msw: {
      handlers: [
        ...handlers,
        // Add custom handlers for the bets page
      ],
    },
    backgrounds: {
      default: 'dark',
    },
  },
  decorators: [
    (Story) => (
      <ThemeProvider attribute="class" defaultTheme="dark" enableSystem={false}>
        <Story />
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof BetsPage>;

export default meta;
type Story = StoryObj<typeof meta>;

// Default view with live games
export const Default: Story = {
  parameters: {
    msw: {
      handlers: [
        ...handlers,
        // Add mock data for live games
        {
          url: '/api/bets',
          method: 'GET',
          response: {
            data: [
              {
                id: '1',
                homeTeam: {
                  name: 'Lakers',
                  score: 89,
                  isHome: true,
                },
                awayTeam: {
                  name: 'Warriors',
                  score: 92,
                  isHome: false,
                },
                status: {
                  type: 'live',
                  period: '3',
                  timeRemaining: '8:45',
                  detail: 'In Progress',
                },
                homeOdds: 1.90,
                awayOdds: 2.10,
              },
              {
                id: '2',
                homeTeam: {
                  name: 'Celtics',
                  score: 58,
                  isHome: true,
                },
                awayTeam: {
                  name: 'Heat',
                  score: 52,
                  isHome: false,
                },
                status: {
                  type: 'halftime',
                  period: '2',
                  detail: 'Halftime',
                },
                homeOdds: 1.80,
                awayOdds: 2.20,
              },
            ],
          },
        },
      ],
    },
  },
};

// Filtered by status
export const FilteredByStatus: Story = {
  parameters: {
    nextjs: {
      navigation: {
        query: {
          status: 'pending',
        },
      },
    },
  },
};

// Filtered by type
export const FilteredByType: Story = {
  parameters: {
    nextjs: {
      navigation: {
        query: {
          type: 'parlay',
        },
      },
    },
  },
};

// Empty state
export const EmptyState: Story = {
  parameters: {
    msw: {
      handlers: [
        ...handlers,
        {
          url: '/api/bets',
          method: 'GET',
          response: {
            data: [],
          },
        },
      ],
    },
  },
};

// Loading state
export const Loading: Story = {
  parameters: {
    msw: {
      handlers: [
        ...handlers,
        {
          url: '/api/bets',
          method: 'GET',
          async response() {
            await new Promise(resolve => setTimeout(resolve, 2000));
            return {
              data: [],
            };
          },
        },
      ],
    },
  },
};

// Error state
export const Error: Story = {
  parameters: {
    msw: {
      handlers: [
        ...handlers,
        {
          url: '/api/bets',
          method: 'GET',
          response: {
            status: 500,
            data: {
              error: 'Failed to fetch bets',
            },
          },
        },
      ],
    },
  },
};
```

## src/stories/BettingActionGroup.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 1143 bytes
- Tokens: 289

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { BettingActionGroup } from "@/components/controls/BettingActionGroup";

const meta = {
  title: "Controls/BettingActionGroup",
  component: BettingActionGroup,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof BettingActionGroup>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
};

export const PlaceBetOnly: Story = {
  args: {
    actions: ["placeBet"],
  },
};

export const WithoutClearBet: Story = {
  args: {
    actions: ["placeBet", "addToParlay"],
  },
};

export const LoadingState: Story = {
  args: {
    buttonStates: {
      placeBet: { loading: true },
      clearBet: {},
      addToParlay: {},
    },
  },
};

export const DisabledState: Story = {
  args: {
    buttonStates: {
      placeBet: { disabled: true },
      clearBet: { disabled: true },
      addToParlay: {},
    },
  },
};

export const MixedStates: Story = {
  args: {
    buttonStates: {
      placeBet: { loading: true },
      clearBet: { disabled: true },
      addToParlay: {},
    },
  },
};
```

## src/stories/BettingCard.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 4336 bytes
- Tokens: 1150

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { BettingCard } from "@/components/controls/BettingCard";
import { useEffect, useState } from "react";
import type { GameStatus } from "@/lib/types/models/games";

const meta = {
  title: "Controls/BettingCard",
  component: BettingCard,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof BettingCard>;

export default meta;
type Story = StoryObj<typeof meta>;

const defaultArgs = {
  homeTeam: {
    name: "Los Angeles Lakers",
    score: 98,
    isHome: true,
  },
  awayTeam: {
    name: "Golden State Warriors",
    score: 95,
    isHome: false,
  },
  homeOdds: 1.85,
  awayOdds: 2.1,
  status: {
    type: "live",
    period: "Q4",
    timeRemaining: "4:30",
    possession: "home",
    detail: "Lakers ball, shooting foul on Curry",
  } as GameStatus,
};

export const Default: Story = {
  args: defaultArgs,
};

export const WithOddsMovement: Story = {
  args: {
    ...defaultArgs,
    previousHomeOdds: 1.95,
    previousAwayOdds: 1.95,
  },
};

export const Halftime: Story = {
  args: {
    ...defaultArgs,
    status: {
      type: "halftime",
      period: "2",
      detail: "Halftime",
    } as GameStatus,
  },
};

export const Final: Story = {
  args: {
    ...defaultArgs,
    status: {
      type: "final",
      detail: "Final",
    } as GameStatus,
  },
};

export const WithSelectedTeam: Story = {
  args: {
    ...defaultArgs,
    selectedTeam: {
      name: "Los Angeles Lakers",
      isHome: true,
    },
  },
};

export const LiveUpdates = {
  render: function Story() {
    const [homeScore, setHomeScore] = useState(98);
    const [awayScore, setAwayScore] = useState(95);
    const [homeOdds, setHomeOdds] = useState(1.85);
    const [awayOdds, setAwayOdds] = useState(2.1);
    const [previousHomeOdds, setPreviousHomeOdds] = useState(1.85);
    const [previousAwayOdds, setPreviousAwayOdds] = useState(2.1);
    const [timeRemaining, setTimeRemaining] = useState("4:30");
    const [possession, setPossession] = useState<"home" | "away">("home");

    useEffect(() => {
      const interval = setInterval(() => {
        // Randomly update scores
        if (Math.random() > 0.7) {
          if (possession === "home") {
            setHomeScore(prev => prev + (Math.random() > 0.7 ? 3 : 2));
          } else {
            setAwayScore(prev => prev + (Math.random() > 0.7 ? 3 : 2));
          }
        }

        // Update possession
        if (Math.random() > 0.8) {
          setPossession(prev => prev === "home" ? "away" : "home");
        }

        // Update odds with previous values
        if (Math.random() > 0.6) {
          setPreviousHomeOdds(homeOdds);
          setPreviousAwayOdds(awayOdds);
          setHomeOdds(prev => prev + (Math.random() - 0.5) * 0.1);
          setAwayOdds(prev => prev + (Math.random() - 0.5) * 0.1);
        }

        // Update time
        setTimeRemaining(prev => {
          const [minutes, seconds] = prev.split(":").map(Number);
          let newSeconds = seconds - 30;
          let newMinutes = minutes;
          if (newSeconds < 0) {
            newSeconds = 30;
            newMinutes--;
          }
          return `${newMinutes}:${newSeconds.toString().padStart(2, "0")}`;
        });
      }, 3000);

      return () => clearInterval(interval);
    }, [possession, homeOdds, awayOdds]);

    return (
      <div className="space-y-4">
        <BettingCard
          homeTeam={{
            name: "Los Angeles Lakers",
            score: homeScore,
            isHome: true,
          }}
          awayTeam={{
            name: "Golden State Warriors",
            score: awayScore,
            isHome: false,
          }}
          homeOdds={homeOdds}
          awayOdds={awayOdds}
          previousHomeOdds={previousHomeOdds}
          previousAwayOdds={previousAwayOdds}
          status={{
            type: "live",
            period: "Q4",
            timeRemaining,
            possession,
            detail: possession === "home" ? "Lakers ball" : "Warriors ball",
          } as GameStatus}
        />
        <p className="text-sm text-muted-foreground text-center">
          Watch as the game updates every 3 seconds with random score changes, possession switches, and odds movements
        </p>
      </div>
    );
  },
};
```

## src/stories/BettingForm.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 4877 bytes
- Tokens: 1233

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { BettingForm } from "@/components/controls/BettingForm";
import { ThemeProvider } from "@/components/providers/ThemeProvider";
import { within, userEvent, waitFor } from "@storybook/testing-library";
import { expect } from "@storybook/jest";

const meta = {
  title: "Controls/BettingForm",
  component: BettingForm,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  decorators: [
    (Story) => (
      <ThemeProvider>
        <div className="w-[400px] p-4 bg-background">
          <Story />
        </div>
      </ThemeProvider>
    ),
  ],
  argTypes: {
    onPlaceBet: { action: "placeBet" },
  },
} satisfies Meta<typeof BettingForm>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    odds: 2.5,
  },
};

export const WithAmericanOdds: Story = {
  args: {
    odds: 2.5,
    oddsFormat: "american",
  },
};

export const WithFractionalOdds: Story = {
  args: {
    odds: 2.5,
    oddsFormat: "fractional",
  },
};

export const Loading: Story = {
  args: {
    odds: 2.5,
    isLoading: true,
  },
};

export const CustomLimits: Story = {
  args: {
    odds: 2.5,
    minBet: 10,
    maxBet: 1000,
  },
};

export const ParlayBet: Story = {
  args: {
    odds: 6.5,
    betType: "parlay",
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const quickAmountButton = canvas.getByText("$50");
    
    await userEvent.click(quickAmountButton);
    const placeBetButton = canvas.getByText("Place Bet");
    await userEvent.click(placeBetButton);
    
    await waitFor(() => {
      expect(canvas.getByText("Confirm your parlay bet of $50 to win $325.00?")).toBeInTheDocument();
    });
  },
};

export const TeaserBet: Story = {
  args: {
    odds: 3.2,
    betType: "teaser",
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const input = canvas.getByLabelText("Bet Amount");
    await userEvent.type(input, "100");
    
    const placeBetButton = canvas.getByText("Place Bet");
    await userEvent.click(placeBetButton);
    
    await waitFor(() => {
      expect(canvas.getByText("Confirm your teaser bet of $100 to win $320.00?")).toBeInTheDocument();
    });
  },
};

export const WithError: Story = {
  args: {
    odds: 2.5,
    minBet: 1,
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const input = canvas.getByLabelText("Bet Amount");
    await userEvent.type(input, "0.5");
    
    await waitFor(() => {
      expect(canvas.getByText("Minimum bet is $1")).toBeInTheDocument();
    });
  },
};

export const WithQuickAmount: Story = {
  args: {
    odds: 2.5,
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByText("$50");
    await userEvent.click(button);
    
    await waitFor(() => {
      const input = canvas.getByLabelText("Bet Amount") as HTMLInputElement;
      expect(input.value).toBe("50");
    });
  },
};

export const BetTypeSwitch: Story = {
  args: {
    odds: 2.5,
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    
    // Switch to parlay
    const parlayButton = canvas.getByText("Parlay");
    await userEvent.click(parlayButton);
    
    // Enter amount
    const input = canvas.getByLabelText("Bet Amount");
    await userEvent.type(input, "25");
    
    // Place bet
    const placeBetButton = canvas.getByText("Place Bet");
    await userEvent.click(placeBetButton);
    
    await waitFor(() => {
      expect(canvas.getByText("Confirm your parlay bet of $25 to win $62.50?")).toBeInTheDocument();
    });
  },
};

export const ConfirmationFlow: Story = {
  args: {
    odds: 2.5,
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    
    // Enter amount
    const input = canvas.getByLabelText("Bet Amount");
    await userEvent.type(input, "100");
    
    // Place bet
    const placeBetButton = canvas.getByText("Place Bet");
    await userEvent.click(placeBetButton);
    
    // Check confirmation dialog
    await waitFor(() => {
      expect(canvas.getByText("Confirm your single bet of $100 to win $250.00?")).toBeInTheDocument();
    });
    
    // Cancel bet
    const cancelButton = canvas.getByText("Cancel");
    await userEvent.click(cancelButton);
    
    // Check if back to initial state
    await waitFor(() => {
      expect(canvas.getByText("Place Bet")).toBeInTheDocument();
    });
  },
};

export const AllFormats: Story = {
  args: {
    odds: 2.5,
  },
  render: (args) => (
    <div className="flex flex-col gap-4">
      <BettingForm {...args} oddsFormat="decimal" />
      <BettingForm {...args} oddsFormat="american" />
      <BettingForm {...args} oddsFormat="fractional" />
    </div>
  ),
};
```

## src/stories/BettingPage.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 746 bytes
- Tokens: 177

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import BettingPage from "@/app/betting/page";
import { ThemeProvider } from "@/components/providers/ThemeProvider";

const meta = {
  title: "Pages/BettingPage",
  component: BettingPage,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
  decorators: [
    (Story) => (
      <ThemeProvider attribute="class" defaultTheme="light" enableSystem={false}>
        <Story />
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof BettingPage>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
};

export const DarkMode: Story = {
  args: {},
  parameters: {
    themes: {
      themeOverride: 'dark',
    },
  },
};
```

## src/stories/BettingTemplate.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 3750 bytes
- Tokens: 790

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { BettingTemplate } from "@/components/templates/BettingTemplate";
import { BettingForm } from "@/components/controls/BettingForm";
import { LiveScoreCard } from "@/components/controls/LiveScoreCard";
import { ThemeProvider } from "@/components/providers/ThemeProvider";

const meta = {
  title: "Templates/BettingTemplate",
  component: BettingTemplate,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
  decorators: [
    (Story) => (
      <ThemeProvider attribute="class" defaultTheme="light" enableSystem={false}>
        <div className="min-h-screen">
          <Story />
        </div>
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof BettingTemplate>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: (
      <div>
        <div className="mb-8">
          <h1 className="text-3xl font-bold font-display">NFL Games</h1>
          <p className="mt-2 text-muted-foreground">Live games happening now</p>
        </div>

        <div className="grid gap-8">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            <LiveScoreCard
              teams={[
                {
                  name: "San Francisco 49ers",
                  score: 21,
                  isHome: false,
                },
                {
                  name: "Kansas City Chiefs",
                  score: 24,
                  isHome: true,
                },
              ]}
              gameStatus="Live"
              sportType="NFL"
              keyStats={{
                timeRemaining: "2:30",
                period: "4",
                periodType: "quarter",
                possession: "home",
                lastPlay: "P. Mahomes pass complete to T. Kelce for 12 yards",
              }}
            />
            <LiveScoreCard
              teams={[
                {
                  name: "Detroit Lions",
                  score: 14,
                  isHome: false,
                },
                {
                  name: "Green Bay Packers",
                  score: 17,
                  isHome: true,
                },
              ]}
              gameStatus="Live"
              sportType="NFL"
              keyStats={{
                timeRemaining: "8:45",
                period: "3",
                periodType: "quarter",
                possession: "away",
                lastPlay: "J. Goff pass incomplete to A. St. Brown",
              }}
            />
            <LiveScoreCard
              teams={[
                {
                  name: "Philadelphia Eagles",
                  score: 28,
                  isHome: false,
                },
                {
                  name: "Dallas Cowboys",
                  score: 28,
                  isHome: true,
                },
              ]}
              gameStatus="Live"
              sportType="NFL"
              keyStats={{
                timeRemaining: "0:45",
                period: "4",
                periodType: "quarter",
                possession: "home",
                lastPlay: "D. Prescott scrambles for 8 yards",
              }}
            />
          </div>

          <div className="rounded-lg border bg-card p-6">
            <h2 className="mb-4 text-xl font-semibold">Place a Bet</h2>
            <div className="max-w-sm">
              <BettingForm odds={2.5} />
            </div>
          </div>
        </div>
      </div>
    ),
  },
};

export const DarkMode: Story = {
  args: {
    ...Default.args,
  },
  parameters: {
    backgrounds: {
      default: 'dark',
    },
    themes: {
      themeOverride: 'dark',
    },
  },
};
```

## src/stories/button.css
- Language: CSS
- Encoding: utf-8
- Size: 642 bytes
- Tokens: 213

```css
.storybook-button {
  display: inline-block;
  cursor: pointer;
  border: 0;
  border-radius: 3em;
  font-weight: 700;
  line-height: 1;
  font-family: 'Nunito Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif;
}
.storybook-button--primary {
  background-color: #555ab9;
  color: white;
}
.storybook-button--secondary {
  box-shadow: rgba(0, 0, 0, 0.15) 0px 0px 0px 1px inset;
  background-color: transparent;
  color: #333;
}
.storybook-button--small {
  padding: 10px 16px;
  font-size: 12px;
}
.storybook-button--medium {
  padding: 11px 20px;
  font-size: 14px;
}
.storybook-button--large {
  padding: 12px 24px;
  font-size: 16px;
}
```

## src/stories/Button.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 3058 bytes
- Tokens: 739

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from '@/components/controls/Button';
import { userEvent, within } from '@storybook/testing-library';
import { expect } from '@storybook/jest';

const meta = {
  title: 'Controls/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  args: {
    children: 'Button',
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Primary Button',
  },
};

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Button',
  },
};

export const Outline: Story = {
  args: {
    variant: 'outline',
    children: 'Outline Button',
  },
};

export const Small: Story = {
  args: {
    size: 'sm',
    children: 'Small Button',
  },
};

export const Large: Story = {
  args: {
    size: 'lg',
    children: 'Large Button',
  },
};

export const Loading: Story = {
  args: {
    isLoading: true,
    children: 'Loading Button',
  },
};

export const LoadingWithCustomText: Story = {
  args: {
    isLoading: true,
    loadingText: 'Processing...',
    children: 'Submit',
  },
};

export const Disabled: Story = {
  args: {
    disabled: true,
    children: 'Disabled Button',
  },
};

export const DisabledOutline: Story = {
  args: {
    disabled: true,
    variant: 'outline',
    children: 'Disabled Outline',
  },
};

export const DisabledSecondary: Story = {
  args: {
    disabled: true,
    variant: 'secondary',
    children: 'Disabled Secondary',
  },
};

export const WithInteractions: Story = {
  args: {
    children: 'Interactive Button',
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    
    // Get the button
    const button = canvas.getByRole('button');
    
    // Hover the button
    await userEvent.hover(button);
    expect(button).toHaveClass('hover:scale-[1.02]');
    
    // Focus the button
    await button.focus();
    expect(button).toHaveClass('focus:scale-[1.02]');
    
    // Click the button (active state)
    await userEvent.click(button);
    expect(button).toHaveClass('active:scale-[0.98]');
    
    // Test loading state
    button.setAttribute('data-loading', 'true');
    expect(button).toHaveAttribute('data-loading', 'true');
    expect(button).toHaveClass('animate-pulse');
    
    // Test disabled state
    button.setAttribute('disabled', '');
    expect(button).toBeDisabled();
    expect(button).toHaveClass('disabled:scale-100');
  },
};

export const AnimationShowcase: Story = {
  render: () => (
    <div className="flex flex-col gap-4">
      <div className="flex gap-4">
        <Button>Hover Me</Button>
        <Button variant="secondary">Focus Me</Button>
        <Button variant="outline">Click Me</Button>
      </div>
      <p className="text-sm text-muted-foreground text-center">
        Try hovering, focusing, and clicking the buttons to see animations
      </p>
    </div>
  ),
};
```

## src/stories/Button.tsx
- Language: TSX
- Encoding: utf-8
- Size: 966 bytes
- Tokens: 226

```tsx
import React from 'react';

import './button.css';

export interface ButtonProps {
  /** Is this the principal call to action on the page? */
  primary?: boolean;
  /** What background color to use */
  backgroundColor?: string;
  /** How large should the button be? */
  size?: 'small' | 'medium' | 'large';
  /** Button contents */
  label: string;
  /** Optional click handler */
  onClick?: () => void;
}

/** Primary UI component for user interaction */
export const Button = ({
  primary = false,
  size = 'medium',
  backgroundColor,
  label,
  ...props
}: ButtonProps) => {
  const mode = primary ? 'storybook-button--primary' : 'storybook-button--secondary';
  return (
    <button
      type="button"
      className={['storybook-button', `storybook-button--${size}`, mode].join(' ')}
      {...props}
    >
      {label}
      <style jsx>{`
        button {
          background-color: ${backgroundColor};
        }
      `}</style>
    </button>
  );
};
```

## src/stories/Configure.mdx
- Language: text
- Encoding: utf-8
- Size: 12898 bytes
- Tokens: 2000

```text
import { Meta } from "@storybook/blocks";
import Image from "next/image";

import Github from "./assets/github.svg";
import Discord from "./assets/discord.svg";
import Youtube from "./assets/youtube.svg";
import Tutorials from "./assets/tutorials.svg";
import Styling from "./assets/styling.png";
import Context from "./assets/context.png";
import Assets from "./assets/assets.png";
import Docs from "./assets/docs.png";
import Share from "./assets/share.png";
import FigmaPlugin from "./assets/figma-plugin.png";
import Testing from "./assets/testing.png";
import Accessibility from "./assets/accessibility.png";
import Theming from "./assets/theming.png";
import AddonLibrary from "./assets/addon-library.png";

export const RightArrow = () => <svg 
    viewBox="0 0 14 14" 
    width="8px" 
    height="14px" 
    style={{ 
      marginLeft: '4px',
      display: 'inline-block',
      shapeRendering: 'inherit',
      verticalAlign: 'middle',
      fill: 'currentColor',
      'path fill': 'currentColor'
    }}
>
  <path d="m11.1 7.35-5.5 5.5a.5.5 0 0 1-.7-.7L10.04 7 4.9 1.85a.5.5 0 1 1 .7-.7l5.5 5.5c.2.2.2.5 0 .7Z" />
</svg>

<Meta title="Configure your project" />

<div className="sb-container">
  <div className='sb-section-title'>
    # Configure your project

    Because Storybook works separately from your app, you'll need to configure it for your specific stack and setup. Below, explore guides for configuring Storybook with popular frameworks and tools. If you get stuck, learn how you can ask for help from our community.
  </div>
  <div className="sb-section">
    <div className="sb-section-item">
      <Image
        src={Styling}
        alt="A wall of logos representing different styling technologies"
        width={0}
        height={0}
        style={{ width: '100%', height: 'auto' }}
      />
      <h4 className="sb-section-item-heading">Add styling and CSS</h4>
      <p className="sb-section-item-paragraph">Like with web applications, there are many ways to include CSS within Storybook. Learn more about setting up styling within Storybook.</p>
      <a
        href="https://storybook.js.org/docs/configure/styling-and-css/?renderer=react"
        target="_blank"
      >Learn more<RightArrow /></a>
    </div>
    <div className="sb-section-item">
      <Image 
        width={0}
        height={0}
        style={{ width: '100%', height: 'auto' }}
        src={Context}
        alt="An abstraction representing the composition of data for a component"
      />
      <h4 className="sb-section-item-heading">Provide context and mocking</h4>
      <p className="sb-section-item-paragraph">Often when a story doesn't render, it's because your component is expecting a specific environment or context (like a theme provider) to be available.</p>
      <a
        href="https://storybook.js.org/docs/writing-stories/decorators/?renderer=react#context-for-mocking"
        target="_blank"
      >Learn more<RightArrow /></a>
    </div>
    <div className="sb-section-item">
      <Image 
        width={0}
        height={0}
        style={{ width: '100%', height: 'auto' }} 
        src={Assets} 
        alt="A representation of typography and image assets" 
      />
      <div>
        <h4 className="sb-section-item-heading">Load assets and resources</h4>
        <p className="sb-section-item-paragraph">To link static files (like fonts) to your projects and stories, use the
        `staticDirs` configuration option to specify folders to load when
        starting Storybook.</p>
        <a
          href="https://storybook.js.org/docs/configure/images-and-assets/?renderer=react"
          target="_blank"
        >Learn more<RightArrow /></a>
      </div>
    </div>
  </div>
</div>
<div className="sb-container">
  <div className='sb-section-title'>
    # Do more with Storybook

    Now that you know the basics, let's explore other parts of Storybook that will improve your experience. This list is just to get you started. You can customise Storybook in many ways to fit your needs.
  </div>

  <div className="sb-section">
    <div className="sb-features-grid">
      <div className="sb-grid-item">
        <Image 
          width={0}
          height={0}
          style={{ width: '100%', height: 'auto' }} 
          src={Docs} 
          alt="A screenshot showing the autodocs tag being set, pointing a docs page being generated" 
        />
        <h4 className="sb-section-item-heading">Autodocs</h4>
        <p className="sb-section-item-paragraph">Auto-generate living,
          interactive reference documentation from your components and stories.</p>
        <a
          href="https://storybook.js.org/docs/writing-docs/autodocs/?renderer=react"
          target="_blank"
        >Learn more<RightArrow /></a>
      </div>
      <div className="sb-grid-item">
        <Image 
          width={0}
          height={0}
          style={{ width: '100%', height: 'auto' }} 
          src={Share} 
          alt="A browser window showing a Storybook being published to a chromatic.com URL" 
        />
        <h4 className="sb-section-item-heading">Publish to Chromatic</h4>
        <p className="sb-section-item-paragraph">Publish your Storybook to review and collaborate with your entire team.</p>
        <a
          href="https://storybook.js.org/docs/sharing/publish-storybook/?renderer=react#publish-storybook-with-chromatic"
          target="_blank"
        >Learn more<RightArrow /></a>
      </div>
      <div className="sb-grid-item">
        <Image 
          width={0}
          height={0}
          style={{ width: '100%', height: 'auto' }} 
          src={FigmaPlugin} 
          alt="Windows showing the Storybook plugin in Figma" 
        />
        <h4 className="sb-section-item-heading">Figma Plugin</h4>
        <p className="sb-section-item-paragraph">Embed your stories into Figma to cross-reference the design and live
          implementation in one place.</p>
        <a
          href="https://storybook.js.org/docs/sharing/design-integrations/?renderer=react#embed-storybook-in-figma-with-the-plugin"
          target="_blank"
        >Learn more<RightArrow /></a>
      </div>
      <div className="sb-grid-item">
        <Image 
          width={0}
          height={0}
          style={{ width: '100%', height: 'auto' }} 
          src={Testing} 
          alt="Screenshot of tests passing and failing" 
        />
        <h4 className="sb-section-item-heading">Testing</h4>
        <p className="sb-section-item-paragraph">Use stories to test a component in all its variations, no matter how
          complex.</p>
        <a
          href="https://storybook.js.org/docs/writing-tests/?renderer=react"
          target="_blank"
        >Learn more<RightArrow /></a>
      </div>
      <div className="sb-grid-item">
        <Image 
          width={0}
          height={0}
          style={{ width: '100%', height: 'auto' }} 
          src={Accessibility} 
          alt="Screenshot of accessibility tests passing and failing" 
        />
        <h4 className="sb-section-item-heading">Accessibility</h4>
        <p className="sb-section-item-paragraph">Automatically test your components for a11y issues as you develop.</p>
        <a
          href="https://storybook.js.org/docs/writing-tests/accessibility-testing/?renderer=react"
          target="_blank"
        >Learn more<RightArrow /></a>
      </div>
      <div className="sb-grid-item">
        <Image 
          width={0}
          height={0}
          style={{ width: '100%', height: 'auto' }} 
          src={Theming} 
          alt="Screenshot of Storybook in light and dark mode" 
        />
        <h4 className="sb-section-item-heading">Theming</h4>
        <p className="sb-section-item-paragraph">Theme Storybook's UI to personalize it to your project.</p>
        <a
          href="https://storybook.js.org/docs/configure/theming/?renderer=react"
          target="_blank"
        >Learn more<RightArrow /></a>
      </div>
    </div>
  </div>
</div>
<div className='sb-addon'>
  <div className='sb-addon-text'>
    <h4>Addons</h4>
    <p className="sb-section-item-paragraph">Integrate your tools with Storybook to connect workflows.</p>
    <
```

## src/stories/DateTimePicker.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 5227 bytes
- Tokens: 1271

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { DateTimePicker } from "@/components/controls/DateTimePicker";
import { userEvent, within } from '@storybook/testing-library';
import { expect } from '@storybook/jest';
import { ThemeProvider } from "@/components/providers/ThemeProvider";

const meta = {
  title: "Controls/DateTimePicker",
  component: DateTimePicker,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  decorators: [
    (Story) => (
      <ThemeProvider attribute="class" defaultTheme="light" enableSystem={false}>
        <div className="p-4 bg-background">
          <Story />
        </div>
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof DateTimePicker>;

export default meta;
type Story = StoryObj<typeof meta>;

const today = new Date();
const tomorrow = new Date(today);
tomorrow.setDate(tomorrow.getDate() + 1);

const nextWeek = new Date(today);
nextWeek.setDate(nextWeek.getDate() + 7);

export const Default: Story = {
  args: {
    value: today,
    mode: "datetime",
  },
};

export const DarkMode: Story = {
  args: {
    value: today,
    mode: "datetime",
  },
  parameters: {
    backgrounds: { default: 'dark' },
    themes: {
      themeOverride: 'dark',
    },
  },
};

export const DateOnly: Story = {
  args: {
    value: today,
    mode: "date",
  },
};

export const TimeOnly: Story = {
  args: {
    value: today,
    mode: "time",
  },
};

export const DateTimeInteractive: Story = {
  args: {
    mode: "datetime",
    value: today,
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    
    // Get the input and open the picker
    const input = canvas.getByRole("textbox");
    await userEvent.click(input);
    
    // Select a date
    const dayButton = canvas.getByRole("button", { name: tomorrow.getDate().toString() });
    await userEvent.click(dayButton);
    
    // Change the time
    const incrementHourButton = canvas.getByRole("button", { name: "Increment hour" });
    const incrementMinuteButton = canvas.getByRole("button", { name: "Increment minute" });
    
    await userEvent.click(incrementHourButton);
    await userEvent.click(incrementHourButton);
    await userEvent.click(incrementMinuteButton);
    await userEvent.click(incrementMinuteButton);
    
    // Verify the input has both date and time
    const selectedDate = new Date(today);
    selectedDate.setDate(tomorrow.getDate());
    selectedDate.setHours(selectedDate.getHours() + 2);
    selectedDate.setMinutes(selectedDate.getMinutes() + 2);
    
    expect(input).toHaveValue(
      `${selectedDate.toISOString().split("T")[0]}T${selectedDate.toTimeString().slice(0, 5)}`
    );
  },
};

export const DateTimeFeatures = {
  render: () => (
    <div className="space-y-8">
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Calendar Navigation</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium mb-1 block">Previous/Next Month</label>
            <DateTimePicker mode="datetime" value={today} />
          </div>
          <div>
            <label className="text-sm font-medium mb-1 block">Previous/Next Year</label>
            <DateTimePicker mode="datetime" value={today} />
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-medium">Time Selection</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium mb-1 block">Hour Increment/Decrement</label>
            <DateTimePicker mode="datetime" value={today} />
          </div>
          <div>
            <label className="text-sm font-medium mb-1 block">Minute Increment/Decrement</label>
            <DateTimePicker mode="datetime" value={today} />
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-medium">Date Range Restrictions</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium mb-1 block">Future Dates Only</label>
            <DateTimePicker mode="datetime" value={today} min={today} />
          </div>
          <div>
            <label className="text-sm font-medium mb-1 block">Within Next Week</label>
            <DateTimePicker mode="datetime" value={today} min={today} max={nextWeek} />
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-medium">Input Formats</h3>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="text-sm font-medium mb-1 block">Date Only (YYYY-MM-DD)</label>
            <DateTimePicker mode="date" value={today} />
          </div>
          <div>
            <label className="text-sm font-medium mb-1 block">Time Only (HH:MM)</label>
            <DateTimePicker mode="time" value={today} />
          </div>
          <div>
            <label className="text-sm font-medium mb-1 block">Date & Time (YYYY-MM-DDTHH:MM)</label>
            <DateTimePicker mode="datetime" value={today} />
          </div>
        </div>
      </div>
    </div>
  ),
};
```

## src/stories/Error.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 3285 bytes
- Tokens: 718

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { ErrorMessage } from '@/components/atoms/ErrorMessage';
import { ErrorState } from '@/components/molecules/ErrorState';
import { ErrorBoundary } from '@/components/organisms/ErrorBoundary';
import { ThemeProvider } from '@/components/providers/ThemeProvider';
import { Icon } from '@/components/controls/Icon';
import { HeroIcons } from '@/lib/types/models/icons';

const meta = {
  title: 'Error Components',
  decorators: [
    (Story) => (
      <ThemeProvider>
        <div className="p-4">
          <Story />
        </div>
      </ThemeProvider>
    ),
  ],
  tags: ['autodocs'],
} satisfies Meta<typeof ErrorMessage>;

export default meta;

// ErrorMessage Stories
export const DefaultErrorMessage: StoryObj<typeof ErrorMessage> = {
  render: () => (
    <ErrorMessage
      message="Something went wrong while processing your request."
    />
  ),
};

export const ErrorMessageWithTitle: StoryObj<typeof ErrorMessage> = {
  render: () => (
    <ErrorMessage
      title="Connection Error"
      message="Unable to connect to the server. Please try again later."
    />
  ),
};

export const WarningMessage: StoryObj<typeof ErrorMessage> = {
  render: () => (
    <ErrorMessage
      title="Warning"
      message="This action cannot be undone."
      variant="warning"
    />
  ),
};

// ErrorState Stories
export const DefaultErrorState: StoryObj<typeof ErrorState> = {
  render: () => (
    <ErrorState
      message="We encountered an error while processing your request."
    />
  ),
};

export const ErrorStateWithActions: StoryObj<typeof ErrorState> = {
  render: () => (
    <ErrorState
      title="Analysis Failed"
      message="Unable to complete the market analysis. Please try again."
      actions={{
        primary: {
          label: 'Retry Analysis',
          onClick: () => console.log('Retrying analysis...'),
        },
        secondary: {
          label: 'Cancel',
          onClick: () => console.log('Cancelling...'),
        },
      }}
    />
  ),
};

export const CustomErrorState: StoryObj<typeof ErrorState> = {
  render: () => (
    <ErrorState
      title="No Data Available"
      message="Unable to fetch market data for the selected time period."
      icon={<Icon name={HeroIcons.Status.InformationCircle} className="h-6 w-6 text-blue-600" />}
      actions={{
        primary: {
          label: 'Refresh Data',
          onClick: () => console.log('Refreshing data...'),
        },
      }}
    />
  ),
};

// ErrorBoundary Stories
const BuggyComponent = () => {
  throw new Error('This is a simulated error');
};

export const DefaultErrorBoundary: StoryObj<typeof ErrorBoundary> = {
  render: () => (
    <ErrorBoundary>
      <BuggyComponent />
    </ErrorBoundary>
  ),
};

export const ErrorBoundaryWithCustomFallback: StoryObj<typeof ErrorBoundary> = {
  render: () => (
    <ErrorBoundary
      fallback={
        <ErrorState
          title="Custom Error"
          message="This is a custom error message"
          actions={{
            primary: {
              label: 'Custom Action',
              onClick: () => console.log('Custom action clicked'),
            },
          }}
        />
      }
    >
      <BuggyComponent />
    </ErrorBoundary>
  ),
};
```

## src/stories/GameDetailsPage.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 1384 bytes
- Tokens: 328

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import GameDetailsPage from '@/app/game/[id]/page';
import { ThemeProvider } from '@/components/providers/ThemeProvider';

const meta = {
  title: 'Pages/GameDetails',
  component: GameDetailsPage,
  parameters: {
    layout: 'fullscreen',
    nextjs: {
      appDirectory: true,
      navigation: {
        params: {
          id: 'lakers-warriors',
        },
      },
    },
    backgrounds: {
      default: 'dark',
    },
  },
  decorators: [
    (Story) => (
      <ThemeProvider attribute="class" defaultTheme="dark" enableSystem={false}>
        <Story />
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof GameDetailsPage>;

export default meta;
type Story = StoryObj<typeof meta>;

// Default view with live game
export const Default: Story = {};

// With different bet types
export const WithParlay: Story = {
  parameters: {
    nextjs: {
      navigation: {
        searchParams: {
          type: 'parlay',
        },
      },
    },
  },
};

export const WithTeaser: Story = {
  parameters: {
    nextjs: {
      navigation: {
        searchParams: {
          type: 'teaser',
        },
      },
    },
  },
};

// With bet amount
export const WithBetAmount: Story = {
  parameters: {
    nextjs: {
      navigation: {
        searchParams: {
          amount: '100',
        },
      },
    },
  },
};
```

## src/stories/header.css
- Language: CSS
- Encoding: utf-8
- Size: 623 bytes
- Tokens: 196

```css
.storybook-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  padding: 15px 20px;
  font-family: 'Nunito Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

.storybook-header svg {
  display: inline-block;
  vertical-align: top;
}

.storybook-header h1 {
  display: inline-block;
  vertical-align: top;
  margin: 6px 0 6px 10px;
  font-weight: 700;
  font-size: 20px;
  line-height: 1;
}

.storybook-header button + button {
  margin-left: 10px;
}

.storybook-header .welcome {
  margin-right: 10px;
  color: #333;
  font-size: 14px;
}
```

## src/stories/Header.tsx
- Language: TSX
- Encoding: utf-8
- Size: 1525 bytes
- Tokens: 501

```tsx
import React from 'react';

import { Button } from './Button';
import './header.css';

type User = {
  name: string;
};

export interface HeaderProps {
  user?: User;
  onLogin?: () => void;
  onLogout?: () => void;
  onCreateAccount?: () => void;
}

export const Header = ({ user, onLogin, onLogout, onCreateAccount }: HeaderProps) => (
  <header>
    <div className="storybook-header">
      <div>
        <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
          <g fill="none" fillRule="evenodd">
            <path
              d="M10 0h12a10 10 0 0110 10v12a10 10 0 01-10 10H10A10 10 0 010 22V10A10 10 0 0110 0z"
              fill="#FFF"
            />
            <path
              d="M5.3 10.6l10.4 6v11.1l-10.4-6v-11zm11.4-6.2l9.7 5.5-9.7 5.6V4.4z"
              fill="#555AB9"
            />
            <path
              d="M27.2 10.6v11.2l-10.5 6V16.5l10.5-6zM15.7 4.4v11L6 10l9.7-5.5z"
              fill="#91BAF8"
            />
          </g>
        </svg>
        <h1>Acme</h1>
      </div>
      <div>
        {user ? (
          <>
            <span className="welcome">
              Welcome, <b>{user.name}</b>!
            </span>
            <Button size="small" onClick={onLogout} label="Log out" />
          </>
        ) : (
          <>
            <Button size="small" onClick={onLogin} label="Log in" />
            <Button primary size="small" onClick={onCreateAccount} label="Sign up" />
          </>
        )}
      </div>
    </div>
  </header>
);
```

## src/stories/Icon.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 4338 bytes
- Tokens: 1064

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Icon } from '@/components/controls/Icon';
import { ThemeProvider } from '@/components/providers/ThemeProvider';
import { HeroIcons, HeroIconName } from '@/lib/types';
import * as React from 'react';

const meta = {
  title: 'Controls/Icon',
  component: Icon,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  decorators: [
    (Story) => (
      <ThemeProvider attribute="class" defaultTheme="light" enableSystem={false}>
        <div className="p-4 bg-background">
          <Story />
        </div>
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof Icon>;

export default meta;
type Story = StoryObj<typeof meta>;

// Basic examples
export const Default: Story = {
  args: {
    name: HeroIcons.Navigation.ArrowRight,
    solid: false,
  },
};

export const Solid: Story = {
  args: {
    name: HeroIcons.Navigation.ArrowRight,
    solid: true,
  },
};

// Different sizes
export const Sizes: Story = {
  args: {
    name: HeroIcons.Navigation.ArrowRight,
  },
  render: (args) => (
    <div className="flex items-center gap-4">
      <Icon {...args} size="sm" />
      <Icon {...args} size="md" />
      <Icon {...args} size="lg" />
    </div>
  ),
};

// Different categories
export const Categories: Story = {
  args: {
    name: HeroIcons.UI.Bell,
  },
  render: () => (
    <div className="flex items-center gap-4">
      <Icon name={HeroIcons.UI.Bell} size="md" />
      <Icon name={HeroIcons.Status.InformationCircle} size="md" />
      <Icon name={HeroIcons.Actions.Plus} size="md" />
      <Icon name={HeroIcons.Commerce.CurrencyDollar} size="md" />
      <Icon name={HeroIcons.User.UserCircle} size="md" />
    </div>
  ),
};

// Dark mode example
export const DarkMode: Story = {
  args: {
    name: HeroIcons.Navigation.ArrowRight,
    solid: true,
  },
  parameters: {
    backgrounds: { default: 'dark' },
    themes: {
      themeOverride: 'dark',
    },
  },
};

// Custom styling
export const CustomStyling: Story = {
  args: {
    name: HeroIcons.Navigation.ArrowRight,
  },
  render: (args) => (
    <div className="flex items-center gap-4">
      <Icon {...args} className="text-primary hover:text-primary/80 transition-colors" />
      <Icon {...args} className="text-secondary hover:text-secondary/80 transition-colors" />
      <Icon {...args} className="text-accent hover:text-accent/80 transition-colors" />
    </div>
  ),
};

// Interactive example
export const Interactive: Story = {
  args: {
    name: HeroIcons.Navigation.ArrowRight,
    label: "Interactive Icon",
  },
  render: (args) => (
    <div className="flex items-center gap-4">
      <Icon {...args} className="cursor-pointer text-muted-foreground hover:text-primary transition-colors" />
    </div>
  ),
};

// All icons by category
export const AllIcons: Story = {
  args: {
    name: HeroIcons.Navigation.ArrowRight,
    size: "sm",
  },
  render: () => (
    <div className="space-y-8 w-full max-w-[1200px] p-6">
      {Object.entries(HeroIcons).map(([categoryName, icons]) => (
        <div key={categoryName}>
          <h2 className="text-xl font-bold mb-4 text-foreground">{categoryName}</h2>
          <div className="grid grid-cols-6 sm:grid-cols-8 md:grid-cols-10 lg:grid-cols-12 gap-4">
            {Object.entries(icons).map(([iconName, iconValue]) => {
              // Skip comments in the object (strings starting with //)
              if (typeof iconValue !== 'string' || !iconValue.endsWith('Icon')) {
                return null;
              }
              return (
                <div 
                  key={iconName} 
                  className="flex flex-col items-center space-y-1 p-2 rounded-lg hover:bg-accent/10 transition-colors"
                  title={iconName}
                >
                  <Icon 
                    name={iconValue as HeroIconName}
                    size="sm" 
                    className="text-foreground"
                  />
                  <span className="text-xs text-muted-foreground text-center whitespace-nowrap overflow-hidden text-ellipsis w-full">
                    {iconName}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  ),
  parameters: {
    layout: 'fullscreen',
  },
};
```

## src/stories/IconButton.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 1645 bytes
- Tokens: 421

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { IconButton } from '@/components/controls/IconButton';
import { ThemeProvider } from '@/components/providers/ThemeProvider';
import { HeroIcons } from '@/lib/types';

const meta = {
  title: 'Controls/IconButton',
  component: IconButton,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  decorators: [
    (Story) => (
      <ThemeProvider>
        <div className="p-4">
          <Story />
        </div>
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof IconButton>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    icon: HeroIcons.Navigation.ArrowRight,
    label: 'Navigate',
  },
};

export const Secondary: Story = {
  args: {
    icon: HeroIcons.UI.Cog6Tooth,
    label: 'Settings',
    variant: 'secondary',
  },
};

export const Small: Story = {
  args: {
    icon: HeroIcons.UI.Bell,
    label: 'Notifications',
    size: 'sm',
  },
};

export const Large: Story = {
  args: {
    icon: HeroIcons.Actions.Plus,
    label: 'Add Item',
    size: 'lg',
  },
};

export const Ghost: Story = {
  args: {
    icon: HeroIcons.UI.Bars3,
    label: 'Menu',
    variant: 'ghost',
  },
};

export const Success: Story = {
  args: {
    icon: HeroIcons.Status.Check,
    label: 'Success',
    variant: 'secondary',
  },
};

export const Info: Story = {
  args: {
    icon: HeroIcons.Status.InformationCircle,
    label: 'Information',
    variant: 'outline',
  },
};

export const Disabled: Story = {
  args: {
    icon: HeroIcons.User.LockClosed,
    label: 'Locked',
    disabled: true,
  },
};
```

## src/stories/Input.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 4589 bytes
- Tokens: 1168

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Input } from "@/components/controls/Input";
import { userEvent, within } from '@storybook/testing-library';
import { expect } from '@storybook/jest';

const meta = {
  title: "Controls/Input",
  component: Input,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof Input>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    placeholder: "Enter text",
  },
};

export const Numeric: Story = {
  args: {
    placeholder: "Numbers only",
    pattern: "numeric",
  },
};

export const Alphanumeric: Story = {
  args: {
    placeholder: "Letters and numbers",
    pattern: "alphanumeric",
  },
};

export const Alphabetical: Story = {
  args: {
    placeholder: "Letters only",
    pattern: "alphabetical",
  },
};

export const Date: Story = {
  args: {
    placeholder: "YYYY-MM-DD",
    pattern: "date",
  },
};

export const Time: Story = {
  args: {
    placeholder: "HH:MM",
    pattern: "time",
  },
};

export const DateTime: Story = {
  args: {
    placeholder: "YYYY-MM-DDTHH:MM",
    pattern: "datetime",
  },
};

export const Email: Story = {
  args: {
    placeholder: "email@example.com",
    pattern: "email",
  },
};

export const Phone: Story = {
  args: {
    placeholder: "(123) 456-7890",
    pattern: "phone",
  },
};

export const Currency: Story = {
  args: {
    placeholder: "$0.00",
    pattern: "currency",
  },
};

export const Percentage: Story = {
  args: {
    placeholder: "0%",
    pattern: "percentage",
  },
};

export const WithError: Story = {
  args: {
    placeholder: "Error state",
    variant: "error",
    error: "This field is required",
  },
};

export const WithSuccess: Story = {
  args: {
    placeholder: "Success state",
    variant: "success",
    success: "Valid input",
  },
};

export const Clearable: Story = {
  args: {
    placeholder: "Clearable input",
    clearable: true,
    value: "Clear me!",
  },
};

export const Disabled: Story = {
  args: {
    placeholder: "Disabled input",
    disabled: true,
  },
};

export const WithInteractions: Story = {
  args: {
    placeholder: "Type something...",
    pattern: "currency",
    clearable: true,
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    
    // Get the input
    const input = canvas.getByPlaceholderText("Type something...");
    
    // Type a value
    await userEvent.type(input, "123.45");
    expect(input).toHaveValue("$123.45");
    
    // Clear the input
    const clearButton = canvas.getByRole("button", { name: "Clear input" });
    await userEvent.click(clearButton);
    expect(input).toHaveValue("");
    
    // Type invalid characters (should be filtered out)
    await userEvent.type(input, "abc123.45");
    expect(input).toHaveValue("$123.45");
  },
};

export const AllPatterns = {
  render: () => (
    <div className="space-y-4 w-[300px]">
      <div>
        <label className="text-sm font-medium mb-1 block">Numeric</label>
        <Input pattern="numeric" placeholder="123" />
      </div>
      <div>
        <label className="text-sm font-medium mb-1 block">Alphanumeric</label>
        <Input pattern="alphanumeric" placeholder="abc123" />
      </div>
      <div>
        <label className="text-sm font-medium mb-1 block">Alphabetical</label>
        <Input pattern="alphabetical" placeholder="abc" />
      </div>
      <div>
        <label className="text-sm font-medium mb-1 block">Date</label>
        <Input pattern="date" placeholder="YYYY-MM-DD" />
      </div>
      <div>
        <label className="text-sm font-medium mb-1 block">Time</label>
        <Input pattern="time" placeholder="HH:MM" />
      </div>
      <div>
        <label className="text-sm font-medium mb-1 block">DateTime</label>
        <Input pattern="datetime" placeholder="YYYY-MM-DDTHH:MM" />
      </div>
      <div>
        <label className="text-sm font-medium mb-1 block">Email</label>
        <Input pattern="email" placeholder="email@example.com" />
      </div>
      <div>
        <label className="text-sm font-medium mb-1 block">Phone</label>
        <Input pattern="phone" placeholder="(123) 456-7890" />
      </div>
      <div>
        <label className="text-sm font-medium mb-1 block">Currency</label>
        <Input pattern="currency" placeholder="$0.00" />
      </div>
      <div>
        <label className="text-sm font-medium mb-1 block">Percentage</label>
        <Input pattern="percentage" placeholder="0%" />
      </div>
    </div>
  ),
};
```

## src/stories/Leaderboard.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2170 bytes
- Tokens: 629

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Leaderboard } from "@/components/controls/Leaderboard";
import { userEvent, within } from "@storybook/testing-library";
import { expect } from "@storybook/jest";

const meta = {
  title: "Controls/Leaderboard",
  component: Leaderboard,
  parameters: {
    layout: "padded",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof Leaderboard>;

export default meta;
type Story = StoryObj<typeof meta>;

const sampleEntries = [
  {
    id: "1",
    rank: 1,
    username: "BettingKing",
    winnings: 50000,
    winRate: 68,
    parlayStreak: 5,
    totalBets: 245,
  },
  {
    id: "2",
    rank: 2,
    username: "LuckyCharm",
    winnings: 35000,
    winRate: 62,
    parlayStreak: 3,
    totalBets: 178,
  },
  {
    id: "3",
    rank: 3,
    username: "SportsPro",
    winnings: 28000,
    winRate: 59,
    parlayStreak: 2,
    totalBets: 156,
  },
  {
    id: "4",
    rank: 4,
    username: "BetMaster",
    winnings: 22000,
    winRate: 55,
    parlayStreak: 1,
    totalBets: 134,
  },
  {
    id: "5",
    rank: 5,
    username: "OddsWizard",
    winnings: 18000,
    winRate: 52,
    parlayStreak: 0,
    totalBets: 112,
  },
];

export const Default: Story = {
  args: {
    entries: sampleEntries,
    timePeriod: "weekly",
    sportType: "all",
  },
};

export const EmptyState: Story = {
  args: {
    entries: [],
    timePeriod: "daily",
    sportType: "all",
  },
};

export const SingleSport: Story = {
  args: {
    entries: sampleEntries,
    timePeriod: "monthly",
    sportType: "NFL",
  },
};

export const WithInteractions: Story = {
  args: {
    entries: sampleEntries,
    timePeriod: "weekly",
    sportType: "all",
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Click the Monthly filter
    const monthlyButton = canvas.getByText("Monthly");
    await userEvent.click(monthlyButton);

    // Click the NBA filter
    const nbaButton = canvas.getByText("NBA");
    await userEvent.click(nbaButton);

    // Verify the table is still visible
    const table = canvas.getByRole("table");
    expect(table).toBeInTheDocument();
  },
};
```

## src/stories/LeaderboardPage.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 1490 bytes
- Tokens: 341

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import LeaderboardPage from "@/app/leaderboard/page";
import { ThemeProvider } from "@/components/providers/ThemeProvider";
import { userEvent, within } from "@storybook/testing-library";
import { expect } from "@storybook/jest";

const meta = {
  title: "Pages/LeaderboardPage",
  component: LeaderboardPage,
  parameters: {
    layout: "fullscreen",
  },
  tags: ["autodocs"],
  decorators: [
    (Story) => (
      <ThemeProvider attribute="class" defaultTheme="light" enableSystem={false}>
        <Story />
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof LeaderboardPage>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
};

export const DarkMode: Story = {
  args: {},
  parameters: {
    themes: {
      themeOverride: 'dark',
    },
  },
};

export const WithInteractions: Story = {
  args: {},
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Wait for the page to load
    await expect(canvas.getByText("Leaderboard")).toBeInTheDocument();

    // Click the Monthly filter
    const monthlyButton = canvas.getByText("Monthly");
    await userEvent.click(monthlyButton);

    // Click the NBA filter
    const nbaButton = canvas.getByText("NBA");
    await userEvent.click(nbaButton);

    // Verify the table is still visible
    const table = canvas.getByRole("table");
    expect(table).toBeInTheDocument();
  },
};
```

## src/stories/LiveScoreCard.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2209 bytes
- Tokens: 607

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { LiveScoreCard } from "@/components/controls/LiveScoreCard";

const meta = {
  title: "Controls/LiveScoreCard",
  component: LiveScoreCard,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof LiveScoreCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const NFLLiveGame: Story = {
  args: {
    teams: [
      {
        name: "Kansas City Chiefs",
        score: 24,
        isHome: false,
      },
      {
        name: "San Francisco 49ers",
        score: 21,
        isHome: true,
      },
    ],
    gameStatus: "Live",
    sportType: "NFL",
    keyStats: {
      timeRemaining: "4:32",
      period: "4",
      periodType: "quarter",
      possession: "home",
      lastPlay: "J. Garoppolo pass complete to D. Samuel for 18 yards",
    },
  },
};

export const NBALiveGame: Story = {
  args: {
    teams: [
      {
        name: "Los Angeles Lakers",
        score: 89,
        isHome: false,
      },
      {
        name: "Golden State Warriors",
        score: 92,
        isHome: true,
      },
    ],
    gameStatus: "Live",
    sportType: "NBA",
    keyStats: {
      timeRemaining: "8:45",
      period: "3",
      periodType: "quarter",
      possession: "away",
      lastPlay: "L. James layup made (K. Nunn assist)",
    },
  },
};

export const Halftime: Story = {
  args: {
    teams: [
      {
        name: "Boston Celtics",
        score: 58,
        isHome: false,
      },
      {
        name: "Miami Heat",
        score: 52,
        isHome: true,
      },
    ],
    gameStatus: "Halftime",
    sportType: "NBA",
    keyStats: {
      timeRemaining: "15:00",
      period: "2",
      periodType: "half",
    },
  },
};

export const FinalScore: Story = {
  args: {
    teams: [
      {
        name: "Buffalo Bills",
        score: 35,
        isHome: false,
      },
      {
        name: "New England Patriots",
        score: 28,
        isHome: true,
      },
    ],
    gameStatus: "Final",
    sportType: "NFL",
    keyStats: {
      timeRemaining: "0:00",
      period: "4",
      periodType: "quarter",
      lastPlay: "End of game",
    },
  },
};
```

## src/stories/OddsDisplay.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2880 bytes
- Tokens: 754

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { OddsDisplay } from "@/components/controls/OddsDisplay";
import { useEffect, useState } from "react";

const meta = {
  title: "Controls/OddsDisplay",
  component: OddsDisplay,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof OddsDisplay>;

export default meta;
type Story = StoryObj<typeof meta>;

export const DecimalOdds: Story = {
  args: {
    value: 2.5,
    format: "decimal",
  },
};

export const FractionalOdds: Story = {
  args: {
    value: 2.5,
    format: "fractional",
  },
};

export const AmericanOddsPositive: Story = {
  args: {
    value: 2.5,
    format: "american",
  },
};

export const AmericanOddsNegative: Story = {
  args: {
    value: 1.5,
    format: "american",
  },
};

export const EvenOdds: Story = {
  args: {
    value: 1,
    format: "american",
  },
};

export const WithOddsIncrease: Story = {
  args: {
    value: 2.75,
    previousValue: 2.5,
    format: "decimal",
  },
};

export const WithOddsDecrease: Story = {
  args: {
    value: 2.25,
    previousValue: 2.5,
    format: "decimal",
  },
};

export const LiveOddsUpdate = {
  render: function Story() {
    const [currentValue, setCurrentValue] = useState(2.5);
    const [previousValue, setPreviousValue] = useState<number | undefined>();

    useEffect(() => {
      const interval = setInterval(() => {
        setPreviousValue(currentValue);
        // Random value between 2.0 and 3.0
        setCurrentValue(2 + Math.random());
      }, 3000);

      return () => clearInterval(interval);
    }, [currentValue]);

    return (
      <div className="space-y-4">
        <div className="flex gap-4 items-center">
          <OddsDisplay value={currentValue} previousValue={previousValue} format="decimal" />
          <OddsDisplay value={currentValue} previousValue={previousValue} format="fractional" />
          <OddsDisplay value={currentValue} previousValue={previousValue} format="american" />
        </div>
        <p className="text-sm text-muted-foreground">
          Odds update every 3 seconds with random values
        </p>
      </div>
    );
  },
};

export const AllFormats = {
  args: {
    value: 2.5,
  },
  render: function Story(args: { value: number }) {
    return (
      <div className="flex flex-col gap-4">
        <div className="flex gap-4 items-center">
          <span className="w-24">Decimal:</span>
          <OddsDisplay {...args} format="decimal" />
        </div>
        <div className="flex gap-4 items-center">
          <span className="w-24">Fractional:</span>
          <OddsDisplay {...args} format="fractional" />
        </div>
        <div className="flex gap-4 items-center">
          <span className="w-24">American:</span>
          <OddsDisplay {...args} format="american" />
        </div>
      </div>
    );
  },
};
```

## src/stories/OddsList.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 3507 bytes
- Tokens: 1091

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { OddsList } from "@/components/templates/OddsList";
import { Game } from "@/components/templates/OddsList";
import { ThemeProvider } from "@/components/providers/ThemeProvider";

const meta = {
  title: "Templates/OddsList",
  component: OddsList,
  parameters: {
    layout: "padded",
  },
  tags: ["autodocs"],
  decorators: [
    (Story, context) => {
      const theme = context.parameters.themes?.themeOverride || 'light';
      return (
        <ThemeProvider attribute="class" defaultTheme={theme} enableSystem={false}>
          <div className={theme === 'dark' ? 'dark' : ''}>
            <div className="min-h-screen bg-background p-6">
              <Story />
            </div>
          </div>
        </ThemeProvider>
      );
    },
  ],
} satisfies Meta<typeof OddsList>;

export default meta;
type Story = StoryObj<typeof meta>;

const sampleGames: Game[] = [
  {
    id: "1",
    homeTeam: {
      name: "Kansas City Chiefs",
      isHome: true,
    },
    awayTeam: {
      name: "San Francisco 49ers",
      isHome: false,
    },
    homeOdds: 1.95,
    awayOdds: 1.85,
    startTime: "2024-02-11T23:30:00Z",
    sport: "NFL",
    status: {
      type: "upcoming",
      startTime: "2024-02-11T23:30:00Z"
    }
  },
  {
    id: "2",
    homeTeam: {
      name: "Green Bay Packers",
      isHome: true,
    },
    awayTeam: {
      name: "Detroit Lions",
      isHome: false,
    },
    homeOdds: 2.10,
    awayOdds: 1.75,
    startTime: "2024-02-11T20:00:00Z",
    sport: "NFL",
    status: {
      type: "upcoming",
      startTime: "2024-02-11T20:00:00Z"
    }
  },
  {
    id: "3",
    homeTeam: {
      name: "Los Angeles Lakers",
      isHome: true,
    },
    awayTeam: {
      name: "Golden State Warriors",
      isHome: false,
    },
    homeOdds: 1.90,
    awayOdds: 1.90,
    startTime: "2024-02-11T03:00:00Z",
    sport: "NBA",
    status: {
      type: "live",
      period: "Q3",
      timeRemaining: "8:45",
      possession: "home"
    }
  },
  {
    id: "4",
    homeTeam: {
      name: "Boston Celtics",
      isHome: true,
    },
    awayTeam: {
      name: "Miami Heat",
      isHome: false,
    },
    homeOdds: 1.65,
    awayOdds: 2.25,
    startTime: "2024-02-11T00:00:00Z",
    sport: "NBA",
    status: {
      type: "halftime",
      detail: "15:00 until Q3"
    }
  },
  {
    id: "5",
    homeTeam: {
      name: "New York Yankees",
      isHome: true,
    },
    awayTeam: {
      name: "Boston Red Sox",
      isHome: false,
    },
    homeOdds: 1.80,
    awayOdds: 2.00,
    startTime: "2024-02-11T17:00:00Z",
    sport: "MLB",
    status: {
      type: "upcoming",
      startTime: "2024-02-11T17:00:00Z"
    }
  },
  {
    id: "6",
    homeTeam: {
      name: "Toronto Maple Leafs",
      isHome: true,
    },
    awayTeam: {
      name: "Montreal Canadiens",
      isHome: false,
    },
    homeOdds: 1.75,
    awayOdds: 2.15,
    startTime: "2024-02-11T23:00:00Z",
    sport: "NHL",
    status: {
      type: "upcoming",
      startTime: "2024-02-11T23:00:00Z"
    }
  },
];

export const Default: Story = {
  args: {
    games: sampleGames,
  },
};

export const WithDarkMode: Story = {
  args: {
    games: sampleGames,
  },
  parameters: {
    themes: {
      themeOverride: 'dark',
    },
  },
};

export const EmptyState: Story = {
  args: {
    games: [],
  },
};

export const SingleSport: Story = {
  args: {
    games: sampleGames.filter((game) => game.sport === "NFL"),
  },
};
```

## src/stories/page.css
- Language: CSS
- Encoding: utf-8
- Size: 1125 bytes
- Tokens: 384

```css
.storybook-page {
  margin: 0 auto;
  padding: 48px 20px;
  max-width: 600px;
  color: #333;
  font-size: 14px;
  line-height: 24px;
  font-family: 'Nunito Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

.storybook-page h2 {
  display: inline-block;
  vertical-align: top;
  margin: 0 0 4px;
  font-weight: 700;
  font-size: 32px;
  line-height: 1;
}

.storybook-page p {
  margin: 1em 0;
}

.storybook-page a {
  color: inherit;
}

.storybook-page ul {
  margin: 1em 0;
  padding-left: 30px;
}

.storybook-page li {
  margin-bottom: 8px;
}

.storybook-page .tip {
  display: inline-block;
  vertical-align: top;
  margin-right: 10px;
  border-radius: 1em;
  background: #e7fdd8;
  padding: 4px 12px;
  color: #357a14;
  font-weight: 700;
  font-size: 11px;
  line-height: 12px;
}

.storybook-page .tip-wrapper {
  margin-top: 40px;
  margin-bottom: 40px;
  font-size: 13px;
  line-height: 20px;
}

.storybook-page .tip-wrapper svg {
  display: inline-block;
  vertical-align: top;
  margin-top: 3px;
  margin-right: 4px;
  width: 12px;
  height: 12px;
}

.storybook-page .tip-wrapper svg path {
  fill: #1ea7fd;
}
```

## src/stories/Page.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2592 bytes
- Tokens: 745

```tsx
import React from 'react';

import { Header } from './Header';
import './page.css';

type User = {
  name: string;
};

export const Page: React.FC = () => {
  const [user, setUser] = React.useState<User>();

  return (
    <article>
      <Header
        user={user}
        onLogin={() => setUser({ name: 'Jane Doe' })}
        onLogout={() => setUser(undefined)}
        onCreateAccount={() => setUser({ name: 'Jane Doe' })}
      />

      <section className="storybook-page">
        <h2>Pages in Storybook</h2>
        <p>
          We recommend building UIs with a{' '}
          <a href="https://componentdriven.org" target="_blank" rel="noopener noreferrer">
            <strong>component-driven</strong>
          </a>{' '}
          process starting with atomic components and ending with pages.
        </p>
        <p>
          Render pages with mock data. This makes it easy to build and review page states without
          needing to navigate to them in your app. Here are some handy patterns for managing page data
          in Storybook:
        </p>
        <ul>
          <li>
            Use a higher-level connected component. Storybook helps you compose such data from the
            &ldquo;args&rdquo; of child component stories
          </li>
          <li>
            Assemble data in the page component from your services. You can mock these services out
            using Storybook.
          </li>
        </ul>
        <p>
          Get a guided tutorial on component-driven development at{' '}
          <a href="https://storybook.js.org/tutorials/" target="_blank" rel="noopener noreferrer">
            Storybook tutorials
          </a>
          . Read more in the{' '}
          <a href="https://storybook.js.org/docs" target="_blank" rel="noopener noreferrer">
            docs
          </a>
          .
        </p>
        <div className="tip-wrapper">
          <span className="tip">Tip</span> Adjust the width of the canvas with the{' '}
          <svg width="10" height="10" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg">
            <g fill="none" fillRule="evenodd">
              <path
                d="M1.5 5.2h4.8c.3 0 .5.2.5.4v5.1c-.1.2-.3.3-.4.3H1.4a.5.5 0 01-.5-.4V5.7c0-.3.2-.5.5-.5zm0-2.1h6.9c.3 0 .5.2.5.4v7a.5.5 0 01-1 0V4H1.5a.5.5 0 010-1zm0-2.1h9c.3 0 .5.2.5.4v9.1a.5.5 0 01-1 0V2H1.5a.5.5 0 010-1zm4.3 5.2H2V10h3.8V6.2z"
                id="a"
                fill="#999"
              />
            </g>
          </svg>
          Viewports addon in the toolbar
        </div>
      </section>
    </article>
  );
};
```

## src/stories/ParlayBetDisplay.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 6134 bytes
- Tokens: 1586

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { ParlayBetDisplay } from "@/components/controls/ParlayBetDisplay";
import { userEvent, within } from '@storybook/testing-library';
import { expect } from '@storybook/jest';
import { ThemeProvider } from "@/components/providers/ThemeProvider";

const meta = {
  title: "Controls/ParlayBetDisplay",
  component: ParlayBetDisplay,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  decorators: [
    (Story) => (
      <ThemeProvider attribute="class" defaultTheme="light" enableSystem={false}>
        <div className="w-[800px] p-4 bg-background">
          <Story />
        </div>
      </ThemeProvider>
    ),
  ],
  argTypes: {
    onRemoveGame: { action: "removeGame" },
    onPlaceBet: { action: "placeBet" },
    onReorder: { action: "reorder" },
    onAddSuggestedGame: { action: "addSuggestedGame" },
  },
} satisfies Meta<typeof ParlayBetDisplay>;

export default meta;
type Story = StoryObj<typeof meta>;

const sampleGames = [
  {
    homeTeam: {
      name: "Los Angeles Lakers",
      isHome: true,
      score: 105,
    },
    awayTeam: {
      name: "Golden State Warriors",
      isHome: false,
      score: 98,
    },
    homeOdds: 1.85,
    awayOdds: 2.1,
    status: {
      type: "live" as const,
      period: "Q4",
      timeRemaining: "2:30",
      possession: "home" as const,
    },
    selectedTeam: {
      name: "Los Angeles Lakers",
      isHome: true,
    },
  },
  {
    homeTeam: {
      name: "Boston Celtics",
      isHome: true,
    },
    awayTeam: {
      name: "Miami Heat",
      isHome: false,
    },
    homeOdds: 1.65,
    awayOdds: 2.35,
    status: {
      type: "upcoming" as const,
      startTime: "Today, 8:00 PM",
    },
    selectedTeam: {
      name: "Miami Heat",
      isHome: false,
    },
  },
];

const suggestedGames = [
  {
    homeTeam: {
      name: "Brooklyn Nets",
      isHome: true,
    },
    awayTeam: {
      name: "Philadelphia 76ers",
      isHome: false,
    },
    homeOdds: 2.0,
    awayOdds: 1.9,
    status: {
      type: "upcoming" as const,
      startTime: "Today, 9:00 PM",
    },
  },
];

export const Default: Story = {
  args: {
    bettingCards: sampleGames,
    onRemoveGame: (index: number) => console.log('Remove game at index:', index),
    onPlaceBet: (amount: number) => console.log('Place bet with amount:', amount),
  },
};

export const WithAmericanOdds: Story = {
  args: {
    bettingCards: sampleGames,
    oddsFormat: "american",
    onRemoveGame: (index: number) => console.log('Remove game at index:', index),
    onPlaceBet: (amount: number) => console.log('Place bet with amount:', amount),
  },
};

export const WithFractionalOdds: Story = {
  args: {
    bettingCards: sampleGames,
    oddsFormat: "fractional",
    onRemoveGame: (index: number) => console.log('Remove game at index:', index),
    onPlaceBet: (amount: number) => console.log('Place bet with amount:', amount),
  },
};

export const SingleGame: Story = {
  args: {
    bettingCards: [sampleGames[0]],
    onRemoveGame: (index: number) => console.log('Remove game at index:', index),
    onPlaceBet: (amount: number) => console.log('Place bet with amount:', amount),
  },
};

export const ThreeGames: Story = {
  args: {
    bettingCards: [
      ...sampleGames,
      {
        homeTeam: {
          name: "Brooklyn Nets",
          isHome: true,
        },
        awayTeam: {
          name: "Philadelphia 76ers",
          isHome: false,
        },
        homeOdds: 2.0,
        awayOdds: 1.9,
        status: {
          type: "upcoming" as const,
          startTime: "Today, 9:00 PM",
        },
        selectedTeam: {
          name: "Brooklyn Nets",
          isHome: true,
        },
      },
    ],
    onRemoveGame: (index: number) => console.log('Remove game at index:', index),
    onPlaceBet: (amount: number) => console.log('Place bet with amount:', amount),
  },
};

export const WithSuggestions: Story = {
  args: {
    bettingCards: sampleGames,
    suggestedGames,
    onRemoveGame: (index: number) => console.log('Remove game at index:', index),
    onPlaceBet: (amount: number) => console.log('Place bet with amount:', amount),
    onAddSuggestedGame: (game) => console.log('Add suggested game:', game),
  },
};

export const WithDragAndDrop: Story = {
  args: {
    bettingCards: sampleGames,
    onRemoveGame: (index: number) => console.log('Remove game at index:', index),
    onPlaceBet: (amount: number) => console.log('Place bet with amount:', amount),
    onReorder: (startIndex: number, endIndex: number) => 
      console.log('Reorder from', startIndex, 'to', endIndex),
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    
    // Wait for the component to load
    await new Promise((resolve) => setTimeout(resolve, 500));
    
    // Find the draggable elements
    const firstGame = canvas.getByText("Los Angeles Lakers").closest('[draggable="true"]');
    const secondGame = canvas.getByText("Boston Celtics").closest('[draggable="true"]');
    
    if (firstGame && secondGame) {
      // Simulate drag and drop
      const dragStartEvent = new MouseEvent('dragstart', { bubbles: true });
      const dropEvent = new MouseEvent('drop', { bubbles: true });
      
      firstGame.dispatchEvent(dragStartEvent);
      secondGame.dispatchEvent(dropEvent);
    }
  },
};

export const WithPayoutCalculations: Story = {
  args: {
    bettingCards: sampleGames,
    onRemoveGame: (index: number) => console.log('Remove game at index:', index),
    onPlaceBet: (amount: number) => console.log('Place bet with amount:', amount),
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    
    // Enter bet amount
    const input = canvas.getByPlaceholderText("Enter bet amount");
    await userEvent.type(input, "100");
    
    // Verify payout information is displayed
    expect(canvas.getByText("Payout Ratio:")).toBeInTheDocument();
    expect(canvas.getByText("Implied Probability:")).toBeInTheDocument();
    expect(canvas.getByText("Break Even %:")).toBeInTheDocument();
  },
};
```

## src/stories/ParlayBetPage.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2494 bytes
- Tokens: 584

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import ParlayBetPage from "@/app/parlay/page";
import { ThemeProvider } from "@/components/providers/ThemeProvider";
import { within, userEvent, waitFor } from "@storybook/testing-library";
import { expect } from "@storybook/jest";

const meta = {
  title: "Pages/ParlayBet",
  component: ParlayBetPage,
  parameters: {
    layout: "fullscreen",
    nextjs: {
      appDirectory: true,
    },
    backgrounds: {
      default: 'dark',
    },
  },
  tags: ["autodocs"],
  decorators: [
    (Story) => (
      <ThemeProvider attribute="class" defaultTheme="dark" enableSystem={false}>
        <Story />
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof ParlayBetPage>;

export default meta;
type Story = StoryObj<typeof meta>;

// Default view
export const Default: Story = {};

// With selected markets
export const WithSelectedMarkets: Story = {
  parameters: {
    nextjs: {
      navigation: {
        searchParams: {
          markets: 'lakers-warriors,chiefs-49ers',
        },
      },
    },
  },
};

// Filtered by sport
export const FilteredBySport: Story = {
  parameters: {
    nextjs: {
      navigation: {
        searchParams: {
          sport: 'NBA',
        },
      },
    },
  },
};

// With search query
export const WithSearch: Story = {
  parameters: {
    nextjs: {
      navigation: {
        searchParams: {
          search: 'Lakers',
        },
      },
    },
  },
};

export const WithInteractions: Story = {
  args: {},
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    
    // Wait for the page to load
    await waitFor(() => {
      expect(canvas.getByText("Create Parlay Bet")).toBeInTheDocument();
    });

    // Select first game (home team)
    const firstGameBetButton = canvas.getAllByText("Kansas City Chiefs")[0];
    await userEvent.click(firstGameBetButton);

    // Select second game (away team)
    const secondGameBetButton = canvas.getAllByText("Golden State Warriors")[0];
    await userEvent.click(secondGameBetButton);

    // Verify parlay bet form appears
    await waitFor(() => {
      expect(canvas.getByText("Parlay Bet")).toBeInTheDocument();
    });

    // Enter bet amount
    const betAmountInput = canvas.getByPlaceholderText("Enter bet amount");
    await userEvent.type(betAmountInput, "100");

    // Place bet
    const placeBetButton = canvas.getByText("Place Parlay Bet");
    await userEvent.click(placeBetButton);
  },
};
```

## src/stories/PromotionCard.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 1689 bytes
- Tokens: 463

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { PromotionCard } from "@/components/controls/PromotionCard";

const meta = {
  title: "Controls/PromotionCard",
  component: PromotionCard,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof PromotionCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const DepositBonus: Story = {
  args: {
    title: "Welcome Bonus",
    description: "Get a 100% match on your first deposit up to $500",
    type: "bonus",
    value: "$500",
    expiresAt: "2024-12-31",
    terms: "Minimum deposit $20. Wagering requirements apply.",
  },
};

export const ParlayBoost: Story = {
  args: {
    title: "Parlay Power Boost",
    description: "Get 3x odds on your next parlay bet with 5+ selections",
    type: "parlay",
    value: "3x",
    expiresAt: "2024-03-31",
    terms: "Minimum odds 1.20 per selection. Maximum stake $100.",
  },
};

export const FreeBet: Story = {
  args: {
    title: "Risk-Free First Bet",
    description: "Place your first bet with confidence - get up to $50 back if you lose",
    type: "free-bet",
    value: "$50",
    expiresAt: "2024-06-30",
    terms: "Valid for first bet only. Refund as betting credit.",
  },
};

export const NoExpiry: Story = {
  args: {
    title: "VIP Rewards",
    description: "Exclusive rewards for our VIP members",
    type: "bonus",
    value: "10%",
    terms: "Available for Gold tier members and above.",
  },
};

export const NoTerms: Story = {
  args: {
    title: "Quick Bonus",
    description: "Instant $10 bonus on your next bet",
    type: "bonus",
    value: "$10",
    expiresAt: "2024-04-15",
  },
};
```

## src/stories/Promotions.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2670 bytes
- Tokens: 708

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Promotions } from "@/components/controls/Promotions";
import { userEvent, within } from "@storybook/testing-library";
import { expect } from "@storybook/jest";

const meta = {
  title: "Controls/Promotions",
  component: Promotions,
  parameters: {
    layout: "padded",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof Promotions>;

export default meta;
type Story = StoryObj<typeof meta>;

const samplePromotions = [
  {
    id: "1",
    title: "Welcome Bonus",
    description: "Get a 100% match on your first deposit up to $500",
    type: "bonus" as const,
    value: "$500",
    expiresAt: "2024-12-31",
    terms: "Minimum deposit $20. Wagering requirements apply.",
  },
  {
    id: "2",
    title: "Parlay Power Boost",
    description: "Get 3x odds on your next parlay bet with 5+ selections",
    type: "parlay" as const,
    value: "3x",
    expiresAt: "2024-03-31",
    terms: "Minimum odds 1.20 per selection. Maximum stake $100.",
  },
  {
    id: "3",
    title: "Risk-Free First Bet",
    description: "Place your first bet with confidence - get up to $50 back if you lose",
    type: "free-bet" as const,
    value: "$50",
    expiresAt: "2024-06-30",
    terms: "Valid for first bet only. Refund as betting credit.",
  },
  {
    id: "4",
    title: "VIP Rewards",
    description: "Exclusive rewards for our VIP members",
    type: "bonus" as const,
    value: "10%",
    terms: "Available for Gold tier members and above.",
  },
  {
    id: "5",
    title: "March Madness Boost",
    description: "Get enhanced odds on all college basketball parlay bets",
    type: "parlay" as const,
    value: "2x",
    expiresAt: "2024-04-08",
    terms: "Valid for college basketball games only.",
  },
];

export const Default: Story = {
  args: {
    promotions: samplePromotions,
  },
};

export const EmptyState: Story = {
  args: {
    promotions: [],
  },
};

export const SingleType: Story = {
  args: {
    promotions: samplePromotions.filter(p => p.type === "bonus"),
  },
};

export const WithInteractions: Story = {
  args: {
    promotions: samplePromotions,
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Click the Parlay Boosts filter
    const parlayButton = canvas.getByText("Parlay Boosts");
    await userEvent.click(parlayButton);

    // Verify only parlay promotions are shown
    const parlayCards = canvas.getAllByText(/Parlay/);
    expect(parlayCards.length).toBeGreaterThan(0);

    // Click a claim button
    const claimButtons = canvas.getAllByText("Claim Offer");
    await userEvent.click(claimButtons[0]);
  },
};
```

## src/stories/PromotionsPage.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 1350 bytes
- Tokens: 316

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import PromotionsPage from "@/app/promotions/page";
import { ThemeProvider } from "@/components/providers/ThemeProvider";

const meta = {
  title: "Pages/Promotions",
  component: PromotionsPage,
  parameters: {
    layout: "fullscreen",
    nextjs: {
      appDirectory: true,
    },
    backgrounds: {
      default: "dark",
    },
  },
  tags: ["autodocs"],
  decorators: [
    (Story) => (
      <ThemeProvider attribute="class" defaultTheme="dark" enableSystem={false}>
        <Story />
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof PromotionsPage>;

export default meta;
type Story = StoryObj<typeof meta>;

// Default view
export const Default: Story = {};

// With activated features
export const WithActivatedFeatures: Story = {
  parameters: {
    nextjs: {
      navigation: {
        searchParams: {
          activated: "ai-analysis,market-alerts",
        },
      },
    },
  },
};

// Filtered by tier
export const FilteredByTier: Story = {
  parameters: {
    nextjs: {
      navigation: {
        searchParams: {
          tier: "premium",
        },
      },
    },
  },
};

// Loading state
export const Loading: Story = {
  parameters: {
    nextjs: {
      navigation: {
        searchParams: {
          loading: "true",
        },
      },
    },
  },
};
```

## src/stories/Select.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 6404 bytes
- Tokens: 1542

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Select } from "@/components/controls/Select";
import { userEvent, within } from '@storybook/testing-library';
import { expect } from '@storybook/jest';
import { ThemeProvider } from "@/components/providers/ThemeProvider";

const meta = {
  title: "Controls/Select",
  component: Select,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  decorators: [
    (Story) => (
      <ThemeProvider attribute="class" defaultTheme="light" enableSystem={false}>
        <div className="p-4 bg-background">
          <Story />
        </div>
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof Select>;

export default meta;
type Story = StoryObj<typeof meta>;

const sampleOptions = [
  { value: "1", label: "Option 1" },
  { value: "2", label: "Option 2" },
  { value: "3", label: "Option 3" },
  { value: "4", label: "Option 4" },
  { value: "5", label: "Option 5" },
];

const sampleGroups = [
  {
    label: "Group 1",
    options: [
      { value: "1.1", label: "Option 1.1" },
      { value: "1.2", label: "Option 1.2" },
      { value: "1.3", label: "Option 1.3" },
    ],
  },
  {
    label: "Group 2",
    options: [
      { value: "2.1", label: "Option 2.1" },
      { value: "2.2", label: "Option 2.2" },
      { value: "2.3", label: "Option 2.3" },
    ],
  },
];

export const Default: Story = {
  args: {
    options: sampleOptions,
    placeholder: "Select an option",
  },
};

export const DarkMode: Story = {
  args: {
    options: sampleOptions,
    placeholder: "Select an option",
  },
  parameters: {
    backgrounds: { default: 'dark' },
    themes: {
      themeOverride: 'dark',
    },
  },
};

export const WithGroups: Story = {
  args: {
    options: sampleGroups,
    placeholder: "Select a grouped option",
  },
};

export const MultiSelectBasic: Story = {
  args: {
    options: sampleOptions,
    multiple: true,
    placeholder: "Select multiple options",
  },
};

export const MultiSelectWithGroups: Story = {
  args: {
    options: sampleGroups,
    multiple: true,
    placeholder: "Select multiple grouped options",
  },
};

export const MultiSelectWithLimit: Story = {
  args: {
    options: sampleOptions,
    multiple: true,
    maxSelections: 2,
    placeholder: "Select up to 2 options",
  },
};

export const MultiSelectInteractive: Story = {
  args: {
    options: sampleOptions,
    multiple: true,
    maxSelections: 3,
    placeholder: "Select up to 3 options",
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    
    // Get the select element
    const select = canvas.getByRole("listbox") as HTMLSelectElement;
    
    // Select multiple options
    await userEvent.selectOptions(select, ["1", "2", "3"]);
    
    // Verify multiple selections
    const selectedOptions = Array.from(select.selectedOptions).map(opt => opt.value);
    expect(selectedOptions).toEqual(["1", "2", "3"]);
    
    // Try to select more than max (should not work)
    await userEvent.selectOptions(select, ["4"]);
    expect(selectedOptions.length).toBe(3);
  },
};

export const SelectFeatures = {
  render: () => (
    <div className="space-y-8">
      <div className="space-y-4">
        <h3 className="text-lg font-medium">Single Select</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium mb-1 block">Basic Select</label>
            <Select options={sampleOptions} placeholder="Choose one option" />
          </div>
          <div>
            <label className="text-sm font-medium mb-1 block">With Groups</label>
            <Select options={sampleGroups} placeholder="Choose from groups" />
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-medium">Multi Select</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium mb-1 block">Basic Multi-select</label>
            <Select
              options={sampleOptions}
              multiple
              placeholder="Choose multiple options"
            />
          </div>
          <div>
            <label className="text-sm font-medium mb-1 block">With Selection Limit</label>
            <Select
              options={sampleOptions}
              multiple
              maxSelections={2}
              placeholder="Choose up to 2 options"
            />
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-medium">Grouped Multi-select</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium mb-1 block">Basic Grouped</label>
            <Select
              options={sampleGroups}
              multiple
              placeholder="Choose from groups"
            />
          </div>
          <div>
            <label className="text-sm font-medium mb-1 block">With Selection Limit</label>
            <Select
              options={sampleGroups}
              multiple
              maxSelections={3}
              placeholder="Choose up to 3 options"
            />
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-medium">States</h3>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="text-sm font-medium mb-1 block">With Error</label>
            <Select
              options={sampleOptions}
              multiple
              variant="error"
              error="Please select at least one option"
              placeholder="Error state"
            />
          </div>
          <div>
            <label className="text-sm font-medium mb-1 block">With Success</label>
            <Select
              options={sampleOptions}
              multiple
              variant="success"
              success="Valid selection"
              placeholder="Success state"
              value={["1", "2"]}
            />
          </div>
          <div>
            <label className="text-sm font-medium mb-1 block">Disabled</label>
            <Select
              options={sampleOptions}
              multiple
              disabled
              placeholder="Disabled state"
            />
          </div>
        </div>
      </div>
    </div>
  ),
};
```

## src/stories/Settings.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 2037 bytes
- Tokens: 465

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Settings } from "@/components/controls/Settings";
import { ThemeProvider } from "@/components/providers/ThemeProvider";
import { userEvent, within } from "@storybook/testing-library";
import { expect } from "@storybook/jest";

const meta = {
  title: "Controls/Settings",
  component: Settings,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  decorators: [
    (Story) => (
      <ThemeProvider>
        <div className="p-4">
          <Story />
        </div>
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof Settings>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
};

export const DarkMode: Story = {
  args: {},
  parameters: {
    backgrounds: { default: 'dark' },
    themes: {
      themeOverride: 'dark',
    },
  },
};

export const WithInteractions: Story = {
  args: {},
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Click the settings button
    const settingsButton = canvas.getByRole("button", { name: /open settings/i });
    await userEvent.click(settingsButton);

    // Verify the menu is open
    const signInButton = canvas.getByRole("button", { name: /sign in/i });
    expect(signInButton).toBeInTheDocument();

    // Verify navigation links are present
    expect(canvas.getByRole("link", { name: /betting/i })).toBeInTheDocument();
    expect(canvas.getByRole("link", { name: /parlay bets/i })).toBeInTheDocument();
    expect(canvas.getByRole("link", { name: /promotions/i })).toBeInTheDocument();
    expect(canvas.getByRole("link", { name: /leaderboard/i })).toBeInTheDocument();

    // Click the theme toggle
    const themeToggle = canvas.getByRole("button", { name: /toggle theme/i });
    await userEvent.click(themeToggle);

    // Click outside to close
    await userEvent.click(canvas.getByTestId("backdrop"));

    // Verify the menu is closed
    expect(signInButton).not.toBeInTheDocument();
  },
};
```

## src/stories/StatsCard.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 970 bytes
- Tokens: 283

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { StatsCard } from "@/components/controls/StatsCard";

const meta = {
  title: "Controls/StatsCard",
  component: StatsCard,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof StatsCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Money: Story = {
  args: {
    title: "Available Balance",
    value: 1234.56,
    type: "money",
  },
};

export const MoneyWithTrend: Story = {
  args: {
    title: "Total Won",
    value: 1234.56,
    type: "money",
    trend: 12.5,
  },
};

export const Percentage: Story = {
  args: {
    title: "Win Rate",
    value: 65,
    type: "percentage",
  },
};

export const Count: Story = {
  args: {
    title: "Pending Bets",
    value: 5,
    type: "count",
  },
};

export const NegativeTrend: Story = {
  args: {
    title: "Total Won",
    value: 1234.56,
    type: "money",
    trend: -8.3,
  },
};
```

## src/stories/TextField.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 4417 bytes
- Tokens: 1199

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { TextField } from "@/components/controls/TextField";
import { userEvent, within } from '@storybook/testing-library';
import { expect } from '@storybook/jest';

const meta = {
  title: "Controls/TextField",
  component: TextField,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof TextField>;

export default meta;
type Story = StoryObj<typeof TextField>;

export const Default: Story = {
  args: {
    placeholder: "Enter text",
    label: "Text Input",
  },
};

export const WithStartIcon: Story = {
  args: {
    label: "Amount",
    placeholder: "Enter amount",
    startIcon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="h-4 w-4"
      >
        <path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
      </svg>
    ),
  },
};

export const WithClearButton: Story = {
  args: {
    label: "Clearable Input",
    placeholder: "Type something",
    clearable: true,
    value: "Clear me!",
  },
};

export const WithCharacterCount: Story = {
  args: {
    label: "Limited Input",
    placeholder: "Max 50 characters",
    maxLength: 50,
    showCount: true,
  },
};

export const WithCurrencyMask: Story = {
  args: {
    label: "Bet Amount",
    placeholder: "Enter amount",
    mask: "currency",
    startIcon: (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="h-4 w-4"
      >
        <path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
      </svg>
    ),
  },
};

export const WithDecimalMask: Story = {
  args: {
    label: "Decimal Number",
    placeholder: "Enter decimal",
    mask: "decimal",
  },
};

export const WithError: Story = {
  args: {
    label: "Error Input",
    placeholder: "Enter value",
    error: "This field is required",
    value: "",
  },
};

export const WithSuccess: Story = {
  args: {
    label: "Success Input",
    placeholder: "Enter value",
    success: "Value is valid",
    value: "Valid input",
  },
};

export const Disabled: Story = {
  args: {
    label: "Disabled Input",
    placeholder: "Cannot edit",
    disabled: true,
  },
};

export const WithInteractions: Story = {
  args: {
    label: "Interactive Input",
    placeholder: "Type here",
    clearable: true,
    maxLength: 20,
    showCount: true,
  },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    
    // Get the input
    const input = canvas.getByRole('textbox');
    
    // Type some text
    await userEvent.type(input, 'Hello, World!');
    expect(input).toHaveValue('Hello, World!');
    
    // Check character count
    const charCount = canvas.getByText('13/20');
    expect(charCount).toBeInTheDocument();
    
    // Clear the input
    const clearButton = canvas.getByRole('button');
    await userEvent.click(clearButton);
    expect(input).toHaveValue('');
  },
};

export const AllVariants: Story = {
  render: () => (
    <div className="flex flex-col gap-4 w-[300px]">
      <TextField
        label="Default Input"
        placeholder="Default variant"
      />
      <TextField
        label="Error Input"
        placeholder="Error variant"
        error="Something went wrong"
      />
      <TextField
        label="Success Input"
        placeholder="Success variant"
        success="Looking good!"
      />
      <TextField
        label="Currency Input"
        placeholder="0.00"
        mask="currency"
        startIcon={(
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="h-4 w-4"
          >
            <path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
          </svg>
        )}
      />
      <TextField
        label="Limited Input"
        placeholder="With character count"
        maxLength={20}
        showCount
        clearable
      />
    </div>
  ),
};
```

## src/stories/ThemeToggle.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 891 bytes
- Tokens: 216

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { ThemeToggle } from "@/components/controls/ThemeToggle";
import { ThemeProvider } from "@/components/providers/ThemeProvider";

const meta = {
  title: "Controls/ThemeToggle",
  component: ThemeToggle,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  decorators: [
    (Story) => (
      <ThemeProvider attribute="class" defaultTheme="light" enableSystem={false}>
        <div className="p-4">
          <Story />
        </div>
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof ThemeToggle>;

export default meta;
type Story = StoryObj<typeof meta>;

// Basic light/dark toggle
export const Default: Story = {
  args: {},
};

// Dark mode
export const DarkMode: Story = {
  args: {},
  parameters: {
    backgrounds: { default: 'dark' },
    themes: {
      themeOverride: 'dark',
    },
  },
};
```

## src/stories/Toggle.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 623 bytes
- Tokens: 157

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Toggle } from "@/components/controls/Toggle";

const meta = {
  title: "Controls/Toggle",
  component: Toggle,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
} satisfies Meta<typeof Toggle>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
};

export const Checked: Story = {
  args: {
    checked: true,
  },
};

export const Disabled: Story = {
  args: {
    disabled: true,
  },
};

export const DisabledChecked: Story = {
  args: {
    disabled: true,
    checked: true,
  },
};
```

## src/stories/UserDashboard.stories.tsx
- Language: TSX
- Encoding: utf-8
- Size: 3297 bytes
- Tokens: 943

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import { UserDashboard } from '@/components/controls/UserDashboard';
import { ThemeProvider } from '@/components/providers/ThemeProvider';
import type { Analysis } from '@/lib/types';
import type { MultiMarketAnalysis } from '@/lib/types/models/analysis';

const mockRecentAnalyses: Analysis[] = [
  {
    id: '1',
    correlationStrength: 0.85,
    confidence: 0.91,
    potentialValue: 95.5,
    status: 'active',
    createdAt: '2024-03-20T18:00:00Z',
    market: {
      homeTeam: 'Lakers',
      awayTeam: 'Warriors',
      status: {
        type: 'live',
        period: '3rd',
        timeRemaining: '8:45',
        possession: 'home',
        startTime: '2024-03-20T19:30:00Z',
      },
      homeScore: 89,
      awayScore: 92,
      startTime: '2024-03-20T19:30:00Z',
    },
    predictedOutcome: 'Lakers',
  },
  {
    id: '2',
    correlationStrength: 0.92,
    confidence: 0.88,
    potentialValue: 52.5,
    status: 'completed',
    createdAt: '2024-03-19T17:00:00Z',
    market: {
      homeTeam: 'Celtics',
      awayTeam: 'Heat',
      status: {
        type: 'final',
        startTime: '2024-03-19T19:00:00Z',
      },
      homeScore: 112,
      awayScore: 98,
      startTime: '2024-03-19T19:00:00Z',
    },
    predictedOutcome: 'Celtics',
  },
];

const mockMultiMarketAnalyses: MultiMarketAnalysis[] = [
  {
    id: '1',
    analyses: mockRecentAnalyses,
    correlationStrength: 0.89,
    confidence: 0.85,
    potentialValue: 200.55,
    status: 'active',
    createdAt: '2024-03-20T18:00:00Z',
  },
];

const meta = {
  title: 'Controls/UserDashboard',
  component: UserDashboard,
  parameters: {
    layout: 'fullscreen',
  },
  tags: ['autodocs'],
  decorators: [
    (Story) => (
      <ThemeProvider>
        <div className="p-4">
          <Story />
        </div>
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof UserDashboard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    accountInfo: {
      balance: 1000.00,
      totalAnalyses: 5000,
      successfulPredictions: 5500,
      accuracyRate: 55.0,
      activeAnalyses: 3,
      totalInvested: 2000.00,
      totalReturns: 500.00,
      pendingReturns: 0,
      availableCapital: 500.00,
      currency: 'USD',
      verificationStatus: 'verified',
    },
    recentAnalyses: mockRecentAnalyses,
    multiMarketAnalyses: mockMultiMarketAnalyses,
  },
};

export const Loading: Story = {
  args: {
    accountInfo: {
      balance: 0,
      totalAnalyses: 0,
      successfulPredictions: 0,
      accuracyRate: 0,
      activeAnalyses: 0,
      totalInvested: 0,
      totalReturns: 0,
      pendingReturns: 0,
      availableCapital: 0,
      currency: 'USD',
      verificationStatus: 'unverified',
    },
    recentAnalyses: [],
    multiMarketAnalyses: [],
  },
};

export const Empty: Story = {
  args: {
    accountInfo: {
      balance: 500,
      totalAnalyses: 0,
      successfulPredictions: 0,
      accuracyRate: 0,
      activeAnalyses: 0,
      totalInvested: 500,
      totalReturns: 0,
      pendingReturns: 0,
      availableCapital: 500,
      currency: 'USD',
      verificationStatus: 'verified',
    },
    recentAnalyses: [],
    multiMarketAnalyses: [],
  },
};
```

## src/stories/assets/accessibility.svg
- Language: text
- Encoding: utf-8
- Size: 1542 bytes
- Tokens: 884

```text
<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="none" viewBox="0 0 48 48"><title>Accessibility</title><circle cx="24.334" cy="24" r="24" fill="#A849FF" fill-opacity=".3"/><path fill="#A470D5" fill-rule="evenodd" d="M27.8609 11.585C27.8609 9.59506 26.2497 7.99023 24.2519 7.99023C22.254 7.99023 20.6429 9.65925 20.6429 11.585C20.6429 13.575 22.254 15.1799 24.2519 15.1799C26.2497 15.1799 27.8609 13.575 27.8609 11.585ZM21.8922 22.6473C21.8467 23.9096 21.7901 25.4788 21.5897 26.2771C20.9853 29.0462 17.7348 36.3314 17.3325 37.2275C17.1891 37.4923 17.1077 37.7955 17.1077 38.1178C17.1077 39.1519 17.946 39.9902 18.9802 39.9902C19.6587 39.9902 20.253 39.6293 20.5814 39.0889L20.6429 38.9874L24.2841 31.22C24.2841 31.22 27.5529 37.9214 27.9238 38.6591C28.2948 39.3967 28.8709 39.9902 29.7168 39.9902C30.751 39.9902 31.5893 39.1519 31.5893 38.1178C31.5893 37.7951 31.3639 37.2265 31.3639 37.2265C30.9581 36.3258 27.698 29.0452 27.0938 26.2771C26.8975 25.4948 26.847 23.9722 26.8056 22.7236C26.7927 22.333 26.7806 21.9693 26.7653 21.6634C26.7008 21.214 27.0231 20.8289 27.4097 20.7005L35.3366 18.3253C36.3033 18.0685 36.8834 16.9773 36.6256 16.0144C36.3678 15.0515 35.2722 14.4737 34.3055 14.7305C34.3055 14.7305 26.8619 17.1057 24.2841 17.1057C21.7062 17.1057 14.456 14.7947 14.456 14.7947C13.4893 14.5379 12.3937 14.9873 12.0715 15.9502C11.7493 16.9131 12.3293 18.0044 13.3604 18.3253L21.2873 20.7005C21.674 20.8289 21.9318 21.214 21.9318 21.6634C21.9174 21.9493 21.9053 22.2857 21.8922 22.6473Z" clip-rule="evenodd"/></svg>
```

## src/stories/assets/discord.svg
- Language: text
- Encoding: utf-8
- Size: 2393 bytes
- Tokens: 1361

```text
<svg xmlns="http://www.w3.org/2000/svg" width="33" height="32" fill="none" viewBox="0 0 33 32"><g clip-path="url(#clip0_10031_177575)"><mask id="mask0_10031_177575" style="mask-type:luminance" width="33" height="25" x="0" y="4" maskUnits="userSpaceOnUse"><path fill="#fff" d="M32.5034 4.00195H0.503906V28.7758H32.5034V4.00195Z"/></mask><g mask="url(#mask0_10031_177575)"><path fill="#5865F2" d="M27.5928 6.20817C25.5533 5.27289 23.3662 4.58382 21.0794 4.18916C21.0378 4.18154 20.9962 4.20057 20.9747 4.23864C20.6935 4.73863 20.3819 5.3909 20.1637 5.90358C17.7042 5.53558 15.2573 5.53558 12.8481 5.90358C12.6299 5.37951 12.307 4.73863 12.0245 4.23864C12.003 4.20184 11.9614 4.18281 11.9198 4.18916C9.63431 4.58255 7.44721 5.27163 5.40641 6.20817C5.38874 6.21578 5.3736 6.22848 5.36355 6.24497C1.21508 12.439 0.078646 18.4809 0.636144 24.4478C0.638667 24.477 0.655064 24.5049 0.677768 24.5227C3.41481 26.5315 6.06609 27.7511 8.66815 28.5594C8.70979 28.5721 8.75392 28.5569 8.78042 28.5226C9.39594 27.6826 9.94461 26.7968 10.4151 25.8653C10.4428 25.8107 10.4163 25.746 10.3596 25.7244C9.48927 25.3945 8.66058 24.9922 7.86343 24.5354C7.80038 24.4986 7.79533 24.4084 7.85333 24.3653C8.02108 24.2397 8.18888 24.109 8.34906 23.977C8.37804 23.9529 8.41842 23.9478 8.45249 23.963C13.6894 26.3526 19.359 26.3526 24.5341 23.963C24.5682 23.9465 24.6086 23.9516 24.6388 23.9757C24.799 24.1077 24.9668 24.2397 25.1358 24.3653C25.1938 24.4084 25.19 24.4986 25.127 24.5354C24.3298 25.0011 23.5011 25.3945 22.6296 25.7232C22.5728 25.7447 22.5476 25.8107 22.5754 25.8653C23.0559 26.7955 23.6046 27.6812 24.2087 28.5213C24.234 28.5569 24.2794 28.5721 24.321 28.5594C26.9357 27.7511 29.5869 26.5315 32.324 24.5227C32.348 24.5049 32.3631 24.4783 32.3656 24.4491C33.0328 17.5506 31.2481 11.5584 27.6344 6.24623C27.6256 6.22848 27.6105 6.21578 27.5928 6.20817ZM11.1971 20.8146C9.62043 20.8146 8.32129 19.3679 8.32129 17.5913C8.32129 15.8146 9.59523 14.368 11.1971 14.368C12.8115 14.368 14.0981 15.8273 14.0729 17.5913C14.0729 19.3679 12.7989 20.8146 11.1971 20.8146ZM21.8299 20.8146C20.2533 20.8146 18.9541 19.3679 18.9541 17.5913C18.9541 15.8146 20.228 14.368 21.8299 14.368C23.4444 14.368 24.7309 15.8273 24.7057 17.5913C24.7057 19.3679 23.4444 20.8146 21.8299 20.8146Z"/></g></g><defs><clipPath id="clip0_10031_177575"><rect width="32" height="32" fill="#fff" transform="translate(0.5)"/></clipPath></defs></svg>
```

## src/stories/assets/github.svg
- Language: text
- Encoding: utf-8
- Size: 2721 bytes
- Tokens: 1683

```text
<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" viewBox="0 0 32 32"><path fill="#161614" d="M16.0001 0C7.16466 0 0 7.17472 0 16.0256C0 23.1061 4.58452 29.1131 10.9419 31.2322C11.7415 31.3805 12.0351 30.8845 12.0351 30.4613C12.0351 30.0791 12.0202 28.8167 12.0133 27.4776C7.56209 28.447 6.62283 25.5868 6.62283 25.5868C5.89499 23.7345 4.8463 23.2419 4.8463 23.2419C3.39461 22.2473 4.95573 22.2678 4.95573 22.2678C6.56242 22.3808 7.40842 23.9192 7.40842 23.9192C8.83547 26.3691 11.1514 25.6609 12.0645 25.2514C12.2081 24.2156 12.6227 23.5087 13.0803 23.1085C9.52648 22.7032 5.7906 21.3291 5.7906 15.1886C5.7906 13.4389 6.41563 12.0094 7.43916 10.8871C7.27303 10.4834 6.72537 8.85349 7.59415 6.64609C7.59415 6.64609 8.93774 6.21539 11.9953 8.28877C13.2716 7.9337 14.6404 7.75563 16.0001 7.74953C17.3599 7.75563 18.7297 7.9337 20.0084 8.28877C23.0623 6.21539 24.404 6.64609 24.404 6.64609C25.2749 8.85349 24.727 10.4834 24.5608 10.8871C25.5868 12.0094 26.2075 13.4389 26.2075 15.1886C26.2075 21.3437 22.4645 22.699 18.9017 23.0957C19.4756 23.593 19.9869 24.5683 19.9869 26.0634C19.9869 28.2077 19.9684 29.9334 19.9684 30.4613C19.9684 30.8877 20.2564 31.3874 21.0674 31.2301C27.4213 29.1086 32 23.1037 32 16.0256C32 7.17472 24.8364 0 16.0001 0ZM5.99257 22.8288C5.95733 22.9084 5.83227 22.9322 5.71834 22.8776C5.60229 22.8253 5.53711 22.7168 5.57474 22.6369C5.60918 22.5549 5.7345 22.5321 5.85029 22.587C5.9666 22.6393 6.03284 22.7489 5.99257 22.8288ZM6.7796 23.5321C6.70329 23.603 6.55412 23.5701 6.45291 23.4581C6.34825 23.3464 6.32864 23.197 6.40601 23.125C6.4847 23.0542 6.62937 23.0874 6.73429 23.1991C6.83895 23.3121 6.85935 23.4605 6.7796 23.5321ZM7.31953 24.4321C7.2215 24.5003 7.0612 24.4363 6.96211 24.2938C6.86407 24.1513 6.86407 23.9804 6.96422 23.9119C7.06358 23.8435 7.2215 23.905 7.32191 24.0465C7.41968 24.1914 7.41968 24.3623 7.31953 24.4321ZM8.23267 25.4743C8.14497 25.5712 7.95818 25.5452 7.82146 25.413C7.68156 25.2838 7.64261 25.1004 7.73058 25.0035C7.81934 24.9064 8.00719 24.9337 8.14497 25.0648C8.28381 25.1938 8.3262 25.3785 8.23267 25.4743ZM9.41281 25.8262C9.37413 25.9517 9.19423 26.0088 9.013 25.9554C8.83203 25.9005 8.7136 25.7535 8.75016 25.6266C8.78778 25.5003 8.96848 25.4408 9.15104 25.4979C9.33174 25.5526 9.45044 25.6985 9.41281 25.8262ZM10.7559 25.9754C10.7604 26.1076 10.6067 26.2172 10.4165 26.2196C10.2252 26.2238 10.0704 26.1169 10.0683 25.9868C10.0683 25.8534 10.2185 25.7448 10.4098 25.7416C10.6001 25.7379 10.7559 25.8441 10.7559 25.9754ZM12.0753 25.9248C12.0981 26.0537 11.9658 26.1862 11.7769 26.2215C11.5912 26.2554 11.4192 26.1758 11.3957 26.0479C11.3726 25.9157 11.5072 25.7833 11.6927 25.7491C11.8819 25.7162 12.0512 25.7937 12.0753 25.9248Z"/></svg>
```

## src/stories/assets/tutorials.svg
- Language: text
- Encoding: utf-8
- Size: 1259 bytes
- Tokens: 653

```text
<svg xmlns="http://www.w3.org/2000/svg" width="33" height="32" fill="none" viewBox="0 0 33 32"><g clip-path="url(#clip0_10031_177597)"><path fill="#B7F0EF" fill-rule="evenodd" d="M17 7.87059C17 6.48214 17.9812 5.28722 19.3431 5.01709L29.5249 2.99755C31.3238 2.64076 33 4.01717 33 5.85105V22.1344C33 23.5229 32.0188 24.7178 30.6569 24.9879L20.4751 27.0074C18.6762 27.3642 17 25.9878 17 24.1539L17 7.87059Z" clip-rule="evenodd" opacity=".7"/><path fill="#87E6E5" fill-rule="evenodd" d="M1 5.85245C1 4.01857 2.67623 2.64215 4.47507 2.99895L14.6569 5.01848C16.0188 5.28861 17 6.48354 17 7.87198V24.1553C17 25.9892 15.3238 27.3656 13.5249 27.0088L3.34311 24.9893C1.98119 24.7192 1 23.5242 1 22.1358V5.85245Z" clip-rule="evenodd"/><path fill="#61C1FD" fill-rule="evenodd" d="M15.543 5.71289C15.543 5.71289 16.8157 5.96289 17.4002 6.57653C17.9847 7.19016 18.4521 9.03107 18.4521 9.03107C18.4521 9.03107 18.4521 25.1106 18.4521 26.9629C18.4521 28.8152 19.3775 31.4174 19.3775 31.4174L17.4002 28.8947L16.2575 31.4174C16.2575 31.4174 15.543 29.0765 15.543 27.122C15.543 25.1674 15.543 5.71289 15.543 5.71289Z" clip-rule="evenodd"/></g><defs><clipPath id="clip0_10031_177597"><rect width="32" height="32" fill="#fff" transform="translate(0.5)"/></clipPath></defs></svg>
```

## src/stories/assets/youtube.svg
- Language: text
- Encoding: utf-8
- Size: 717 bytes
- Tokens: 416

```text
<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="none" viewBox="0 0 32 32"><path fill="#ED1D24" d="M31.3313 8.44657C30.9633 7.08998 29.8791 6.02172 28.5022 5.65916C26.0067 5.00026 16 5.00026 16 5.00026C16 5.00026 5.99333 5.00026 3.4978 5.65916C2.12102 6.02172 1.03665 7.08998 0.668678 8.44657C0 10.9053 0 16.0353 0 16.0353C0 16.0353 0 21.1652 0.668678 23.6242C1.03665 24.9806 2.12102 26.0489 3.4978 26.4116C5.99333 27.0703 16 27.0703 16 27.0703C16 27.0703 26.0067 27.0703 28.5022 26.4116C29.8791 26.0489 30.9633 24.9806 31.3313 23.6242C32 21.1652 32 16.0353 32 16.0353C32 16.0353 32 10.9053 31.3313 8.44657Z"/><path fill="#fff" d="M12.7266 20.6934L21.0902 16.036L12.7266 11.3781V20.6934Z"/></svg>
```

## src/types/components/icons.types.ts
- Language: TypeScript
- Encoding: utf-8
- Size: 1126 bytes
- Tokens: 296

```typescript
// Icon component prop types
export interface IconProps {
  /** Name of the Heroicon */
  name: HeroIconName;
  /** Whether to use the solid or outline variant */
  solid?: boolean;
  /** Size of the icon */
  size?: "sm" | "md" | "lg" | "xl";
  /** Optional className for custom styling */
  className?: string;
  /** Accessible label for the icon */
  label?: string;
  /** Direction of the label relative to the icon */
  labelDirection?: "left" | "right" | "top" | "bottom";
  /** Theme color for the icon */
  color?: ThemeColor;
  /** Whether the icon should spin (for loading states) */
  spin?: boolean;
  /** Whether the icon should pulse (for attention states) */
  pulse?: boolean;
  /** Optional click handler */
  onClick?: (event: React.MouseEvent<HTMLSpanElement>) => void;
}

// Theme color types for icons
export type ThemeColor = 
  | "primary"
  | "secondary"
  | "accent"
  | "muted"
  | "foreground"
  | "background"
  | "border"
  | "ring"
  | "destructive"
  | "success"
  | "warning"
  | "info";

// Import the HeroIconName type from the domain models
import type { HeroIconName } from '@/lib/types';
```

## src/types/pages/betting.types.ts
- Language: TypeScript
- Encoding: utf-8
- Size: 412 bytes
- Tokens: 103

```typescript
// Page-specific types for market analysis pages
import type { DtoAnalysis, DtoMultiMarketAnalysis } from '@/lib/types/dto/analysis';

export interface AnalysisPageFilters {
  status?: 'all' | 'active' | 'completed' | 'archived';
  type?: 'all' | 'single' | 'multi-market';
}

export interface AnalysisPageProps {
  initialAnalyses?: (DtoAnalysis | DtoMultiMarketAnalysis)[];
  filters?: AnalysisPageFilters;
}
```
