def alter(generated_message, index):
    """
       Return the input genrated_message after inverting the indexed character
       args:
           generated_message(string): m-bit message consisting of a string
           of 0s and 1s.
           index(int): the index of the character in the generated message
           to be inverted
    """
    if(index >= len(generated_message) or index < 0):
        return generated_message
    generated_message = list(generated_message)
    if(generated_message[index] == '1'):
        generated_message[index] = '0'
    else:
        generated_message[index] = '1'
    return ''.join(generated_message)
