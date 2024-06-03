export type Tensor =
	| NumericVector
	| StringVector
	| NumericStringVector
	| NumericMatrix
	| StringMatrix
	| NumericStringMatrix;

export type Vector<T> = Array<T>;

export type NumericVector = Array<number>;
export type StringVector = Array<string>;
export type NumericStringVector = Array<string | number>;

export type Matrix<T> = Array<Array<T>>;

export type NumericMatrix = Matrix<number>;
export type StringMatrix = Matrix<string>;
export type NumericStringMatrix = Matrix<string | number>;
