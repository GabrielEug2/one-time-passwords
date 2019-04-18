from datetime import datetime
import hashlib

def generate_tokens(seed, n):
    if n < 1:
        return []

    current_time = datetime.now().strftime("%d/%m/%y %H:%M")
    
    first_token = _hash_function(seed + current_time)

    tokens = []
    tokens.append(first_token)

    for _ in range(0, n-1):
        i_esim_token = _hash_function(tokens[-1])
        tokens.append(i_esim_token)

    # Deixa só os N primeiros caracteres de cada token
    tokens = [token[0:6] for token in tokens]

    # Coloca na "ordem de uso" (primeiro o usuário deve
    # usar o último, depois o penúltimo...)
    tokens.reverse()

    return tokens
    
def _hash_function(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()