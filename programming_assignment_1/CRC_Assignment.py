from generator import concatenation
from alter import alter
from verifier import verifier

output = open('transmitted_message.txt', 'w')

with open('input.txt', 'r') as file:
    lines = file.readlines()
    for i in range(len(lines)/2):
        if len(lines[i]) < 1:
            continue
        message = lines[i]
        generator = lines[i+1]
        output_message = concatenation(message, generator)
        print("the result of generator is {}".format(output))
        verify = verifier(message=output_message, plynomial=generator)
        if verify:
            print("result of verify is correct and the message is {}".format(verify))
            output.write(output_message)
            output.write("\n message is correct \n \n")
        else:
            print("wrong message")
        alt = input("please enter the alter bit index as a number or the default alter is 3 eg. $ 5 \n")
        if alt:
            new_message = alter(output_message, int(alt))
        else:
            new_message = alter(output_message, 3)

        verify = verifier(message=new_message, plynomial=generator)
        print(verify)
        if verify:
            print("result of verify is correct and the message is {}".format(verify))
        else:
            print("wrong message")
            output.write(new_message)
            output.write("\n message is not correct \n \n")
