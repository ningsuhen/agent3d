import * as vscode from 'vscode';
import * as path from 'path';

export interface Identifier {
    type: 'test-case' | 'requirement' | 'feature' | 'file-reference';
    id: string;
    location: vscode.Location;
    status?: 'complete' | 'pending' | 'skipped' | 'in-progress';
    description?: string;
    relatedIds?: string[];
}

export interface FileReference {
    filePath: string;
    referencedIn: vscode.Location[];
    actualFile?: vscode.Uri;
}

export class IdentifierIndex {
    private identifiers: Map<string, Identifier> = new Map();
    private references: Map<string, vscode.Location[]> = new Map();
    private fileReferences: Map<string, FileReference> = new Map();

    async buildIndex(workspaceFolder: vscode.WorkspaceFolder): Promise<void> {
        this.identifiers.clear();
        this.references.clear();
        this.fileReferences.clear();

        const config = vscode.workspace.getConfiguration('dddNavigator');
        const excludeDirectories = config.get<string[]>('excludeDirectories', ['.agent3d-tmp', 'node_modules', '.git', '.vscode', 'out', 'dist', 'build']);

        // Create exclude pattern for findFiles
        const excludePattern = `{${excludeDirectories.map(dir => `**/${dir}/**`).join(',')}}`;

        // Find all text-based files (markdown, text, code files)
        const textFiles = await vscode.workspace.findFiles(
            new vscode.RelativePattern(workspaceFolder, '**/*.{md,txt,js,ts,py,java,c,cpp,h,hpp,cs,php,rb,rs,swift,kt,scala,clj,hs,ml,fs,elm,dart,lua,r,m,pl,sh,bat,ps1,yaml,yml,json,xml,html,css,scss,less,sql}'),
            excludePattern
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

            // Parse file references (programming files mentioned in markdown)
            this.parseFileReferences(document, text, fileUri);

        } catch (error) {
            console.error(`Error indexing file ${fileUri.fsPath}:`, error);
        }
    }

    private parseTestCases(document: vscode.TextDocument, text: string, fileName: string, config: vscode.WorkspaceConfiguration): void {
        const testCaseFiles = config.get<string[]>('testCaseFiles', ['docs/features/*.md']);
        const pattern = new RegExp(config.get('testCasePattern', 'TC-[A-Za-z0-9-]+'), 'g');

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
        const pattern = new RegExp(config.get('requirementPattern', 'REQ-[A-Za-z0-9-]+'), 'g');

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
        const featureDirs = config.get<string[]>('featureDirs', ['docs/features/']);

        // Check for legacy FEATURES.md files
        const isLegacyFeatureFile = featureFiles.some(file => fileName.endsWith(file));

        // Check for new merged structure files in docs/features/
        const isMergedFeatureFile = featureDirs.some(dir => fileName.includes(dir) && fileName.endsWith('.md'));

        if (!isLegacyFeatureFile && !isMergedFeatureFile) {
            return;
        }

        const lines = text.split('\n');

        if (isMergedFeatureFile) {
            // Parse merged FT-TC structure (docs/features/*.md)
            this.parseMergedFeatureStructure(document, lines);
        } else {
            // Parse legacy FEATURES.md structure
            this.parseLegacyFeatureStructure(document, lines);
        }
    }

    private parseMergedFeatureStructure(document: vscode.TextDocument, lines: string[]): void {
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];

            // Match feature headers: ## FT-CORE-001 - Feature Name
            const featureMatch = line.match(/^## (FT-[A-Z]+-\d+) - (.+)$/);
            if (featureMatch) {
                const [, ftId, featureName] = featureMatch;
                const position = new vscode.Position(i, 0);

                const identifier: Identifier = {
                    type: 'feature',
                    id: ftId,
                    location: new vscode.Location(document.uri, position),
                    status: 'complete', // Default status for merged structure
                    description: featureName.trim()
                };

                this.identifiers.set(ftId, identifier);
            }

            // Match test case entries: - [x] **TC-CORE-001** - Test Name
            const testCaseMatch = line.match(/^\s+- \[([x~\s])\] \*\*(TC-[A-Z]+-\d+[a-z]?)\*\* - (.+)/);
            if (testCaseMatch) {
                const [, statusChar, tcId, testName] = testCaseMatch;
                const status = statusChar === 'x' ? 'complete' : statusChar === '~' ? 'in-progress' : 'pending';
                const position = new vscode.Position(i, 0);

                const identifier: Identifier = {
                    type: 'test-case',
                    id: tcId,
                    location: new vscode.Location(document.uri, position),
                    status,
                    description: testName.trim()
                };

                this.identifiers.set(tcId, identifier);
            }
        }
    }

    private parseLegacyFeatureStructure(document: vscode.TextDocument, lines: string[]): void {
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
        const tcPattern = /\b(TC-[A-Za-z0-9-]+)\b/g;
        const reqPattern = /\b(REQ-[A-Za-z0-9-]+)\b/g;

        [tcPattern, reqPattern].forEach(pattern => {
            let match;
            while ((match = pattern.exec(text)) !== null) {
                const id = match[0];
                const position = document.positionAt(match.index);
                this.addReference(id, new vscode.Location(document.uri, position));
            }
        });
    }

    private extractStatus(lineText: string): 'complete' | 'pending' | 'skipped' | 'in-progress' | undefined {
        if (lineText.includes('✅') || lineText.includes('[x]')) {
            return 'complete';
        } else if (lineText.includes('🚧') || lineText.includes('[~]')) {
            return 'in-progress';
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

    private parseFileReferences(document: vscode.TextDocument, text: string, fileUri: vscode.Uri): void {
        const fileName = path.basename(fileUri.fsPath);

        // Only parse file references in markdown files
        if (!fileName.endsWith('.md')) {
            return;
        }

        // Pattern to match file paths in markdown (code blocks, inline code, links)
        // Matches: `src/file.js`, `./path/file.py`, `/absolute/path/file.ts`, etc.
        const filePathPattern = /(?:`([^`]+\.[a-zA-Z0-9]+)`|```[a-zA-Z]*\n([^`]+)```|\[([^\]]+)\]\(([^)]+\.[a-zA-Z0-9]+)\)|(\S+\.[a-zA-Z0-9]+))/g;

        let match;
        while ((match = filePathPattern.exec(text)) !== null) {
            // Extract the file path from different capture groups
            const filePath = match[1] || match[4] || match[5];

            if (filePath && this.isValidFilePath(filePath)) {
                const position = document.positionAt(match.index);
                this.addFileReference(filePath, new vscode.Location(document.uri, position));
            }
        }
    }

    private isValidFilePath(filePath: string): boolean {
        // Check if it looks like a programming file
        const programmingExtensions = [
            '.js', '.ts', '.jsx', '.tsx', '.py', '.java', '.go', '.c', '.cpp', '.h', '.hpp',
            '.cs', '.php', '.rb', '.rs', '.swift', '.kt', '.scala', '.clj', '.hs', '.ml',
            '.fs', '.elm', '.dart', '.lua', '.r', '.m', '.pl', '.sh', '.bat', '.ps1'
        ];

        return programmingExtensions.some(ext => filePath.toLowerCase().endsWith(ext)) &&
               !filePath.includes('node_modules') &&
               !filePath.includes('.git') &&
               filePath.length > 3 &&
               filePath.length < 200; // Reasonable length limits
    }

    private addFileReference(filePath: string, location: vscode.Location): void {
        if (!this.fileReferences.has(filePath)) {
            this.fileReferences.set(filePath, {
                filePath,
                referencedIn: []
            });
        }
        this.fileReferences.get(filePath)!.referencedIn.push(location);
    }

    findFileReference(filePath: string): FileReference | undefined {
        return this.fileReferences.get(filePath);
    }

    findFileReferencesForCurrentFile(currentFileUri: vscode.Uri): vscode.Location[] {
        const currentFileName = path.basename(currentFileUri.fsPath);
        const currentFilePath = vscode.workspace.asRelativePath(currentFileUri);

        // Look for references to this file by name or relative path
        for (const [refPath, fileRef] of this.fileReferences) {
            if (refPath.endsWith(currentFileName) ||
                refPath === currentFilePath ||
                refPath.endsWith('/' + currentFileName)) {
                return fileRef.referencedIn;
            }
        }

        return [];
    }

    getAllFileReferences(): Map<string, FileReference> {
        return new Map(this.fileReferences);
    }
}
