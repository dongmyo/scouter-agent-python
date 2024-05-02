import contextlib
import datetime
import inspect
import threading

from starlette.requests import Request

from scouterx.common.logger.logger import error_logger
from scouterx.common.netdata.apicallstep import ApiCallStep
from scouterx.common.netdata.hmessagestep import HashedMessageStep
from scouterx.common.netdata.messagestep import MessageStep
from scouterx.common.netdata.methodstep import MethodStep
from scouterx.common.netdata.pmessagestep import PMessageStep, PMSG_ERROR
from scouterx.common.netdata.threadstep import AsyncServiceStep
from scouterx.common.netdata.xlogpack import *
from scouterx.common.util.background_context import BackgroundContext
from scouterx.common.util.hexa_util import int_to_xlog_string32
from scouterx.common.util.keygen.keygen import KeyGen
from scouterx.common.util.time_util import millis_to_now
from scouterx.counter.servicemetering import ServiceMetering
from scouterx.netio.dataproxy import *
from scouterx.netio.tcpclient.tcpmanager import start_tcp
from scouterx.strace.tctxmanager.tctxmanager import register_end_stuck_service_forcibly_func, get_trace_context, end, start, new_trace_context
from scouterx.strace.xlogsampler import get_xlog_sampler

ac = Configure()


def start_tracing_mode():
    register_end_stuck_service_forcibly_func(end_stuck_service_forcibly)
    start_tcp()


def is_stream(ctx):
    with contextlib.suppress(Exception):
        if ctx is None:
            return False
        tctx = get_trace_context(ctx)
        if tctx is None:
            return False
        return tctx.is_stream


def set_as_stream(ctx):
    with contextlib.suppress(Exception):
        if ctx is None:
            return False
        tctx = get_trace_context(ctx)
        if tctx is None:
            return False
        tctx.is_stream = True
        return True


def mark_as_error(ctx, error_message):
    with contextlib.suppress(Exception):
        if ctx is None:
            return
        tctx = get_trace_context(ctx)
        if tctx is None:
            return
        if tctx.error == 0:
            tctx.error = send_error(error_message)
        add_pmessage_step(ctx, PMSG_ERROR, error_message, 0)


def mark_as_error_forcibly(ctx, error_message):
    with contextlib.suppress(Exception):
        if ctx is None:
            return
        tctx = get_trace_context(ctx)
        if tctx is None:
            return
        tctx.error = send_error(error_message)


def set_service_name_forcibly(ctx, service_name):
    with contextlib.suppress(Exception):
        if ctx is None:
            return
        tctx = get_trace_context(ctx)
        if tctx is None:
            return
        tctx.service_name = service_name
        tctx.service_hash = send_service_name(service_name)


def add_step(ctx, step):
    with contextlib.suppress(Exception):
        if ctx is None:
            return
        tctx = get_trace_context(ctx)
        if tctx is None:
            return
        tctx.profile.add(step)


def add_message_step(ctx, message):
    with contextlib.suppress(Exception):
        if ctx is None:
            return
        tctx = get_trace_context(ctx)
        if tctx is None:
            return

        step = MessageStep(message, millis_to_now(tctx.start_time))
        tctx.profile.add(step)


def add_hashed_message_step(ctx, message, value, elapsed):
    with contextlib.suppress(Exception):
        if ctx is None:
            return
        tctx = get_trace_context(ctx)
        if tctx is None:
            return

        step = HashedMessageStep(send_hashed_message(message), millis_to_now(tctx.start_time))
        step.value = value
        step.time = elapsed
        tctx.profile.add(step)


def add_pmessage_step(ctx, level, message, elapsed, *params):
    with contextlib.suppress(Exception):
        if ctx is None:
            return
        tctx = get_trace_context(ctx)
        if tctx is None:
            return

        step = PMessageStep(millis_to_now(tctx.start_time))
        step.set_message(send_hashed_message(message), *params)
        step.elapsed = elapsed
        step.level = level
        tctx.profile.add(step)


def start_http_service(ctx, req: Request):
    with contextlib.suppress(Exception):
        if ctx is None:
            return BackgroundContext()

        service_name = f"{req.url.path}<{req.method}>"

        # TODO: propagation request (gxid, caller)
        # TODO: query profile
        # TODO: body (of specific service) profile

        new_ctx, tctx = start_service(ctx, service_name, get_remote_ip(req))
        tctx.x_type = XTYPE_WEB_SERVICE
        tctx.user_agent = send_user_agent(req.headers.get('User-Agent'))
        tctx.http_method = req.method
        tctx.referer = send_referer(req.headers.get('Referer'))
        profile_http_headers(req, tctx)

        return new_ctx, tctx


def get_remote_ip(req: Request):
    ip = req.client.host
    if ac.trace_http_client_ip_header_key != "":
        header_ip = req.headers.get(ac.trace_http_client_ip_header_key)
        if header_ip:
            ip = header_ip
    return ip


def normalize_ip(ip):
    return ip.split(':')[0]


def end_http_service(ctx, req, res):
    with contextlib.suppress(Exception):
        # TODO: body (of specific service) profile from req.body

        if res is not None:
            if ctx is None:
                return
            tctx = get_trace_context(ctx)
            if tctx is None or tctx.closed:
                return
            tctx.status = numpy.int32(res.status_code)
        end_any_service(ctx)


def start_service(ctx, service_name, remote_ip):
    with contextlib.suppress(Exception):
        if ctx is None:
            ctx = BackgroundContext()

        new_ctx, tctx = start_service_logic(ctx, service_name, remote_ip)
        tctx.x_type = XTYPE_APP_SERVICE

        return new_ctx, tctx


def end_service(ctx):
    with contextlib.suppress(Exception):
        end_any_service(ctx)


def start_new_inheritance_service(ctx, parent_tctx):
    with contextlib.suppress(Exception):
        if ctx is None:
            ctx = BackgroundContext()
        new_ctx, new_tctx = start_service_logic(ctx, parent_tctx.service_name, parent_tctx.remote_ip)
        new_tctx = inherit_tctx(new_tctx, parent_tctx)

        return new_ctx, new_tctx


def inherit_tctx(new_tctx, parent_tctx):
    new_tctx.inherit = True
    new_tctx.gxid = parent_tctx.gxid
    new_tctx.x_type = parent_tctx.x_type
    new_tctx.profile.add(MessageStep("scouter inheritance step", 0))
    new_tctx.is_stream = parent_tctx.is_stream

    new_tctx.error = parent_tctx.error
    new_tctx.http_method = parent_tctx.http_method
    new_tctx.http_query = parent_tctx.http_query
    new_tctx.http_content_type = parent_tctx.http_content_type

    new_tctx.sql_count = parent_tctx.sql_count
    new_tctx.sql_time = parent_tctx.sql_time
    new_tctx.sqltext = parent_tctx.sqltext

    new_tctx.apicall_name = parent_tctx.apicall_name
    new_tctx.apicall_count = parent_tctx.apicall_count
    new_tctx.apicall_time = parent_tctx.apicall_time
    new_tctx.apicall_target = parent_tctx.apicall_target

    new_tctx.userid = parent_tctx.userid
    new_tctx.user_agent = parent_tctx.user_agent
    new_tctx.user_agent_string = parent_tctx.user_agent_string
    new_tctx.referer = parent_tctx.referer

    new_tctx.is_child_tx = True
    new_tctx.caller = parent_tctx.txid
    new_tctx.caller_obj_hash = ac.obj_hash

    new_tctx.login = parent_tctx.login
    new_tctx.desc = parent_tctx.desc

    new_tctx.text1 = parent_tctx.text1
    new_tctx.text2 = parent_tctx.text2
    new_tctx.text3 = parent_tctx.text3
    new_tctx.text4 = parent_tctx.text4
    new_tctx.text5 = parent_tctx.text5

    return new_tctx


def go_with_trace(ctx, service_name, func_for_thread):
    with contextlib.suppress(Exception):
        new_ctx, child_tctx = start_child_goroutine_service(ctx, service_name)

        def thread_function():
            if child_tctx is not None:
                child_tctx.start_time = datetime.datetime.now()
            try:
                func_for_thread(new_ctx)
            finally:
                end_child_goroutine_service(new_ctx)

        threading.Thread(target=thread_function).start()


def start_child_goroutine_service(ctx, service_name):
    if ctx is None:
        return ctx, None
    parent_tctx = get_trace_context(ctx)
    if parent_tctx is None:
        return ctx, None

    ctx4_goroutine, child_tctx = start_service(ctx, service_name, parent_tctx.remote_ip)
    child_tctx.x_type = XTYPE_BACK_THREAD2
    child_tctx.caller = parent_tctx.txid
    child_tctx.gxid = parent_tctx.gxid
    if child_tctx.gxid == 0:
        child_tctx.gxid = parent_tctx.txid
        parent_tctx.gxid = parent_tctx.txid

    async_step = AsyncServiceStep()
    async_step.txid = child_tctx.txid
    async_step.start_time = millis_to_now(parent_tctx.start_time)
    async_step.hash = send_apicall(service_name)
    parent_tctx.profile.add(async_step)

    return ctx4_goroutine, child_tctx


def end_child_goroutine_service(ctx):
    with contextlib.suppress(Exception):
        end_any_service(ctx)


def start_service_logic(ctx, service_name, remote_addr):
    new_ctx, tctx = new_trace_context(ctx)
    start(tctx)

    tctx.gxid = tctx.txid
    tctx.goid = threading.get_ident()
    tctx.profile.add(MessageStep(f"thread:{tctx.goid}", 0))

    tctx.service_name = service_name
    tctx.service_hash = send_service_name(service_name)
    tctx.remote_ip = normalize_ip(remote_addr)
    return new_ctx, tctx


def end_any_service(ctx):
    if ctx is None:
        return
    tctx = get_trace_context(ctx)
    if tctx is None or tctx.closed:
        return
    end_any_service_of_trace_context(tctx)


def end_stuck_service_forcibly(tctx):
    with contextlib.suppress(Exception):
        if ac.stuck_service_remove_enabled:
            step = PMessageStep(millis_to_now(tctx.start_time))
            step.set_message(send_hashed_message("Service currently may running, not finished!"))
            step.level = PMSG_ERROR
            tctx.profile.add(step)

            if tctx.error == 0:
                tctx.error = send_error("This stuck service currently may running, not finished!")
            end_any_service_of_trace_context(tctx)


def end_any_service_of_trace_context(tctx):
    if tctx.closed:
        return
    tctx.closed = True

    tctx.service_hash = send_service_name(tctx.service_name)
    end(tctx)

    elapsed = millis_to_now(tctx.start_time)
    discard_type = find_xlog_discard(tctx, elapsed)
    xlog = tctx.to_xlog(discard_type, elapsed)

    write_profile = (discard_type == XLOG_DISCARD_NONE)  # TODO: consequence sampling
    tctx.profile.close(write_profile)

    ServiceMetering().add(int(xlog.elapsed), xlog.error != 0)
    # TODO: meteringInteraction

    if (xlog.discard_type != XLOG_DISCARD_ALL and xlog.discard_type != XLOG_DISCARD_ALL_FORCE) or \
            (not xlog.is_driving() and xlog.discard_type == XLOG_DISCARD_ALL):
        send_xlog(xlog)
    else:
        # TODO: send Dropped XLog
        pass


def find_xlog_discard(tctx, elapsed):
    if tctx.error != 0:
        discard_mode = XLOG_DISCARD_NONE
    else:
        discard_mode = get_xlog_sampler().evaluate_xlog_discard(elapsed, tctx.service_name)

    # Check xlog discard pattern
    if get_xlog_sampler().is_discard_service_pattern(tctx.service_name):
        discard_mode = XLOG_DISCARD_ALL_FORCE
        if tctx.error != 0:
            discard_mode = XLOG_DISCARD_NONE

    return discard_mode


def start_method(ctx):
    return start_method_with_param_internal(ctx)


def start_method_with_param(ctx, *params):
    return start_method_with_param_internal(ctx, *params)


def start_custom_method(ctx, method_name):
    return start_custom_method_with_param(ctx, method_name)


def start_custom_method_with_param(ctx, method_name, *params):
    if ctx is None:
        return None

    tctx = get_trace_context(ctx)
    if tctx is None:
        return None

    return start_method_with_param0(tctx, method_name, method_name, *params)


def start_method_with_param_internal(ctx, *params):
    if ctx is None:
        return None

    tctx = get_trace_context(ctx)
    if tctx is None:
        return None

    func_name = ctx.get('func_name')
    method_name = f"{func_name}()" if func_name else 'unknown()'

    return start_method_with_param0(tctx, func_name, method_name, *params)


def start_method_with_param0(tctx, func_name, method_name, *params):
    add_message_step_if_param_exist(tctx, params)
    tctx.last_method = func_name

    step = MethodStep(0, 0, 0, 0)
    step.hash = send_method(method_name)
    step.start_time = millis_to_now(tctx.start_time)
    tctx.profile.push(step)
    return step


def add_message_step_if_param_exist(tctx, params):
    if not params:
        return
    for param in params:
        if param is None:
            continue
        step = MessageStep(f"param: {param}", millis_to_now(tctx.start_time))
        step.start_time = millis_to_now(tctx.start_time)
        tctx.profile.add(step)


def end_method(ctx, step):
    with contextlib.suppress(Exception):
        if ctx is None or step is None:
            return
        tctx = get_trace_context(ctx)
        if tctx is None:
            return
        step.elapsed = millis_to_now(tctx.start_time) - step.start_time
        tctx.profile.pop(step)


def profile_http_headers(r, tctx):
    start_time = millis_to_now(tctx.start_time)
    if ac.profile_http_header_enabled:
        not_all = len(ac.profile_http_header_keys) > 0
        if not_all:
            split = ac.profile_http_header_keys.split(',')
            for k in split:
                values = r.headers.get(k.strip())
                if values:
                    v = ', '.join(values)
                    tctx.profile.add(MessageStep(f"header: {k}: {v}", start_time))
        else:
            for k, v in r.headers.items():
                tctx.profile.add(MessageStep(f"header: {k}: {v}", start_time))

    if ac.profile_http_querystring_enabled:
        tctx.profile.add(MessageStep(f"query: {r.url.query}", start_time))


def start_api_call(ctx, api_call_name, address):
    with contextlib.suppress(Exception):
        if ctx is None:
            return None
        tctx = get_trace_context(ctx)
        if tctx is None:
            return None

        return start_api_call_internal(api_call_name, tctx, address)


INTERSERVICE_GXID_HEADER_KEY = "X-Scouter-Gxid"
INTERSERVICE_CALLER_HEADER_KEY = "X-Scouter-Caller"
INTERSERVICE_CALLEE_HEADER_KEY = "X-Scouter-Callee"
INTERSERVICE_CALLER_OBJ_HEADER_KEY = "X-Scouter-Caller-Obj"


def start_api_call_with_propagation(ctx, req, api_call_name, address):
    with contextlib.suppress(Exception):
        if ctx is None:
            return None
        tctx = get_trace_context(ctx)
        if tctx is None:
            return None

        step = start_api_call_internal(api_call_name, tctx, address)
        if tctx.gxid == 0:
            tctx.gxid = tctx.txid

        if req is not None:
            req.headers.add(INTERSERVICE_GXID_HEADER_KEY, int_to_xlog_string32(tctx.gxid))
            req.headers.add(INTERSERVICE_CALLER_HEADER_KEY, int_to_xlog_string32(tctx.txid))
            req.headers.add(INTERSERVICE_CALLEE_HEADER_KEY, int_to_xlog_string32(step.txid))
            req.headers.add(INTERSERVICE_CALLER_OBJ_HEADER_KEY, str(ac.obj_hash))

        return step


def start_api_call_internal(api_call_name, tctx, address):
    step = ApiCallStep()
    step.hash = send_apicall(api_call_name)
    step.start_time = millis_to_now(tctx.start_time)
    if address:
        step.opt = 1
    step.address = address
    step.txid = KeyGen.get_instance().next()
    tctx.profile.push(step)

    return step


def end_api_call(ctx, step, err):
    with contextlib.suppress(Exception):
        if ctx is None or step is None:
            return
        tctx = get_trace_context(ctx)
        if tctx is None:
            return

        step.elapsed = millis_to_now(tctx.start_time) - step.start_time
        tctx.apicall_count += 1
        tctx.apicall_time += step.elapsed
        if err is not None:
            step.error = send_error(str(err))
            if tctx.error == 0:
                tctx.error = step.error

        tctx.profile.pop(step)
