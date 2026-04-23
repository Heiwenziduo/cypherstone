# make heavy cryptography logics not blocking main thread

from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import threading

# from gui.console_screen import cys_console, cys_start_multi_task
from script.errors import CryptoError


# def thread_crypto_task(fun, callback, *args):
#     try:
#         fun(*args)
#         callback()
#     except CryptoError as e:
#         callback(e)

# def on_crypto_task_complete(e: Exception | None = None):
#     ''''''
    
#     if e:
#         error_handler(e)
    
#     return 


# ========================================================
# futures_executor = ThreadPoolExecutor(max_workers=1)
# def futures_finished(future):
#     ''''''

# ========================================================
def start_crypto_thread(fun, callback):
    ''''''
    def a():
        print(f"Thread Name: {threading.current_thread().name}")
        try:
            fun()
            callback()
        except CryptoError as e:
            print(e)
            # cys_error(e)
    # Global Interpreter Lock
    '''Python's GIL ensures that only one thread can execute Python code at a time
    heavy mathematical methods may cause the gui widget to lag
    '''
    # threading.Thread(target=a).start()

    # This creates a totally separate instance of Python in Windows Task Manager
    multiprocessing.Process(target=a).start()

# ========================================================
