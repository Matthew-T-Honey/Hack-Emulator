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