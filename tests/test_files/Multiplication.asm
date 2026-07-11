#A script to check if two input numbers multiply to give the specified value
#Usage, type 4 numbers, a,b,c,d into the keyboard
#The program verifies if axb=cd
.text
inputloop1:
  laod KBD
  mov m d
  load 0value
  subl m d
  load inputloop1
  mov d; jlt
  load 9
  subl a d
  load inputloop1
  mov d; jgt
  load 9
  add a d
  load input1
  mov d m

waitingloop1:
  load KBD
  mov m d
  load waitingloop1
  mov d ;jne

inputloop2:
  load KBD
  mov m d
  load 0value
  subl m d
  load inputloop2
  mov d; jlt
  load 9
  subl a d
  load inputloop2
  mov d; jgt
  load 9
  add a d
  load input2
  mov d m

waitingloop2:
  load KBD
  mov m d
  load waitingloop2
  mov d ;jne

inputloop3:
  load KBD
  mov m d
  load 0value
  subl m d
  load inputloop3
  mov d; jlt
  load 9
  subl a d
  load inputloop3
  mov d; jgt
  load 9
  add a d
  load digit1
  mov d m

waitingloop3:
  load KBD
  mov m d
  load waitingloop3
  mov d ;jne

inputloop4:
  load KBD
  mov m d
  load 0value
  subl m d
  load inputloop4
  mov d; jlt
  load 9
  subl a d
  load inputloop4
  mov d; jgt
  load 9
  add a d
  load digit2
  mov d m

waitingloop4:
  load KBD
  mov m d
  load waitingloop4
  mov d ;jne

#Calculate expected output
  mult_10_loop
    load loop_index
    mov m d
    load mult_10_loop_end
    mov d ;jlt
    load loop_index
    dec m m

    load digit1
    mov m d
    load expected_output
    add m m
    load mult_10_loop
    mov 0 ;jmp

  mult_10_loop_end:
  load digit2
  mov m d
  load expected_output
  add m m

mult_loop:
  load input1
  mov m d
  load mult_loop_end
  mov d ;jeq
  
  load input1
  dec m m

  load input2
  mov m d
  load result
  subr m m
  load mult_loop
  mov 0 ;jmp


mult_loop_end:
  load result
  mov m d
  load expected_output
  subl m d
  load success_condition
  mov d ;jeq
  load fail_condition
  mov 0;jmp

success_condition:
  #Draw a tick
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
  load endloop
  mov 0;jmp

fail_condition:
  #Draw a cross
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
  load endloop
  mov 0;jmp

endloop:
  load endloop
  mov 0;jmp



.data
input1
digit1
digit2
expected_output: 0
result: 0
0value: 48
9value: 57
loop_index: 10
cross_index
cross_value: 1
tick_value: 1
tick_index: 22533
