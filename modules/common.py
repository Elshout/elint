import dataclasses
import typing

final = typing.final
Final = typing.Final
dataclass = dataclasses.dataclass

src_end: Final = 0
statement_end: Final = 1
parenthesis_left: Final = 2
parenthesis_right: Final = 3
symbol_plus: Final = 4
symbol_minus: Final = 5
symbol_asterisk: Final = 6
symbol_slash: Final = 7
symbol_comma: Final = 8
brace_left: Final = 9
brace_right: Final = 10
literal_true: Final = 11
literal_false: Final = 12
declaration_or: Final = 13
declaration_and: Final = 14
declaration_not: Final = 15
function: Final = 16
cmp_less: Final = 17
cmp_more: Final = 18
declaration_var: Final = 19
declaration_while: Final = 20
declaration_if: Final = 21
declaration_else: Final = 22
equals: Final = 23
dual_equals: Final = 24
identifier_string: Final = 25
literal_string: Final = 26
literal_int: Final = 27
literal_dbl: Final = 28
declaration_return: Final = 29


@final
@dataclass
class Program:
    scope_depth: int = 0
    ignore_err: bool = False
    err: int = 0
    current: int = 0
    stream: Final = []
