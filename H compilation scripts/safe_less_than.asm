#"<"
.text
load 5
neg a s
load 5
neg a s


load case3
pop D ;jlt
load case2
mov S S ;jlt
case1:
#++
    subl S D
    load yes
    mov D ;jlt
    load no
    mov 0 ;jmp

case2:
    #+-
    load no
    pop ;jmp

case3:
    #-+
    load case4
    mov S S;jlt
    load yes
    pop ;jmp

case4:
#--
    subr S D
    load no
    mov D ;jle

yes:
    push 1
    load end
    mov 0;jmp
no: 
    push 0
end:
load end
mov 0;jmp