#Evaluates "return <expression>;"

#First: evaluate expression, pushed val onto stack

#temporarily store return address
#Return address stored at LCL + 3
load 3
mov a d
load $local
add m a
mov m d
load $return
mov d m


#Store return value at arg
pop d
load $arg
mov m a
mov d m

#Set P to Arg + 1
load $arg
dec m p

#Set arg to old arg (LCL+1)
load $local
inc m a
mov m d
load $arg
mov d m

#Set local to old local (LCL+2)
load $local
inc m d
inc d a
mov m d
load $local
mov d m

#Jump to return address
load $return
mov m a ;jmp
