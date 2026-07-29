# The Mother of all Test Scripts (TMOATS)

#Address 2 for test result data
#Address 3 for number of tests
#Adresss 4 for the result of the test (-1 or 1)

.text
load movtests
mov 0 ;jmp

.data
testspassed: 0
targettests: 63
testresult: 0

#===========================================================================================
#                                   MOV tests - 4 tests - tests 1-4
#===========================================================================================

.data
movtest1  
movtest2: -1
movtest3  
movtest4  

.text
movtests:

#Setup mov tests
    load movtest1
    mov 1 m
    load movtest2
    mov -1 M
    load 4
    mov A d
    load movtest3
    mov D M
    load 32767
    mov A D
    load movtest4
    mov D M

#test movtest1
    load movtest1  
    mov M D
    load 1
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test movtest2
    load movtest2 
    mov M D
    load 1
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test movtest3
    load movtest3
    mov M D
    load 4
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test movtest4
    load movtest4
    mov M D
    load 32767
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load inctests
    mov 0 ;jmp

#===========================================================================================
#                                   INC tests - 3 tests - tests 5-7
#===========================================================================================

.data
inctest1: 1  #2
inctest2: -1  #0
inctest3: 32767  #-32768

.text
inctests:
#Setup inc tests
    load inctest1
    inc M m
    load inctest2
    inc M m
    load inctest3
    inc M m

#test inctest1
    load inctest1
    mov M D
    load 2
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test inctest2
    load inctest2
    mov M D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test inctest3
    load inctest3
    mov M D
    load 32767
    not A A
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load dectests
    mov 0 ;jmp

#===========================================================================================
#                                   DEC tests - 3 tests - tests 8-10
#===========================================================================================

.data
dectest1: 1         #0
dectest2: 0         #-1
dectest3: -32768    #32767

.text
dectests:
    #Setup dec tests
    load dectest1
    dec M m
    load dectest2
    dec M m
    load dectest3
    dec M m

#test dectest1
    load dectest1
    mov M D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test dectest2
    load dectest2
    mov M D
    load 1
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test dectest3
    load dectest3
    mov M D
    load 32767
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load negtests
    mov 0 ;jmp

#===========================================================================================
#                                   NEG tests - 3 tests tests 11-13
#===========================================================================================

.data
negtest1: 1  #-1
negtest2: 0  #0
negtest3: -32768  #-32768


.text
negtests:
#Setup neg tests
    load negtest1
    neg M M
    load negtest2
    neg M M
    load negtest3
    neg M M

#test negtest1
    load negtest1
    mov M D
    load 1
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test negtest2
    load negtest2
    mov M D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test negtest3
    load negtest3
    mov M D
    load 32767
    not A A
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load nottests
    mov 0 ;jmp


#===========================================================================================
#                                   NOT tests - 3 tests - tests 14-16
#===========================================================================================

.data
nottest1: 0  #-1
nottest2: 1  #-2
nottest3: -32768  #32767

.text
nottests:
    #Setup not tests
    load nottest1
    not M M
    load nottest2
    not M M
    load nottest3
    not M M

#test nottest1
    load nottest1
    mov M D
    load 1
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test nottest2
    load nottest2
    mov M D
    load 2
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test nottest3
    load nottest3
    mov M D
    load 32767
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load addtests
    mov 0 ;jmp

#===========================================================================================
#                                   add tests - 3 tests - tests 17-19
#===========================================================================================

.data
addtest1: 1  #1 + -2 = -1
addtest2: 32767  #32767 + 1 = -32768
addtest3: -32768  #-32768 + 32767 = -1

.text
addtests:
    #Setup add tests
    load 2
    neg A D
    load addtest1
    add M M
    load 1
    mov A D
    load addtest2
    add M M
    load 32767
    mov A D
    load addtest3
    add M M

#test addtest1
    load addtest1
    mov M D
    load 1
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test addtest2
    load addtest2
    mov M D
    load 32767
    not A A
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test addtest3
    load addtest3
    mov M D
    load 1
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load subltests
    mov 0 ;jmp



#===========================================================================================
#                                   subl tests - 3 tests - tests 20-22
#===========================================================================================

.data
subltest1: 1      # 0-1 = -1
subltest2: 0      # 100-0 = 100
subltest3: 32767  # -2-32767 = 32767

.text
subltests:
    #Setup subl tests
    load 0
    mov A D
    load subltest1
    subl M M
    load 100
    mov a d
    load subltest2
    subl M M
    load 2
    neg A D
    load subltest3
    subl M M

#test subltest1
    load subltest1
    mov M D
    load 1
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test subltest2
    load subltest2
    mov M D
    load 100
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test subltest3
    load subltest3
    mov M D
    load 32767
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load subrtests
    mov 0 ;jmp



#===========================================================================================
#                                   subr tests - 3 tests - test 23-25
#===========================================================================================

.data
subrtest1: 1      # 1-0 = 1
subrtest2: 0      # 0-100 = -100
subrtest3: 32767  # 32767--2 = -32767

.text
subrtests:
    #Setup subr tests
    load 0
    mov A D
    load subrtest1
    subr M M
    load 100
    mov A d
    load subrtest2
    subr M M
    load 2
    neg A D
    load subrtest3
    subr M M

#test subrtest1
    load subrtest1
    mov M D
    load 1
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test subrtest2
    load subrtest2
    mov M D
    load 100
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test subrtest3
    load subrtest3
    mov M D
    load 32767
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load andtests
    mov 0 ;jmp



#===========================================================================================
#                                   and tests - 3 tests - tests 26-28
#===========================================================================================

.data
andtest1: 1  #1 & 1235 = 1
andtest2: 0  #0 & 1235 = 0
andtest3: -1 #-1 & 1235 = 1235

.text
andtests:
    #Setup and tests
    load 1235
    mov A D
    load andtest1
    and M M
    load andtest2
    and M M
    load andtest3
    and M M

#test andtest1
    load andtest1
    mov M D
    load 1
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test andtest2
    load andtest2
    mov M D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test andtest3
    load andtest3
    mov M D
    load 1235
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load ortests
    mov 0 ;jmp

#===========================================================================================
#                                   or tests - 3 tests - tests 29-31
#===========================================================================================

.data
ortest1: 1  #1 | 1235 = 1235
ortest2: 0  #0 | 1235 = 1235
ortest3: -1  #-1 | 1235 = -1

.text
ortests:
    #Setup or tests
    load 1235
    mov A D
    load ortest1
    or M M
    load ortest2
    or M M
    load ortest3
    or M M

#test ortest1
    load ortest1
    mov M D
    load 1235
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test ortest2
    load ortest2
    mov M D
    load 1235
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test ortest3
    load ortest3
    mov M D
    load 1
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load pushtests
    mov 0 ;jmp


#===========================================================================================
#                                   push tests - 4 tests - tests 32-35
#===========================================================================================

.data
pushtest1: 10
pushtest2: 100
pushtest3: 1000

.text
pushtests:
    load 16383
    mov A D
    load failcondition
    subl P ;jne
    load testspassed
    inc M M

    load pushtest1
    push M

    load 16382
    mov A D
    load failcondition
    subl P ;jne
    load testspassed
    inc M M

    load pushtest2
    push M

    load 16381
    mov A D
    load failcondition
    subl P ;jne
    load testspassed
    inc M M

    load pushtest3
    push M

    load 16380
    mov A D
    load failcondition
    subl P ;jne
    load testspassed
    inc M M

    load poptests
    mov 0 ;jmp


#===========================================================================================
#                                   pop tests - 6 tests - tests 36-41
#===========================================================================================

.data
poptest1: 1000
poptest2: 100
poptest3: 10


.text
poptests:

    pop D
    load poptest1
    subl M D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load 16381
    mov A D
    load failcondition
    subl P ;jne
    load testspassed
    inc M M


    pop D
    load poptest2
    subl M D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load 16382
    mov A D
    load failcondition
    subl P ;jne
    load testspassed
    inc M M


    pop D
    load poptest3
    subl M D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load 16383
    mov A D
    load failcondition
    subl P ;jne
    load testspassed
    inc M M

    load heaptest
    mov 0 ;jmp


#===========================================================================================
#                                   screen tests - 1 tests - test 43
#===========================================================================================

.data
screenvalue: 16384

.text
screentest:
    load screenvalue
    mov M D
    load SCREEN
    subl a d

    load failcondition
    mov d ;jne
    load testspassed
    inc M M
    load kbdtest
    mov 0 ;jmp


#===========================================================================================
#                                   kbd tests - 1 tests - test 44
#===========================================================================================

.data
kbdvalue: 24576

.text
kbdtest:
    load kbdvalue
    mov M D
    load KBD
    subl a d

    load failcondition
    mov d ;jne
    load testspassed
    inc M M
    load multtests
    mov 0 ;jmp


#===========================================================================================
#                                   mult tests - 3 tests
#===========================================================================================

.data
multtest1: -2  #-2*5 = -10
multtest2: -32768  #-32768 * 2 = 0
multtest3: -1234  #-1234 * -5678 = -5700

.text
multtests:
    #Setup mult tests
    load 5
    mov a d
    load multtest1
    mult M M
    load 2
    mov a D
    load multtest2
    mult M M
    load 5678
    neg a D
    load multtest3
    mult M M

#test multtest1
    load multtest1
    mov M D
    load 10
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test multtest2
    load multtest2
    mov M D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test multtest3
    load multtest3
    mov M D
    load 5700
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load sqrtests
    mov 0 ;jmp

#===========================================================================================
#                                   sqr tests - 4 tests
#===========================================================================================

.data
sqrtest1: 2  #2^2 = 4
sqrtest2: -4  #-4^2 = 16
sqrtest3: 200  #200^2 = -25536
sqrtest4: 2000  #2000^2 = 2304

.text
sqrtests:
    #Setup sqr tests
    load sqrtest1
    sqr M M
    load sqrtest2
    sqr M M
    load sqrtest3
    sqr M M
    load sqrtest4
    sqr M M

#test sqrtest1
    load sqrtest1
    mov M D
    load 4
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test sqrtest2
    load sqrtest2
    mov M D
    load 16
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test sqrtest3
    load sqrtest3
    mov M D
    load 25536
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test sqrtest4
    load sqrtest4
    mov M D
    load 2304
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load divltests
    mov 0 ;jmp

#===========================================================================================
#                                   divl tests - 3 tests
#===========================================================================================

.data
divltest1: 2  #7/2 = 3
divltest2: -10  #1000/-10 = -100
divltest3: -3  #-500/-3 = 166

.text
divltests:
    #Setup divl tests
    load 7
    mov a d
    load divltest1
    divl M M
    load 1000
    mov a D
    load divltest2
    divl M M
    load 500
    neg a D
    load divltest3
    divl M M

#test divltest1
    load divltest1
    mov M D
    load 3
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test divltest2
    load divltest2
    mov M D
    load 100
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test divltest3
    load divltest3
    mov M D
    load 166
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load divrtests
    mov 0 ;jmp


#===========================================================================================
#                                   divr tests - 3 tests
#===========================================================================================

.data
divrtest1: 12340  #12340/567 = 21
divrtest2: -12345  #-12345/678 = -19
divrtest3: -24680  #-24680/-1357 = 18

.text
divrtests:
    #Setup divr tests
    load 567
    mov a D
    load divrtest1
    divr M M
    load 678
    mov a d
    load divrtest2
    divr M M
    load 1357
    neg a d
    load divrtest3
    divr M M

#test divrtest1
    load divrtest1
    mov M D
    load 21
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test divrtest2
    load divrtest2
    mov M D
    load 19
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test divrtest3
    load divrtest3
    mov M D
    load 18
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load modltests
    mov 0 ;jmp

#===========================================================================================
#                                   modl tests - 3 tests
#===========================================================================================

.data
modltest1: 3  #10%3 = 1
modltest2: 3  #-10%3 = 2
modltest3: -3  #-10%-3 = -1

.text
modltests:
    #Setup modl tests
    load 10
    mov a D
    load modltest1
    modl M M
    load 10
    neg a D
    load modltest2
    modl M M
    load 10
    neg a D
    load modltest3
    modl M M

#test modltest1
    load modltest1
    mov M D
    load 1
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test modltest2
    load modltest2
    mov M D
    load 2
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test modltest3
    load modltest3
    mov M D
    load 1
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load modrtests
    mov 0 ;jmp

#===========================================================================================
#                                   modr tests - 3 tests
#===========================================================================================

.data
modrtest1: 10  #10%3 = 1
modrtest2: 10  #10%-3 = -2
modrtest3: -10  #-10%-3 = -1

.text
modrtests:
    #Setup modr tests
    load 3
    mov a D
    load modrtest1
    modr M M
    load 3
    neg a d
    load modrtest2
    modr M M
    load 3
    neg a d
    load modrtest3
    modr M M

#test modrtest1
    load modrtest1
    mov M D
    load 1
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test modrtest2
    load modrtest2
    mov M D
    load 2
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test modrtest3
    load modrtest3
    mov M D
    load 1
    add A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load successcondition
    mov 0 ;jmp



successcondition:
    load testresult
    mov 1 M
    load endloop
    mov 0 ;jmp

failcondition:
    load testresult
    mov -1 M
    load endloop
    mov 0 ;jmp

endloop:
    load endloop
    mov 0 ;jmp

#===========================================================================================
#                                   heap tests - 1 tests - test 42
#===========================================================================================

.text
heaptest:
    load thismultaddress
    inc A D
    load HEAP
    subl a d

    load failcondition
    mov d ;jne
    load testspassed
    inc M M
    load screentest
    mov 0 ;jmp

.data
thismultaddress  # Address near the start of the heap
