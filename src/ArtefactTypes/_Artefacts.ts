// TODO - look for generic ways to import all sub types and Union them
// https://stackoverflow.com/questions/71831486/typescript-programmatic-generation-of-union-types-from-exports

import * as Graphs from "./Graph";
import * as Tensors from "./Tensor";

export type Artefact = Graphs.Graph | Tensors.Tensor;

export default { ...Graphs, ...Tensors };
