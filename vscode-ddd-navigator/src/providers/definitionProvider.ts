import * as vscode from 'vscode';
import * as path from 'path';
import { IdentifierIndex } from '../index/identifierIndex';

export class IdentifierDefinitionProvider implements vscode.DefinitionProvider {
    constructor(private index: IdentifierIndex) {}

    async provideDefinition(
        document: vscode.TextDocument,
        position: vscode.Position,
        token: vscode.CancellationToken
    ): Promise<vscode.Definition | undefined> {

        // First, try to handle file navigation
        const fileNavigation = await this.handleFileNavigation(document, position);
        if (fileNavigation) {
            return fileNavigation;
        }

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

    private async handleFileNavigation(document: vscode.TextDocument, position: vscode.Position): Promise<vscode.Location | vscode.Location[] | undefined> {
        const fileName = path.basename(document.uri.fsPath);
        const isMarkdownFile = fileName.endsWith('.md');

        if (isMarkdownFile) {
            // Markdown file: Check if clicking on a file path reference
            return this.handleMarkdownToFileNavigation(document, position);
        } else {
            // Programming file: Navigate to markdown files that reference this file
            return this.handleFileToMarkdownNavigation(document);
        }
    }

    private async handleMarkdownToFileNavigation(document: vscode.TextDocument, position: vscode.Position): Promise<vscode.Location | vscode.Location[] | undefined> {
        const line = document.lineAt(position.line);
        const text = line.text;

        // Pattern to match file paths in markdown
        const filePathPattern = /`([^`]+\.[a-zA-Z0-9]+)`|\[([^\]]+)\]\(([^)]+\.[a-zA-Z0-9]+)\)|(\S+\.[a-zA-Z0-9]+)/g;

        let match;
        while ((match = filePathPattern.exec(text)) !== null) {
            const filePath = match[1] || match[3] || match[4];
            const startPos = match.index;
            const endPos = startPos + match[0].length;

            // Check if cursor is within this file path
            if (position.character >= startPos && position.character <= endPos) {
                if (filePath && this.isValidFilePath(filePath)) {
                    return this.findActualFile(filePath);
                }
            }
        }

        return undefined;
    }

    private async handleFileToMarkdownNavigation(document: vscode.TextDocument): Promise<vscode.Location | vscode.Location[] | undefined> {
        // Find markdown files that reference this programming file
        const references = this.index.findFileReferencesForCurrentFile(document.uri);

        if (references.length === 0) {
            return undefined;
        }

        if (references.length === 1) {
            return references[0];
        }

        // Multiple references found - show quick pick
        return this.showFileReferencesPicker(path.basename(document.uri.fsPath), references);
    }

    private async findActualFile(filePath: string): Promise<vscode.Location | vscode.Location[] | undefined> {
        // Try to find the actual file in the workspace
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) {
            return undefined;
        }

        const possiblePaths = [
            filePath, // Exact path
            `./${filePath}`, // Relative path
            `**/${path.basename(filePath)}`, // Just filename
            `**/${filePath}` // Glob pattern
        ];

        for (const searchPath of possiblePaths) {
            try {
                const files = await vscode.workspace.findFiles(searchPath, '**/node_modules/**', 10);
                if (files.length > 0) {
                    if (files.length === 1) {
                        return new vscode.Location(files[0], new vscode.Position(0, 0));
                    } else {
                        // Multiple files found - show picker
                        return files.map(uri => new vscode.Location(uri, new vscode.Position(0, 0)));
                    }
                }
            } catch (error) {
                // Continue to next search pattern
            }
        }

        return undefined;
    }

    private isValidFilePath(filePath: string): boolean {
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

    private async showFileReferencesPicker(fileName: string, references: vscode.Location[]): Promise<vscode.Location | undefined> {
        const items = references.map(location => {
            const refFileName = location.uri.fsPath.split('/').pop() || '';
            const line = location.range.start.line + 1;

            return {
                label: `${refFileName}:${line}`,
                description: `References ${fileName}`,
                detail: location.uri.fsPath,
                location: location
            };
        });

        const selected = await vscode.window.showQuickPick(items, {
            placeHolder: `Choose markdown file referencing ${fileName} (${references.length} found)`,
            matchOnDescription: true,
            matchOnDetail: true
        });

        return selected?.location;
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
