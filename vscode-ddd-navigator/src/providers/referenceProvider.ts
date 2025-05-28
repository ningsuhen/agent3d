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

        // Get the word at the current position
        const wordRange = document.getWordRangeAtPosition(
            position,
            /\b(TC-[A-Z0-9-]+|REQ-[A-Z0-9-]+)\b/
        );

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
}
