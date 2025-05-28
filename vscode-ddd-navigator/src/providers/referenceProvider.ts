import * as vscode from 'vscode';
import { IdentifierIndex } from '../index/identifierIndex';

export class IdentifierReferenceProvider implements vscode.ReferenceProvider {
    constructor(private index: IdentifierIndex) {}

    provideReferences(
        document: vscode.TextDocument,
        position: vscode.Position,
        context: vscode.ReferenceContext,
        token: vscode.CancellationToken
    ): vscode.ProviderResult<vscode.Location[]> {

        // Get the full identifier range manually for better detection
        const wordRange = this.getFullIdentifierRange(document, position);

        if (!wordRange) {
            return [];
        }

        const identifier = document.getText(wordRange);
        const references = this.index.findReferences(identifier);

        // Include the definition if requested
        if (context.includeDeclaration) {
            const definition = this.index.findDefinition(identifier);
            if (definition) {
                references.unshift(definition.location);
            }
        }

        return references;
    }

    private getFullIdentifierRange(document: vscode.TextDocument, position: vscode.Position): vscode.Range | undefined {
        const line = document.lineAt(position.line);
        const text = line.text;

        // More robust pattern to match TC-XXX-XXX or REQ-XXX-XXX identifiers
        // Using non-word boundaries to better handle hyphens
        const pattern = /(^|[^A-Za-z0-9-])(TC-[A-Za-z0-9-]+|REQ-[A-Za-z0-9-]+)(?=[^A-Za-z0-9-]|$)/g;

        let match;
        while ((match = pattern.exec(text)) !== null) {
            // match[2] contains the actual identifier (TC-... or REQ-...)
            const identifier = match[2];
            const startPos = match.index + match[1].length; // Skip the prefix
            const endPos = startPos + identifier.length;

            // Check if the cursor position is within this match
            if (position.character >= startPos && position.character <= endPos) {
                return new vscode.Range(
                    position.line, startPos,
                    position.line, endPos
                );
            }
        }

        return undefined;
    }
}
