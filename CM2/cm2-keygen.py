import random,string
#Variables
EAX,ECX,EDX = 0x0000000,0x0000000,0x0000000
#------ Logic used to get the size of the input string ------
def logic(size):
    EAX = size
    EAX*=EAX
    EDX =EAX
    ECX = EAX*size
    EAX = size*size
    EAX = EAX<<2
    EAX = EAX+EDX
    ECX = ECX-EAX
    EDX = size
    EAX = EDX
    EAX+= EAX
    EAX = EAX+EDX
    EAX+= EAX
    ECX-= EAX
    EAX = ECX
    EAX = EAX-int('0x38',16)
    return hex(EAX)
#------------------------------------------------------------
def get_password(word):
    i=0
    ECX=0
    for s in word:
        if i<=5:
            val = ord(s)
            EAX = val 
            EAX = EAX+EAX+EAX
            EAX = EAX - int('0x28',16)
            ECX += EAX*val
            i+=1
        else:
            break
    #print(hex(ECX))
    EAX = int('0x66666667',16)*ECX
    EDX = EAX >> 32
    EDX = EDX >> 2
    EAX = ECX
    EAX = EAX >> int('0x1F',16)
    EDX = EDX - EAX
    EAX = EDX
    EAX = EAX << 2
    EAX = EAX + EDX
    EAX += EAX
    ECX = ECX - EAX
    return hex(ECX)

def randomString():
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(7))   
while True:
    word = randomString()
    hex_val = get_password(word)
    if hex_val == '0x0':
        print(word)
        break