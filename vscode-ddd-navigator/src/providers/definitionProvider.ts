import * as vscode from 'vscode';
import { IdentifierIndex } from '../index/identifierIndex';

export class IdentifierDefinitionProvider implements vscode.DefinitionProvider {
    constructor(private index: IdentifierIndex) {}

    async provideDefinition(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken
    ): Promise<vscode.Definition | undefined> {

        // Get the full identifier range manually for better detection
        const wordRange = this.getFullIdentifierRange(document, position);

        if (!wordRange) {
            return undefined;
        }

        const identifier = document.getText(wordRange);
        const definition = this.index.findDefinition(identifier);
        const references = this.index.findReferences(identifier);

        // If there's a definition, always include it first
        const allLocations: vscode.Location[] = [];
        if (definition) {
            allLocations.push(definition.location);
        }

        // Add all references
        allLocations.push(...references);

        // Remove duplicates based on URI and line
        const uniqueLocations = allLocations.filter((location, index, array) => {
            return array.findIndex(l =>
                l.uri.toString() === location.uri.toString() &&
                l.range.start.line === location.range.start.line
            ) === index;
        });

        if (uniqueLocations.length === 0) {
            return undefined;
        }

        if (uniqueLocations.length === 1) {
            return uniqueLocations[0];
        }

        // Multiple locations found - show quick pick
        return this.showLocationPicker(identifier, uniqueLocations);
    }

    private async showLocationPicker(identifier: string, locations: vscode.Location[]): Promise<vscode.Location | undefined> {
        const items = locations.map(location => {
            const fileName = location.uri.fsPath.split('/').pop() || '';
            const line = location.range.start.line + 1;

            return {
                label: `${fileName}:${line}`,
                description: this.getLocationContext(location),
                detail: location.uri.fsPath,
                location: location
            };
        });

        const selected = await vscode.window.showQuickPick(items, {
            placeHolder: `Choose location for ${identifier} (${locations.length} found)`,
            matchOnDescription: true,
            matchOnDetail: true
        });

        return selected?.location;
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

    private getLocationContext(location: vscode.Location): string {
        try {
            // Try to get some context from the file
            const document = vscode.workspace.textDocuments.find(doc =>
                doc.uri.toString() === location.uri.toString()
            );

            if (document) {
                const line = document.lineAt(location.range.start.line);
                return line.text.trim().substring(0, 80) + (line.text.length > 80 ? '...' : '');
            }
        } catch (error) {
            // Ignore errors
        }

        return 'Click to navigate';
    }
}
