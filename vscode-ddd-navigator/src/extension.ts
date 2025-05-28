import * as vscode from 'vscode';
import { IdentifierDefinitionProvider } from './providers/definitionProvider';
import { IdentifierReferenceProvider } from './providers/referenceProvider';
import { IdentifierHoverProvider } from './providers/hoverProvider';
import { IdentifierIndex } from './index/identifierIndex';
import { QuickPickProvider } from './providers/quickPickProvider';

let identifierIndex: IdentifierIndex;

export function activate(context: vscode.ExtensionContext) {
    console.log('DDD Navigator extension is now active!');

    // Initialize the identifier index
    identifierIndex = new IdentifierIndex();

    // Create providers
    const definitionProvider = new IdentifierDefinitionProvider(identifierIndex);
    const referenceProvider = new IdentifierReferenceProvider(identifierIndex);
    const hoverProvider = new IdentifierHoverProvider(identifierIndex);
    const quickPickProvider = new QuickPickProvider(identifierIndex);

    // Register language providers for all file types
    context.subscriptions.push(
        vscode.languages.registerDefinitionProvider(
            { scheme: 'file' },
            definitionProvider
        ),
        vscode.languages.registerReferenceProvider(
            { scheme: 'file' },
            referenceProvider
        ),
        vscode.languages.registerHoverProvider(
            { scheme: 'file' },
            hoverProvider
        )
    );

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('dddNavigator.goToTestCase', () => {
            quickPickProvider.showTestCasePicker();
        }),
        vscode.commands.registerCommand('dddNavigator.goToRequirement', () => {
            quickPickProvider.showRequirementPicker();
        }),
        vscode.commands.registerCommand('dddNavigator.goToFeature', () => {
            quickPickProvider.showFeaturePicker();
        }),
        vscode.commands.registerCommand('dddNavigator.showRelated', () => {
            showRelatedItems();
        }),
        vscode.commands.registerCommand('dddNavigator.refreshIndex', () => {
            refreshIndex();
        })
    );

    // Build initial index
    buildIndex();

    // Watch for file changes
    const watcher = vscode.workspace.createFileSystemWatcher('**/*.md');
    watcher.onDidChange(() => buildIndex());
    watcher.onDidCreate(() => buildIndex());
    watcher.onDidDelete(() => buildIndex());
    context.subscriptions.push(watcher);
}

async function buildIndex() {
    if (vscode.workspace.workspaceFolders) {
        for (const folder of vscode.workspace.workspaceFolders) {
            await identifierIndex.buildIndex(folder);
        }
    }
}

async function refreshIndex() {
    vscode.window.showInformationMessage('Refreshing DDD Navigator index...');
    await buildIndex();
    vscode.window.showInformationMessage('DDD Navigator index refreshed!');
}

async function showRelatedItems() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        return;
    }

    const position = editor.selection.active;
    const wordRange = editor.document.getWordRangeAtPosition(position, /\b(TC-[A-Z0-9]+-[A-Z0-9]+|REQ-[A-Z0-9]+-[A-Z0-9]+)\b/);

    if (!wordRange) {
        vscode.window.showInformationMessage('No identifier found at cursor position');
        return;
    }

    const identifier = editor.document.getText(wordRange);
    const related = identifierIndex.findRelated(identifier);

    if (related.length === 0) {
        vscode.window.showInformationMessage(`No related items found for ${identifier}`);
        return;
    }

    const items = related.map(item => ({
        label: item.id,
        description: item.description || '',
        detail: `${item.type} - ${item.status || 'unknown'}`,
        location: item.location
    }));

    const selected = await vscode.window.showQuickPick(items, {
        placeHolder: `Related items for ${identifier}`
    });

    if (selected) {
        const uri = selected.location.uri;
        const range = selected.location.range;
        await vscode.window.showTextDocument(uri, { selection: range });
    }
}

export function deactivate() {
    // Cleanup if needed
}
