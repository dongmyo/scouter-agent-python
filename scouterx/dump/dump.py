import cProfile
import os
import pstats
import sys
import threading
import time
import traceback
from datetime import datetime

from scouterx.common.netdata.listvalue import ListValue
from scouterx.common.netdata.mappack import MapPack
from scouterx.common.util.os_util import get_scouter_path
from scouterx.dump.mutext_logger import MutexLogger

suffix = 'pprof'


def stack_trace(count):
    pc_len = count
    if pc_len == 0:
        pc_len = 1

    stack = traceback.extract_stack()[:-1]
    if len(stack) > pc_len:
        stack = stack[-pc_len:]

    formatted_trace = []
    for frame in stack:
        # Each frame is a named tuple (filename, line number, function name, text)
        filename = frame.filename.split('/')[-1]  # Only the file name
        formatted_trace.append(f"{frame.name} {filename}:{frame.lineno}")

    return "\n".join(formatted_trace)


def heavy_all_stack_trace():
    file_name, err = _heavy_all_stack_trace()
    pack = MapPack()
    if err is not None:
        return pack
    pack.put("name", file_name)
    return pack


def _heavy_all_stack_trace():
    file_name = os.path.join(get_dump_path(), datetime.now().strftime("py_dump_%Y%m%d_%H%M%S.log"))

    try:
        file = open(file_name, 'w')
    except IOError as e:
        print(f"Could not open file {file_name} for writing, using standard output instead: {str(e)}", file=sys.stderr)
        file = sys.stdout

    # Write stack traces of all current threads
    try:
        for thread in threading.enumerate():
            file.write(f"Thread ID: {thread.ident}, Name: {thread.name}\n")
            stack = traceback.format_stack(sys._current_frames()[thread.ident])
            file.write(''.join(stack))
            file.write("\n")
    finally:
        if file is not sys.stdout:
            file.close()

    return file_name, None


def get_dump_path():
    path = get_scouter_path()
    dump_path = os.path.join(path, 'dump')
    os.makedirs(dump_path, exist_ok=True)
    return dump_path


def profile_binary_cpu(sec):
    file_name = os.path.join(get_binary_dump_path(), f"py_cpu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{suffix}")
    threading.Thread(target=profile_cpu, args=(file_name, sec)).start()
    return {"status": "Profiling started"}


def profile_cpu(file_name, sec):
    profiler = cProfile.Profile()
    try:
        profiler.enable()
        time.sleep(sec)  # simulate work by sleeping for `sec` seconds
        profiler.disable()
        with open(file_name, 'w') as file:
            ps = pstats.Stats(profiler, stream=file)
            ps.strip_dirs().sort_stats('time').print_stats()
    except Exception as e:
        print(f"Error during profiling: {e}")


def profile_block(sec, rate, level):
    file_name = os.path.join(get_dump_path(), f"py_block_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    threading.Thread(target=profile_block_worker, args=(file_name, sec, rate, level)).start()
    return {"status": "Block profiling started"}


def profile_block_worker(file_name, sec, rate, level):
    # Simulate setting a block profile rate if necessary
    profiler = cProfile.Profile()
    try:
        profiler.enable()
        time.sleep(sec)  # Allow some time to collect data
        profiler.disable()
        with open(file_name, 'w') as file:
            stats = pstats.Stats(profiler, stream=file)
            stats.sort_stats('time').print_stats()
    except Exception as e:
        print(f"Error during block profiling: {e}")


def profile_block_binary_dump(sec, rate):
    file_name = os.path.join(get_binary_dump_path(), f"py_block_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{suffix}")
    threading.Thread(target=profile_block_worker, args=(file_name, sec, rate)).start()
    return {"status": "Block profiling started"}


def get_binary_dump_path():
    path = get_scouter_path()
    dump_path = os.path.join(path, 'binary_dump')
    os.makedirs(dump_path, exist_ok=True)
    return dump_path


def profile_mutex(sec, rate):
    file_name = os.path.join(get_dump_path(), f"py_mutex_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    mutex_logger = MutexLogger(file_name)
    threading.Thread(target=run_with_mutex, args=(mutex_logger, sec)).start()


def run_with_mutex(mutex_logger, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        mutex_logger.acquire()
        time.sleep(0.1)  # Simulating work while holding the lock
        mutex_logger.release()
    mutex_logger.save_log()


def profile_mutex_binary_dump(sec, rate):
    file_name = os.path.join(get_binary_dump_path(), f"py_mutex_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{suffix}")
    threading.Thread(target=run_with_mutex, args=(file_name, sec, rate, 0)).start()


def list_dump_files():
    pack = MapPack()
    name_lv = ListValue()
    pack.put("name", name_lv)
    size_lv = ListValue()
    pack.put("size", size_lv)
    modified_lv = ListValue()
    pack.put("last_modified", modified_lv)

    dump_path = get_dump_path()
    for root, dirs, files in os.walk(dump_path):
        for file in files:
            file_path = os.path.join(root, file)
            stat = os.stat(file_path)
            name_lv.add_string(file)
            size_lv.add_int64(stat.st_size)
            modified_lv.add_int64(stat.st_mtime)
    return pack


def list_binary_dump_files():
    pack = {'name': [], 'size': []}
    dump_path = get_binary_dump_path()
    for root, dirs, files in os.walk(dump_path):
        for file in files:
            if file.endswith(suffix):
                file_path = os.path.join(root, file)
                stat = os.stat(file_path)
                pack['name'].append(file)
                pack['size'].append(stat.st_size)
    return pack


def download_binary_dump_files(out, file_name):
    if file_name == "" or not file_name.endswith(suffix):
        return
    dump_path = get_binary_dump_path()
    full_name = os.path.join(dump_path, file_name)
    try:
        with open(full_name, 'rb') as f:
            b = f.read(300)  # Adjust size as needed
            out.write(b)
    except Exception as e:
        print(f"Error reading file: {e}")


def delete_binary_dump_files(file_name):
    if file_name == "" or not file_name.endswith(suffix):
        return {'success': False, 'msg': "No filename"}
    dump_path = get_binary_dump_path()
    full_name = os.path.join(dump_path, file_name)
    try:
        os.remove(full_name)
        return {'success': True, 'msg': "Success"}
    except Exception as e:
        return {'success': False, 'msg': str(e)}


def stream_dump_file_contents(param, out):
    name = param.get('name')
    dump_file = os.path.join(get_dump_path(), name)
    try:
        with open(dump_file, 'rb') as file:
            while chunk := file.read(4096):
                out.write(chunk)
    except Exception as e:
        print(f"Failed to read: {e}")
