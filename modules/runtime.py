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
    table_loc = None
    instr_offset: int = 0
    stack_base: int = 0
