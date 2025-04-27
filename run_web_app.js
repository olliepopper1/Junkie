// Run Web App
const { execSync } = require('child_process');
const path = require('path');

// Execute TypeScript compiler
console.log('Compiling TypeScript...');
try {
  execSync('npx tsc', { stdio: 'inherit' });
  console.log('TypeScript compilation successful!');
} catch (error) {
  console.error('TypeScript compilation failed:', error.message);
  process.exit(1);
}

// Start the server
console.log('Starting web server...');
try {
  require('./dist/index.js');
} catch (error) {
  console.error('Failed to start server:', error.message);
  process.exit(1);
}