label:              #No section declaration
.code               #Invalid section declaration
.data goes here     #Invalid section declaration
.data               #Valid
var: 100            #Valid
100                 #Valid
Screen              #Valid
my_var   :    0     #Valid
!"£$%^&*()Q}{[]}:0  #Valid
var2: Screen        #Valid
var3                #Valid
var4: var4          #Valid
var5: var4          #Valid
var                 #Already defined
var2: 100           #Already defined
label:              #Invalid variable declaration
SCREEN: 100         #Cannot assign value to keyword
kbd: 100            #Cannot assign value to keyword
Heap: 100           #Cannot assign value to keyword
100: 100            #Cannot assign value to int
my variable         #Cannot have multi part variables
my variable: 100    #Cannot have multi part variables
my.variable         #"." is a blocked character
my;variable:        #";" is a blcoked character
:variable           #Invalid syntax
:variable: 100      #Invalid syntax
.text               #Valid
label:              #Valid
mov 1 d             #Valid
mov 1               #Valid
mov 1 d ;jeq        #Valid
inc d D             #Valid
add m P;jlt         #Valid
or a ;jgt           #Valid
load label          #Valid
load var            #Valid
load 100            #Valid
load heap           #Valid
push 1 ;jmp         #Valid
pop a ;jmp          #Valid
label:              #Invalid - already defined label
var:                #Invalid - already defined variable
mov 1 d;            #Invalid
inc 1 D             #Invalid
dec 0               #Invalid
add d D             #Invalid
push a s            #Invalid
pop 1 A             #Invalid
pop 1               #Invalid
load -1             #Invalid
load A              #Invalid
load: kbd           #Invalid
.data               #Valid
label               #Invalid - already defined variable
label:0             #Invalid - already defined variable