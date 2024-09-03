import { float } from 'aws-sdk/clients/cloudfront';
import { exec } from 'child_process';
import * as fs from 'fs';

/* Funktion für die ausführung des Python-Skripts (DecisionTreeTask.py) */
function runPythonScript(scriptPath: string, args: string[]): Promise<string> {
    return new Promise((resolve, reject) => {
        const command = `python ${scriptPath} ${args.join(' ')}`;
        exec(command, (error, stdout, stderr) => {
            if (error) {
                reject(error.message);
                return;
            }
            if (stderr) {
                reject(stderr);
                return;
            }
            resolve(stdout);
        });
    });
}

/* Funktionen, für die strukturierung der übergebenen Lösungeswerte aus CARPET in Listen */
function createNodesList(nodes: any[]): [string, string, number, string, any][] {
    // NODE (KEY, LEVEL, LABEL, PARENTEDGE, INFOGAIN)
    return nodes.map((node: any) => [node['key'], node['attributes']['level'], node['attributes']['name'], node['attributes']['parentedge'], node['attributes']['infogain']]);
}

function createEdgesList(edges: any[]): [string, any, string, string, string, string, string, float][] {
    // EDGE (KEY, LEVEL, LABEL, PARENTKEY, PARENTNODELABEL, CHILDKEY, CHILDNODELABEL, ENTROPY)
    return edges.map((edge: any) => [edge['key'], edge['attributes']['level'], edge['attributes']['name'], edge['source'], edge['attributes']['parentnode'], edge['target'], edge['attributes']['childnode'], edge['attributes']['entropy']]);
}

/* Wrapper-Funktion */
export async function DecisionTreeValidator(graph: any) {
    const nodes = graph['graph']['nodes'];
    const edges = graph['graph']['edges'];

    const actual_nodes = createNodesList(nodes);
    const actual_edges = createEdgesList(edges);

    console.log("--- Erhaltener DecisionTree ---");
    console.log("Nodes: \n", actual_nodes);
    console.log("Edges: \n", actual_edges);

	try {
		const pythonScriptPath = 'src/Tasks/DecisionTrees/DecisionTreeTask.py';
        const jsonStringNodes = JSON.stringify(actual_nodes);
        const jsonStringEdges = JSON.stringify(actual_edges);

        const modifiedJsonStringNodes = jsonStringNodes.replace(/"([^"]+)"/g, (_, p1) => `'${p1}'`);
        const modifiedJsonStringEdges = jsonStringEdges.replace(/"([^"]+)"(,|\])/g, (_, p1, p2) => `'${p1}'${p2}`);

        const argumentsToPythonScript = [modifiedJsonStringNodes, modifiedJsonStringEdges];

		const result = await runPythonScript(pythonScriptPath, argumentsToPythonScript);
        const parsedResult = JSON.parse(result);

        return {'solution_nodes_list': parsedResult['nodes'], 'solution_edges_list': parsedResult['edges'], 'status': parsedResult['finished'], 'entropies': parsedResult['entropies']}

	} catch(error) {
		console.error('Error running Python script: ', error);
	}
}
