import fs from "fs";
const path = require("path");

export function generateExperimentierenDataMain(parameter: any) {
    console.log('hier : ', parameter);
    const filePath = path.join(__dirname, "/internData/frontendUserData.json");
    
	let jsonString = JSON.stringify(parameter, null, 4);

	
	try {
		fs.writeFileSync(filePath, jsonString, "utf-8");
		return true;
	} catch (error) {
		return false;
	}
    return true;
}