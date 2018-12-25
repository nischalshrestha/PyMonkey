"""
Functions to assist in finding macros and expanding them
"""

from monkey import ast
from monkey import object
from monkey import evaluator as e

def ExpandMacros(program, env):
    def modifier(node):
        call_expression = node
        if not isinstance(call_expression, ast.CallExpression):
            return node
        macro = is_macro_call(call_expression, env)
        if not macro:
            return node 
        args = quote_args(call_expression)
        eval_env = extend_macro_env(macro, args)
        evaluated = e.Eval(macro.body, eval_env)
        quote = evaluated
        if not isinstance(quote, object.Quote):
            sys.exit('we only support returning AST-nodes from macros')
        return quote.node
    return ast.Modify(program, modifier)

def is_macro_call(exp, env):
    identifier = exp.function
    if not isinstance(identifier, ast.Identifier):
        return None
    obj = env.get(identifier.value)
    if not obj:
        return None
    macro = obj
    if not isinstance(macro, object.Macro):
        return None
    return macro

def quote_args(exp):
    args = []
    for a in exp.arguments:
        args.append(object.Quote(a))
    return args

def extend_macro_env(macro, args):
    extended = e.new_enclosed_environment(macro.env)
    for pidx, p in enumerate(macro.parameters):
        extended.set_name(p.value, args[pidx])
    return extended

def DefineMacros(program, env):
    definitions = []
    for i, statement in enumerate(program.statements):
        if is_macro_definition(statement):
            add_macro(statement, env)
            definitions.append(i)

    for i in definitions[::-1]:
        definition_index = i
        program.statements = \
            program.statements[:definition_index] \
            + program.statements[definition_index+1:]

def is_macro_definition(node):
    let_statement = node
    if not isinstance(let_statement, ast.LetStatement):
        return False
    if not isinstance(let_statement.value, ast.MacroLiteral):
        return False
    return True

def add_macro(stmt, env):
    let_statement = stmt
    macro_literal = let_statement.value
    macro = object.Macro(macro_literal.parameters, env, macro_literal.body)
    env.set_name(let_statement.name.value, macro)


