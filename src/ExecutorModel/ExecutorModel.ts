import { RNG } from "../Util/Randomizer";

export interface TaskConfiguration {
	taskName: string;
}

export interface ExecutionParameters {
	[key: string]: any;
	seed: string | number;
}

export type ExecutionNodeID = string;
export type ExecutionEdgeID = string;

export class ExecutionGraphNode<T> {
	private id: ExecutionNodeID;

	constructor() {}
}

export class ExecutionGraphEdge<T> {
	private id: ExecutionEdgeID;
	private from: ExecutionNodeID;
	private to: ExecutionNodeID;

	constructor() {}
}

export class ExecutionGraph {
	constructor() {}

	public addNode() {}
	public removeNode() {}

	public addEdge() {}
	public removeEdge() {}
}

export class ExecutorModel {
	constructor(private model: ExecutionGraph) {}

	public execute() {}

	private generateExecutionPlan() {}
}
