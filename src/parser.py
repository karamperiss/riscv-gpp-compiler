import state
from intermediate import genquad, nextquad, newtemp, makeList, mergeList, backPatch
from symbol_table import Scope, Entity, Argument, getEntityFromScopeList2, resolveVariable, getFunctionVarialbles, checkFunctionVariables

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None

    # check the current token
    def match_token(self, expected_type, expected_value=None, error_message=None):
        while self.current_token and self.current_token.tokenType == 'comment':
            self.next_token()

        token = self.current_token
        if token is None:
            raise SyntaxError("Unexpected end of input.")

        if token.tokenType == expected_type and (expected_value is None or token.token == expected_value):
            self.next_token()
        else:
            message = (
                error_message
                if error_message
                else f"Syntax error in line: {token.line_counter}: Expected: '{expected_value or expected_type}', found '{token.token}'."
            )
            raise SyntaxError(message)

    # move to next token
    def next_token(self):
        self.current_token_index += 1
        self.current_token = (
            self.tokens[self.current_token_index] if self.current_token_index < len(self.tokens) else None
        )

    def program(self):
        self.match_token("keyword", "πρόγραμμα", "Should start with 'πρόγραμμα'")
        function_name = self.identifier("Expected program name after 'πρόγραμμα'.")
        state.programName = function_name
        scope = Scope(state.nesting)
        entity = Entity(function_name, "prog", 8)
        scope.appendEntity(entity)
        state.scopeList.append(scope)
        self.program_block(function_name)
        state.deletedScopes.append(state.scopeList.pop())

    def identifier(self, error_message="Identifier expected."):
        if self.current_token and self.current_token.tokenType == "identifier":
            id = self.current_token.token
            self.match_token("identifier")
            return id
        else:
            line = self.current_token.line_counter
            raise SyntaxError(f"Error in line {line}: {error_message}")

    def program_block(self, function_name):
        self.declarations()
        self.subprograms()
        genquad("begin_block", function_name, "_", "_")
        self.match_token("keyword", "αρχή_προγράμματος", "Expected 'αρχή_προγράμματος'.")
        self.sequence()
        self.match_token("keyword", "τέλος_προγράμματος", "Expected 'τέλος_προγράμματος'.")
        genquad("halt", "_", "_", "_")
        genquad("end_block", function_name, "_", "_")

    def declarations(self):
        while self.current_token and self.current_token.token == "δήλωση":
            self.match_token("keyword", "δήλωση", "Expected 'δήλωση'.")
            if not (self.current_token and self.current_token.tokenType == "identifier"):
                line = self.current_token.line_counter
                raise SyntaxError(f"Error in line {line}: Expected varlist after 'δήλωση'.")
            variables = self.var_list()

            for variable in variables:
                if variable in state.declaredVariables:
                    raise SyntaxError(f"Error : Variable '{variable}' already declared.")

            state.declaredVariables += variables

    def var_list(self):
        variables = []

        id0 = self.identifier("Expected identifier in varlist.")
        scope0 = state.scopeList[-1]
        ent = Entity(id0, "var", (scope0.getScopeOffset() + 4))
        ent.parMode = state.varListCaller
        variables.append(id0)
        if ent.name not in scope0.getEntityNames():
            scope0.appendEntity(ent)
        else:
            var_ent = getEntityFromScopeList2(id0)
            var_ent.parMode = state.varListCaller

        while self.current_token and self.current_token.token == ",":
            self.match_token("delimiter", ",", "Expected ',' between variables.")
            id = self.identifier("Expected identifier after ','.")
            ent = Entity(id ,"var", (scope0.getScopeOffset()+4))
            ent.setParMode(state.varListCaller)
            if id in variables :
                raise SyntaxError(f"Error : Variable '{id}' already declared.")
            else:
                variables.append(id)

            if ent.name not in scope0.getEntityNames():
                scope0.appendEntity(ent)
            else:
                var_ent = getEntityFromScopeList2(id)
                var_ent.parMode = state.varListCaller

        return variables

    def subprograms(self):
        while self.current_token and self.current_token.token in ["συνάρτηση", "διαδικασία"]:
            if self.current_token.token == "συνάρτηση":
                self.func()
            elif self.current_token.token == "διαδικασία":
                self.proc()

    def func(self):
        self.match_token("keyword", "συνάρτηση", "Expected 'συνάρτηση'.")
        id = self.identifier("Expected όνομα συνάρτησης.")

        if id in state.functions:
            raise SyntaxError(f"Function {id} is already defined.")
        else:
            state.functions.append(id)

        scope0 = state.scopeList[-1]
        entity0 = Entity(id, "func", -1)
        scope0.appendEntity(entity0)
        state.nesting += 1
        scope1 = Scope(state.nesting)
        entity1 = Entity(id, "func",8)
        scope1.appendEntity(entity1)
        state.scopeList.append(scope1)

        self.match_token("groupSymbol", "(", "Expected '('after function's name.")
        variables = self.formal_par_list()
        self.match_token("groupSymbol", ")", "Expected ')' after arguments.")
        self.func_block(id)
        state.functionReturn = False
        genquad("end_block", id, "_", "_")

        state.nesting -= 1
        frameLength = scope1.getScopeOffset() + 4
        functionEntity = scope0.entityList[-1]
        functionEntity.setFrameLength(frameLength)
        if variables != None:
            functionEntity.setNumOfParameters(len(variables))
        state.deletedScopes.append(state.scopeList.pop())

    def proc(self):
        self.match_token("keyword", "διαδικασία", "Expected 'διαδικασία'.")
        id = self.identifier("Expected όνομα διαδικασίας.")

        if id in state.functions:
            raise SyntaxError(f"Process {id} is already defined.")
        else:
            state.functions.append(id)
        
        scope0 = state.scopeList[-1]
        entity0 = Entity(id, "proc", -1)
        scope0.appendEntity(entity0)
        state.nesting += 1
        scope1 = Scope(state.nesting)
        entity1 = Entity(id,"proc", 8)
        scope1.appendEntity(entity1)
        state.scopeList.append(scope1)
        self.match_token("groupSymbol", "(", "Expected '(' after function's name.")
        variables = self.formal_par_list()
        self.match_token("groupSymbol", ")", "Expected ')' after arguments.")
        self.proc_block(id)
        genquad("end_block", id, "_", "_")
        state.nesting -= 1
        frameLength = scope1.getScopeOffset() + 4
        functionEntity = scope0.entityList[-1]
        functionEntity.setFrameLength(frameLength)
        if variables != None:
            functionEntity.setNumOfParameters(len(variables))
        state.deletedScopes.append(state.scopeList.pop())

    def formal_par_list(self):
        if self.current_token and self.current_token.tokenType == "identifier":
            variables = self.var_list()
            return variables

    def func_block(self,id):
        self.match_token("keyword", "διαπροσωπεία", "Expected 'διαπροσωπεία' in the function block.")
        self.func_input()
        self.func_output()
        self.declarations()

        if self.tokens[self.current_token_index].token == 'συνάρτηση' or self.tokens[self.current_token_index ].token == 'διαδικασία':
            self.subprograms()

        if self.tokens[self.current_token_index + 1].token == "συνάρτηση" or self.tokens[self.current_token_index + 1].token == "διαδικασία":
            self.next_token()
            self.subprograms()

        genquad("begin_block", id, "_", "_")
        self.match_token("keyword", "αρχή_συνάρτησης", "Expected 'αρχή_συνάρτησης'.")
        self.sequence()
        self.match_token("keyword", "τέλος_συνάρτησης", "Expected 'τέλος_συνάρτησης'.")
        if not state.functionReturn:
            raise SyntaxError(f"Function {id} does not return an item in the function block.")

    def proc_block(self,id):
        self.match_token("keyword", "διαπροσωπεία", "Expected 'διαπροσωπεία' in the function block.")
        self.func_input()
        self.func_output()
        self.declarations()

        if self.tokens[self.current_token_index].token == 'συνάρτηση' or self.tokens[self.current_token_index ].token == 'διαδικασία':
            self.subprograms()

        if self.tokens[self.current_token_index + 1].token == 'συνάρτηση' or self.tokens[self.current_token_index + 1].token == 'διαδικασία':
            self.next_token()
            self.subprograms()

        genquad("begin_block", id, "_", "_")
        self.match_token("keyword", "αρχή_διαδικασίας", "Expected 'αρχή_διαδικασίας'.")
        self.sequence()
        self.match_token("keyword", "τέλος_διαδικασίας", "Expected 'τέλος_διαδικασίας'.")

    def func_input(self):
        if self.current_token.token == "είσοδος":
            self.match_token("keyword", "είσοδος", "Expected 'είσοδος'")
            state.varListCaller = "in"
            variables = self.var_list()
            state.varListCaller = ""
            scope0 = state.scopeList[state.nesting - 1]
            entityFunc = scope0.entityList[-1]
            argIn = Argument("in")
            entityFunc.addArgument(argIn)
            entityFunc.setCvParameters(entityFunc.getCvParameters()+ len(variables))
            entityFunc.setStartQuad(nextquad())

    def func_output(self):
        if self.current_token.token == "έξοδος":
            self.match_token("keyword", "έξοδος", "Expected 'έξοδος'")
            state.varListCaller = "io"
            variables = self.var_list()
            state.varListCaller = ""
            scope0 = state.scopeList[state.nesting - 1]
            entityFunc = scope0.entityList[-1]
            argIn = Argument("io")
            entityFunc.addArgument(argIn)
            entityFunc.setRefParameters(entityFunc.getRefParameters() + len(variables))

            if entityFunc.getStartQuad() == 0:
                entityFunc.setStartQuad(nextquad())

    def sequence(self):
        while self.current_token and self.current_token.tokenType == 'comment':
            self.next_token()

        self.statement()

        while self.current_token and self.current_token.token == ";":
            self.match_token("delimiter", ";")
            while self.current_token and self.current_token.tokenType == 'comment':
                self.next_token()
            self.statement()

    def statement(self):
        token = self.current_token
        if not token:
            raise SyntaxError("Εrror: Unexpected end of input.")

        statements = {
            "εάν": self.if_stat,
            "όσο": self.while_stat,
            "επανάλαβε": self.do_stat,
            "για": self.for_stat,
            "διάβασε": self.input_stat,
            "γράψε": self.print_stat,
            "εκτέλεσε": self.call_stat,
        }

        if token.token in statements:
            statements[token.token]()
        elif token.tokenType == "identifier":
            self.assignment_stat()
        else:
            raise SyntaxError(f"Error in line {token.line_counter}: Unexpected token '{token.token}'.")

    def assignment_stat(self):
        identifier = self.identifier("Expected identifier in varlist")

        if(resolveVariable(identifier) == False):
            raise SyntaxError(f"Error variable {identifier} is undeclared")

        if identifier in state.for_identifiers:
            raise SyntaxError(f"Error for identifier {identifier} can not be changed manually.")

        self.match_token("assignOperator", ":=")
        exp = self.expression()

        scope0 = state.scopeList[state.nesting - 1]
        entityFunc = scope0.entityList[-1]
        if identifier == entityFunc.getName() and entityFunc.type == "func":
            state.functionReturn = True
            genquad("retv", exp, "_", "_")
        else:
            genquad(":=", exp, "_", identifier)

        scope1 = state.scopeList[state.nesting]
        ent1 = Entity(exp, "temp", (scope1.getScopeOffset() + 4))
        ent1.setParMode(state.varListCaller)
        if not exp.isdigit() and not exp in state.listOfVariables:
            scope1.appendEntity(ent1)

    def if_stat(self):
        self.match_token("keyword", "εάν")
        B_true, B_false = self.condition()
        self.match_token("keyword", "τότε")
        backPatch(B_true, nextquad())
        self.sequence()
        ifList = makeList(nextquad())
        genquad("jump", "_", "_", "_")
        backPatch(B_false, nextquad())
        if self.current_token and self.current_token.token == "αλλιώς":
            self.else_stat()
        backPatch(ifList, nextquad())
        self.match_token("keyword", "εάν_τέλος")

    def else_stat(self):
        self.match_token("keyword", "αλλιώς")
        self.sequence()

    def while_stat(self):
        self.match_token("keyword", "όσο")
        Bquad = nextquad()
        B_true,B_false = self.condition()
        self.match_token("keyword", "επανάλαβε")
        backPatch(B_true,nextquad())
        self.sequence()
        genquad("jump", "_", "_", Bquad)
        backPatch(B_false, nextquad())
        self.match_token("keyword", "όσο_τέλος")

    def do_stat(self):
        self.match_token("keyword", "επανάλαβε")
        sQuad = nextquad()
        self.sequence()
        self.match_token("keyword", "μέχρι")
        cond_true, cond_false = self.condition()
        backPatch(cond_false, sQuad)
        backPatch(cond_true, nextquad())

    def for_stat(self):
        self.match_token("keyword", "για")
        id = self.identifier()
        state.for_identifiers.append(id)
        self.match_token("assignOperator", ":=")
        exp_start = self.expression()
        # {P1 start}
        genquad(":=", exp_start, "_", id)
        # {P1 end}
        self.match_token("keyword", "έως")
        exp_end = self.expression()

        # {P2 start}
        condquad = nextquad()
        stepChanged = False
        step = "1"

        if self.current_token and self.current_token.token == "με_βήμα":
            step = self.step()
            stepChanged = True

        if not stepChanged:
            true = makeList(nextquad())
            genquad("<=", id, exp_end, "_")
            false = makeList(nextquad())
            genquad("jump", "_", "_", "_")
            backPatch(true, nextquad())

        else:
            if step.startswith("t") or int(step) >= 0:
                true = makeList(nextquad())
                genquad("<=", id, exp_end, "_")
                false = makeList(nextquad())
                genquad("jump", "_", "_", "_")
                backPatch(true, nextquad())
            elif int(step) < 0:
                true = makeList(nextquad())
                genquad(">=", id, exp_end, "_")
                false = makeList(nextquad())
                genquad("jump", "_", "_", "_")
                backPatch(true, nextquad())
        # {P2 end}

        self.match_token("keyword", "επανάλαβε")
        self.sequence()

        # {P3 start}
        if not stepChanged:
            genquad("+", id, "1", id)
        else:
            if step.startswith("t") or int(step) >= 0:
                genquad("+", id, step, id)
            else:
                abs_Step = str(abs(int(step)))
                genquad("-", id, abs_Step, id)
        # {P3 end}

        # {P4 start}
        genquad("jump", "_", "_", condquad)
        backPatch(false, nextquad())
        # {P4 end}

        self.match_token("keyword", "για_τέλος")
        state.for_identifiers.pop()

    def boolfactor_for_loop(self, var, rel_op, value):
        true_list = makeList(nextquad())
        genquad(rel_op, var, value, "_")
        false_list = makeList(nextquad())
        genquad("jump", "_", "_", "_")
        return true_list, false_list

    def step(self):
        self.match_token("keyword", "με_βήμα")
        exp = self.step_expression()
        return exp

    def print_stat(self):
        self.match_token("keyword", "γράψε")
        exp = self.expression()
        genquad("out",exp,"_","_")

    def input_stat(self):
        self.match_token("keyword", "διάβασε")
        id = self.identifier()
        genquad("inp",id, "_", "_")

    def call_func(self):
        id = self.identifier()

        if resolveVariable(id) == False:
            raise SyntaxError(f"Object : {id} can not be called.")

        if self.current_token and self.current_token.token == "(":
            parameters = self.actualpars()

            if(len(parameters) != getFunctionVarialbles(id)):
                raise SyntaxError(f"Number of parameters given for function or proc {id} is incorrect")

            if not checkFunctionVariables(id,parameters):
                raise SyntaxError(f"Parameters given for function or proc {id} is incorrect")

            temp = newtemp()
            scope1 = state.scopeList[state.nesting]
            ent = Entity(temp, "temp", (scope1.getScopeOffset() + 4))
            ent.setParMode(state.varListCaller)
            if temp in state.listOfVariables:
                scope1.appendEntity(ent)
            genquad("par", temp, "RET", "_")
            genquad("call", id, "_", "_")

            return temp
        return id

    def call_stat(self):
        self.match_token("keyword", "εκτέλεσε")
        id = self.identifier()
        if self.current_token and self.current_token.token == "(":
            self.actualpars()
        genquad("call", id, "_", "_")

    def actualpars(self):
        parameters = []
        self.match_token("groupSymbol", "(")
        if self.current_token.token != ")":
            parameters = self.actualparlist()
        self.match_token("groupSymbol", ")")
        return parameters

    def actualparlist(self):
        parameters = []
        id0 = self.actualparitem()
        parameters.append(id0)
        while self.current_token and self.current_token.token == ",":
            self.match_token("delimiter", ",")
            id = self.actualparitem()
            parameters.append(id)

        return parameters

    def actualparitem(self):
        if self.current_token and self.current_token.token == "%":
            self.match_token("referenceOp", "%")
            id = self.identifier()
            genquad("par",id, "ref","_")
            return "REF:"+id

        else:
            id = self.expression()
            genquad("par", id, "CV","_")
            return "CV:"+id

    def condition(self):
        Q1_true, Q1_false = self.boolterm()
        B_true = Q1_true
        B_false = Q1_false

        while self.current_token and self.current_token.token == "ή":
            backPatch(B_false, nextquad())
            self.match_token("keyword", "ή")
            Q2_true, Q2_false = self.boolterm()
            B_true = mergeList(B_true, Q2_true)
            B_false = Q2_false
        return B_true, B_false

    def boolterm(self):
        R1_true, R1_false = self.boolfactor()
        Q_true = R1_true
        Q_false = R1_false

        while self.current_token and self.current_token.token == "και":
            backPatch(Q_true, nextquad())
            self.match_token("keyword", "και")
            R2_true, R2_false  = self.boolfactor()
            Q_false = mergeList(Q_false, R2_false)
            Q_true = R2_true
        return Q_true, Q_false

    def boolfactor(self):
        if self.current_token and self.current_token.token == "όχι":
            self.match_token("keyword", "όχι")
            self.match_token("groupSymbol", "[")
            B_true, B_false  = self.condition()

            self.match_token("groupSymbol", "]")
            R_true = B_false
            R_false = B_true

        elif self.current_token and self.current_token.token == "[":
            self.match_token("groupSymbol", "[")
            B_true, B_false = self.condition()
            self.match_token("groupSymbol", "]")
            R_true = B_true
            R_false = B_false

        else:
            ex1 = self.expression()
            rel_op = self.relational_oper()
            ex2 = self.expression()
            R_true = makeList(nextquad())
            genquad(rel_op, ex1, ex2, "_")
            R_false = makeList(nextquad())
            genquad("jump", "_", "_", "_")
        return R_true, R_false

    def expression(self):

        opt_sign = self.optional_sign()
        t1 = self.term()

        if opt_sign == "-":
            w = newtemp()
            genquad(opt_sign, 0, t1, w)
            t1 = w
            scope1 = state.scopeList[state.nesting]
            ent1 = Entity(t1, "temp", (scope1.getScopeOffset() + 4))
            ent1.setParMode(state.varListCaller)
            if t1  in state.listOfVariables:
                scope1.appendEntity(ent1)

        while self.current_token and self.current_token.token in ["+", "-"]:
            operator1 = self.add_oper()
            t2 = self.term()
            w = newtemp()
            genquad(operator1, t1, t2, w)
            t1 = w
            scope1 = state.scopeList[state.nesting]
            ent2 = Entity(t1, "temp", (scope1.getScopeOffset() + 4))
            ent2.setParMode(state.varListCaller)
            if t1  in state.listOfVariables:
                scope1.appendEntity(ent2)
        return t1

    def step_expression(self):
        opt_sign = self.optional_sign()
        t1 = self.term()
        while self.current_token and self.current_token.token in ["+", "-"]:
            w = newtemp()
            operator1 = self.add_oper()
            t2 = self.term()
            genquad(operator1, t1, t2, w)
            t1 = w
        if opt_sign == "-":
            if t1.isdigit() or (t1.startswith("-") and t1[1:].isdigit()):
                return str(0 - int(t1))
            else:
                raise SyntaxError(f"Step can not be a temp value.")
        return t1

    def optional_sign(self):
        if self.current_token and self.current_token.token in ["+", "-"]:
            operator = self.add_oper()
            return operator

    def term(self):
        f1 = self.factor()
        while self.current_token and self.current_token.token in ["*", "/"]:

            operator = self.mul_oper()
            f2 = self.factor()
            w = newtemp()
            genquad(operator, f1 ,f2 , w)
            f1 = w
            scope1 = state.scopeList[state.nesting]
            ent = Entity(w, "temp", (scope1.getScopeOffset() + 4))
            ent.setParMode(state.varListCaller)
            if w in state.listOfVariables:
                scope1.appendEntity(ent)

        temp = f1
        return temp

    def factor(self):
        if self.current_token and self.current_token.token == "(":
            self.match_token("groupSymbol", "(")
            exp = self.expression()
            self.match_token("groupSymbol", ")")
            scope1 = Scope(state.nesting)
            offset = scope1.getScopeOffset()
            scope0 = state.scopeList[-1]
            entityFunc = scope0.entityList[-1]
            entityFunc.setFrameLength(offset+4)
            return exp

        elif self.current_token and self.current_token.tokenType == "identifier":
            identifier_name = self.call_func()
            return identifier_name

        elif self.current_token and self.current_token.tokenType == "number":
            number_value = self.current_token.token
            self.match_token("number")
            return number_value

        elif self.current_token and self.current_token.tokenType == "keyword":
            keyword = self.current_token.token
            return keyword

        else:
            line = self.current_token.line_counter
            raise SyntaxError(f"Error in line {line}: Expected identifier, number, or '('.")

    def relational_oper(self):
        valid_operators = ["=", "<=", ">=", "<>", "<", ">"]
        if self.current_token and self.current_token.token in valid_operators:
            relOp = self.current_token.token
            self.match_token("relationalOp")
            return relOp
        else:
            line = self.current_token.line_counter
            raise SyntaxError(f"Error in line{line}: Expected: {valid_operators}.")

    def add_oper(self):
        if self.current_token and self.current_token.token in ["+", "-"]:
            addOp = self.current_token.token
            self.match_token("mathOp")
            return addOp
        else:
            line = self.current_token.line_counter
            raise SyntaxError(f"Error in line {line}: Expected '+' or '-'.")

    def mul_oper(self):
        if self.current_token and self.current_token.token in ["*", "/"]:
            mulOp = self.current_token.token
            self.match_token("mathOp")
            return mulOp
        else:
            line = self.current_token.line_counter
            raise SyntaxError(f"Error in line {line}: Expected '*' or '/'.")