#Evaluates "func(args...)"

#N = number of Arguements
#func = function label

#First: evaluate args - this will push them to stack

#Push retun address to stack
load $return_xxxx
push a

#Push old local to stack
load $local 
push m

#Push old arg to stack
load $arg
push m

#Set arg to P + 3 + N
mov p d
load 3+N   #Evaluate at compile time
add a d
load $arg
mov d m

load $local
mov p m

load func
mov 0;jmp

$return_xxxx:
