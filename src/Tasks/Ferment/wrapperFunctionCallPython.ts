import { exec } from "child_process";
import fs from "fs";
const path = require("path");

function runPythonScript(scriptPath: string, args: any): Promise<string> {
	try {
		return new Promise((resolve, reject) => {
			const command = `python ${scriptPath} ${args.join(" ")}`;
			console.log(command);
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

export async function generateFermentationDataMain(parameter: any) {
	let result = { foo: "bar" };
    console.log("PARAMETER:");
	console.log(parameter);
	try {
		let pythonScriptPath = "generateFermentationData.py";
		pythonScriptPath = path.join(__dirname, pythonScriptPath);
		//console.log(parameter["distance"]);

		const argumentsToPythonScript = [...Object.values(parameter.parameters)];
		//delete argumentsToPythonScript[2];
        //console.log("ARGUMENTS TO PYTHON SCRIPT");
		//console.log(argumentsToPythonScript);
		(await runPythonScript(pythonScriptPath, argumentsToPythonScript)) as any;

		//let foo = fs.readFileSync(path.join(__dirname, 'data.json'), 'utf-8');

		result = JSON.parse(fs.readFileSync(path.join(__dirname, "data.json"), "utf-8"));
        console.log(result);
		//insofern kryptsiche Zeichen in der JSON Ausgabe vorhanden sind .> Workaround mittels File
	} catch (error) {
		console.error("Error running Python script:", error);
	}
	return result;
}
