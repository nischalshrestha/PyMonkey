from monkey import ast
from monkey import object

def DefineMacros(program, env):
    definitions = []
    for i, statement in enumerate(program.statements):
        if is_macro_definition(statement):
            add_macro(statement, env)
            definitions.append(i)

    for i in definitions[::-1]:
        definition_index = i
        program.statements = program.statements[:definition_index] + program.statements[definition_index+1:]

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