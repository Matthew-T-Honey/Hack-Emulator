from src.H_compiler.nodetype import NodeType
from src.H_compiler.tokentype import TokenType
from src.H_compiler.token import Token
from src.H_compiler.parsenode import ParseNode


class Generator:
    def __init__(self):
        self.code_string = ""
        self.function_identifiers = []
        self.local_variables = {}
        self.static_variables = {}
        self.function_args = {}
        self.current_function = None
        self.while_labels = 0
        self.if_labels = 0
        self.binary_operations_labels = 0
        self.unary_operations_labels = 0
        self.function_returns = 0

    def add_line(self, line):
        if self.code_string == "":
            self.code_string = line
        else:
            self.code_string += "\n"+line

    def generate_code(self, parse_tree, function_data):
        self.function_identifiers = function_data[0]
        self.local_variables = function_data[1]
        self.static_variables = function_data[2]
        self.function_args = function_data[3]
        self.code_string = ""

        self.while_labels = 0
        self.if_labels = 0
        self.binary_operations_labels = 0
        self.unary_operations_labels = 0
        self.function_returns = 0

        assert(parse_tree.type == NodeType.CODE)
        if "main" in self.function_identifiers:
            

            self.add_line(".text")
            self.add_line("load $arg")
            self.add_line("mov P M")
            self.add_line("load $endloop")
            self.add_line("push A")
            self.add_line("push 0")
            self.add_line("push 0")
            self.add_line("load $local")
            self.add_line("mov P M")

            self.add_line("load main")
            self.add_line("mov 0 ;jmp")
            self.add_line(".data")
            self.add_line("$local")
            self.add_line("$arg")
            self.add_line("$return")
            
        self.add_line(".text")

        for node in parse_tree.nodes:
            assert(node.type == NodeType.FUNCTION)
            self.generate_function(node)

        self.add_line("$endloop:")
        self.add_line("load $endloop")
        self.add_line("mov 0 ;jmp")

        return self.code_string

    def generate_function(self, node):
        self.current_function = node.nodes[1].text

        #Create function static section
        if len(self.static_variables[self.current_function]) > 0:
            self.add_line(".data")
            for static_variable in self.static_variables[self.current_function]:
                self.add_line(static_variable)
            self.add_line(".text")

        #Function Jump label
        self.add_line(f"{self.current_function}:")

        #Create space for local variables on stack
        num_of_locals = len(self.local_variables[self.current_function])
        if num_of_locals == 1:
            self.add_line("dec P P")
        if num_of_locals == 2:
            self.add_line("dec P P")
            self.add_line("dec P P")
        elif num_of_locals > 0:
            self.add_line(f"load {num_of_locals}")
            self.add_line("mov A D")
            self.add_line("subr P P")

        #Function statements start from the 6th term of the parse tree
        assert(node.nodes[5].type == TokenType.LEFT_BRACE)
        for subnode in node.nodes[6:]:
            if subnode.type == TokenType.RIGHT_BRACE:
                return
            self.generate_statement(subnode)

    def generate_statement(self, node):
        if node.type == NodeType.WHILE_LOOP:
            self.generate_while_loop(node)
        if node.type == NodeType.IF_CONDITION:
            self.generate_if_statement(node)
        if node.type == NodeType.VAR_DECLARATION:
            self.generate_variable_declaration(node)
        if node.type == NodeType.RETURN_STATEMENT:
            self.generate_return_statement(node)
        if node.type == NodeType.EXPRESSION_STATEMENT:
            self.generate_expression_statement(node)


    def generate_while_loop(self, node):
        assert(node.nodes[0].type == TokenType.WHILE)
        assert(node.nodes[2].type == NodeType.EXPRESSION)
        while_number = self.while_labels
        self.while_labels += 1

        #Initial Jump label
        self.add_line(f"$whilestart{while_number}:")

        #While condition
        self.generate_expression(node.nodes[2])

        #Jump on failed condition
        self.add_line(f"load $whileend{while_number}")
        self.add_line("pop ;jeq")

        assert(node.nodes[4].type == TokenType.LEFT_BRACE)
        for subnode in node.nodes[5:]:
            if subnode.type == TokenType.RIGHT_BRACE:
                self.add_line(f"load $whilestart{while_number}")
                self.add_line("mov 0 ;jmp")
                self.add_line(f"$whileend{while_number}:")
                return
            self.generate_statement(subnode)



    def generate_if_statement(self, node):
        assert(node.nodes[0].type == TokenType.IF)
        assert(node.nodes[2].type == NodeType.EXPRESSION)
        if_number = self.if_labels
        self.if_labels += 1

        #While condition
        self.generate_expression(node.nodes[2])
        self.add_line(f"load $elsecon{if_number}")
        self.add_line("pop ;jeq")

        assert(node.nodes[4].type == TokenType.LEFT_BRACE)
        node_index = 5
        while node.nodes[node_index].type != TokenType.RIGHT_BRACE:
            self.generate_statement(node.nodes[node_index])
            node_index += 1
        self.add_line(f"load $ifconend{if_number}")
        self.add_line("mov 0 ;jmp")

        self.add_line(f"$elsecon{if_number}:")
        
        if len(node.nodes) > node_index + 1:
            node_index += 1
            assert(node.nodes[node_index].type == TokenType.ELSE)
            node_index += 2
            while node.nodes[node_index].type != TokenType.RIGHT_BRACE:
                self.generate_statement(node.nodes[node_index])
                node_index += 1


        self.add_line(f"$ifconend{if_number}:")


    def generate_return_statement(self, node):

        if node.nodes[1].type != TokenType.SEMICOLON:
            self.generate_expression(node.nodes[1])
        else:
            self.add_line("push -1")


        self.add_line("load 3")
        self.add_line("mov A D")
        self.add_line("load $local")
        self.add_line("add M A")
        self.add_line("mov M D")
        self.add_line("load $return")
        self.add_line("mov D M")

        self.add_line("pop D")
        self.add_line("load $arg")
        self.add_line("mov M A")
        self.add_line("mov D M")

        self.add_line("load $arg")
        self.add_line("dec M P")

        self.add_line("load $local")
        self.add_line("inc M A")
        self.add_line("mov M D")
        self.add_line("load $arg")
        self.add_line("mov D M")

        self.add_line("load $local")
        self.add_line("inc M D")
        self.add_line("inc D A")
        self.add_line("mov M D")
        self.add_line("load $local")
        self.add_line("mov D M")

        self.add_line("load $return")
        self.add_line("mov M A ;jmp")



    def generate_variable_declaration(self, node):

        identifiers = []
        if node.nodes[0].type == TokenType.STATIC:
            node_index = 2
        else:
            node_index = 1
        assert(node.nodes[node_index - 1].type == TokenType.VAR)
        assert(node.nodes[node_index].type == TokenType.IDENTIFIER)

        identifiers.append(node.nodes[node_index].text)

        while node.nodes[node_index+1].type == TokenType.COMMA:
            node_index +=2
            identifiers.append(node.nodes[node_index].text)

        if node.nodes[node_index+1].type == TokenType.EQUALS:
            node_index +=2
            self.generate_expression(node.nodes[node_index])

        for id in identifiers:
            self.load_identifier(id)
            self.add_line("pop M")
            self.add_line("push M")

        self.add_line("pop")
        

    def generate_expression_statement(self, node):
        assert(len(node.nodes) == 2)
        self.generate_expression(node.nodes[0])
        #Pop the result left on the stack
        self.add_line("pop")

    def generate_expression(self, node):
        #Evaluates the expression and stores the result to the top of the stack
        if node.type == NodeType.TERM:
            self.generate_term(node)
            return

        if len(node.nodes) == 1:
            self.generate_expression(node.nodes[0])
            return

        assert(len(node.nodes) == 3)
        self.generate_expression(node.nodes[2])

        if node.nodes[1].type == TokenType.EQUALS:
            self.generate_assignment(node.nodes[0])
            return

        self.generate_expression(node.nodes[0])
        self.generate_binary_operation(node.nodes[1])


    def generate_term(self, node):
        #Generates the given term
        #Pushes the value onto the stack
        if node.nodes[0].type == TokenType.INTEGER_LITERAL:
            self.add_line(f"load {node.nodes[0].text}")
            self.add_line("push a")
        
        elif node.nodes[0].type == TokenType.KEYWORD:
            if node.nodes[0].text == "true":
                self.add_line("push 1")
            elif node.nodes[0].text == "false":
                self.add_line("push 0")
            elif node.nodes[0].text == "null":
                self.add_line("push -1")
            else:
                #heap, kbd or screen
                self.add_line(f"load {node.nodes[0].text}")
                self.add_line("push a")

        elif node.nodes[0].type == TokenType.LEFT_BRACKET:
            assert(len(node.nodes) == 3)
            self.generate_expression(node.nodes[1])

        elif node.nodes[0].type == TokenType.OPERATOR:
            assert(len(node.nodes) == 2)
            self.generate_term(node.nodes[1])
            self.generate_unary_operation(node.nodes[0])

        elif node.nodes[0].type == NodeType.VARIABLE:
            self.generate_variable_access(node.nodes[0])

        elif node.nodes[0].type == NodeType.FUNCTION_CALL:
            self.generate_function_call(node.nodes[0])

        else:
            assert(False)


    def generate_binary_operation(self, node):
        #Performs the binary operation from the token in node
        #on the two elements on top of the stack
        #Pushes the result onto the stack

        #  "==","||","&&","|","&",
        #  "<",">","<=",">=","+",
        #  "-","*","/","%"

        assert(node.type == TokenType.OPERATOR)
        match node.text:
            case "==":
                self.add_line("pop D")
                self.add_line("subl S D")
                self.add_line(f"load $binop{self.binary_operations_labels}_1")
                self.add_line("mov D ;jeq")
                self.add_line("push 0")
                self.add_line(f"load $binop{self.binary_operations_labels}_2")
                self.add_line("mov 0 ;jmp")
                self.add_line(f"$binop{self.binary_operations_labels}_1:")
                self.add_line("push 1")
                self.add_line(f"$binop{self.binary_operations_labels}_2:")
                self.binary_operations_labels += 1

            case "||":
                self.add_line(f"load $binop{self.binary_operations_labels}_1")
                self.add_line("pop D ;jne")
                self.add_line("pop D ;jne")
                self.add_line("push 0")
                self.add_line(f"load $binop{self.binary_operations_labels}_2")
                self.add_line("mov 0 ;jmp")
                self.add_line(f"$binop{self.binary_operations_labels}_1:")
                self.add_line("push 1")
                self.add_line(f"$binop{self.binary_operations_labels}_2:")
                self.binary_operations_labels += 1 

            case "&&":
                self.add_line("pop D")
                self.add_line("mult S D")
                self.add_line(f"load $binop{self.binary_operations_labels}_1")
                self.add_line("mov D ;jne")
                self.add_line("push 0")
                self.add_line(f"load $binop{self.binary_operations_labels}_2")
                self.add_line("mov 0 ;jmp")
                self.add_line(f"$binop{self.binary_operations_labels}_1:")
                self.add_line("push 1")
                self.add_line(f"$binop{self.binary_operations_labels}_2:")
                self.binary_operations_labels += 1

            case "|":
                self.add_line("pop D")
                self.add_line("or S S")

            case "&":
                self.add_line("pop D")
                self.add_line("and S S")

            case "<":
                self.add_line("pop D")
                self.add_line("subl S D")
                self.add_line(f"load $binop{self.binary_operations_labels}_1")
                self.add_line("mov D ;jlt")
                self.add_line("push 0")
                self.add_line(f"load $binop{self.binary_operations_labels}_2")
                self.add_line("mov 0 ;jmp")
                self.add_line(f"$binop{self.binary_operations_labels}_1:")
                self.add_line("push 1")
                self.add_line(f"$binop{self.binary_operations_labels}_2:")
                self.binary_operations_labels += 1

            case ">":
                self.add_line("pop D")
                self.add_line("subl S D")
                self.add_line(f"load $binop{self.binary_operations_labels}_1")
                self.add_line("mov D ;jgt")
                self.add_line("push 0")
                self.add_line(f"load $binop{self.binary_operations_labels}_2")
                self.add_line("mov 0 ;jmp")
                self.add_line(f"$binop{self.binary_operations_labels}_1:")
                self.add_line("push 1")
                self.add_line(f"$binop{self.binary_operations_labels}_2:")
                self.binary_operations_labels += 1

            case "<=":
                self.add_line("pop D")
                self.add_line("subl S D")
                self.add_line(f"load $binop{self.binary_operations_labels}_1")
                self.add_line("mov D ;jge")
                self.add_line("push 0")
                self.add_line(f"load $binop{self.binary_operations_labels}_2")
                self.add_line("mov 0 ;jmp")
                self.add_line(f"$binop{self.binary_operations_labels}_1:")
                self.add_line("push 1")
                self.add_line(f"$binop{self.binary_operations_labels}_2:")
                self.binary_operations_labels += 1              

            case ">=":
                self.add_line("pop D")
                self.add_line("subl S D")
                self.add_line(f"load $binop{self.binary_operations_labels}_1")
                self.add_line("mov D ;jle")
                self.add_line("push 0")
                self.add_line(f"load $binop{self.binary_operations_labels}_2")
                self.add_line("mov 0 ;jmp")
                self.add_line(f"$binop{self.binary_operations_labels}_1:")
                self.add_line("push 1")
                self.add_line(f"$binop{self.binary_operations_labels}_2:")
                self.binary_operations_labels += 1 

            case "+":
                self.add_line("pop D")
                self.add_line("add S S")

            case "-":
                self.add_line("pop D")
                self.add_line("subl S S")

            case "*":
                self.add_line("pop D")
                self.add_line("mult S S")

            case "/":
                self.add_line("pop D")
                self.add_line("divl S S")

            case "%":
                self.add_line("pop D")
                self.add_line("modl S S")

            case _:
                raise SyntaxError(f"Unrecognised character: {node.text}")
        


    def generate_unary_operation(self, node):
        #Performs the unary operation from the token in node
        #on the element on top of the stack
        #Pushes the result onto the stack
        #"*","-","~","!"
        assert(node.type == TokenType.OPERATOR)
        match node.text:
            case "*":
                self.add_line("pop A")
                self.add_line("push M")
            case "-":
                self.add_line("neg S S")
            case "~":
                self.add_line("not S S")
            case "!":
                self.add_line(f"load $binop{self.unary_operations_labels}_1")
                self.add_line("pop ;jeq")
                self.add_line(f"load $binop{self.unary_operations_labels}_2")
                self.add_line("push 0 ;jmp")
                self.add_line(f"$binop{self.unary_operations_labels}_1:")
                self.add_line("push 1")
                self.add_line(f"$binop{self.unary_operations_labels}_2:")
                self.unary_operations_labels += 1


    def generate_assignment(self, node):
        #Pops s into the variable defined at node
        #Pushes this value back onto the stack
        #Nodetype = Term (e.g '-', term(var)) or Nodetype = Variable
        #Variable cannt contain '&'
        self.load_variable(node,0)
        self.add_line("pop M")
        self.add_line("push M")


    def generate_variable_access(self, node):
        #Nodetype == Variable with possible '&'
        self.load_variable(node,0)
        if node.nodes[0].type == TokenType.OPERATOR:
            assert (node.nodes[0].text == "&")
            self.add_line("push A")
        else:
            self.add_line("push M")

    def generate_function_call(self, node):
        assert(node.nodes[0].type == TokenType.IDENTIFIER)

        
        arguements = 0
        if node.nodes[2].type != TokenType.RIGHT_BRACKET:
            self.generate_expression(node.nodes[2])
            arguements += 1

            node_index = 3
            while node.nodes[node_index].type != TokenType.RIGHT_BRACKET:
                self.generate_expression(node.nodes[node_index+1])
                node_index += 2
                arguements += 1


        self.add_line(f"load $functionreturn{self.function_returns}")
        self.add_line("push A")

        self.add_line("load $local")
        self.add_line("push M")
        self.add_line("load $arg")
        self.add_line("push M")

        self.add_line("mov P D")
        self.add_line(f"load {3+arguements}")
        self.add_line("add A D")
        self.add_line("load $arg")
        self.add_line("mov D M")

        self.add_line("load $local")
        self.add_line("mov P M")

        self.add_line(f"load {node.nodes[0].text}")
        self.add_line("mov 0 ;jmp")

        self.add_line(f"$functionreturn{self.function_returns}:")

        self.function_returns += 1



    def load_variable(self, node, level_of_dereference):
        if node.type == NodeType.TERM:
            if node.nodes[0].type == NodeType.VARIABLE:
                self.load_variable(node.nodes[0], level_of_dereference)
            elif node.nodes[0].type == TokenType.OPERATOR:
                assert(node.nodes[0].text == "*")
                self.load_variable(node.nodes[1], level_of_dereference + 1)
            return
        
        assert(node.type == NodeType.VARIABLE)

        token_offset = 0
        if node.nodes[0].type == TokenType.OPERATOR:
            token_offset = 1

        array_offset = False
        if len(node.nodes) > 1 + token_offset:
            self.generate_expression(node.nodes[2 + token_offset])
            array_offset = True

        identifier = node.nodes[0 + token_offset].text
        self.load_identifier(identifier)

        if array_offset:
            self.add_line("mov M A")
            self.add_line("pop D")
            self.add_line("add A A")

        for i in range(level_of_dereference):
            self.add_line("mov M A")



    def load_identifier(self, identifier):
        if identifier in self.static_variables[self.current_function]:
            self.add_line(f"load {identifier}")
        elif identifier in self.local_variables[self.current_function]:
            index = self.local_variables[self.current_function].index(identifier)
            if index == 0:
                self.add_line("load $local")
                self.add_line("mov M A")

            elif index == 1:
                self.add_line("load $local")
                self.add_line("mov M A")
                self.add_line("inc A A")
            elif index == 2:
                self.add_line("load $local")
                self.add_line("mov M A")
                self.add_line("inc A A")
                self.add_line("inc A A")
            else:
                self.add_line(f"load {index}")
                self.add_line("mov A D")
                self.add_line("load $local")
                self.add_line("mov M A")
                self.add_line("subr A A")
        elif identifier in self.function_args[self.current_function]:
            index = self.function_args[self.current_function].index(identifier)
            if index == 0:
                self.add_line("load $arg")
                self.add_line("mov M A")

            elif index == 1:
                self.add_line("load $arg")
                self.add_line("mov M A")
                self.add_line("inc A A")
            elif index == 2:
                self.add_line("load $arg")
                self.add_line("mov M A")
                self.add_line("inc A A")
                self.add_line("inc A A")
            else:
                self.add_line(f"load {index}")
                self.add_line("mov A D")
                self.add_line("load $arg")
                self.add_line("mov M A")
                self.add_line("subr A A")









