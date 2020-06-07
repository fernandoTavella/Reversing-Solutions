

<p class="has-line-data" data-line-start="0" data-line-end="1">This is a write up for the crackme called “cm2” found on <a href="https://crackmes.one/">https://crackmes.one/</a></p>
<p class="has-line-data" data-line-start="2" data-line-end="4">Let’s start by running it with PEStudio. We can observe the following information:<br>
-Signature of the program:Dev-C++ 4.9.9.2 -&gt; Bloodshed Software</p>
<p class="has-line-data" data-line-start="5" data-line-end="6">We are going to use x64DBG to resolve this crackme since it was programed with c++ therefore we need to disassembly it (if it were .NET, we could have used dnspy to decompile).</p>
<p class="has-line-data" data-line-start="7" data-line-end="9">When we execute the crackme, it asks us to type a password. If the password is wrong, the program closes itself.<br>
So, let’s start by finding the conditional jumps to bypass its logic.</p>
<p class="has-line-data" data-line-start="10" data-line-end="11">If we want to patch the binary without understanding what passwords are valid, we only need to replace with NOP’s (“No Operation” instructions, value “90” in hexadecimal) the following instructions:</p>
<ul>
<li class="has-line-data" data-line-start="11" data-line-end="12">004013A1 | 0F85 88000000            | JNE cm2.40142F                                    |</li>
<li class="has-line-data" data-line-start="12" data-line-end="14">0040141F | 75 0E                    | JNE cm2.40142F                                    |</li>
</ul>
<p class="has-line-data" data-line-start="14" data-line-end="17">Now, if we want to know what passwords are valid, we need to study its logic in depth and build a keygen.<br>
To start, we can try a random password and observe what happens:<br>
value = password</p>
<p class="has-line-data" data-line-start="18" data-line-end="20">Now what we are going to do, is to separate the logic of the crackme in two parts.<br>
I do this, because we will see that the logic does two things:</p>
<ol>
<li class="has-line-data" data-line-start="20" data-line-end="21">Length input validation</li>
<li class="has-line-data" data-line-start="21" data-line-end="23">Password validation</li>
</ol>
<p class="has-line-data" data-line-start="23" data-line-end="24">#------------------------- LENGTH INPUT VALIDATION -------------------------</p>
<p class="has-line-data" data-line-start="25" data-line-end="26">0040135 | E8 48060000                   | call &lt;JMP.&amp;scanf&gt;                       |</p>
<p class="has-line-data" data-line-start="27" data-line-end="53">0040135 | 8D85 E8FEFFFF                 | lea eax,dword ptr ss:[ebp-118]          |<br>
0040135 | 890424                        | mov dword ptr ss:[esp],eax              | [esp]:“password”<br>
0040136 | E8 2A060000                   | call &lt;JMP.&amp;strlen&gt;                      |<br>
0040136 | 8945 F4                       | mov dword ptr ss:[ebp-C],eax            |<br>
0040136 | 8B45 F4                       | mov eax,dword ptr ss:[ebp-C]            |<br>
0040136 | 0FAF45 F4                     | imul eax,dword ptr ss:[ebp-C]           |<br>
0040137 | 89C1                          | mov ecx,eax                             | eax:“password”<br>
0040137 | 0FAF4D F4                     | imul ecx,dword ptr ss:[ebp-C]           |<br>
0040137 | 8B45 F4                       | mov eax,dword ptr ss:[ebp-C]            |<br>
0040137 | 89C2                          | mov edx,eax                             | eax:“password”<br>
0040137 | 0FAF55 F4                     | imul edx,dword ptr ss:[ebp-C]           |<br>
0040137 | 89D0                          | mov eax,edx                             | eax:“password”<br>
0040138 | C1E0 02                       | shl eax,2                               | eax:“password”<br>
0040138 | 01D0                          | add eax,edx                             | eax:“password”<br>
0040138 | 29C1                          | sub ecx,eax                             | eax:“password”<br>
0040138 | 8B55 F4                       | mov edx,dword ptr ss:[ebp-C]            |<br>
0040138 | 89D0                          | mov eax,edx                             | eax:“password”<br>
0040138 | 01C0                          | add eax,eax                             | eax:“password”<br>
0040138 | 01D0                          | add eax,edx                             | eax:“password”<br>
0040139 | 01C0                          | add eax,eax                             | eax:“password”<br>
0040139 | 29C1                          | sub ecx,eax                             | eax:“password”<br>
0040139 | 89C8                          | mov eax,ecx                             | eax:“password”<br>
0040139 | 83E8 38                       | sub eax,38                              | eax:“password”<br>
0040139 | 8945 F4                       | mov dword ptr ss:[ebp-C],eax            |<br>
0040139 | 837D F4 00                    | cmp dword ptr ss:[ebp-C],0              |<br>
004013A | 0F85 88000000                 | jne cm2.40142F                          |</p>
<p class="has-line-data" data-line-start="54" data-line-end="55">This logic can be explained as follows:</p>
<p class="has-line-data" data-line-start="56" data-line-end="66">1)Takes the input length, multiplies that value against itself and the result is stored in EAX.<br>
Interesting to know, at this point EAX and EDX have the same value.<br>
2)Previous result is multiplied again with itself, but this time the result is stored in ECX<br>
3)The EAX value is operated with  SHL (Shift Left) and the result is sum with the EDX value<br>
4)Performs a substract between EAX and ECX, and the result is stored in ECX<br>
5)Stores the string length in EDX<br>
6)Stores the length value on EAX, sums itself, adds the EDX value, sums itself again, subtracts the result with ECX,<br>
saves the result in EAX and subtracts value 28.<br>
7)Compares previous result with “0”. If both values are 0, the result of the comparison is true and the password is valid.<br>
If they are different, result is false and password is not valid.</p>
<p class="has-line-data" data-line-start="67" data-line-end="69">So, based on this logic, we know we need a password whose lenght allows us to obtain that “0” result, which means is valid. To achieve this, the lenght we need for the password to be valid,<br>
is any word that is 7 characters long (Check the <a href="http://script-cm2.py">script-cm2.py</a> file)</p>
<p class="has-line-data" data-line-start="70" data-line-end="72">Now that we know this, instead of using the word “password” which is 8 characters long, we are going to use “abcdefg” which is 7 characters long:<br>
value = abcdefg</p>
<p class="has-line-data" data-line-start="73" data-line-end="74">The following instructions are found in the “false” part of the program’s logic:</p>
<p class="has-line-data" data-line-start="75" data-line-end="111">#----------------------------- PASSWORD VALIDATION -----------------------------<br>
004013B1 | 83BD E4FE | CMP DWORD PTR SS:[EBP - 11C], 5                   |<br>
004013B8 | 7F 3D     | JG cm2.4013F7                                     |<br>
004013BA | 8D45 F8   | LEA EAX, DWORD PTR SS:[EBP - 8]                   |<br>
004013BD | 0385 E4FE | ADD EAX, DWORD PTR SS:[EBP - 11C]                 |<br>
004013C3 | 2D 100100 | SUB EAX, 110                                      |----&gt; Takes the input password<br>
004013C8 | 0FBE10    | MOVSX EDX, BYTE PTR DS:[EAX]                      |----&gt; Takes the first character<br>
004013CB | 89D0      | MOV EAX, EDX                                      |----&gt; Stores EDX in EAX<br>
004013CD | 01C0      | ADD EAX, EAX                                      |----&gt; Sums with itself<br>
004013CF | 01D0      | ADD EAX, EDX                                      |----&gt; Sums with EDX<br>
004013D1 | 8D50 D8   | LEA EDX, DWORD PTR DS:[EAX - 28]                  |----&gt; Loads “EAX-28” address in memory<br>
004013D4 | 8D45 F8   | LEA EAX, DWORD PTR SS:[EBP - 8]                   |<br>
004013D7 | 0385 E4FE | ADD EAX, DWORD PTR SS:[EBP - 11C]                 |<br>
004013DD | 2D 100100 | SUB EAX, 110                                      |<br>
004013E2 | 0FBE00    | MOVSX EAX, BYTE PTR DS:[EAX]                      |----&gt; Takes a character and stores it in EAX<br>
004013E5 | 0FAFD0    | IMUL EDX, EAX                                     |----&gt; Multiplies the result on EDX<br>
004013E8 | 8D45 EC   | LEA EAX, DWORD PTR SS:[EBP - 14]                  |<br>
004013EB | 0110      | ADD DWORD PTR DS:[EAX], EDX                       |<br>
004013ED | 8D85 E4FE | LEA EAX, DWORD PTR SS:[EBP - 11C]                 |<br>
004013F3 | FF00      | INC DWORD PTR DS:[EAX]                            |<br>
004013F5 | EB BA     | JMP cm2.4013B1                                    |<br>
004013F7 | 8B4D EC   | MOV ECX, DWORD PTR SS:[EBP - 14]                  |–&gt; loads the result of the previous operations on ECX<br>
004013FA | B8 676666 | MOV EAX, 66666667                                 |–&gt; Loads 66666667 on EAX<br>
004013FF | F7E9      | IMUL ECX                                          |–&gt; Multiplication of EAX with ECX<br>
00401401 | C1FA 02   | SAR EDX, 2                                        |–&gt; Shift Right 2 bits on EAX<br>
00401404 | 89C8      | MOV EAX, ECX                                      |–&gt; Loads ECX on EAX<br>
00401406 | C1F8 1F   | SAR EAX, 1F                                       |–&gt; Shift Right 1F on EAX<br>
00401409 | 29C2      | SUB EDX, EAX                                      |–&gt; Substract between EAX with EDX, the result gets loaded on EDX<br>
0040140B | 89D0      | MOV EAX, EDX                                      |–&gt; Loads ECX on EAX<br>
0040140D | C1E0 02   | SHL EAX, 2                                        |–&gt; Shift left 2 bits on EAX<br>
00401410 | 01D0      | ADD EAX, EDX                                      |–&gt; Adds EDX with EAX, result gets loaded on EAX<br>
00401412 | 01C0      | ADD EAX, EAX                                      |–&gt; Self EAX summatory<br>
00401414 | 29C1      | SUB ECX, EAX                                      |–&gt; Substract between EAX and ECX, the result gets loaded on ECX<br>
00401416 | 89C8      | MOV EAX, ECX                                      |–&gt; Loads ECX on EAX<br>
00401418 | 8945 F0   | MOV DWORD PTR SS:[EBP - 10], EAX                  |–&gt; Loads EAX on the stack<br>
0040141B | 837D F0 0 | CMP DWORD PTR SS:[EBP - 10], 0                    |–&gt; If the result is not 0, show us the bad password</p>
<hr>
<p class="has-line-data" data-line-start="112" data-line-end="114">Now that we have a better understanding about the crackme, check the keygen build it in python.<br>
r3v3r1nG 4 Fun :)</p>
