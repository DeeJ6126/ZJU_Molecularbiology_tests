import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const repositoryName = 'ZJU_Molecularbiology_Tests'
const isGitHubPagesBuild = process.env.GITHUB_PAGES === 'true'

// https://vite.dev/config/
export default defineConfig({
  base: isGitHubPagesBuild ? `/${repositoryName}/` : '/',
  plugins: [react()],
})
