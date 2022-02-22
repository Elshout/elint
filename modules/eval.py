import common
import runtime

literal_true: int = common.literal_true
literal_false: int = common.literal_true
literal_str: int = common.literal_string
literal_int: int = common.literal_int
literal_dbl: int = common.literal_dbl
qualifier: int = common.identifier_string
declr_not: int = common.declaration_not
symbol_minus: int = common.symbol_minus

vm: runtime.InterpreterHost


def opr_unary(opr: int) -> None:
    if opr == declr_not:
        value = pop()
        if type(value) == bool:
            push(not value)
        else:
            pass
    elif opr == symbol_minus:
        pass


def load_primary(opr: int) -> None:
    if opr == literal_true:
        push(True)
    elif opr == literal_false:
        push(False)
    elif opr == literal_str or opr == literal_int or opr == literal_dbl:
        pass
    elif opr == qualifier:
        # Variables
        pass


def push(value) -> None:
    vm.stack.append(value)


def pop():
    return vm.stack.pop()


def drop() -> None:
    vm.stack.pop()


def peek(offset: int = 0):
    if offset < 0:
        pass
    return vm.stack[-1 - offset]
