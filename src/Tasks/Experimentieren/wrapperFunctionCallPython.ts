
import { record } from "fp-ts";
import { lastIndexOf } from "lodash";
import path from 'path';

import { 
	saveObjectAsJsonFile, 
	getValueByPathFromJson,
    extractFunctionData
} from "./Utils";



interface ILatexDataItem {
	inputType		?: string;
	value 			?: string;
	selectedOption 	?: string;
    functionName    ?: string;
    parameters      ?: Array<any>
}

type LatexData = Record<string,ILatexDataItem>;

const selectValueOptions = {
    callFunction : 'funktion aufruf',
    initFromPath : 'vom pfad initialisieren'
} as const;
type selectValueOptions = (typeof selectValueOptions)[keyof typeof selectValueOptions];

async function resolveInputValue(latexData: LatexData): Promise<LatexData | boolean> {
    if (Object.keys(latexData).length === 0) return false;

    for (const key of Object.keys(latexData)) {
        const elementData = latexData[key];

        if (!elementData?.selectedOption) continue;

        const option: string = elementData.selectedOption.toLowerCase();
        if (!option || option.length === 0) continue;

        switch (option) {
            case selectValueOptions.initFromPath: {
                const [fileName, pathKey] = elementData.value.split(':');

                const filePath = path.join(__dirname, 'internData', `${fileName}.json`);

                const newValue: string = getValueByPathFromJson(filePath, pathKey);
                elementData.value = newValue;
                break;
            }

            case selectValueOptions.callFunction : {
                
                const functionData = extractFunctionData(elementData.value);
                latexData[key] = {
                    ...elementData,
                    ...functionData
                }
                const functionName = latexData[key].functionName;
                const parameters : any = latexData[key].parameters;
                
                const utils = await import('./Utils');
                latexData[key].value = (utils as any)[functionName](...parameters as any[]);
                
                break;
            }
            default:
                break;
        }
    }
    
    return latexData;
}

export async function generateExperimentierenDataMain(userDataObject: any) {
    let latexData = await resolveInputValue(userDataObject?.parameters?.latexData as LatexData);
	
	if(!latexData) return null;
	userDataObject.parameters.latexData = latexData;

	const check = saveObjectAsJsonFile(userDataObject,`${__dirname}/internData/frontendUserData.json`);
    return check;
}