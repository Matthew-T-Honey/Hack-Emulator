# The Mother of all Test Scripts (TMOATS)

#Address 2 for test result data
#Address 3 for number of tests
#Adresss 4 for the result of the test (-1 or 1)

.text
load movtests
mov 0 ;jmp

.data
testspassed: 0
targettests: 44
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
    load this_address
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
this_address  # Address near the start of the heap
