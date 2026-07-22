.text
drawgrid_loop:
	#Loop condition
	load drawgrid_index
	mov m d
	load KBD
	subl a d
	load draw
	mov d ;jeq

	drawgrid_rowloop:
		load 15
		mov a d
		load drawgrid_row
		subl m d
		load drawgrid_notrowend
		mov d ;jne
		
		drawgrid_rowend:
			load drawgrid_index
			mov m a
			mov -1 m
			load drawgrid_rowcon_end
			mov 0 ;jmp
		drawgrid_notrowend:
			load drawgrid_index
			mov m a
			mov 1 m
		drawgrid_rowcon_end:
	
		load drawgrid_index
		inc m m
		
		load 32
		mov a d
		load drawgrid_column
		inc m m
		subl m d
		load drawgrid_rowloop
		mov d ;jne
	
	load drawgrid_column
	mov 0 m
	load 15 
	mov a d
	load drawgrid_row
	inc m m
	and m m
	load drawgrid_loop
	mov 0 ;jmp

	
.data
drawgrid_index: SCREEN
drawgrid_column: 0
drawgrid_row: 0 

.text
waitingloop:
	load 32
	mov a d
	load KBD
	subl m d
	load waitingloop
	mov d ;jne
	load compute
	mov 0; jmp




.text
#Draw all thee grid squares
draw:
    #Reset x,y
    load x
    mov 0 m
    load y
    mov 0 m

    #Set starting address
    load SCREEN
    mov a d
    load draw_x_address
    mov d m


    draw_xloop:
        #Loop condition
        load 32
        mov a d
        load x
        subl m d
        load draw_xloop_end
        mov d;jeq

        #Load start address
        load draw_x_address
        mov m d
        load draw_address
        mov d m

        #Load column data
        load x
        mov m d
        load grid_data
        add a a
        mov m d
        load draw_columndata
        mov d m

        draw_yloop:
            #Loop condition
            load 16
            mov a d
            load y
            subl m d
            load draw_yloop_end
            mov d;jeq

            #Set square value
            load draw_columndata
            mov m d
            load draw_notfilled
            mov d; jge

            draw_filled:
                load draw_squarevalue
                mov -1 m
                load draw_filled_con_end
                mov 0;jmp

            draw_notfilled:
                load draw_squarevalue
                mov 1 m

            draw_filled_con_end:
            
            #Loop over square rows
            load 15
            mov a d
            load draw_loopindex
            mov d m

            draw_inner_loop:
                #Loop condition
                load draw_loopindex
                mov m d
                load draw_inner_loop_end
                mov d;jeq
                load draw_loopindex
                dec m m

                #Draw row
                load draw_squarevalue
                mov m d
                load draw_address
                mov m a
                mov d m

                load 32
                mov a d
                load draw_address
                add m m
                load draw_inner_loop
                mov 0 ;jmp



            draw_inner_loop_end:

            load draw_columndata
            mov m d
            add m m


            #Increment values
            load y
            inc m m
            load 32
            mov a d
            load draw_address
            add m m

            #Loop
            load draw_yloop
            mov 0;jmp

        draw_yloop_end:

        #Increment values
        load draw_x_address
        inc m m
        load x
        inc m m
        load y
        mov 0 m

        #Loop
        load draw_xloop
        mov 0;jmp


    draw_xloop_end:
    load compute
    mov 0;jmp



.data
draw_address
draw_x_address
draw_loopindex
draw_columndata
draw_squarevalue



.text
#Compute the next grid state
compute:
    load 32
    mov a d
    load compute_loopindex
    mov d m

    load x
    mov 0 m
    #Copy grid_data into data_copy
    compute_copyloop1:
        load compute_loopindex
        mov m d
        load compute_copyloop1_end
        mov d;jeq

        load x
        mov m d
        load grid_data
        add a a
        mov m d
        load compute_temp
        mov d m

        load x
        mov m d
        load data_copy
        add a d
        load compute_temp2
        mov d m

        load compute_temp
        mov m d
        load compute_temp2
        mov m a
        mov d m

        load x
        inc m m
        load compute_loopindex
        dec m m

        load compute_copyloop1
        mov 0;jmp

    compute_copyloop1_end:


    #All the data manipulation go here:

    #Psedocode:
    #for x in range(32)
    #   for y in range(16)
    #       count = 0
    #       for x2 in [-1,0,1]:
    #           for y2 in [-1,0,1]:
    #               mask = masks[y2]
    #               data = grid_data[x2]
    #               if mask & grid_data != 0:
    #                   count++
    #       mask = masks[y]
    #       data = grid_data[x]
    #       alive = mask and data !=0
    #       if alive:
    #           if count<3:
    #               data_copy[x] -= mask
    #           if count>4:
    #               data_copy[x] -= mask
    #       else:
    #            if count == 3:
    #                data_copy[x] += mask


    #x=31
    load 31
    mov a d 
    load x
    mov d m

    compute_xloop:
        #Loop condition
        load x
        mov m d
        load compute_xloop_end
        mov d; jlt

        #y=15
        load 15
        mov a d
        load y
        mov d m 

        compute_yloop:
            #Loop condition
            load y
            mov m d
            load compute_yloop_end
            mov d; jlt

            #Count = 0
            load count
            mov 0 m

            #x2 = -1
            load x2
            mov -1 m

            compute_x2loop:

                #y2 = -1
                load y2
                mov -1 m
                compute_y2loop:

                    #Get the mask
                    load masks
                    mov a d
                    load y 
                    add m d 
                    load y2 
                    add m d 
                    mov d a 
                    mov m d 
                    load mask
                    mov d m

                    #Get the data
                    load grid_data
                    mov a d
                    load x 
                    add m d 
                    load x2 
                    add m d 
                    mov d a 
                    mov m d 
                    
                    load mask
                    and m d
                    load count_adj_con_end
                    mov d; jeq

                    load count
                    inc m m

                    count_adj_con_end:

                    #Loop condition
                    load y2
                    dec m d
                    inc m m
                    load compute_y2loop
                    mov d;jlt

                compute_y2loop_end:

                #Loop condition
                load x2
                dec m d
                inc m m
                load compute_x2loop
                mov d;jlt

            compute_x2loop_end:


            #Get the mask
            load masks
            mov a d
            load y 
            add m d 
            mov d a 
            mov m d 
            load mask
            mov d m

            #Get the data
            load grid_data
            mov a d
            load x 
            add m d 
            mov d a 
            mov m d 

            load mask
            and m d
            load result
            mov d m 

            load compute_dead_con
            mov d; jeq

            #Alive
                load count
                dec m m
                dec m m 
                mov m d
                load compute_alive_con2
                mov d; jgt

                #Starvation
                    #Get the data
                    load data_copy
                    mov a d
                    load x 
                    add m d 
                    load data
                    mov d m

                    #Subtract the mask
                    load mask
                    mov m d

                    load data 
                    mov m a 
                    subr m m 
                    
                    load compute_dead_con_end
                    mov 0;jmp


                compute_alive_con2:
                load count
                dec m m
                dec m m
                mov m d
                load compute_dead_con_end
                mov d; jle

                #Overpopulation
                    #Get the data
                    load data_copy
                    mov a d
                    load x 
                    add m d 
                    load data
                    mov d m

                    #Subtract the mask
                    load mask
                    mov m d

                    load data 
                    mov m a 
                    subr m m 
                    
                    load compute_dead_con_end
                    mov 0;jmp





            compute_dead_con:
            #Dead
            load count
            dec m m
            dec m m 
            dec m m
            mov m d
            load compute_dead_con_end
            mov d;jne
            #Revival
                #Get the data
                load data_copy
                mov a d
                load x 
                add m d 
                load data
                mov d m

                #Add the mask
                load mask
                mov m d

                load data 
                mov m a 
                add m m 
                
                load compute_dead_con_end
                mov 0;jmp


            compute_dead_con_end:



            load y
            dec m m 
            load compute_yloop
            mov 0;jmp

        compute_yloop_end:

        load x
        dec m m 
        load compute_xloop
        mov 0;jmp

    compute_xloop_end:


    #End of data manipulation

    load 32
    mov a d
    load compute_loopindex
    mov d m

    load x
    mov 0 m

    #Copy data_copy into grid_data
    compute_copyloop2:
        load compute_loopindex
        mov m d
        load compute_copyloop2_end
        mov d;jeq

        load x
        mov m d
        load data_copy
        add a a
        mov m d
        load compute_temp
        mov d m

        load x
        mov m d
        load grid_data
        add a d
        load compute_temp2
        mov d m

        load compute_temp
        mov m d
        load compute_temp2
        mov m a
        mov d m

        load x
        inc m m
        load compute_loopindex
        dec m m

        load compute_copyloop2
        mov 0;jmp

    compute_copyloop2_end:

    load draw
    mov 0;jmp

.data
compute_loopindex
compute_temp
compute_temp2
x2
y2
mask
result
count
data


.data
x:0
y:0

0 #Padding
masks:1
2
4
8
16
32
64
128
256
512
1024
2048
4096
8192
16384
32768
0 #Padding

0 #Padding
grid_data: 0
0
0
0
0
0
0
0
0
0
0
0
8
4
28
384
384
28
4
8
0
0
0
0
0
0
0
0
0
0
0
0
0 #Padding

data_copy: 0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0
0