import multiprocessing
from thread.openpgp import openpgp_encrypt

def multiprocessing_encrypt(key, in_path, out_path, queue):
    """This function lives in a totally separate process."""
    print('////////////////////////////////////////////////////')
    print(key, in_path, out_path, queue)
    try:
        # Example of progress tracking
        queue.put("Start")

        openpgp_encrypt(key, in_path, out_path)

        # Suppose your encryption has steps:
        # For 1 to 100:
        #    ... encrypt chunk ...
        #    queue.put(current_percent) 
        
        # perform_encryption(in_path, out_path, key)
        
        queue.put("Done")
    except Exception as e:
        queue.put(f"Error: {str(e)}")

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