def xor (m,n):
    
    result = []
    for i in range(1,len(n)):
        if m[i] == n[i]:
            result.append('0')
        else:
            result.append('1')
            
    return ''.join(result)

def division(data,divisor):
    """ Modulo 2 Division to get reminder """
    
    size = len(divisor)
    y = data[0:size]
    while size < len(data):
        if y[0] == '1':
            y = xor (divisor,y) + data[size]
        else:
            y = xor ('0'*size,y) + data[size]
        size += 1
    if y[0] == '1' :
        y = xor (divisor,y)
    else:
        y = xor ('0'*size,y)

    return y

def concatenation (message,generator):
    """ Concatena message with reminder to get transmitted data"""
    
    x = len(generator)
    data = message + '0'*(x-1)
    reminder = division(data,generator)
    transmitted_data = message + reminder

    return transmitted_data
