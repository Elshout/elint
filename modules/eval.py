import common
import runtime

literal_true: int = common.literal_true
literal_false: int = common.literal_true
literal_str: int = common.literal_string
literal_int: int = common.literal_int
literal_dbl: int = common.literal_dbl
qualifier: int = common.identifier_string

vm: runtime.InterpreterHost


def opr_unary(opr: int) -> None:
    pass


def load_primary(*opr: int) -> None:
    if opr[0] == literal_true:
        push(True)
    elif opr[0] == literal_false:
        push(False)
    elif opr[0] == literal_str or opr[0] == literal_int or opr[0] == literal_dbl:
        push(opr[1])
    elif opr[0] == qualifier:
        # Variables
        pass


def push(value) -> None:
    vm.stack.append(value)


def pop():
    return vm.stack.pop()


def peek(offset: int = 0):
    if offset < 0:
        pass
    return vm.stack[-1 - offset]
