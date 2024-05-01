import contextvars
import time
from typing import Callable, List, Optional

from scouterx.common.netdata.alertpack import AlertLevel
from scouterx.common.structure.lra.lra import Cache
from scouterx.conf.configure import Configure
from scouterx.netio.dataproxy import send_alert
from scouterx.netio.tracecontext import TraceContext

# Context key for storing TraceContext
tctx_key = contextvars.ContextVar('tctx_key')

ac = Configure()
txid_map = Cache(10000)

# Placeholder functions
f_end_stuck_service_forcibly: Callable[[TraceContext], None] | None = None
noop_tctx = TraceContext(True)


def register_end_stuck_service_forcibly_func(f: Callable[[TraceContext], None]) -> None:
    global f_end_stuck_service_forcibly
    f_end_stuck_service_forcibly = f


def size() -> int:
    # Placeholder for size calculation
    return 0


def get_trace_context_fallback_noop(ctx) -> TraceContext:
    tctx = get_trace_context(ctx)
    return tctx if tctx is not None else noop_tctx


def get_trace_context(ctx) -> Optional[TraceContext]:
    return tctx_key.get()


def get_trace_context_by_txid(txid: int) -> Optional[TraceContext]:
    return txid_map.get(txid)


def new_trace_context(ctx) -> (contextvars.Token, TraceContext):
    tctx = TraceContext()
    token = tctx_key.set(tctx)
    return token, tctx


def start(tctx: TraceContext) -> None:
    txid_map.add(tctx.txid, tctx)


def end(tctx: TraceContext) -> None:
    txid_map.remove(tctx.txid)


def get_all_tctx() -> List[TraceContext]:
    return list(txid_map.get_values())


def get_active_count() -> List[int]:
    max_count = 2000
    count = 0
    active = [0, 0, 0]
    now = time.time()

    for tctx in txid_map.get_values():
        if count >= max_count:
            break
        count += 1

        elapsed = int((now - tctx.start_time) * 1000)
        if elapsed <= ac.trace_activeservice_yellow_time:
            active[0] += 1
        elif elapsed <= ac.trace_activeservice_red_time:
            active[1] += 1
        else:
            active[2] += 1

        if elapsed > ac.stuck_service_base_time_ms:
            f_end_stuck_service_forcibly(tctx)
            message = f"service: {tctx.service_name}, elapsed: {elapsed}, threadId: {tctx.goid}, tctxThreadId: {tctx.goid}"
            if ac.stuck_service_alert_enabled:
                send_alert(AlertLevel.ERROR, "STUCK_SERVICE", message)
            else:
                send_alert(AlertLevel.WARN, "STUCK_SERVICE", message)

    return active
