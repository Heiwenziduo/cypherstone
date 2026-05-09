import multiprocessing
from thread.openpgp import openpgp_encrypt, openpgp_decrypt



def multiprocessing_encrypt(fp, in_path, out_path, queue):
    """This function lives in a totally separate process."""
    print('////////////////////////////////////////////////////')
    print(fp, in_path, out_path, queue)
    try:
        queue.put("Start")
        
        openpgp_encrypt(fp, in_path, out_path)

        # TODO progressing bar
        # For 1 to 100:
        #    ... encrypt chunk ...
        #    queue.put(current_percent) 
        
        
        queue.put(f"Done;Success, encrypted file at: {out_path}")
    except Exception as e:
        queue.put(f"Error;Error: {str(e)}")

def multiprocessing_decrypt(in_path, out_path, queue):
    """This function lives in a totally separate process."""
    try:
        queue.put("Start")
        
        openpgp_decrypt(in_path, out_path)
        
        queue.put(f"Done;Success, decrypted file at: {out_path}")
    except Exception as e:
        queue.put(f"Error;Error: {str(e)}")