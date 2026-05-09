import multiprocessing
from cryptography.hazmat.primitives import serialization
from thread.openpgp import openpgp_encrypt
from script.data import user_db

##
def get_public_key_by_fp(fp: str):
    ''''''
    # TODO: empty fp always fetches the first row
    rowdata = user_db.get_row_by_fp(fp)
    if not rowdata:
        # cys_console("Can not get data. Invalid finger-print.")
        # TODO: throwing an exception and catching that at console screen maybe better.
        return
    alias = rowdata[0]
    finger_print = rowdata[1]
    public_bytes_der = rowdata[3]
    print(f"fp: {fp}")
    print(f"User {alias} has got the public key.")
    '''
    If your bytes are raw binary (often how they are stored in SQLite for efficiency),
    you cannot just name the file .pem.
    You must first turn them back into a Public Key object and then "export" them as PEM.
    '''
    public_key = serialization.load_der_public_key(public_bytes_der)
    '''
    PEM (.pem): It is "Human Readable."
    You can open it in Notepad and see the headers. This is great for sharing keys with other people or systems.

    DER/Bytes: It is "Machine Readable."
    It takes up less space and is faster for a database like SQLite to process
    because it doesn't have to deal with text encoding.
    '''
    # return (alias, finger_print, public_key)
    return public_key


def multiprocessing_encrypt(fp, in_path, out_path, queue):
    """This function lives in a totally separate process."""
    print('////////////////////////////////////////////////////')
    print(fp, in_path, out_path, queue)
    try:
        queue.put("Start")
        public_key = get_public_key_by_fp(fp)
        if public_key:
            openpgp_encrypt(public_key, in_path, out_path)

        # Suppose your encryption has steps:
        # For 1 to 100:
        #    ... encrypt chunk ...
        #    queue.put(current_percent) 
        
        # perform_encryption(in_path, out_path, key)
        
        queue.put(f"Done;Success, encrypted file at: {out_path}")
    except Exception as e:
        queue.put(f"Error;Error: {str(e)}")

def multiprocessing_decrypt(key, in_path, out_path, queue):
    """This function lives in a totally separate process."""
    try:
        # Example of progress tracking
        queue.put("Start")
        
        # Suppose your encryption has steps:
        # For 1 to 100:
        #    ... encrypt chunk ...
        #    queue.put(current_percent) 
        
        # perform_encryption(in_path, out_path, key)
        
        queue.put("Done")
    except Exception as e:
        queue.put(f"Error: {str(e)}")