import sys
barray1=bytearray.fromhex("AA 89 C4 FE 46")
barray2=bytearray.fromhex("78 F0 D0 03 E7")
barray3=bytearray.fromhex("F7 FD F4 E7 B9")
barray4=bytearray.fromhex("B5 1B C9 50 73")

#First type of xor starting from the secon argument in the userString
def xorTypeOne(list1,list2):
	y = 0
	for x in range(len(list1)):
		result = list1[x]^list2[y]
		list2[y] = list1[x]
		list1[x] = result
		y=y+1
		if y == 5:
			y=0
		
#Second type of xor starts from the last value of the first list and it's xored with the second one
def xorTypeTwo(list1,list2):
		y=0
		for x in range(len(list1),0,-1):
			x=x-1
			result = list1[x]^list2[y]
			list2[y] = list1[x]
			list1[x] = result
			y=y+1
			if y == 5:
				y=0

def getStringAndDivide(barr1):
	byteArray= bytearray(4)
	result=bytearray()
	#Getting values for division
	for eax in range(len(barr1)):
		ecx = eax & 0x3
		bl = byteArray[ecx]
		cl = barr1[eax]
		bl = bl + cl
		byteArray[ecx]= bl & 0xff
	#Division Logic
	divideMe = int.from_bytes(byteArray, byteorder="little")
	divider = 0xA
	while divideMe is not 0:
		resto = divideMe % divider
		divideMe = int(divideMe / divider)
		result.append(0x30+int(resto))
	#Final reverse of values logic	
	result.reverse()
	return ''.join(chr(c) for c in result)

name=sys.argv[1]
if len(name)>=4:
	userString = bytearray(name.encode('ascii'))
	userString.append(0)
	#Since we dont need the first value we can just deleted
	del userString[0]
	xorTypeOne(userString,barray1)
	xorTypeTwo(userString,barray2)
	xorTypeOne(userString,barray3)
	xorTypeTwo(userString,barray4)
	print("The Reg. Code for the user %s, is: %s" % (sys.argv[1],getStringAndDivide(userString)))
else:
	print("Insert username at least 4 chars...")
	print(sys.argv[1])
