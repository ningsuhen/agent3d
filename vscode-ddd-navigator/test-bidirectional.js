#!/usr/bin/env node

/**
 * Simple test script to verify bidirectional navigation functionality
 * This script simulates the extension's file reference detection
 */

const fs = require('fs');
const path = require('path');

// Test file paths
const testMarkdownFile = './test-files/test-navigation.md';
const testJsFile = './test-files/src/app.js';
const testTsFile = './test-files/models/user.ts';

console.log('🔍 Testing Bidirectional Navigation Functionality\n');

// Test 1: Parse file references from markdown
console.log('📄 Test 1: Parsing file references from markdown');
try {
    const markdownContent = fs.readFileSync(testMarkdownFile, 'utf8');
    console.log('✅ Markdown file loaded successfully');
    
    // Pattern to match file paths (same as in extension)
    const filePathPattern = /(?:`([^`]+\.[a-zA-Z0-9]+)`|```[a-zA-Z]*\n([^`]+)```|\[([^\]]+)\]\(([^)]+\.[a-zA-Z0-9]+)\)|(\S+\.[a-zA-Z0-9]+))/g;
    
    let match;
    const foundFiles = [];
    while ((match = filePathPattern.exec(markdownContent)) !== null) {
        const filePath = match[1] || match[4] || match[5];
        if (filePath && isValidFilePath(filePath)) {
            foundFiles.push(filePath);
        }
    }
    
    console.log(`✅ Found ${foundFiles.length} file references:`);
    foundFiles.forEach(file => console.log(`   - ${file}`));
    
} catch (error) {
    console.log('❌ Error reading markdown file:', error.message);
}

// Test 2: Check if programming files exist
console.log('\n🔧 Test 2: Checking programming file existence');
[testJsFile, testTsFile].forEach(filePath => {
    if (fs.existsSync(filePath)) {
        console.log(`✅ ${path.basename(filePath)} exists`);
    } else {
        console.log(`❌ ${path.basename(filePath)} not found`);
    }
});

// Test 3: Simulate reverse navigation (programming file -> markdown)
console.log('\n🔄 Test 3: Simulating reverse navigation');
try {
    const markdownContent = fs.readFileSync(testMarkdownFile, 'utf8');
    const jsFileName = path.basename(testJsFile);
    const tsFileName = path.basename(testTsFile);
    
    if (markdownContent.includes(jsFileName)) {
        console.log(`✅ ${jsFileName} is referenced in markdown`);
    } else {
        console.log(`❌ ${jsFileName} not found in markdown`);
    }
    
    if (markdownContent.includes(tsFileName)) {
        console.log(`✅ ${tsFileName} is referenced in markdown`);
    } else {
        console.log(`❌ ${tsFileName} not found in markdown`);
    }
    
} catch (error) {
    console.log('❌ Error during reverse navigation test:', error.message);
}

console.log('\n🎯 Test Summary:');
console.log('- File reference parsing: Implemented');
console.log('- Programming file detection: Implemented');
console.log('- Reverse navigation logic: Implemented');
console.log('- VS Code integration: Ready for testing');

function isValidFilePath(filePath) {
    const programmingExtensions = [
        '.js', '.ts', '.jsx', '.tsx', '.py', '.java', '.go', '.c', '.cpp', '.h', '.hpp',
        '.cs', '.php', '.rb', '.rs', '.swift', '.kt', '.scala', '.clj', '.hs', '.ml',
        '.fs', '.elm', '.dart', '.lua', '.r', '.m', '.pl', '.sh', '.bat', '.ps1'
    ];
    
    return programmingExtensions.some(ext => filePath.toLowerCase().endsWith(ext)) &&
           !filePath.includes('node_modules') &&
           !filePath.includes('.git') &&
           filePath.length > 3 &&
           filePath.length < 200;
}
