from typing import List, Optional

from scouterx.common.netdata.dataoutputx import DataOutputX
from scouterx.common.netdata.step import Step


def steps_to_bytes(steps: List[Step]) -> Optional[bytes]:
    if steps is None:
        return None
    dout = DataOutputX()
    for step in steps:
        if step is not None:
            dout.write_step(step)
    return dout.get_bytes()
