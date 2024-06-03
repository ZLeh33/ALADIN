import {
	GrGenModel,
	GrGenEdge,
	GrGenNode,
	GrGenEntityAttributeType,
	GrGenEdgeType,
} from "../../../../src/ArtefactGenerators/GraphGenerators/GraphRewriting/GrGenWrapper/GrGenModelWrapper";

const n = new GrGenNode("TestNode", true, { id: GrGenEntityAttributeType.INT, Type: GrGenEntityAttributeType.STRING });
const n2 = new GrGenNode("TestNode2", false, {}, ["TestNode"]);

const e = new GrGenEdge("TestEdge", GrGenEdgeType.ARBITRARY, true, {
	id: GrGenEntityAttributeType.INT,
	Type: GrGenEntityAttributeType.STRING,
});
const e2 = new GrGenEdge("TestEdge2", GrGenEdgeType.DIRECTED, false, {}, ["TestEdge"]);
const model = new GrGenModel([n, n2], [e, e2]);
const output = `abstract node class TestNode {
\tid: int;
\tType: string;
};
node class TestNode2 extends TestNode;
abstract arbitrary edge class TestEdge {
\tid: int;
\tType: string;
};
directed edge class TestEdge2 extends TestEdge;`;

describe("test GrGenModel output writer", () => {
	it("should return correctly edited GrGen-Model output", () => {
		expect(model.writeModel()).toBe(output);
	});
});

// it("should return 5 for add(2,3)", () => {
//     expect(add(2, 3)).toBe(5);
//   });
