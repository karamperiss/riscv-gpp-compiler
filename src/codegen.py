import state
import symbol_table

def gnlvCode(n):
    gnvlCodeList = []
    nestingLvlDown = -1
    nestingLvlUp = -1
    foundEntityDown = False
    foundEntityUp = False
    for scope in state.deletedScopes:
        ScopeEntities = scope.getEntityList()
        for entity in ScopeEntities:
            if entity.getName() == n and not foundEntityDown and not foundEntityUp:
                foundEntityDown = True
                nestingLvlDown = scope.getNestingLevel()
                break

            elif entity.getName() == n and foundEntityDown and not foundEntityUp:
                currentEntityUp = entity
                foundEntityUp = True
                nestingLvlUp = scope.getNestingLevel()
                break

    if not foundEntityDown:
        raise ValueError(f"Entity {n} not found")

    gnlvCode0 = 'lw t0, -4(sp)'
    gnvlCodeList.append(gnlvCode0)

    while nestingLvlUp  < nestingLvlDown:
        gnlvCode1 = 'lw t0, -4(t0)'
        gnvlCodeList.append(gnlvCode1)
        nestingLvlUp += 1

    gnlvCode2 = 'addi t0, t0, -' + str(currentEntityUp.getOffset())
    gnvlCodeList.append(gnlvCode2)
    return gnvlCodeList

def loadvar(quadvar, tempregister):
    loadVarList = []
    currentEntity = None

    nestingLvlDown = -1
    nestingLvlUp = -1
    foundEntityDown = False
    foundEntityUp = False
    for scope in state.deletedScopes:
        ScopeEntities = scope.getEntityList()
        for entity in ScopeEntities:
            if entity.getName() == quadvar and not foundEntityDown and not foundEntityUp :
                currentEntityDown = entity
                foundEntityDown = True
                nestingLvlDown = scope.getNestingLevel()
                break

            elif entity.getName() == quadvar and foundEntityDown and not foundEntityUp :
                currentEntityUp = entity
                foundEntityUp = True
                nestingLvlUp = scope.getNestingLevel()
                break

    if  foundEntityDown and not foundEntityUp:
        nestingLvlDown = nestingLvlUp
        currentEntity = currentEntityDown

    elif foundEntityDown and foundEntityUp:
        if currentEntityUp.type == 'var':
            currentEntity = currentEntityUp
            nestingLvlDown = nestingLvlUp
        elif currentEntityDown.type == 'var':
            currentEntity = currentEntityDown
        else:
            currentEntity = currentEntityUp

    if isinstance(quadvar, int) or quadvar.isdigit():
        loadVar = 'li t'+ str(tempregister) + ',' + str(quadvar)
        loadVarList.append(loadVar)

    elif nestingLvlDown == 0:
        loadVar = 'lw t'+ str(tempregister) + ',-' + str(currentEntity.getOffset()) +'(s0)'
        loadVarList.append(loadVar)

    elif (currentEntity.parMode == "" and nestingLvlDown == nestingLvlUp) or (quadvar[0:2] =="t@" ) or (currentEntity.parMode == "in" and nestingLvlDown == nestingLvlUp):
        loadVar = 'lw t'+ str(tempregister) + ',-' + str(currentEntity.getOffset()) +'(sp)'
        loadVarList.append(loadVar)

    elif  currentEntity.parMode =="io"  and nestingLvlDown == nestingLvlUp:
        loadVar1 = 'lw t' + str(tempregister) + ',-' + str(currentEntity.getOffset()) + '(sp)'
        loadVar2 = 'lw t' + str(tempregister) + ',(t0)'
        loadVarList.append(loadVar1)
        loadVarList.append(loadVar2)

    elif (currentEntity.parMode == "" and nestingLvlDown == nestingLvlUp) or (currentEntity.parMode == "in" and nestingLvlDown != nestingLvlUp):
        loadVar1 = gnlvCode(currentEntity.getName())
        loadVar2 = 'lw t' + str(tempregister) + ',(t0)'
        loadVarList += loadVar1
        loadVarList.append(loadVar2)

    elif currentEntity.parMode == "io" and nestingLvlDown != nestingLvlUp:
        loadVar1 = gnlvCode(quadvar)
        loadVar2 = 'lw t0,(t0)'
        loadVar3 = 'lw t' + str(tempregister) + ',(t0)'
        loadVarList += loadVar1
        loadVarList.append(loadVar2)
        loadVarList.append(loadVar3)

    else:
        loadVar = "Error in loadvar"
        loadVarList.append(loadVar)
        print("loadvar(" + str(quadvar) + "," + str(tempregister) + ") has an error")

    return loadVarList

def storevar(r, v):
    currentEntity = None
    nestingLvl = -1
    storeVarList = []
    nestingLvlDown = -1
    nestingLvlUp = -1
    foundEntityDown = False
    foundEntityUp = False
    for scope in state.deletedScopes:
        ScopeEntities = scope.getEntityList()
        for entity in ScopeEntities:
            if entity.getName() == v and not foundEntityDown and not foundEntityUp:
                currentEntityDown = entity
                foundEntityDown = True
                nestingLvlDown = scope.getNestingLevel()
                break

            elif entity.getName() == v and foundEntityDown and not foundEntityUp:
                currentEntityUp = entity
                foundEntityUp = True
                nestingLvlUp = scope.getNestingLevel()
                break

    if foundEntityDown and not foundEntityUp:
        nestingLvlDown = nestingLvlUp
        currentEntity = currentEntityDown

    elif foundEntityDown and foundEntityUp:
        if currentEntityUp.type == 'var':
            currentEntity = currentEntityUp
            nestingLvlDown = nestingLvlUp
        elif currentEntityDown.type == 'var':
            currentEntity = currentEntityDown
        else:
            currentEntity = currentEntityUp

    if currentEntity is None:
        raise ValueError(f"Entity not found in storevar")


    #KATHOLIKI METAVLITI ANIKEI STO KYRIOS PROGRAMMA
    if nestingLvl == 0:
        storeVar = 'sw t' + str(r) + ',-' + str(currentEntity.getOffset()) + '(s0)'
        storeVarList.append(storeVar)

    #TOPIKH METAVLHTH H TYPIKH PARAMETROS PERNAEI ME TIMH IDIO BATHOS H PROSORINI METAVLITI
    elif (v[0:2] =="t@" ) or (currentEntity.parMode == "in" and nestingLvlDown == nestingLvlUp) or (currentEntity.parMode == "" and nestingLvlDown == nestingLvlUp):
        storeVar = 'sw t' + str(r) + ',-' + str(currentEntity.getOffset()) + '(sp)'
        storeVarList.append(storeVar)

    #TYPIKH PARAMETROS POU PERNAEI ME ANAFORA KAI BATHOS IDIO ME TREXON
    elif currentEntity.parMode == "io" and nestingLvlDown == nestingLvlUp:
        storeVar1 = 'lw t0'  + ',-' + str(currentEntity.getOffset()) + '(sp)'
        storeVar2 = 'sw t' + str(r) + ',(t0)'
        storeVarList.append(storeVar1)
        storeVarList.append(storeVar2)

    #TOPIKH METAVLITI H TYPIKH PARAMETROS(PERNAEI ME TIMH) ME VATHOS MIKROTERO APO TO TREXON
    elif (isinstance(r, str) and r[0:2] =="t@" )  or (currentEntity.parMode == "in" and nestingLvlDown != nestingLvlUp):
        storeVar1 = gnlvCode(v)
        storeVar2 = 'sw t'+ str(r)  +',(t0)'
        storeVarList += storeVar1
        storeVarList.append(storeVar2)

    #TYPIKH PARAMETROS (PERNAEI ME ANAFORA) KAI BATHOS MIKROTERO APO TREXON
    elif currentEntity.parMode == "io" and nestingLvlDown != nestingLvlUp:
        storeVar1 = gnlvCode(v)
        storeVar2 = 'lw t0,(t0)'
        storeVar3 = 'sw t' + str(r) +',(t0)'
        storeVarList += storeVar1
        storeVarList.append(storeVar2)
        storeVarList.append(storeVar3)

    else:
        storeVar = "Error in storevar"
        storeVarList.append(storeVar)
        print("storevar("+str(r)+","+str(v)+") has an error")

    return  storeVarList

def quadToFinalCode(quad):
    retList = []
    flag = True

    if quad.op =="jump":
        ret = "j L_" + str(quad.z)
        retList.append(ret)

    #relop(?),x,y,z
    elif quad.op == "=":
        ret1 = loadvar(quad.x, 1)
        ret2 = loadvar(quad.y, 2)
        ret3 = "beq t" + str(1) + "," + "t" + str(2) + ",L_" + str(quad.z)
        retList += ret1 + ret2
        retList.append(ret3)

    elif quad.op == "<":
        ret1 = loadvar(quad.x, 1)
        ret2 = loadvar(quad.y, 2)
        ret3 = "blt t" + str(1) + "," + "t" + str(2) + ",L_" + str(quad.z)
        retList += ret1 + ret2
        retList.append(ret3)

    elif quad.op == "<=":
        ret1 = loadvar(quad.x, 1)
        ret2 = loadvar(quad.y, 2)
        ret3 = "ble t" + str(1) + "," + "t" + str(2) + ",L_" + str(quad.z)
        retList += ret1 + ret2
        retList.append(ret3)

    elif quad.op == "<>":
        ret1 = loadvar(quad.x, 1)
        ret2 = loadvar(quad.y, 2)
        ret3 = "bne t" + str(1) + "," + "t" + str(2) + ",L_" + str(quad.z)
        retList += ret1 + ret2
        retList.append(ret3)

    elif quad.op == ">":
        ret1 = loadvar(quad.x, 1)
        ret2 = loadvar(quad.y, 2)
        ret3 = "bgt t" + str(1) + "," + "t" + str(2) + ",L_" + str(quad.z)
        retList += ret1 + ret2
        retList.append(ret3)

    elif quad.op == ">=":
        ret1 = loadvar(quad.x, 1)
        ret2 = loadvar(quad.y, 2)
        ret3 = "bge t" + str(1) + "," + "t" + str(2) + ",L_" + str(quad.z)
        retList += ret1 + ret2
        retList.append(ret3)

    #:=,x,"_",z
    elif quad.op == ":=":
        ret1 = loadvar(quad.x, 1)
        ret2 = storevar(1, quad.z)
        retList += ret1 + ret2

    #op,x,y,z
    elif quad.op == "+":
        ret1 = loadvar(quad.x, 1)
        ret2 = loadvar(quad.y, 2)
        ret3 = "add " + "t" + str(1)+ "," + "t" + str(1) + ","+ "t" + str(2)
        ret4 = storevar(1, quad.z)
        retList = retList + ret1 + ret2
        retList.append(ret3)
        retList += ret4

    elif quad.op == "-":
        ret1 = loadvar(quad.x, 1)
        ret2 = loadvar(quad.y, 2)
        ret3 = "sub " + "t" + str(1) + "," + "t" + str(1) + "," + "t" + str(2)
        ret4 = storevar(1, quad.z)
        retList += ret1 + ret2
        retList.append(ret3)
        retList += ret4

    elif quad.op == "*":
        ret1 = loadvar(quad.x, 1)
        ret2 = loadvar(quad.y, 2)
        ret3 = "mul " + "t" + str(1) + "," + "t" + str(1) + "," +  "t" + str(2)
        ret4 = storevar(1, quad.z)
        retList += ret1 + ret2
        retList.append(ret3)
        retList += ret4

    elif quad.op == "/":
        ret1 = loadvar(quad.x, 1)
        ret2 = loadvar(quad.y, 2)
        ret3 = "div " + "t" + str(1) + "," + "t" + str(1)+ "," + "t" + str(2)
        ret4 = storevar(1, quad.z)
        retList += ret1 + ret2
        retList.append(ret3)
        retList += ret4

    #retv,"_","_",x
    elif quad.op == "retv":
        ret1 = loadvar(quad.x, 1)
        ret2 = "lw t0,-8(sp)"
        ret3 = "sw t1,(t0)"
        retList += ret1
        retList.append(ret2)
        retList.append(ret3)

    #par,x,CV,_
    elif quad.op == "par":
        foundQuad = False

        if state.parCounter == 0:
            for q in state.quadList:
                if q.ID == quad.ID:
                    foundQuad = True
                    entity_var = symbol_table.getEntityFromScopeList(quad.x)
                elif foundQuad and q.op == "call":
                    entity_func = symbol_table.getEntityFromScopeList(quad.x)
                    framelength = entity_func.getFrameLength()
                    break

            ret = 'addi fp, sp,' + str(framelength)
            retList.append(ret)

        if quad.y == "CV":
            pos = 12 + (4 * state.parCounter)
            state.parCounter +=1
            ret1 = loadvar(quad.x, 1)
            ret2 = "sw t1," + "-" + str(pos) + "(fp)"
            retList += ret1
            retList.append(ret2)

        elif quad.y == "ref":
            pos = 12 + (4 * state.parCounter)
            state.parCounter +=1
            entity = symbol_table.getEntityFromScopeList(quad.x)
            offset = entity.getOffset()

            variableFound = False
            variableNesting = 0
            for scope in state.scopeList:
                for entity_in_scope in scope.entityList:
                    if entity_in_scope.name == quad.x:
                        variableFound = True

                if(variableFound):
                    variableNesting = scope.getNestingLevel()
                    break

            if state.nesting == variableNesting or (entity_var.getParMode() == 1 and 'in' in entity_func.getArgumentList()):
                ret1 = "addi t1,sp" + "," + "-" + str(offset)
                ret2 = "sw t1"+ "," + "-" + str(pos) + "(fp)"
                retList.append(ret1)
                retList.append(ret2)

            elif state.nesting == variableNesting or (entity_var.getParMode() == 1 and 'io' in entity_func.getArgumentList()):
                ret1 = "lw t1"+ "," + "-" + str(offset) + "(sp)"
                ret2 = "sw t1" + "," + "-" + str(pos) + "(fp)"
                retList.append(ret1)
                retList.append(ret2)

            elif state.nesting != variableNesting or (entity_var.getParMode() == 1 and 'in' in entity_func.getArgumentList()):
                ret1 = gnlvCode(quad.x)
                ret2 = "sw t1" + "," + "-" + str(pos) + "(fp)"
                retList += ret1
                retList.append(ret2)

            elif state.nesting != variableNesting or (entity_var.getParMode() == 1 and 'io' in entity_func.getArgumentList()):
                ret1 = gnlvCode(quad.x)
                ret2 = "lw t1,(t1)"
                ret3 = "sw t1" + "," + "-" + str(pos) + "(fp)"
                retList += ret1
                retList.append(ret2)
                retList.append(ret3)

            elif variableNesting == 0:
                print("VARIABLE NOT FOUND IN REF")

        elif quad.y =="RET":
            entity = symbol_table.getEntityFromScopeList(quad.x)
            offset = entity.getOffset()
            ret1 = "addi t1,sp,"+ "-" + str(offset)
            ret2 = "sw t1,-8(fp)"
            retList.append(ret1)
            retList.append(ret2)

    elif quad.op == "call":
        for scope in state.deletedScopes:
            for entity in scope.entityList:
                if entity.name == quad.x:
                    nestingLvl = scope.getNestingLevel()
                break

        entity = symbol_table.getEntityFromScopeList(quad.x)
        framelength = entity.getFrameLength()

        if state.nesting == nestingLvl:
            ret1 = "lw t1,-4(sp)"
            ret2 = "sw t0,-4(sp)"
            retList.append(ret1)
            retList.append(ret2)

        elif state.nesting != nestingLvl:
            ret = "sw sp,-4(fp)"
            retList.append(ret)

        retMove1 = "addi sp,sp," + str(framelength)
        retFunc = "jal " + quad.x
        retMove2 = "addi sp,sp," +"-" +  str(framelength)
        retList.append(retMove1)
        retList.append(retFunc)
        retList.append(retMove2)

    elif quad.op == "begin_block":
        flag = False
        if quad.x == state.programName:
            for scope in state.deletedScopes:
                if scope.getNestingLevel() == 0:
                    mainFrameLength = scope.getScopeOffset()
                    break

            ret1 = "Lmain:"
            ret2 = "addi sp,sp," + "-" + str(mainFrameLength)
            ret3 = "addi gp,sp,0"
            retList.append(ret1)
            retList.append(ret2)
            retList.append(ret3)

        else:
            ret1 = quad.x + ":"
            ret2 = "sw ra,(sp)"
            retList.append(ret1)
            retList.append(ret2)

    elif quad.op == "halt":
        ret1 = "li a7,10"
        ret2 = "ecall"
        ret3 = "la a0,str_nl"
        ret4 = "li a7,4"
        ret5 = "ecall"
        retList.append(ret1)
        retList.append(ret2)
        retList.append(ret3)
        retList.append(ret4)
        retList.append(ret5)

    elif quad.op == "end_block":
        ret1 = "lw ra,(sp)"
        ret2 = "jr ra"
        retList.append(ret1)
        retList.append(ret2)

    elif quad.op =="inp":
        entity = symbol_table.getEntityFromScopeList(quad.x)
        ret1 = "li a7,5"
        ret2 = "ecall"
        ret3 = "addi t0,a0,0"
        ret4 = storevar(0, entity.getName())
        retList.append(ret1)
        retList.append(ret2)
        retList.append(ret3)
        retList += ret4

    elif quad.op =="out":
        entity = symbol_table.getEntityFromScopeList(quad.x)
        ret1 = "li a7,1"

        if isinstance(entity, int):
            ret2 = loadvar(entity, 0)
        else:
            if isinstance(entity, symbol_table.Entity):
                ret2 = loadvar(entity.getName(), 0)
            elif isinstance(int(entity), int):
                ret2 = loadvar(entity, 0)

        ret3 = "addi a0,t0,0"
        ret4 = "ecall"
        ret5 = "la a0,str_nl"
        ret6 = "li a7,4"
        ret7 = "ecall"

        retList.append(ret1)
        retList += ret2
        retList.append(ret3)
        retList.append(ret4)
        retList.append(ret5)
        retList.append(ret6)
        retList.append(ret7)

    if flag == True:
        retListAdd = "L_" + str(quad.ID) + ":"
        retList.insert(0,retListAdd)

    return retList

def test_quadToFinalCode_and_write_output(final_code_filename):
    state.parCounter = 0
    output_lines = []

    for quad in state.quadList:
        retList = quadToFinalCode(quad)
        output_lines.extend(retList)

    with open(final_code_filename, "w", encoding="utf-8") as f:
        f.write('.data\n')
        f.write('str_nl: .asciz "\\n"\n')
        f.write('.text\n')
        f.write('j Lmain\n')
        for line in output_lines:
            f.write(line + "\n")