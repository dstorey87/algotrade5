import { execSync } from 'child_process';
import { readFileSync } from 'fs';
import { join } from 'path';

interface Dependency {
  name: string;
  version: string;
  required: boolean;
}

interface DependencyGroups {
  core: Dependency[];
  ui: Dependency[];
  state: Dependency[];
  charts: Dependency[];
}

const DEPENDENCIES: DependencyGroups = {
  core: [
    { name: 'react', version: '^18', required: true },
    { name: 'react-dom', version: '^18', required: true },
    { name: 'next', version: '^14', required: true },
    { name: '@types/node', version: '^20', required: true },
    { name: '@types/react', version: '^18', required: true },
    { name: '@types/react-dom', version: '^18', required: true },
    { name: 'typescript', version: '^5', required: true },
    { name: 'ts-node', version: '^10', required: true },
  ],
  ui: [
    { name: '@mui/material', version: '^5', required: true },
    { name: '@emotion/react', version: '^11', required: true },
    { name: '@emotion/styled', version: '^11', required: true },
    { name: '@heroicons/react', version: '^2', required: true },
  ],
  charts: [
    { name: '@tremor/react', version: '^3', required: true },
    { name: 'recharts', version: '^2', required: true },
  ],
  state: [
    { name: '@reduxjs/toolkit', version: '^2', required: true },
    { name: 'react-redux', version: '^9', required: true },
  ]
};

interface PackageJson {
  dependencies?: Record<string, string>;
  devDependencies?: Record<string, string>;
}

function checkPackageJson(): PackageJson {
  try {
    const packageJson = JSON.parse(
      readFileSync(join(process.cwd(), 'package.json'), 'utf8')
    ) as PackageJson;
    return packageJson;
  } catch (error) {
    console.error('❌ Failed to read package.json:', error);
    process.exit(1);
  }
}

function validateDependencies(): void {
  console.log('🔍 Checking dependencies...');
  
  const packageJson = checkPackageJson();
  const allDeps = { 
    ...(packageJson.dependencies || {}), 
    ...(packageJson.devDependencies || {}) 
  };
  const missingDeps: string[] = [];
  
  Object.values(DEPENDENCIES).forEach((group: Dependency[]) => {
    group.forEach(({ name, version, required }: Dependency) => {
      if (!allDeps[name]) {
        if (required) {
          missingDeps.push(`${name}@${version}`);
        }
      }
    });
  });

  if (missingDeps.length > 0) {
    console.error('❌ Missing required dependencies:', missingDeps.join(', '));
    console.log('📦 Installing missing dependencies...');
    
    try {
      execSync(`npm install ${missingDeps.join(' ')}`, { stdio: 'inherit' });
      console.log('✅ Successfully installed missing dependencies');
    } catch (error) {
      console.error('❌ Failed to install dependencies:', error);
      process.exit(1);
    }
  }

  if (missingDeps.length === 0) {
    console.log('✅ All dependencies are installed');
  }

  // Update npx and ts-node globally if needed
  try {
    execSync('npm install -g npx ts-node', { stdio: 'inherit' });
  } catch (error) {
    console.error('❌ Failed to update global dependencies:', error);
    process.exit(1);
  }
}

// Run validation
validateDependencies();