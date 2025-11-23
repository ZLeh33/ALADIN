import fs from "fs";
const path = require("path");



export function saveObjectAsJsonFile(dataObject: Record<string, any>, filePath: string) : boolean{ //filePath : absolute
	let jsonString = JSON.stringify(dataObject, null, 4);
	
	try {
		fs.writeFileSync(filePath, jsonString, "utf-8");
		return true;
	} catch (error) {
		return false;
	}
}

export function getValueByPathFromJson(filePath: string, pathKey: string): any | null {
    try {
        const fileContent = fs.readFileSync(filePath, 'utf-8');
        const jsonData = JSON.parse(fileContent);

        const parts = pathKey.split('__');

        let current: any = jsonData;

        for (const part of parts) {
            if (current == null) return null; 

            if (Array.isArray(current)) {
                const index = parseInt(part, 10);
                if (isNaN(index) || index < 0 || index >= current.length) return null;
                current = current[index];
            } else if (typeof current === 'object') {
                if (!(part in current)) return null;
                current = current[part];
            } else {
                return null;
            }
        }

        return current;
    } catch (err) {
        console.error('Error reading JSON file:', err);
        return null;
    }
}

export function extractFunctionData (str : string) : object{
    const functionName = str.substring(0,str.indexOf('('));
    let parametersAsString = str.substring(str.indexOf('(')+1, str.lastIndexOf(')')).split(';');

    return {
        functionName : functionName,
        parameters : parametersAsString.map(param => JSON.parse(param))
    }
}

export function callFunction(arg1:any, arg2:any, arg3: any ): any{
    console.log(arg1);
    console.log(arg2);
    console.log(arg3);
    return 200;
}

