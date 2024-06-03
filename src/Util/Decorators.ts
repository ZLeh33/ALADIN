import { performance } from "perf_hooks";
// Experimental shim for advanced reflection concepts like runtime type-information (ReturnType, ParameterType) access
import "reflect-metadata";

export function Description(data: any) {
	return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
		Reflect.defineMetadata(
			propertyKey,
			{
				// keep previously assigned metadata
				...Reflect.getMetadata(propertyKey, target),
				description: data,
			},
			target
		);
		return descriptor;
	};
}

// common decorator
export const log = () => {
	return (_target: any, propertyKey: string, descriptor: PropertyDescriptor) => {
		const originalMethod = descriptor.value;

		descriptor.value = async function (...args: any[]) {
			const start = performance.now();

			const result = await originalMethod.apply(this, args);

			const finish = performance.now();

			const ms = Math.round(finish - start);
			console.log(`[${propertyKey}] ${ms}ms`);

			return result;
		};

		return descriptor;
	};
};

// Decorator to log class method or all class methods with Reflect
export function Log(): MethodDecorator & ClassDecorator {
	return (target: any, key?: string, descriptor?: TypedPropertyDescriptor<any>) => {
		if (descriptor) {
			// method decorator
			return log()(target, key, descriptor);
		}

		const methodNames = Reflect.ownKeys(target.prototype);
		methodNames.forEach((methodName: string) => {
			if (methodName !== "constructor") {
				const methodDescriptor = Reflect.getOwnPropertyDescriptor(target.prototype, methodName);

				const modifiedMethodDescriptor = log()(target, methodName, methodDescriptor);

				Reflect.defineProperty(target.prototype, methodName, modifiedMethodDescriptor);
			}
		});

		// class decorator
		return target;
	};
}
