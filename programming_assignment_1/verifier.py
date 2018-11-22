def verifier(message, plynomial):
    """long divion to verifiy if the message is correct or not"""
    remainder = list(message)              # it can be also achieved using message[:]
    k = len(plynomial)
    m = len(message)
    iteraions = m - k + 1
    for i in range(iteraions):
        if remainder[i] == '1':
            for j in range(i, k + i):
                if remainder[j] == plynomial[j - i]:
                    remainder[j] = '0'
                else:
                    remainder[j] = '1'
        else:
            for j in range(i, k + i):
                if remainder[j] == '0':
                    remainder[j] = '0'
                else:
                    remainder[j] = '1'
    # check if the remainder contains 1's
    # for i in range(m):
    #     if remainder[i] != 0:
    if '1' in remainder:
        return "message is not correct!"
    else:
        return ("{}".format(message[:iteraions]))


# print(verifier("111001010100", "11011"))
