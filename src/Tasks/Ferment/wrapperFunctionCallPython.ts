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

function parameterBearbeiten(parameter: any){
	//Überprüfen, ob parameter ein String ist und wenn ja, ihn parsen
    let frontendEingaben: any;
	if (parameter === undefined || parameter === null) {
        throw new Error("Parameter ist undefined oder null.");
    }
    if (typeof parameter === "string") {
        try {
            frontendEingaben = JSON.parse(parameter);
        } catch (error) {
            throw new Error("Fehler beim Parsen des JSON-Strings: " + error.message);
        }
    } else if (typeof parameter === "object") {
        frontendEingaben = parameter;
    } else {
        throw new Error("Ungültiges Eingabeformat für parameter.");
    }

    // Einige Schlüsseln Schlüssel entfernen und dessen Inhalt verschieben
    if (frontendEingaben && frontendEingaben.parameters) {
        // Inhalt von "parameters" ins Hauptobjekt verschieben
        Object.assign(frontendEingaben, frontendEingaben.parameters);
        // Schlüssel entfernen
        delete frontendEingaben.parameters;
		delete frontendEingaben.type;
		delete frontendEingaben.task;
		delete frontendEingaben.instruction;
		delete frontendEingaben.language;
    }

    // Schlüsselnamen im Objekt ändern
    const renameKey = (obj: any, oldKey: string, newKey: string) => {
        if (obj.hasOwnProperty(oldKey)) {
            obj[newKey] = obj[oldKey];
            delete obj[oldKey];
        }
        for (const key in obj) {
            if (obj.hasOwnProperty(key) && typeof obj[key] === 'object' && obj[key] !== null) {
                renameKey(obj[key], oldKey, newKey);
            }
        }
    };
    renameKey(frontendEingaben, "nodeAmount", "Modell");
    renameKey(frontendEingaben, "seed", "PhasenAnzahl");
		
	let phasenanzahl = parseInt(frontendEingaben.PhasenAnzahl);
	frontendEingaben.PhasenAnzahl	=	phasenanzahl;
	
	let zuluft 		= 	[];
	let feed 		= 	[];
	let drehzahl	=	[];
	let druck		=	[];
	let dauer		=	[];
	let bolusC		=	[];
	let bolusN		=	[];
	for(let i=0 ; i < phasenanzahl;i++){
		if (Array.isArray(frontendEingaben.userDataMatrix[i][0])){
			zuluft 	[i] = 	parseFloat(frontendEingaben.userDataMatrix[i][0][0]);
			feed	[i]	=	parseFloat(frontendEingaben.userDataMatrix[i][2][0]);
			drehzahl[i]	=	parseFloat(frontendEingaben.userDataMatrix[i][4][0]);
			druck	[i]	=	parseFloat(frontendEingaben.userDataMatrix[i][5][0]);
			dauer	[i]	=	parseFloat(frontendEingaben.userDataMatrix[i][6][0]);
			//! muss gefragt ob richtig sind
			bolusC	[i]	=	parseFloat(frontendEingaben.userDataMatrix[i][1][0]);
			bolusN	[i]	=	parseFloat(frontendEingaben.userDataMatrix[i][3][0]);
		}
		else{
			zuluft 	[i] = 	parseFloat(frontendEingaben.userDataMatrix[i][0]);
			feed	[i]	=	parseFloat(frontendEingaben.userDataMatrix[i][2]);
			drehzahl[i]	=	parseFloat(frontendEingaben.userDataMatrix[i][4]);
			druck	[i]	=	parseFloat(frontendEingaben.userDataMatrix[i][5]);
			dauer	[i]	=	parseFloat(frontendEingaben.userDataMatrix[i][6]);
			//! muss gefragt ob richtig sind
			bolusC	[i]	=	parseFloat(frontendEingaben.userDataMatrix[i][1]);
			bolusN	[i]	=	parseFloat(frontendEingaben.userDataMatrix[i][3]);
		}
	}
	delete frontendEingaben.userDataMatrix;

	frontendEingaben.Dauer		=	dauer;
	frontendEingaben.Druck		=	druck;
	frontendEingaben.Drehzahl 	=	drehzahl;
	frontendEingaben.Zuluft		=	zuluft;
	frontendEingaben.BolusC		=	bolusC;
	frontendEingaben.Feed 		=	feed;
	frontendEingaben.BolusN		= 	bolusN;

	let temperatur = 0;
	let dO = 0;
	let startbiomasse	=	0;
	if(frontendEingaben.userDataInputFelder){
		temperatur = parseFloat(frontendEingaben.userDataInputFelder.T);
		dO = parseFloat(frontendEingaben.userDataInputFelder.DO);
		startbiomasse	=	parseFloat(frontendEingaben.userDataInputFelder.BTM);
		
		delete frontendEingaben.userDataInputFelder;

		frontendEingaben.temperatur		=	temperatur;
		frontendEingaben.startbiomasse	=	startbiomasse;
		frontendEingaben.do				=	dO;
	}
	

	console.log(bolusC);
    // Pfad zur JSON-Datei definieren
    const filePfade = path.join(__dirname, "/interne_daten/Input2.json");

    // JSON.stringify mit einer Replacer-Funktion
    let jsonString = JSON.stringify(frontendEingaben, null, 4);

    // Datei schreiben
    try {
        fs.writeFileSync(filePfade, jsonString, "utf-8");
		return true;
    } catch (error) {
		return false;
        //throw new Error("Fehler beim Schreiben der Datei: " + error.message);
		
    }
}




export async function generateFermentationDataMain(parameter: any) {
	let check =  parameterBearbeiten(parameter);
	let result = { foo: "bar" };
	try {
		let pythonScriptPath = "generateFermentationData.py";
		pythonScriptPath = path.join(__dirname, pythonScriptPath);
		//console.log(parameter["distance"]);

		const argumentsToPythonScript = [...Object.values(parameter)];
		//delete argumentsToPythonScript[2];
        //console.log("ARGUMENTS TO PYTHON SCRIPT");
		//console.log(argumentsToPythonScript);
		(await runPythonScript(pythonScriptPath, argumentsToPythonScript)) as any;

		//let foo = fs.readFileSync(path.join(__dirname, 'data.json'), 'utf-8');

		result = JSON.parse(fs.readFileSync(path.join(__dirname, "data.json"), "utf-8"));
		const filePath = path.join(__dirname, "data.json");
		fs.writeFileSync(filePath, JSON.stringify(result, null, 2), "utf-8");
        //console.log(result);
		//insofern kryptsiche Zeichen in der JSON Ausgabe vorhanden sind .> Workaround mittels File
	} catch (error) {
		console.error("Error running Python script:", error);
	}
	return result;
}
