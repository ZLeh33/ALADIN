import { RNG } from "../Util/Randomizer";

import Artefacts, { Artefact } from "../ArtefactTypes/_Artefacts";

export interface ArtefactGeneratorParameters {
	[key: string]: any;
	seed: string | number;
}

export interface ArtefactContainer {
	[key: string]: Artefact;
}

export abstract class ArtefactGenerator<T> {
	constructor(private rng: RNG) {}

	public abstract generateArtefact(parameters: ArtefactGeneratorParameters): T;
}
