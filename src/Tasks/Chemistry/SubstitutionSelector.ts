export interface SubstitutionParameters {
	seed: string;
}

export type Position = "para" | "meta" | "orto";

import { RNG } from "../../Util/Randomizer";

export const selectSubstitution = (parameters: SubstitutionParameters) => {
	const { seed } = parameters;

	const rng = new RNG(seed);

	const reagentIndex = rng.intBetween(0, reagents.length);
	const substituentIndex = rng.intBetween(0, substituents.length);

	const reagent = reagents[reagentIndex];

	const selectedSubstituent = substituents[substituentIndex];
	const position = selectedSubstituent.position as Position;

	return {
		smiles: productBuilderBasedOnPosition[position](selectedSubstituent.firstSubstituent, reagent.smiles),
		position: position,
		parameter: selectedSubstituent.effects.join(", "),
		hasOverReacted: selectedSubstituent.hasOverReacted,
		reagent: reagent.smiles,
		reactionSmiles: `${selectedSubstituent.firstSubstituent}c1ccccc1>${reagent.smiles}>`,
		firstSubstituent: selectedSubstituent.firstSubstituent,
		benzol: "c1cccc1",
		reagentText: reagent.reagent,
	};
};

const productBuilderBasedOnPosition: { [positon in Position]: Function } = {
	para: (firstSubstituentSmiles: string, reagentSmiles: string) =>
		`${firstSubstituentSmiles}c1ccc(${reagentSmiles})cc1`,
	meta: (firstSubstituentSmiles: string, reagentSmiles: string) =>
		`${firstSubstituentSmiles}c1cc(${reagentSmiles})ccc1`,
	orto: (firstSubstituentSmiles: string, reagentSmiles: string) => "[error]",
};

const answer = {
	firstSubstituent: "[NH3+]",
	benzol: "c1cccc1",
	reagentText: "reagentAlpha",
};

const reagents = [
	{
		reagent: "Bromierung",
		smiles: "BrBr",
		inMolecule: "Br",
	},
	{
		reagent: "reagentAlpha",
		smiles: "ClCl",
		inMolecule: "Cl",
	},
	{
		reagent: "reagentBeta",
		smiles: "II",
		inMolecule: "I",
	},
	{
		reagent: "reagentGamma",
		smiles: "FF",
		inMolecule: "F",
	},
];

const substituents = [
	{
		firstSubstituent: "[O]",
		effects: ["+M"],
		position: "para",
		hasOverReacted: false,
	},
	{
		firstSubstituent: "N",
		effects: ["+M", "-I"],
		position: "para",
		hasOverReacted: false,
	},
	{
		firstSubstituent: "[OH]",
		effects: ["+M", "-I"],
		position: "para",
		hasOverReacted: false,
	},
	{
		firstSubstituent: "O=C([R])N",
		effects: ["+M", "-I"],
		position: "para",
		hasOverReacted: false,
	},
	{
		firstSubstituent: "O=C([R])O",
		effects: ["+M", "-I"],
		position: "para",
		hasOverReacted: false,
	},
	{
		firstSubstituent: "c1ccccc1",
		effects: ["+M", "-I"],
		position: "para",
		hasOverReacted: false,
	},
	{
		firstSubstituent: "[A]",
		effects: ["+M", "-I"],
		position: "para",
		hasOverReacted: false,
	},
	{
		firstSubstituent: "[Cl]",
		effects: ["+I"],
		position: "para",
		hasOverReacted: false,
	},
	{
		firstSubstituent: "[Br]",
		effects: ["+I"],
		position: "para",
		hasOverReacted: false,
	},
	{
		firstSubstituent: "[NH3+]",
		effects: ["-I"],
		position: "meta",
		hasOverReacted: false,
	},
	{
		firstSubstituent: "O=C([R])",
		effects: ["-M", "-I"],
		position: "meta",
		hasOverReacted: false,
	},
	{
		firstSubstituent: "[CN]",
		effects: ["-M", "-I"],
		position: "meta",
		hasOverReacted: false,
	},
	{
		firstSubstituent: "O=S(=O)(O)",
		effects: ["-M", "-I"],
		position: "meta",
		hasOverReacted: false,
	},
	{
		firstSubstituent: "O=[N+](O)",
		effects: ["-M", "-I"],
		position: "meta",
		hasOverReacted: false,
	},
];
