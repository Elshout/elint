import random
import common

final = common.final
Final = common.Final
dataclass = common.dataclass

Program = common.Program
src_end = common.src_end
statement_end = common.statement_end
symbol_plus = common.symbol_plus
symbol_minus = common.symbol_minus
symbol_comma = common.symbol_comma
symbol_asterisk = common.symbol_asterisk
symbol_slash = common.symbol_slash
parenthesis_left = common.parenthesis_left
parenthesis_right = common.parenthesis_right
brace_left = common.brace_left
brace_right = common.brace_right
literal_int = common.literal_int
literal_dbl = common.literal_dbl
literal_string = common.literal_string
identifier_string = common.identifier_string

res: Final = {
    'richtig': common.literal_true,
    'falsch': common.literal_false,
    'als': common.declaration_if,
    'anders': common.declaration_else,
    'ist': common.equals,
    'nicht': common.declaration_not,
    'kleiner': common.cmp_less,
    'größer': common.cmp_more,
    'gleich': common.dual_equals,
    'oder': common.declaration_or,
    'und': common.declaration_and,
    'funktion': common.function,
    'var': common.declaration_var,
    'while': common.declaration_while,
    'return': common.declaration_return
}


@final
@dataclass
class Source:
    code: str = ''
    offset_begin: int = 0
    current_offset_abs: int = 0
    line: int = 1


def load_from(code: str) -> Program:
    sources = Source()
    sources.code = code
    program = Program()
    while not code_endpoint_reached(sources):
        sources.offset_begin_ = sources.current_offset_abs
        increment_through(sources, program)

    program.stream.append((src_end, sources.line))

    return program


def increment_through(sources: Source, program: Program) -> None:
    current = sources.code[sources.current_offset_abs]
    sources.current_offset_abs += 1
    match current:
        case 'ß':
            program.stream.append((statement_end, sources.line))
            return
        case '+':
            program.stream.append((symbol_plus, sources.line))
            return
        case '-':
            program.stream.append((symbol_minus, sources.line))
            return
        case '*':
            program.stream.append((symbol_asterisk, sources.line))
            return
        case ',':
            program.stream.append((symbol_comma, sources.line))
            return
        case '[':
            program.stream.append((parenthesis_left, sources.line))
            return
        case ']':
            program.stream.append((parenthesis_right, sources.line))
            return
        case '>':
            if lookup(sources) == '-' and lookup(sources, 1) == '/':
                sources.current_offset_abs += 2
                program.stream.append((brace_right, sources.line))
                return
        case '/':
            if lookup(sources) == '-' and lookup(sources, 1) == '>':
                sources.current_offset_abs += 2
                program.stream.append((brace_left, sources.line))
            else:
                program.stream.append((symbol_slash, sources.line))
            return
        case '"':
            str_handle(sources, program)
            return
        case ' ':
            return
        case '\r':
            return
        case '\t':
            return
        case '\n':
            sources.line += 1
            return

    if current.isdecimal():
        handle_num(sources, program)
        return

    if current.isalpha() or current == '_':
        identifier_handle(sources, program)
        return

    syntax_error('Invalid syntax', sources.line, program)
    # Error: Unidentified character


def code_endpoint_reached(sources: Source) -> bool:
    return sources.current_offset_abs >= len(sources.code)


def lookup(sources: Source, offset: int = 0) -> str:
    if code_endpoint_reached(sources):
        return '\0'

    return sources.code[sources.current_offset_abs + offset]


def handle_num(sources: Source, program: Program) -> None:
    is_floating_point = False

    while lookup(sources).isdecimal():
        sources.current_offset_abs += 1

    if lookup(sources) == '.' and lookup(sources, 1).isdecimal():
        sources.current_offset_abs += 1
        is_floating_point = True

        while lookup(sources).isdecimal():
            sources.current_offset_abs += 1

    if is_floating_point:
        program.stream.append((literal_dbl, sources.line,
                               float(sources.code[sources.offset_begin:sources.current_offset_abs])))
    else:
        program.stream.append((literal_int, sources.line,
                               int(sources.code[sources.offset_begin:sources.current_offset_abs])))


def identifier_handle(sources: Source, program: Program) -> None:
    while lookup(sources).isalnum() or lookup(sources) == '_':
        if lookup(sources) == 'ß' and not (lookup(sources, 1).isalnum() or lookup(sources, 1) == '_'):
            break

        sources.current_offset_abs += 1

    string_s = sources.code[sources.offset_begin:sources.current_offset_abs]

    if string_s in res:
        program.stream.append((res[string_s], sources.line))
    else:
        program.stream.append((identifier_string, sources.line, string_s))


def str_handle(sources: Source, program: Program) -> None:
    while not (lookup(sources) == '"') and not code_endpoint_reached(sources):
        if lookup(sources) == '\n':
            sources.line += 1

        sources.current_offset_abs += 1

    if code_endpoint_reached(sources):
        syntax_error('Unterminated char literal', sources.line, program)
        return
        # Error for unterminated string

    sources.current_offset_abs += 1
    val = sources.code[sources.offset_begin + 1:sources.current_offset_abs - 1]

    if len(val) > 1:
        syntax_error('Invalid char given', sources.line, program)
        # String is longer than 1, the el spec only allows single chars
        # The actual runtime can support strings just fine, the job of artificially limiting
        # to chars is the job of the lexer

    program.stream.append((literal_string, sources.line, val))


# Report lexical errors but scramble the line they're on, in accordance with el spec
def syntax_error(err: str, line: int, program: Program) -> None:
    print('Syntax error: ' + err + ' on line ' + str(line + random.randint(-9, 9)))
    program.err += 1
