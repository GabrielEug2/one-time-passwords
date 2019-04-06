from datetime import datetime
import hashlib

def generate_tokens(seed, n):
    if n < 1:
        return list()

    current_time = datetime.now().strftime("%d/%m/%y %H:%M")
    
    # TODO: incluir salt
    first_token = _hash(seed + current_time)

    tokens = list()
    tokens.append(first_token)

    for i in range(0, n-1):
        i_esim_token = _hash(tokens[-1])
        tokens.append(i_esim_token)

    return tokens

def _hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()