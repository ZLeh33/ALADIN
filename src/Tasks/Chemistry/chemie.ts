const path = require("path");
const fs = require("fs");
class Answers {
  "Smiles:": string = "";
  "Position:": string = "";
  "Benzol:": string = "";
  "Ueberreaktion:": string = "";
  "Parameter:": string = "";
  "Erstsubsti:": string = "";
  "Zweitsubsti:": string = "";
  "Ergebnis:": boolean = false;
  "text": string = "";
  "SmilesReaction": string = "";

  ErgebnisRichtig(): void {
    this["Ergebnis:"] = true;
  }
}

export async function generatechemie(parameters: {}) {
  const datenVonTypeScript = { key: "value" };

  const { exec } = require("child_process");

  // Pfad zur Java-Laufzeitumgebung
  const javaPath = "java"; // Stellen Sie sicher, dass "java" im System-Pfad ist, oder geben Sie den vollständigen Pfad an

   //Pfad zur JAR-Datei
  const jarPath = path.join(
    __dirname,
     "/AladinJsonGenerator.jar"
   );

    //Befehl zum Ausführen der JAR-Datei
    const command = `${javaPath} -jar ${jarPath}`;

  // JAR-Datei ausführen
  exec(command, (error: Error, stdout: string, stderr: string) => {
   if (error) {
      console.error(`Fehler beim Ausführen der JAR-Datei: ${error.message}`);
  
     return;
    }
     console.log(`Erfolg`);
   });

  const directoryPath = ".";
  const jsonFileName = "Antwort.json";

  function readJsonFile(directory: string, filename: string): Promise<any> {
    const filePath = path.join(directory, filename);

    return new Promise((resolve, reject) => {
      fs.readFile(filePath, "utf8", (err: any, data: any) => {
        if (err) {
          reject(err);
        } else {
          try {
            const jsonDaten = JSON.parse(data);
            resolve(jsonDaten);
          } catch (jsonErr) {
            reject(jsonErr);
          }
        }
      });
    });
  }


  const result=await readJsonFile(directoryPath, jsonFileName)
  return result;

}
