import * as vscode from 'vscode';
import { IdentifierIndex } from '../index/identifierIndex';

export class IdentifierHoverProvider implements vscode.HoverProvider {
    constructor(private index: IdentifierIndex) {}

    provideHover(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken
    ): vscode.ProviderResult<vscode.Hover> {
        
        // Get the word at the current position
        const wordRange = document.getWordRangeAtPosition(
            position, 
            /\b(TC-\d{4}[a-z]*|REQ-[A-Z]*-?\d{3}|[A-Za-z][A-Za-z0-9\s]+)\b/
        );
        
        if (!wordRange) {
            return undefined;
        }

        const identifier = document.getText(wordRange);
        const definition = this.index.findDefinition(identifier);
        
        if (!definition) {
            return undefined;
        }

        // Create hover content
        const markdown = new vscode.MarkdownString();
        markdown.isTrusted = true;
        
        // Add type and status
        const statusIcon = this.getStatusIcon(definition.status);
        markdown.appendMarkdown(`**${definition.type.toUpperCase()}** ${statusIcon}\n\n`);
        
        // Add ID
        markdown.appendMarkdown(`**ID:** \`${definition.id}\`\n\n`);
        
        // Add description if available
        if (definition.description) {
            markdown.appendMarkdown(`**Description:** ${definition.description}\n\n`);
        }
        
        // Add file location
        const fileName = definition.location.uri.fsPath.split('/').pop();
        const line = definition.location.range.start.line + 1;
        markdown.appendMarkdown(`**Location:** ${fileName}:${line}\n\n`);
        
        // Add references count
        const references = this.index.findReferences(definition.id);
        if (references.length > 0) {
            markdown.appendMarkdown(`**References:** ${references.length} found\n\n`);
        }
        
        // Add related items
        const related = this.index.findRelated(definition.id);
        if (related.length > 0) {
            markdown.appendMarkdown(`**Related Items:** ${related.length} found\n\n`);
        }
        
        // Add action links
        markdown.appendMarkdown(`[Go to Definition](command:vscode.open?${encodeURIComponent(JSON.stringify([definition.location.uri, { selection: definition.location.range }]))})`);
        
        if (references.length > 0) {
            markdown.appendMarkdown(` | [Find All References](command:editor.action.findReferences)`);
        }
        
        return new vscode.Hover(markdown, wordRange);
    }
    
    private getStatusIcon(status?: string): string {
        switch (status) {
            case 'complete':
                return '✅';
            case 'pending':
                return '⏸️';
            case 'skipped':
                return '⏭️';
            default:
                return '❓';
        }
    }
}
