#Evaluates ('void'|'var') func(args...){}

#func = function label
#N = number of local variables

#Define all local variables first
.data
$func_var1=x
$func_var2=y
$func_var3=z

.text
#Jump label
func:

#Push local variables to the stack
load var1_val
push a
load var2_val
push a
load var3_val
push a

#var1 = $local
#var2 = $local + 1
#var3 = $local + 2
#etc...
