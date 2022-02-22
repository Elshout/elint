import common
import lexing

Source = common.Source
Program = common.Program

syntax_error = lexing.syntax_error

src_end = common.src_end
statement_end = common.statement_end
func = common.function
var = common.declaration_var
comma = common.symbol_comma
or_opr = common.declaration_or
and_opr = common.declaration_and
declr_if = common.declaration_if
declr_else = common.declaration_else
declr_while = common.declaration_while
declr_return = common.declaration_return
generate_parse_input = lexing.load_from
equals = common.equals
dual_equals = common.dual_equals
declr_not = common.declaration_not
cmp_less = common.cmp_less
cmp_more = common.cmp_more
symbol_plus = common.symbol_plus
symbol_minus = common.symbol_minus
symbol_asterisk = common.symbol_asterisk
symbol_slash = common.symbol_slash
literal_true = common.literal_true
literal_false = common.literal_false
literal_dbl = common.literal_dbl
literal_int = common.literal_int
literal_str = common.literal_string
parenthesis_left = common.parenthesis_left
parenthesis_right = common.parenthesis_right
qualifier = common.identifier_string
brace_left = common.brace_left
brace_right = common.brace_right


def end_of_code(program: Program) -> bool:
    return opr_at(program) == src_end


def opr_at(program: Program) -> int:
    return program.stream[program.current][0]


def expl_increment_if(program: Program, id_expected: int, err: str) -> None:
    if not increment_if(program, id_expected):
        if not program.ignore_err:
            program.ignore_err = True
            syntax_error(err, program.stream[program.current][1], program)


def sync(program: Program) -> None:
    program.ignore_err = False
    while not end_of_code(program):
        if program.stream[program.current - 1][0] == statement_end:
            return
        elif opr_at(program) == func:
            return
        elif opr_at(program) == var:
            return
        elif opr_at(program) == declr_if:
            return
        elif opr_at(program) == declr_while:
            return
        elif opr_at(program) == declr_return:
            return

        increment(program)


def increment_if(program: Program, id_expected: int) -> bool:
    if compare(program, id_expected):
        increment(program)
        return True

    return False


def increment(program: Program) -> None:
    if not end_of_code(program):
        program.current += 1


def compare(program: Program, cmp: int) -> bool:
    if end_of_code(program):
        return False

    return opr_at(program) == cmp


def process_call(program: Program):
    if not compare(program, parenthesis_right):
        expr(program)
        while increment_if(program, comma):
            expr(program)

    expl_increment_if(program, parenthesis_right, 'Expected ] after arguments')


def instr_load(program: Program):
    while not end_of_code(program):
        rule_dispatch(program, False)


def rule_dispatch(program: Program, is_in_func_body: bool):
    if increment_if(program, var):
        declr_var(program)
    elif increment_if(program, func):
        declr_func(program, is_in_func_body)
    else:
        stmt(program, is_in_func_body)

    if program.ignore_err:
        sync(program)


def declr_func(program: Program, is_invalid: bool):
    if compare(program, qualifier):
        pass  # Fetch function name
    expl_increment_if(program, qualifier, 'Expected function name')
    expl_increment_if(program, parenthesis_left, 'Expected [ after function name')

    if not compare(program, parenthesis_right):
        expl_increment_if(program, var, 'Expected parameter declaration')
        expl_increment_if(program, qualifier, 'Expected parameter name')

        while increment_if(program, comma):
            expl_increment_if(program, var, 'Expected parameter declaration')
            if compare(program, qualifier):
                pass  # Fetch param name
            expl_increment_if(program, qualifier, 'Expected parameter name')

    expl_increment_if(program, parenthesis_right, 'Expected ] to end function')
    expl_increment_if(program, brace_left, 'Expected /-> before function body')
    block(program)
    if is_invalid:
        syntax_error('Cannot declare function inside a block or another function',
                     program.stream[program.current][1], program)


def declr_var(program: Program):
    if compare(program, qualifier):
        pass  # Fetch var name

    expl_increment_if(program, qualifier, 'Expected qualified name for variable')

    if increment_if(program, equals):
        expr(program)

    expl_increment_if(program, statement_end, 'Expected ß after variable')


def stmt(program: Program, is_in_func: bool):
    if increment_if(program, brace_left):
        program.scope_depth += 1
        block(program)
        program.scope_depth -= 1
    elif increment_if(program, declr_if):
        cond_if(program, is_in_func)
    elif increment_if(program, declr_while):
        cond_repeat_if(program, is_in_func)
    elif increment_if(program, declr_return):
        stmt_return(program, is_in_func)

    stmt_expr(program)


def stmt_return(program: Program, is_in_func_body: bool):
    if not compare(program, statement_end):
        expr(program)  # Return value
    expl_increment_if(program, statement_end, 'Expected ß after return value')
    if not is_in_func_body:
        syntax_error('Cannot return outside a function', program.stream[program.current][1], program)


def cond_if(program: Program, is_in_func: bool):
    expl_increment_if(program, parenthesis_left, 'Expected [ after als')
    expr(program)
    expl_increment_if(program, parenthesis_right, 'Expected ] after condition')

    stmt(program, is_in_func)  # Branch on succeed

    if increment_if(program, declr_else):
        stmt(program, is_in_func)  # Else branch, if any


def cond_repeat_if(program: Program, is_in_func: bool):
    expl_increment_if(program, parenthesis_left, 'Expected [ after while')
    expr(program)
    expl_increment_if(program, parenthesis_right, 'Expected ] after condition')
    stmt(program, is_in_func)


def opr_or(program: Program):
    opr_and(program)
    while increment_if(program, or_opr):
        opr_and(program)


def opr_and(program: Program):
    equality(program)
    while increment_if(program, and_opr):
        equality(program)


def block(program: Program):
    while not compare(program, brace_right) and not end_of_code(program):
        rule_dispatch(program, True)

    expl_increment_if(program, brace_right, 'Expected >-/ after block')


def stmt_expr(program: Program):
    expr(program)
    expl_increment_if(program, statement_end, 'Expected ß after expression statement')


def expr(program: Program):
    assignment(program)


def assignment(program: Program):
    opr_or(program)

    if increment_if(program, equals):
        assignment(program)
        # Check if the result from the call to equality is a qualifier that can be assigned to and assign
        # it to the value from the above call to assignment, otherwise error out


def equality(program: Program):
    comparison(program)

    while increment_if(program, dual_equals):
        if increment_if(program, declr_not):
            pass
            # Operation checks for inequality, by default checks for equality
        comparison(program)


def comparison(program: Program):
    term(program)

    while increment_if(program, dual_equals) or increment_if(program, cmp_less) or increment_if(program, cmp_more):
        opr = program.stream[program.current - 1][0]
        if opr == dual_equals:
            if increment_if(program, cmp_less):
                pass
                # Left less than right
            elif increment_if(program, cmp_more):
                pass
                # Left more than right
        elif opr == cmp_less:
            pass
        elif opr == cmp_more:
            pass
        term(program)


def term(program: Program):
    factor(program)

    while increment_if(program, symbol_plus) or increment_if(program, symbol_minus):
        opr = program.stream[program.current - 1][0]
        if opr == symbol_plus:
            pass
            # Addition
        elif opr == symbol_minus:
            pass
            # Subtraction
        factor(program)


def factor(program: Program):
    unary(program)

    while increment_if(program, symbol_asterisk) or increment_if(program, symbol_slash):
        opr = program.stream[program.current - 1][0]
        if opr == symbol_asterisk:
            pass
            # Multiplication
        elif opr == symbol_slash:
            pass
            # Division
        unary(program)


def unary(program: Program):
    if increment_if(program, declr_not) or increment_if(program, symbol_minus):
        opr = program.stream[program.current - 1][0]
        if opr == declr_not:
            pass
        elif opr == symbol_minus:
            pass
        unary(program)
        # A goal is to try to avoid actual recursion as much as possible
        # If someone can rewrite this out I'd appreciate it

    call(program)


def call(program: Program):
    primary(program)
    while increment_if(program, parenthesis_left):
        process_call(program)  # TODO pass callee to process_call


def primary(program: Program):
    if increment_if(program, literal_true):
        pass
        # True
    elif increment_if(program, literal_false):
        pass
        # False
    elif increment_if(program, literal_dbl):
        pass
        # Doubles
    elif increment_if(program, literal_int):
        pass
        # Ints
    elif increment_if(program, literal_str):
        pass
        # Strings. As mentioned, the actual runtime can support them just fine
    elif increment_if(program, parenthesis_left):
        expr(program)
        expl_increment_if(program, parenthesis_right, 'Expected ] after expression')
    elif increment_if(program, qualifier):
        pass
        # Qualified names
