import {defineConfig} from '@playwright/test';
export default defineConfig({testDir:'e2e',testMatch:'**/*.e2e.ts',timeout:30000,use:{baseURL:'http://127.0.0.1:5173',headless:true},webServer:{command:'../../scripts/dev.sh',url:'http://127.0.0.1:5173',reuseExistingServer:!process.env.CI,timeout:30000},reporter:'list'});
