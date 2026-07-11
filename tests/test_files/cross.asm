.text
#Draw a cross
start:
  load SCREEN
  mov a d
  load 8
  add a d
  load cross_index
  mov d m

  cross_loop1:
    load KBD
    mov a d
    load cross_index
    subl m d
    load cross_loop1_end
    mov d; jle

    load cross_value
    mov m d
    load cross_index
    mov m a
    mov d m

    load 32
    mov a d
    load cross_index
    add m m
    
    load cross_value
    mov m d
    add m m

    mov m d    
    load cross_loop1
    mov d; jne
    
    load cross_value
    mov 1 m
    load cross_index
    inc m m
    load cross_loop1
    mov 0;jmp


  cross_loop1_end:

  load KBD
  mov a d
  load 24
  subl a d 
  load cross_index
  mov d m
  load cross_value
  mov 1 m

  cross_loop2:
    load SCREEN
    mov a d
    load cross_index
    subr m d
    load endloop
    mov d; jlt

    load cross_value
    mov m d
    load cross_index
    mov m a
    mov d m

    load 32
    mov a d
    load cross_index
    subr m m
    
    load cross_value
    mov m d
    add m m

    mov m d    
    load cross_loop2
    mov d; jne
    
    load cross_value
    mov 1 m
    load cross_index
    inc m m
    load cross_loop2
    mov 0;jmp

endloop:
  load endloop
  mov 0;jmp



.data
cross_index
cross_value: 1
