import { Router } from "express";

export const userRoutes = (router: Router) => {
	router.get("/getLanguage", async (req, res) => {
		try {
		} catch (error) {
			res.status(400).json(JSON.stringify(error));
		}
	});

	return router;
};
