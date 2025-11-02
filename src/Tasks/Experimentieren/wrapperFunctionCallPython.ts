
import { record } from "fp-ts";
import { lastIndexOf } from "lodash";
import { 
	saveObjectAsJsonFile, 
	getValueByPathFromJson,
	callFunction
} from "./Utils";

import path from 'path';

interface ILatexDataItem {
	inputType		?: string;
	value 			?: string;
	selectedOption 	?: string; 
}

type LatexData = Record<string,ILatexDataItem>;


function resolveInputValue(latexData: LatexData): LatexData | boolean {
    if (Object.keys(latexData).length === 0) return false;

    for (const key of Object.keys(latexData)) {
        const elementData = latexData[key];

        if (!elementData?.selectedOption) continue;

        const option: string = elementData.selectedOption.toLowerCase();
        if (!option || option.length === 0) continue;

        switch (option) {
            case 'vom pfad initialisieren': {
                const [fileName, pathKey] = elementData.value.split(':');

                const filePath = path.join(__dirname, 'internData', `${fileName}.json`);

                const newValue: string = getValueByPathFromJson(filePath, pathKey);
                elementData.value = newValue;
                break;
            }

            case 'funktion aufruf': {
                const newValue : string = callFunction(elementData.value);
                elementData.value = newValue;
                break;
            }

            default:
                break;
        }
    }

    return latexData;
}

export function generateExperimentierenDataMain(userDataObject: any) {
    let latexData = resolveInputValue(userDataObject?.parameters?.latexData as LatexData);
	
	if(!latexData) return null;
	userDataObject.parameters.latexData = latexData;
	
	const check = saveObjectAsJsonFile(userDataObject,`${__dirname}/internData/frontendUserData.json`);
    return check;
}