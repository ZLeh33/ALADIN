import { Router } from "express";

import { executeTask, IInstructionConfiguration } from "../TaskWrapper";

export const dbRoutes = (router: Router) => {
	router.post("/queryDB", async (req, res) => {
		let Producer;
		try {
			const { dbName, parameters, instruction } = req.body;
			const configurationObject: IInstructionConfiguration = { parameters, instruction };
			Producer = new RPCProducer(channel, `DB_${dbName}`, configurationObject);
			const response = await Producer.produceTask();
			res.status(200).json(JSON.stringify(response));
		} catch (error) {
			res.status(400).json(JSON.stringify(error));
		} finally {
			if (Producer) Producer.teardown();
		}
	});

	return router;
};

// import { Router } from "express";

// import { executeTask, IInstructionConfiguration } from "../TaskWrapper";

// export const dbRoutes = (router: Router) => {
// 	router.post("/queryDB", async (req, res) => {
// 		let Producer;
// 		try {
// 			const { dbName, parameters, instruction } = req.body;
// 			const configurationObject: IInstructionConfiguration = { parameters, instruction };
// 			const response = await executeTask(configurationObject);
// 			res.status(200).json(JSON.stringify(response));
// 		} catch (error) {
// 			res.status(400).json(JSON.stringify(error));
// 		}
// 	});

// 	return router;
// };
