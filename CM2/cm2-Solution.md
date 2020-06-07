This is a write up for the crackme called "cm2" found on https://crackmes.one/

Let's start by running it with PEStudio. We can observe the following information:
	-Signature of the program:Dev-C++ 4.9.9.2 -> Bloodshed Software

We are going to use x64DBG to resolve this crackme since it was programed with c++ therefore we need to disassembly it (if it were .NET, we could have used dnspy to decompile).

When we execute the crackme, it asks us to type a password. If the password is wrong, the program closes itself. 
So, let's start by finding the conditional jumps to bypass its logic.

If we want to patch the binary without understanding what passwords are valid, we only need to replace with NOP's ("No Operation" instructions, value "90" in hexadecimal) the following instructions:
- 004013A1 | 0F85 88000000            | JNE cm2.40142F                                    |
- 0040141F | 75 0E                    | JNE cm2.40142F                                    |

Now, if we want to know what passwords are valid, we need to study its logic in depth and build a keygen. 
To start, we can try a random password and observe what happens:
value = password

Now what we are going to do, is to separate the logic of the crackme in two parts.
I do this, because we will see that the logic does two things:
1) Length input validation
2) Password validation

#------------------------- LENGTH INPUT VALIDATION -------------------------

0040135 | E8 48060000                   | call <JMP.&scanf>                       |
0040135 | 8D85 E8FEFFFF                 | lea eax,dword ptr ss:[ebp-118]          |
0040135 | 890424                        | mov dword ptr ss:[esp],eax              | [esp]:"password"
0040136 | E8 2A060000                   | call <JMP.&strlen>                      |
0040136 | 8945 F4                       | mov dword ptr ss:[ebp-C],eax            |
0040136 | 8B45 F4                       | mov eax,dword ptr ss:[ebp-C]            |
0040136 | 0FAF45 F4                     | imul eax,dword ptr ss:[ebp-C]           |
0040137 | 89C1                          | mov ecx,eax                             | eax:"password"
0040137 | 0FAF4D F4                     | imul ecx,dword ptr ss:[ebp-C]           |
0040137 | 8B45 F4                       | mov eax,dword ptr ss:[ebp-C]            |
0040137 | 89C2                          | mov edx,eax                             | eax:"password"
0040137 | 0FAF55 F4                     | imul edx,dword ptr ss:[ebp-C]           |
0040137 | 89D0                          | mov eax,edx                             | eax:"password"
0040138 | C1E0 02                       | shl eax,2                               | eax:"password"
0040138 | 01D0                          | add eax,edx                             | eax:"password"
0040138 | 29C1                          | sub ecx,eax                             | eax:"password"
0040138 | 8B55 F4                       | mov edx,dword ptr ss:[ebp-C]            |
0040138 | 89D0                          | mov eax,edx                             | eax:"password"
0040138 | 01C0                          | add eax,eax                             | eax:"password"
0040138 | 01D0                          | add eax,edx                             | eax:"password"
0040139 | 01C0                          | add eax,eax                             | eax:"password"
0040139 | 29C1                          | sub ecx,eax                             | eax:"password"
0040139 | 89C8                          | mov eax,ecx                             | eax:"password"
0040139 | 83E8 38                       | sub eax,38                              | eax:"password"
0040139 | 8945 F4                       | mov dword ptr ss:[ebp-C],eax            |
0040139 | 837D F4 00                    | cmp dword ptr ss:[ebp-C],0              |
004013A | 0F85 88000000                 | jne cm2.40142F                          |

This logic can be explained as follows:

1)Takes the input length, multiplies that value against itself and the result is stored in EAX.
	Interesting to know, at this point EAX and EDX have the same value.
2)Previous result is multiplied again with itself, but this time the result is stored in ECX
3)The EAX value is operated with  SHL (Shift Left) and the result is sum with the EDX value
4)Performs a substract between EAX and ECX, and the result is stored in ECX
5)Stores the string length in EDX
6)Stores the length value on EAX, sums itself, adds the EDX value, sums itself again, subtracts the result with ECX,
	saves the result in EAX and subtracts value 28.
7)Compares previous result with "0". If both values are 0, the result of the comparison is true and the password is valid. 
	If they are different, result is false and password is not valid.

So, based on this logic, we know we need a password whose lenght allows us to obtain that "0" result, which means is valid. To achieve this, the lenght we need for the password to be valid,
 is any word that is 7 characters long (Check the script-cm2.py file)

Now that we know this, instead of using the word "password" which is 8 characters long, we are going to use "abcdefg" which is 7 characters long:
value = abcdefg

The following instructions are found in the "false" part of the program's logic:

#----------------------------- PASSWORD VALIDATION -----------------------------

004013B1 | 83BD E4FE | CMP DWORD PTR SS:[EBP - 11C], 5                   |
004013B8 | 7F 3D     | JG cm2.4013F7                                     |
004013BA | 8D45 F8   | LEA EAX, DWORD PTR SS:[EBP - 8]                   |
004013BD | 0385 E4FE | ADD EAX, DWORD PTR SS:[EBP - 11C]                 |
004013C3 | 2D 100100 | SUB EAX, 110                                      |----> Takes the input password
004013C8 | 0FBE10    | MOVSX EDX, BYTE PTR DS:[EAX]                      |----> Takes the first character
004013CB | 89D0      | MOV EAX, EDX                                      |----> Stores EDX in EAX
004013CD | 01C0      | ADD EAX, EAX                                      |----> Sums with itself
004013CF | 01D0      | ADD EAX, EDX                                      |----> Sums with EDX
004013D1 | 8D50 D8   | LEA EDX, DWORD PTR DS:[EAX - 28]                  |----> Loads "EAX-28" address in memory
004013D4 | 8D45 F8   | LEA EAX, DWORD PTR SS:[EBP - 8]                   |
004013D7 | 0385 E4FE | ADD EAX, DWORD PTR SS:[EBP - 11C]                 |
004013DD | 2D 100100 | SUB EAX, 110                                      |
004013E2 | 0FBE00    | MOVSX EAX, BYTE PTR DS:[EAX]                      |----> Takes a character and stores it in EAX
004013E5 | 0FAFD0    | IMUL EDX, EAX                                     |----> Multiplies the result on EDX
004013E8 | 8D45 EC   | LEA EAX, DWORD PTR SS:[EBP - 14]                  |
004013EB | 0110      | ADD DWORD PTR DS:[EAX], EDX                       |
004013ED | 8D85 E4FE | LEA EAX, DWORD PTR SS:[EBP - 11C]                 |
004013F3 | FF00      | INC DWORD PTR DS:[EAX]                            |
004013F5 | EB BA     | JMP cm2.4013B1                                    |
004013F7 | 8B4D EC   | MOV ECX, DWORD PTR SS:[EBP - 14]                  |--> loads the result of the previous operations on ECX
004013FA | B8 676666 | MOV EAX, 66666667                                 |--> Loads 66666667 on EAX
004013FF | F7E9      | IMUL ECX                                          |--> Multiplication of EAX with ECX
00401401 | C1FA 02   | SAR EDX, 2                                        |--> Shift Right 2 bits on EAX
00401404 | 89C8      | MOV EAX, ECX                                      |--> Loads ECX on EAX
00401406 | C1F8 1F   | SAR EAX, 1F                                       |--> Shift Right 1F on EAX
00401409 | 29C2      | SUB EDX, EAX                                      |--> Substract between EAX with EDX, the result gets loaded on EDX
0040140B | 89D0      | MOV EAX, EDX                                      |--> Loads ECX on EAX
0040140D | C1E0 02   | SHL EAX, 2                                        |--> Shift left 2 bits on EAX
00401410 | 01D0      | ADD EAX, EDX                                      |--> Adds EDX with EAX, result gets loaded on EAX
00401412 | 01C0      | ADD EAX, EAX                                      |--> Self EAX summatory
00401414 | 29C1      | SUB ECX, EAX                                      |--> Substract between EAX and ECX, the result gets loaded on ECX
00401416 | 89C8      | MOV EAX, ECX                                      |--> Loads ECX on EAX
00401418 | 8945 F0   | MOV DWORD PTR SS:[EBP - 10], EAX                  |--> Loads EAX on the stack
0040141B | 837D F0 0 | CMP DWORD PTR SS:[EBP - 10], 0                    |--> If the result is not 0, show us the bad password
----------------------------------------------------------------------------------------------------------------------------------------------------
Now that we have a better understanding about the crackme, check the keygen build it in python.
r3v3r1nG 4 Fun :)
