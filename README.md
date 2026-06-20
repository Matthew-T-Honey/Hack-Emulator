# Hack-Emulator

An emulator for a modified version of hack assembly

## ISA Specification

A Commands:  
0xxx xxxx xxxx xxxx  
Load value into the A register

C Commands:
1xcc cccc aadd djjj  
cccccc Controls the ALU functionality (as standard Hack)  
aa Specifies the operand:  
-  00 - A  
-  01 - M  
-  10 - P  
-  11 - S and P++  

ddd Specifies the destination:  
-  000 - None  
-  001 - D  
-  010 - A  
-  011 - M  
-  100 - P  
-  101 - S and P--  
-  110 - Unspecified  
-  111 - Unspecified

jjj Species the Jump condition (as standard Hack)

- 000 - No Jump
- 001 - Jump if greater than 0
- 010 - Jump if euqal to 0
- 011 - Jump if greaer than or equal to 0
- 100 - Jump if less than 0
- 101 - Jump if not equal to 0
- 110 - Jump if less than or equal to 0
- 111 - Jump

## Assembly Specification

Split code into .text and .data sections

"#" - Used for comments

Keywords:
- HEAP: evaluates to the address after the code segment
- SCREEN: evaluates to 16384
- KBD: evaluates to 24576

\<symbol> ::= (keyword | label | identifier)

### .data section:

"identifier" [":", (integer literal | \<symbol>)]	- Defines a new variable with keyword 

"identifier", defaults to 0 if not initialised

integer literal - Defines an integer literal value with no corresponding identifier

### .text section:

"label": - Defines a jump label

- \<dest> ::= (A|D|M|S|P)      - Removing multiple assignment
- \<jump> ::= ";", ("jlt","jeq","jgt","jle","jne","jge","jmp")

### A instruction
- load (integer literal | \<symbol>) 

### C instructions
- mov, (A|D|M|S|P|"1"|"0"|"-1"), [\<dest>], [\<jump>]
- inc, (A|D|M|S|P), [\<dest>], [\<jump>]
- dec, (A|D|M|S|P), [\<dest>], [\<jump>]
- neg, (A|D|M|S|P), [\<dest>], [\<jump>]
- not, (A|D|M|S|P), [\<dest>], [\<jump>]

- add, (A|M|S|P), [\<dest>], [\<jump>]
- subl, (A|M|S|P), [\<dest>], [\<jump>]  - D-A
- subr, (A|M|S|P), [\<dest>], [\<jump>]  - A-D
- and, (A|M|S|P), [\<dest>], [\<jump>]
- or, (A|M|S|P), [\<dest>], [\<jump>]

### Stack shorthand:
- push, (A|D|M|S|P|"1"|"0"|"-1"), [\<jump>] ::= mov, (A|D|M|S|P|"1"|"0"|"-1"), S [\<jump>]
- pop, [\<dest>], [\<jump>] ::= mov, S, [\<dest>], [\<jump>]
