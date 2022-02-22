import dataclasses
import typing

final = typing.final
Final = typing.Final
dataclass = dataclasses.dataclass

src_end: Final(int) = 0
statement_end: Final(int) = 1
parenthesis_left: Final(int) = 2
parenthesis_right: Final(int) = 3
symbol_plus: Final(int) = 4
symbol_minus: Final(int) = 5
symbol_asterisk: Final(int) = 6
symbol_slash: Final(int) = 7
symbol_comma: Final(int) = 8
brace_left: Final(int) = 9
brace_right: Final(int) = 10
literal_true: Final(int) = 11
literal_false: Final(int) = 12
declaration_or: Final(int) = 13
declaration_and: Final(int) = 14
declaration_not: Final(int) = 15
function: Final(int) = 16
cmp_less: Final(int) = 17
cmp_more: Final(int) = 18
declaration_var: Final(int) = 19
declaration_while: Final(int) = 20
declaration_if: Final(int) = 21
declaration_else: Final(int) = 22
equals: Final(int) = 23
dual_equals: Final(int) = 24
identifier_string: Final(int) = 25
literal_string: Final(int) = 26
literal_int: Final(int) = 27
literal_dbl: Final(int) = 28
declaration_return: Final(int) = 29

@final
@dataclass
class Program:
    scope_depth: int = 0
    ignore_err: bool = False
    err: int = 0
    current: int = 0
    stream: Final(list) = []
