import * as vscode from 'vscode';
import * as path from 'path';

export interface Identifier {
    type: 'test-case' | 'requirement' | 'feature';
    id: string;
    location: vscode.Location;
    status?: 'complete' | 'pending' | 'skipped';
    description?: string;
    relatedIds?: string[];
}

export class IdentifierIndex {
    private identifiers: Map<string, Identifier> = new Map();
    private references: Map<string, vscode.Location[]> = new Map();

    async buildIndex(workspaceFolder: vscode.WorkspaceFolder): Promise<void> {
        this.identifiers.clear();
        this.references.clear();

        const config = vscode.workspace.getConfiguration('dddNavigator');

        // Find all text-based files (markdown, text, code files)
        const textFiles = await vscode.workspace.findFiles(
            new vscode.RelativePattern(workspaceFolder, '**/*.{md,txt,js,ts,py,java,go,c,cpp,h,hpp,cs,php,rb,rs,swift,kt,scala,clj,hs,ml,fs,elm,dart,lua,r,m,pl,sh,bat,ps1,yaml,yml,json,xml,html,css,scss,less,sql}'),
            '**/node_modules/**'
        );

        for (const fileUri of textFiles) {
            await this.indexFile(fileUri, config);
        }
    }

    private async indexFile(fileUri: vscode.Uri, config: vscode.WorkspaceConfiguration): Promise<void> {
        try {
            const document = await vscode.workspace.openTextDocument(fileUri);
            const text = document.getText();
            const fileName = path.basename(fileUri.fsPath);

            // Parse test cases
            if (config.get('enableTestCases', true)) {
                this.parseTestCases(document, text, fileName, config);
            }

            // Parse requirements
            if (config.get('enableRequirements', true)) {
                this.parseRequirements(document, text, fileName, config);
            }

            // Parse features
            if (config.get('enableFeatures', true)) {
                this.parseFeatures(document, text, fileName, config);
            }

            // Parse references
            this.parseReferences(document, text);

        } catch (error) {
            console.error(`Error indexing file ${fileUri.fsPath}:`, error);
        }
    }

    private parseTestCases(document: vscode.TextDocument, text: string, fileName: string, config: vscode.WorkspaceConfiguration): void {
        const testCaseFiles = config.get<string[]>('testCaseFiles', ['TEST-CASES.md', 'docs/TEST-CASES.md']);
        const pattern = new RegExp(config.get('testCasePattern', 'TC-[A-Z0-9-]+'), 'g');

        let match;
        while ((match = pattern.exec(text)) !== null) {
            const id = match[0];
            const position = document.positionAt(match.index);
            const line = document.lineAt(position.line);

            // Check if this is a definition (in test case files) or reference
            const isDefinition = testCaseFiles.some(file => fileName.endsWith(file));

            if (isDefinition) {
                // Extract status and description
                const status = this.extractStatus(line.text);
                const description = this.extractDescription(line.text, id);

                const identifier: Identifier = {
                    type: 'test-case',
                    id,
                    location: new vscode.Location(document.uri, position),
                    status,
                    description
                };

                this.identifiers.set(id, identifier);
            } else {
                // This is a reference
                this.addReference(id, new vscode.Location(document.uri, position));
            }
        }
    }

    private parseRequirements(document: vscode.TextDocument, text: string, fileName: string, config: vscode.WorkspaceConfiguration): void {
        const requirementFiles = config.get<string[]>('requirementFiles', ['REQUIREMENTS.md', 'docs/REQUIREMENTS.md']);
        const pattern = new RegExp(config.get('requirementPattern', 'REQ-[A-Z0-9-]+'), 'g');

        let match;
        while ((match = pattern.exec(text)) !== null) {
            const id = match[0];
            const position = document.positionAt(match.index);
            const line = document.lineAt(position.line);

            const isDefinition = requirementFiles.some(file => fileName.endsWith(file));

            if (isDefinition) {
                const status = this.extractStatus(line.text);
                const description = this.extractDescription(line.text, id);

                const identifier: Identifier = {
                    type: 'requirement',
                    id,
                    location: new vscode.Location(document.uri, position),
                    status,
                    description
                };

                this.identifiers.set(id, identifier);
            } else {
                this.addReference(id, new vscode.Location(document.uri, position));
            }
        }
    }

    private parseFeatures(document: vscode.TextDocument, text: string, fileName: string, config: vscode.WorkspaceConfiguration): void {
        const featureFiles = config.get<string[]>('featureFiles', ['FEATURES.md', 'docs/FEATURES.md']);
        const isFeatureFile = featureFiles.some(file => fileName.endsWith(file));

        if (!isFeatureFile) {
            return;
        }

        const lines = text.split('\n');
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const featureMatch = line.match(/^- \[([ x])\] (.+?) - (.+?)(?:\s+\(Criteria:|$)/);

            if (featureMatch) {
                const [, statusChar, featureName, description] = featureMatch;
                const status = statusChar === 'x' ? 'complete' : 'pending';
                const position = new vscode.Position(i, 0);

                const identifier: Identifier = {
                    type: 'feature',
                    id: featureName.trim(),
                    location: new vscode.Location(document.uri, position),
                    status,
                    description: description.trim()
                };

                this.identifiers.set(featureName.trim(), identifier);
            }
        }
    }

    private parseReferences(document: vscode.TextDocument, text: string): void {
        // Find all TC-#### and REQ-### references
        const tcPattern = /\b(TC-[A-Z0-9-]+)\b/g;
        const reqPattern = /\b(REQ-[A-Z0-9-]+)\b/g;

        [tcPattern, reqPattern].forEach(pattern => {
            let match;
            while ((match = pattern.exec(text)) !== null) {
                const id = match[0];
                const position = document.positionAt(match.index);
                this.addReference(id, new vscode.Location(document.uri, position));
            }
        });
    }

    private extractStatus(lineText: string): 'complete' | 'pending' | 'skipped' | undefined {
        if (lineText.includes('✅') || lineText.includes('[x]')) {
            return 'complete';
        } else if (lineText.includes('⏸️') || lineText.includes('[ ]')) {
            return 'pending';
        } else if (lineText.includes('⏭️')) {
            return 'skipped';
        }
        return undefined;
    }

    private extractDescription(lineText: string, id: string): string | undefined {
        // Remove the ID and status markers, extract remaining text as description
        const cleaned = lineText
            .replace(new RegExp(`\\b${id}\\b`), '')
            .replace(/[✅⏸️⏭️\[\]x]/g, '')
            .replace(/^[-*]\s*/, '')
            .trim();

        return cleaned || undefined;
    }

    private addReference(id: string, location: vscode.Location): void {
        if (!this.references.has(id)) {
            this.references.set(id, []);
        }
        this.references.get(id)!.push(location);
    }

    findDefinition(id: string): Identifier | undefined {
        return this.identifiers.get(id);
    }

    findReferences(id: string): vscode.Location[] {
        return this.references.get(id) || [];
    }

    findRelated(id: string): Identifier[] {
        // Find items that reference this ID or are referenced by this ID
        const related: Identifier[] = [];
        const refs = this.findReferences(id);

        // Add items that reference this ID
        for (const [otherId, otherIdentifier] of this.identifiers) {
            if (otherId !== id && refs.some(ref => ref.uri.toString() === otherIdentifier.location.uri.toString())) {
                related.push(otherIdentifier);
            }
        }

        return related;
    }

    getAllByType(type: 'test-case' | 'requirement' | 'feature'): Identifier[] {
        return Array.from(this.identifiers.values()).filter(id => id.type === type);
    }

    search(query: string): Identifier[] {
        const lowerQuery = query.toLowerCase();
        return Array.from(this.identifiers.values()).filter(id =>
            id.id.toLowerCase().includes(lowerQuery) ||
            (id.description && id.description.toLowerCase().includes(lowerQuery))
        );
    }
}
