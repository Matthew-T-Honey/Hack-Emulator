.text
loop1:

    load index
    mov m A
    mov -1 M

    load kbd
    mov a d
    load index
    inc m M
    subl m D
    load loop1
    mov d ;jne

    load SCREEN
    mov A D
    load index
    mov D M
    load loop2
    mov 0 ;jmp

loop2:

    load index
    mov m A
    mov 0 M

    load kbd
    mov a d
    load index
    inc m M
    subl m D
    load loop2
    mov d ;jne

    load SCREEN
    mov A D
    load index
    mov D M
    load loop1
    mov 0 ;jmp


.data
index: SCREEN

.text
endloop:
load endloop
mov 0 ;jmp