import sys

class CypherStoneError(Exception):
    def __init__(self, *args,):
        super().__init__(*args)

class CryptoError(CypherStoneError):
    def __init__(self, *args,):
        super().__init__(*args)


# This function runs whenever the program is about to crash
# def global_exception_handler(exctype, value, tb):
#     '''print program exception on console screen'''

#     print(exctype.__name__, CryptoError.__name__)
#     if exctype.__name__.endswith(CryptoError.__name__):
#         cys_console(f"{value}", tag="error")
#     else:
#         cys_console(f"Unknown exception occurs!", tag="error")
#         error_msg = f"{exctype.__name__}: {value}"
#         print(error_msg)

# sys.excepthook = global_exception_handler