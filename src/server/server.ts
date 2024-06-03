require("dotenv").config();
const path = require("path");
const router = require("express").Router();
// const routes = require("./api/LTI/advantage");
import { LTIAdvantageRoutes } from "./api/LTI/advantage";
import { PlatformRoutes } from "./api/LTI/platformHandling";

const lti = require("ltijs").Provider;

import { TaskRouteManager, ISerializedTaskRoute } from "./api/TaskRouteManager";
import { taskParts, tasks } from "./api/TaskGraphManager";
const serializedRoutes: Array<ISerializedTaskRoute> = taskParts.API;

// Setup
lti.setup(
	process.env.LTI_KEY,
	{
		url: `mongodb://${process.env.MONGO_HOST}:${process.env.MONGO_PORT}`,
		connection: { user: process.env.MONGO_USER, pass: process.env.MONGO_PW },
	},
	{
		appRoute: "/launch",
		staticPath: path.join(__dirname, "./public"), // Path to static files
		cookies: {
			secure: true, // Set secure to true if the testing platform is in a different domain and https is being used
			sameSite: "None", // Set sameSite to 'None' if the testing platform is in a different domain and https is being used
		},
		devMode: false, // Set DevMode to true if the testing platform is in a different domain and https is not being used,
		bodyParserOpt: {
			json: {
				limit: "50mb",
			},
			urlencoded: {
				extended: false,
				limit: "50mb",
			},
		},
	}
);

const taskRouteManager = new TaskRouteManager(lti.app);
taskRouteManager.addRoute(serializedRoutes);

lti.whitelist(new RegExp(/^\/api\/.*/));
lti.whitelist(new RegExp(/^\/.*/));

// When receiving successful LTI launch redirects to app
lti.onConnect(async (token: any, req: any, res: any) => {
	if (token && token.hasOwnProperty("platformContext")) {
		const task = `task/${token.platformContext.custom.task}`;
		lti.redirect(res, `/${task}`);
	} else {
		lti.redirect(res, `/`);
	}
});

// When receiving deep linking request redirects to deep screen
lti.onDeepLinking(async (token: any, req: any, res: any) => {
	return lti.redirect(res, "/deeplink", { newResource: true });
});

(async () => {
	const { taskGraph } = await import("./api/TaskGraphManager");
	const { replayRoutes } = await import("./api/Replay");
	lti.app.use("/api", taskGraph(router));
	lti.app.use("/api", replayRoutes(router));
	lti.app.use("/api", PlatformRoutes(router));

	lti.app.use("", LTIAdvantageRoutes(router));
})();

// Wildcard route to deal with redirecting to Vue routes
router.get("/*", (req: any, res: any) => {
	if (/fetchTasklist/i.test(req.originalUrl)) {
		const names = Object.values(tasks).map((task) => task.name);
		res.status(200).json(JSON.stringify(names));
	} else {
		res.sendFile(path.join(__dirname, "./public/index.html"));
	}
});

// Setting up routes
lti.app.use(router);

// Setup function
const setup = async () => {
	await lti.deploy({ port: "8000" });
	/**
	 * Register platform
	 */
	const livePlatform = await lti.registerPlatform({
		url: "https://bildungsportal.sachsen.de/opal",
		name: "OPAL",
		clientId: "OPALADIN_Live",
		authenticationEndpoint: "https://bildungsportal.sachsen.de/opal/ltiauth/",
		accesstokenEndpoint: "https://bildungsportal.sachsen.de/opal/restapi/lti/token",
		authConfig: { method: "JWK_SET", key: "https://bildungsportal.sachsen.de/opal/restapi/lti/keys" },
	});

	const previewPlatform = await lti.registerPlatform({
		url: "https://bildungsportal.sachsen.de/preview/opal",
		name: "OPAL_Preview",
		clientId: "OPALADIN_Preview",
		authenticationEndpoint: "https://bildungsportal.sachsen.de/preview/opal/ltiauth/",
		accesstokenEndpoint: "https://bildungsportal.sachsen.de/preview/opal/restapi/lti/token",
		authConfig: { method: "JWK_SET", key: "https://bildungsportal.sachsen.de/preview/opal/restapi/lti/keys" },
	});

	const referencePlatform = await lti.registerPlatform({
		url: "1",
		name: "OPALexample",
		clientId: "OPALexampleID",
		authenticationEndpoint: "https://lti-ri.imsglobal.org/platforms/4244/authorizations/new",
		accesstokenEndpoint: "https://lti-ri.imsglobal.org/platforms/4244/access_tokens",
		authConfig: {
			method: "RSA_KEY",
			key:
				"-----BEGIN PUBLIC KEY----- MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAq9GHlEtAolsmxr5wpaUM\n" +
				"J6/LccSKH1I/cDlh5yYEsp2FYD6ppFpjcyCAZXfXOScbz+LS6hmPpscrAYj7noKG\n" +
				"MbzPKAuDh28dC5CN+jUpQxu2FyRh95m4aLzzIq6pYnmCMdPZ21EtF/rJhQvmPa66\n" +
				"vlp4l9lwhGtPgVS8tJcNh9XawoogZfbw067mT/YxSpqJHwNjnO1uZ6YyIykT3tEF TvGqjlIouy/1oCjXgmdKeSHPu+Xr/Kj2RsN2M4DyrIIKEE2VFL+R1ugLct/OzvRk\n" +
				"aTqqWuZLQCeOojfKwDnI081GxLmrowWXn8sWnrWpUn5JhlM+znL/8MX1qJyss0NQ qwIDAQAB -----END PUBLIC KEY-----",
		},
	});
};

setup();
