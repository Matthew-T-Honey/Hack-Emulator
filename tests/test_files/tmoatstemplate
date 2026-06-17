#===========================================================================================
#                                   _ tests - X tests
#===========================================================================================

.data
_test1: a  #d
_test2: b  #e
_test3: c  #f

.text
_tests:
    #Setup _ tests
    load _test1
    _ M M
    load _test2
    _ M M
    load _test3
    _ M M

#test _test1
    load _test1
    mov M D
    load X
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test _test2
    load _test2
    mov M D
    load X
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

#test _test3
    load _test3
    mov M D
    load X
    subl A D
    load failcondition
    mov D ;jne
    load testspassed
    inc M M

    load _tests
    mov 0 ;jmp