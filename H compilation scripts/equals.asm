# "=="
pop D
subl S D
load label1
mov D ;JEQ
    push 0
    load label2
    mov 0 ;JMP
label1:
    push 1
label2: