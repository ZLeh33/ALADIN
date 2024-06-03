export type Graphs = "";

export type NodeID = string;
export type EdgeID = string;

export interface Node {
	id: string;
	neighbours: Array<Node>;
}
export interface Edge {
	id: string;
}
export interface DiEdge {
	from: NodeID;
	to: NodeID;
}

export interface Graph {
	nodes: Array<Node>;
	edges: Array<Edge>;
}

export interface DiGraph {
	nodes: Array<Node>;
	edges: Array<DiEdge>;
}

export interface MultiGraph extends Graph {}
export interface MultiDiGraph extends DiGraph {}
