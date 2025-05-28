import * as assert from 'assert';
import * as vscode from 'vscode';
import * as path from 'path';
import { IdentifierIndex } from '../../index/identifierIndex';
import { IdentifierDefinitionProvider } from '../../providers/definitionProvider';
import { IdentifierHoverProvider } from '../../providers/hoverProvider';
import { IdentifierReferenceProvider } from '../../providers/referenceProvider';

suite('DDD Navigator Extension Test Suite', () => {
    let identifierIndex: IdentifierIndex;
    let definitionProvider: IdentifierDefinitionProvider;
    let hoverProvider: IdentifierHoverProvider;
    let referenceProvider: IdentifierReferenceProvider;

    suiteSetup(async () => {
        // Initialize the extension components
        identifierIndex = new IdentifierIndex();
        definitionProvider = new IdentifierDefinitionProvider(identifierIndex);
        hoverProvider = new IdentifierHoverProvider(identifierIndex);
        referenceProvider = new IdentifierReferenceProvider(identifierIndex);

        // Ensure extension is activated
        const extension = vscode.extensions.getExtension('agent3d.ddd-navigator');
        if (extension && !extension.isActive) {
            await extension.activate();
        }
    });

    suite('Identifier Index Tests', () => {
        test('Should build index from test fixtures', async () => {
            const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
            assert.ok(workspaceFolder, 'Workspace folder should be available');

            await identifierIndex.buildIndex(workspaceFolder);

            // Test that test cases are indexed
            const tcDefinition = identifierIndex.findDefinition('TC-0001');
            assert.ok(tcDefinition, 'TC-0001 should be found in index');
            assert.strictEqual(tcDefinition.type, 'test-case');
            assert.strictEqual(tcDefinition.status, 'complete');
        });

        test('Should find test cases with various formats', async () => {
            const testCases = [
                'TC-0001',      // Basic format
                'TC-0003a',     // With lowercase suffix
                'TC-ENV-001',   // With category prefix
                'TC-ENV-002',   // Environment category
                'TC-BATCH-001', // Batch category
                'TC-SYNC-001'   // Sync category
            ];

            for (const tcId of testCases) {
                const definition = identifierIndex.findDefinition(tcId);
                assert.ok(definition, `${tcId} should be found in index`);
                assert.strictEqual(definition.type, 'test-case', `${tcId} should be a test case`);
            }
        });

        test('Should find requirements with various formats', async () => {
            const requirements = [
                'REQ-001',      // Basic format
                'REQ-AUTH-001', // With category prefix
                'REQ-ENV-001',  // Environment category
                'REQ-BATCH-001' // Batch category
            ];

            for (const reqId of requirements) {
                const definition = identifierIndex.findDefinition(reqId);
                assert.ok(definition, `${reqId} should be found in index`);
                assert.strictEqual(definition.type, 'requirement', `${reqId} should be a requirement`);
            }
        });

        test('Should find references across multiple files', async () => {
            // TC-0001 should be referenced in both TEST-CASES.md and sample.js
            const references = identifierIndex.findReferences('TC-0001');
            assert.ok(references.length >= 2, 'TC-0001 should have multiple references');

            // Check that references span different file types
            const fileTypes = references.map(ref => path.extname(ref.uri.fsPath));
            assert.ok(fileTypes.includes('.md'), 'Should have markdown references');
            assert.ok(fileTypes.includes('.js'), 'Should have JavaScript references');
        });
    });

    suite('Definition Provider Tests', () => {
        test('Should provide definition for test case identifiers', async () => {
            const testCasesDoc = await openFixtureDocument('TEST-CASES.md');
            const position = findPositionOfText(testCasesDoc, 'TC-0001');

            const definition = await definitionProvider.provideDefinition(testCasesDoc, position, new vscode.CancellationTokenSource().token);

            assert.ok(definition, 'Definition should be provided for TC-0001');
            if (definition instanceof vscode.Location) {
                assert.ok(definition.uri.fsPath.endsWith('TEST-CASES.md'), 'Definition should point to TEST-CASES.md');
            }
        });

        test('Should provide definition for requirement identifiers', async () => {
            const requirementsDoc = await openFixtureDocument('REQUIREMENTS.md');
            const position = findPositionOfText(requirementsDoc, 'REQ-001');

            const definition = await definitionProvider.provideDefinition(requirementsDoc, position, new vscode.CancellationTokenSource().token);

            assert.ok(definition, 'Definition should be provided for REQ-001');
            if (definition instanceof vscode.Location) {
                assert.ok(definition.uri.fsPath.endsWith('REQUIREMENTS.md'), 'Definition should point to REQUIREMENTS.md');
            }
        });

        test('Should work with identifiers in code files', async () => {
            const codeDoc = await openFixtureDocument('sample.js');
            const position = findPositionOfText(codeDoc, 'TC-0001');

            const definition = await definitionProvider.provideDefinition(codeDoc, position, new vscode.CancellationTokenSource().token);

            assert.ok(definition, 'Definition should be provided for TC-0001 in JavaScript file');
        });

        test('Should handle complex identifier formats', async () => {
            const testCasesDoc = await openFixtureDocument('TEST-CASES.md');

            const complexIdentifiers = [
                'TC-0003a',     // With lowercase suffix
                'TC-ENV-002',   // With category
                'TC-BATCH-001', // Batch category
                'TC-SYNC-001'   // Sync category
            ];

            for (const identifier of complexIdentifiers) {
                const position = findPositionOfText(testCasesDoc, identifier);
                const definition = await definitionProvider.provideDefinition(testCasesDoc, position, new vscode.CancellationTokenSource().token);

                assert.ok(definition, `Definition should be provided for ${identifier}`);
            }
        });
    });

    suite('Hover Provider Tests', () => {
        test('Should provide hover information for test cases', async () => {
            const testCasesDoc = await openFixtureDocument('TEST-CASES.md');
            const position = findPositionOfText(testCasesDoc, 'TC-0001');

            const hover = hoverProvider.provideHover(testCasesDoc, position, new vscode.CancellationTokenSource().token);

            assert.ok(hover, 'Hover should be provided for TC-0001');
            if (hover instanceof vscode.Hover) {
                const content = hover.contents[0];
                if (content instanceof vscode.MarkdownString) {
                    assert.ok(content.value.includes('TEST-CASE'), 'Hover should indicate test case type');
                    assert.ok(content.value.includes('TC-0001'), 'Hover should include identifier');
                }
            }
        });

        test('Should provide hover information for requirements', async () => {
            const requirementsDoc = await openFixtureDocument('REQUIREMENTS.md');
            const position = findPositionOfText(requirementsDoc, 'REQ-001');

            const hover = hoverProvider.provideHover(requirementsDoc, position, new vscode.CancellationTokenSource().token);

            assert.ok(hover, 'Hover should be provided for REQ-001');
            if (hover instanceof vscode.Hover) {
                const content = hover.contents[0];
                if (content instanceof vscode.MarkdownString) {
                    assert.ok(content.value.includes('REQUIREMENT'), 'Hover should indicate requirement type');
                    assert.ok(content.value.includes('REQ-001'), 'Hover should include identifier');
                }
            }
        });

        test('Should show status indicators in hover', async () => {
            const testCasesDoc = await openFixtureDocument('TEST-CASES.md');

            // Test completed test case
            const completedPosition = findPositionOfText(testCasesDoc, 'TC-0001');
            const completedHover = hoverProvider.provideHover(testCasesDoc, completedPosition, new vscode.CancellationTokenSource().token);

            assert.ok(completedHover, 'Hover should be provided for completed test case');
            if (completedHover instanceof vscode.Hover) {
                const content = completedHover.contents[0];
                if (content instanceof vscode.MarkdownString) {
                    assert.ok(content.value.includes('✅'), 'Completed test case should show checkmark');
                }
            }

            // Test pending test case
            const pendingPosition = findPositionOfText(testCasesDoc, 'TC-ENV-002');
            const pendingHover = hoverProvider.provideHover(testCasesDoc, pendingPosition, new vscode.CancellationTokenSource().token);

            assert.ok(pendingHover, 'Hover should be provided for pending test case');
            if (pendingHover instanceof vscode.Hover) {
                const content = pendingHover.contents[0];
                if (content instanceof vscode.MarkdownString) {
                    assert.ok(content.value.includes('⏸️'), 'Pending test case should show pause icon');
                }
            }
        });
    });

    suite('Reference Provider Tests', () => {
        test('Should find all references for test cases', async () => {
            const testCasesDoc = await openFixtureDocument('TEST-CASES.md');
            const position = findPositionOfText(testCasesDoc, 'TC-0001');

            const references = referenceProvider.provideReferences(
                testCasesDoc,
                position,
                { includeDeclaration: true },
                new vscode.CancellationTokenSource().token
            );

            assert.ok(references, 'References should be provided for TC-0001');
            assert.ok(Array.isArray(references), 'References should be an array');
            assert.ok(references.length >= 2, 'TC-0001 should have multiple references');
        });

        test('Should find references across different file types', async () => {
            const codeDoc = await openFixtureDocument('sample.js');
            const position = findPositionOfText(codeDoc, 'TC-0001');

            const references = referenceProvider.provideReferences(
                codeDoc,
                position,
                { includeDeclaration: true },
                new vscode.CancellationTokenSource().token
            );

            assert.ok(references, 'References should be provided from JavaScript file');
            assert.ok(Array.isArray(references), 'References should be an array');

            // Should find references in both .md and .js files
            const fileExtensions = references.map(ref => path.extname(ref.uri.fsPath));
            const uniqueExtensions = [...new Set(fileExtensions)];
            assert.ok(uniqueExtensions.length > 1, 'References should span multiple file types');
        });
    });

    // Helper functions
    async function openFixtureDocument(filename: string): Promise<vscode.TextDocument> {
        const fixturePath = path.join(__dirname, '..', 'fixtures', filename);
        const uri = vscode.Uri.file(fixturePath);
        return await vscode.workspace.openTextDocument(uri);
    }

    function findPositionOfText(document: vscode.TextDocument, text: string): vscode.Position {
        for (let i = 0; i < document.lineCount; i++) {
            const line = document.lineAt(i);
            const index = line.text.indexOf(text);
            if (index !== -1) {
                return new vscode.Position(i, index + Math.floor(text.length / 2));
            }
        }
        throw new Error(`Text "${text}" not found in document`);
    }

    suite('Performance Tests', () => {
        test('Index building should complete within reasonable time', async () => {
            const startTime = Date.now();

            const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
            assert.ok(workspaceFolder, 'Workspace folder should be available');

            await identifierIndex.buildIndex(workspaceFolder);

            const endTime = Date.now();
            const duration = endTime - startTime;

            // Index building should complete within 5 seconds for test fixtures
            assert.ok(duration < 5000, `Index building took ${duration}ms, should be under 5000ms`);
        });

        test('Definition lookup should be fast', async () => {
            const testCasesDoc = await openFixtureDocument('TEST-CASES.md');
            const position = findPositionOfText(testCasesDoc, 'TC-0001');

            const startTime = Date.now();

            const definition = await definitionProvider.provideDefinition(
                testCasesDoc,
                position,
                new vscode.CancellationTokenSource().token
            );

            const endTime = Date.now();
            const duration = endTime - startTime;

            assert.ok(definition, 'Definition should be found');
            // Definition lookup should complete within 100ms
            assert.ok(duration < 100, `Definition lookup took ${duration}ms, should be under 100ms`);
        });

        test('Hover provider should be responsive', async () => {
            const testCasesDoc = await openFixtureDocument('TEST-CASES.md');
            const position = findPositionOfText(testCasesDoc, 'TC-ENV-002');

            const startTime = Date.now();

            const hover = hoverProvider.provideHover(
                testCasesDoc,
                position,
                new vscode.CancellationTokenSource().token
            );

            const endTime = Date.now();
            const duration = endTime - startTime;

            assert.ok(hover, 'Hover should be provided');
            // Hover should complete within 50ms
            assert.ok(duration < 50, `Hover took ${duration}ms, should be under 50ms`);
        });
    });
});
