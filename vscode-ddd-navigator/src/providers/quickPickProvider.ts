import * as vscode from 'vscode';
import { IdentifierIndex, Identifier } from '../index/identifierIndex';

export class QuickPickProvider {
    constructor(private index: IdentifierIndex) {}

    async showTestCasePicker(): Promise<void> {
        const testCases = this.index.getAllByType('test-case');
        await this.showPicker(testCases, 'Select a Test Case');
    }

    async showRequirementPicker(): Promise<void> {
        const requirements = this.index.getAllByType('requirement');
        await this.showPicker(requirements, 'Select a Requirement');
    }

    async showFeaturePicker(): Promise<void> {
        const features = this.index.getAllByType('feature');
        await this.showPicker(features, 'Select a Feature');
    }

    private async showPicker(items: Identifier[], placeholder: string): Promise<void> {
        if (items.length === 0) {
            vscode.window.showInformationMessage(`No ${placeholder.toLowerCase()} found`);
            return;
        }

        const quickPickItems = items.map(item => ({
            label: item.id,
            description: item.description || '',
            detail: `${this.getStatusIcon(item.status)} ${item.type} - ${this.getFileName(item.location.uri)}`,
            identifier: item
        }));

        // Sort by ID
        quickPickItems.sort((a, b) => a.label.localeCompare(b.label));

        const selected = await vscode.window.showQuickPick(quickPickItems, {
            placeHolder: placeholder,
            matchOnDescription: true,
            matchOnDetail: true
        });

        if (selected) {
            const location = selected.identifier.location;
            await vscode.window.showTextDocument(location.uri, {
                selection: location.range
            });
        }
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

    private getFileName(uri: vscode.Uri): string {
        return uri.fsPath.split('/').pop() || '';
    }
}
