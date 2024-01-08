import { exec } from "child_process";
import fs from "fs";
const path = require("path");

function runPythonScript(scriptPath: string, args: any): Promise<string> {
	try {
		return new Promise((resolve, reject) => {
            
			const command = `python3 ${scriptPath} ${args.join(" ")}`;
            console.log(command)
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
	} catch {
		console.log("Error");
	}
}

export async function clusterAnalysisMain(parameter: any) {
	let result = { foo: "bar" };
	console.log(parameter);
	//console.log(result);
	try {
		let pythonScriptPath = "clusterAnalysis.py";
		pythonScriptPath = path.join(__dirname, pythonScriptPath);
		//console.log(pythonScriptPath);
        console.log(parameter['distance']);

		const argumentsToPythonScript = [...Object.values(parameter),...parameter['nodeRange']];
        //delete argumentsToPythonScript[2];
        console.log(argumentsToPythonScript);
		(await runPythonScript(pythonScriptPath, argumentsToPythonScript)) as any;

		//let foo = fs.readFileSync(path.join(__dirname, 'data.json'), 'utf-8');
		//console.log(foo);

		result = JSON.parse(fs.readFileSync(path.join(__dirname, "data.json"), "utf-8"));

		//insofern kryptsiche Zeichen in der JSON Ausgabe vorhanden sind .> Workaround mittels File
	} catch (error) {
		console.error("Error running Python script:", error);
	}
	return result;
}
