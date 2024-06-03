import { createNoise3D } from "simplex-noise";
import alea from "alea";
import { ArtefactGenerator, ArtefactGeneratorParameters } from "../GeneratorBaseClass";
import { Matrix } from "../../ArtefactTypes/Tensor";

export interface SimplexNoise3DGeneratorParameters extends ArtefactGeneratorParameters {
	gridX: number;
	gridY: number;
	scale: number;
}

export class SimplexNoise3DGenerator extends ArtefactGenerator<Matrix<number>> {
	public generateArtefact(parameters: SimplexNoise3DGeneratorParameters): Matrix<number> {
		const { gridX, gridY, scale, seed } = parameters;
		return this.generateNoise(gridX, gridY, scale, seed);
	}

	private generateNoise(gridX: number, gridY: number, scale: number, seed: string | number): Matrix<number> {
		const noise3D = createNoise3D(alea(seed));

		const noiseGrid = [];
		for (let x = 0; x < gridX; x++) {
			noiseGrid[x] = [];
			for (let y = 0; y < gridY; y++) {
				const noise = (noise3D(x / 16, y / 16, 0 / 16) * 0.5 + 0.5) * scale;
				noiseGrid[x][y] = noise;
			}
		}
		return noiseGrid;
	}
}
