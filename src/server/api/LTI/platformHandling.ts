const lti = require("ltijs").Provider;

import { Router } from "express";

export const PlatformRoutes = (router: Router) => {
	// Grading route
	router.post("/addLTIPlatform", async (req, res) => {
		try {
			const platform = req.body.platform;

			const registeredPlatform = await lti.registerPlatform(platform);

			return res.status(201).send(registeredPlatform);
		} catch (err) {
			console.log(err.message);
			return res.status(500).send({ err: err.message });
		}
	});

	return router;
};
