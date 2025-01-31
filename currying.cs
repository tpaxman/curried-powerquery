// pipe
(functions as list) as function =>
    (input as any) as any =>
        List.Accumulate(functions, input, (x,f) => f(x))


// pipeUnlisted
Function.From(
    type function (f as function) as function,
    pipe
)


// run_pipe
Function.From(
    type function (input as any, func as function) as any,
    (input_and_functions as list) =>
        let
            input = List.First(input_and_functions),
            functions = List.RemoveFirstN(input_and_functions, 1)
        in
            Function.Invoke(pipeUnlisted, functions)(input)
)

// makeDataFirst

(origFunc as function) as function =>
    let
        formSignature = (returnType as type, params as record) as record =>
            [ReturnType = returnType, Parameters = params],

        origFuncType = Value.Type(origFunc),
        origReturnType = Type.FunctionReturn(origFuncType),
        origParamTypes = Type.FunctionParameters(origFuncType),
        origNumRequiredParams = Type.FunctionRequiredParameters(origFuncType),

        firstParamName = Record.FeldNames(origParamTypes){0},
        firstParamType = Record.SelectFields(origParamTypes, firstParamName),
        otherParamTypes = Record.RemoveFields(origParamTypes, firstParamName),

        outerReturnType = type function,
        outerSignature = formSignature(outerReturnType, otherParamTypes),
        outerNumRequiredParams = origNumRequiredParams - 1,
        outerFuncType = Type.ForFunction(outerSignature, outerNumRequiredParams),

        innerReturnType = origReturnType,
        innerSignature = formSignature(innerReturnType, firstParamType),
        innerNumRequiredParams = List.Min({1, origNumRequiredParams}),
        innerFuncType = Type.ForFunction(innerSignature, innerNumRequiredParams),

        outerFunc = Function.From(
            outerFuncType,
            (otherArgs as list) as function =>
                Value.ReplaceType(
                    (innerArg) => Function.Invoke(origFunc, {innerArg} & otherArgs),
                    innerFuncType
                )
        )
    in
        outerFunc


// 
