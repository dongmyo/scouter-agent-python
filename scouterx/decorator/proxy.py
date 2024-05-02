import functools

from scouterx.strace.tracemain import end_method, start_method_with_param


def proxy(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        method_name = f"{f.__module__}.{f.__name__}()"

        ctx = {'func_name': f.__name__}

        step = start_method_with_param(ctx, method_name, *args)
        try:
            return f(*args, **kwargs)
        finally:
            end_method(ctx, step)

    return wrapped
