#Draw a tick
.text

start:
  tick_loop1:
    load KBD
    mov a d
    load tick_index
    subl m d
    load tick_loop1_end
    mov d;jle
  
    load tick_value
    mov m d
    load tick_index
    mov m a
    mov d m
   
    load 32
    mov a d
    load tick_index
    add m m
    
    load tick_value
    mov m d
    add m m

    mov m d
    load tick_loop1
    mov d;jne

    load tick_value
    mov 1 m
    load tick_index
    inc m m
    load tick_loop1
    mov 0 ;jmp
    
  tick_loop1_end:
  load 32
  mov a d
  load tick_index
  subr m m

  tick_loop2:
    load SCREEN
    mov a d
    load tick_index
    subr m d
    load endloop
    mov d;jlt
  
    load tick_value
    mov m d
    load tick_index
    mov m a
    mov d m
   
    load 32
    mov a d
    load tick_index
    subr m m
    
    load tick_value
    mov m d
    add m m

    mov m d
    load tick_loop2
    mov d;jne

    load tick_value
    mov 1 m
    load tick_index
    inc m m
    load tick_loop2
    mov 0 ;jmp

endloop:
  load endloop
  mov 0;jmp





.data
tick_value: 1
tick_index: 22533
