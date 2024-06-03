import { RNG } from "../Util/Randomizer";

export abstract class ArtefactManipulator<P, T> {
	constructor(private rng: RNG) {}

	public abstract transform(args: P): T;
}

// export class GraphMatrixOverlay {
//     private generateGraph(grid: Array<Array<number>>, measurementRange: Array<number>): IGeoInterpolationGraph {
//         const [measurementMin, measurementMax] = measurementRange;
//         const measurementCount = this.rng.intBetween(measurementMin, measurementMax);

//         const [x] = randomSample(grid.keys(), 1, true, this.rng);
//         const [y] = randomSample(grid[x].keys(), 1, true, this.rng);
//         const unknownPoint: IMeasurementPoint = { id: 0, x, y, value: grid[x][y] };

//         const columnIndices = randomSample(grid.keys(), measurementCount, true, this.rng);
//         const measurementPoints: Array<IMeasurementPoint> = columnIndices.map((columnIndex, i) => {
//             const [rowIndex] = randomSample(grid[columnIndex].keys(), 1, true, this.rng);
//             return {
//                 id: i + 1,
//                 value: parseFloat(grid[columnIndex][rowIndex].toFixed(2)),
//                 x: columnIndex,
//                 y: rowIndex,
//                 distance: this.euclidianDistance([unknownPoint.x, unknownPoint.y], [columnIndex, rowIndex]),
//             };
//         });

//         return { unknownPoint, measurementPoints };
//     }
// }
