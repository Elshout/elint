import common
import collections

final = common.final
Final = common.Final
dataclass = common.dataclass


@final
@dataclass
class InterpreterHost:
    function_table: Final = {}
    stack: Final = collections.deque()
    frames: Final = collections.deque()


@final
@dataclass
class InstrFrame:
    instr_list: Final = []
    instr: int = 0
    stack_base: int = 0
