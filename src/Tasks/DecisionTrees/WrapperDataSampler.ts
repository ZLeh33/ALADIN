import { exec } from 'child_process';
import * as fs from 'fs';

/* Funktion für die ausführung des Python-Skripts (DataSampler.py) */
function runPythonScript(scriptPath: string, args: string[]): Promise<string> {
    return new Promise((resolve, reject) => {
        const command = `python ${scriptPath} ${args.join(' ')}`;
        exec(command, (error, stdout, stderr) => {
            if (error) {
                reject(error.message);
                return;
            }
            if (stderr) {
                reject(stderr);
                return;
            }
            resolve(stdout);
        });
    });
}

/* Funktion für das Auslesen einer JSON-Datei (generated_dataset.json) */
async function readJsonFile(filePath: string): Promise<any[]> {
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf-8', (err, data) => {
            if (err) {
                reject(err);
                return;
            }

            try {
                const jsonData = data.split('\n').filter(Boolean).map(line => JSON.parse(line));
                resolve(jsonData);
            } catch (parseError) {
                reject(parseError);
            }
        });
    });
}

/* Tabelle aus einem JSON erstellen */
function generateTableFromJson(jsonArray: Array<any>, tableColumns: string[]) {
    return jsonArray.map((jsonObj) => {
        const tableRow: Record<string, any> = {};
        tableColumns.forEach((column, index) => {
            tableRow[column] = jsonObj[column];
        });
        return tableRow;
    });
}

/* Wrapper-Funktion */
export async function DataSamplingGenerator() {
    try {
        const pythonScriptPath = 'src/Tasks/DecisionTrees/DataSampler.py';
        const argumentsToPythonScript = [''];
        await runPythonScript(pythonScriptPath, argumentsToPythonScript);

        const filename = 'src/Tasks/DecisionTrees/datasets/generated_dataset.json';

        try {
            const jsonData = await readJsonFile(filename);
            const tableColumns = Array.from(new Set(jsonData.flatMap(Object.keys)));

            const tableData = generateTableFromJson(jsonData, tableColumns);
            console.log('Table: ', tableData);

            return { "table": tableData };
        } catch (jsonError) {
            console.error(`Error parsing JSON file ${filename}: ${jsonError}`);
        }
    } catch (error) {
        console.error('Error running Python script: ', error);
    }
}
