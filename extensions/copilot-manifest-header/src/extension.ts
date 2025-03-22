import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

function getManifestHeader(): string {
    // Define the path to the manifest file in the project root
    // Assumes that the project root is the workspace root
    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (!workspaceFolders) {
        return '';
    }
    const manifestPath = path.join(workspaceFolders[0].uri.fsPath, 'project_manifest.txt');
    try {
        const manifestContent = fs.readFileSync(manifestPath, 'utf8');
        // Create a header comment (using a simple comment style)
        const header = `/*\nProject Manifest (Auto-generated):\n${manifestContent}\n*/\n\n`;
        return header;
    } catch (err) {
        console.error('Error reading project_manifest.txt:', err);
        return '';
    }
}

export function activate(context: vscode.ExtensionContext) {
    // Function to insert or update header in the active text editor
    const insertHeader = () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            return;
        }
        const document = editor.document;
        const firstLine = document.lineAt(0);
        const header = getManifestHeader();
        // Check if the header already exists by seeing if the first line contains "Project Manifest"
        if (firstLine.text.includes("Project Manifest")) {
            // Replace the current header (assumes header is in the first 20 lines)
            const headerRange = new vscode.Range(0, 0, Math.min(20, document.lineCount), 0);
            editor.edit(editBuilder => {
                editBuilder.replace(headerRange, header);
            });
        } else {
            // Insert the header at the top of the file
            editor.edit(editBuilder => {
                editBuilder.insert(new vscode.Position(0, 0), header);
            });
        }
    };

    // Command to insert the header
    let disposable = vscode.commands.registerCommand('copilotManifestHeader.insertHeader', () => {
        insertHeader();
    });

    context.subscriptions.push(disposable);

    // Automatically insert/update header when a file is opened or saved
    vscode.workspace.onDidOpenTextDocument(insertHeader);
    vscode.workspace.onDidSaveTextDocument(insertHeader);
}

export function deactivate() {}
