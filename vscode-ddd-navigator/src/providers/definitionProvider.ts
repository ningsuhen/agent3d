import * as vscode from 'vscode';
import { IdentifierIndex } from '../index/identifierIndex';

export class IdentifierDefinitionProvider implements vscode.DefinitionProvider {
    constructor(private index: IdentifierIndex) {}

    provideDefinition(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken
    ): vscode.ProviderResult<vscode.Definition> {

        // Get the word at the current position
        const wordRange = document.getWordRangeAtPosition(
            position,
            /\b(TC-[A-Z0-9-]+|REQ-[A-Z0-9-]+)\b/
        );

        if (!wordRange) {
            return undefined;
        }

        const identifier = document.getText(wordRange);
        const definition = this.index.findDefinition(identifier);

        if (definition) {
            return definition.location;
        }

        return undefined;
    }
}
