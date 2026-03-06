import state

class Entity:
    def __init__(self, name, type, offset):
        self.name = name
        self.type = type
        self.offset = offset
        self.startQuad = 0
        self.argumentList = []
        self.frameLength = 0
        self.value = ""
        self.parMode = ""
        self.NumOfParameters = 0
        self.CvParameters = 0
        self.RefParameters = 0

    def setName(self,name): self.name = name
    def setStartQuad(self, quad): self.startQuad = quad
    def setArgumentList(self, argumentList): self.argumentList = argumentList
    def setFrameLength(self, frameLength): self.frameLength = frameLength
    def setValue(self, value): self.value = value
    def setParMode(self, parMode): self.parMode = parMode
    def setNumOfParameters(self, numOfParameters): self.NumOfParameters = numOfParameters
    def setCvParameters(self, cvParameters): self.CvParameters = cvParameters
    def setRefParameters(self, refParameters): self.RefParameters = refParameters

    def getName(self): return self.name
    def getStartQuad(self): return self.startQuad
    def getArgumentList(self): return self.argumentList
    def getFrameLength(self): return self.frameLength
    def getValue(self): return self.value
    def getParMode(self): return self.parMode
    def getOffset(self): return self.offset
    def getNumOfParameters(self): return self.NumOfParameters
    def getCvParameters(self): return self.CvParameters
    def getRefParameters(self): return self.RefParameters

    def addArgument(self, argument):
        self.argumentList.append(argument)

class Scope:
    def __init__(self, nestingLevel):
        self.entityList = []
        self.nestingLevel = nestingLevel

    def setEntityList(self, entity): self.entity = entity
    def setNestingLevel(self, nestingLevel): self.nestingLevel = nestingLevel
    def getEntityList(self): return self.entityList
    def getNestingLevel(self): return self.nestingLevel
    def appendEntity(self, entity): self.entityList.append(entity)

    def getScopeOffset(self):
        if len(self.entityList) == 0:
            return 0
        else:
            lastEntity = -1
            entity = self.entityList[lastEntity]
            while(entity.getOffset() < 0):
                lastEntity -= 1
                entity = self.entityList[lastEntity]
            return entity.getOffset()

    def getEntityNames(self):
        entityNames = []
        for entity in self.entityList:
            entityNames.append(entity.name)
        return entityNames

class Argument:
    def __init__(self, parMode):
        self.parMode = parMode
    def setParMode(self, parMode): self.parMode = parMode
    def getParMode(self): return self.parMode

def symbolTableGenerator(filename):
    with open(filename, "w", encoding="utf-8") as file1:
        file1.write("Symbol Table:\n")
        for scope in state.deletedScopes:
            file1.write("\n")
            file1.write("Scope " + str(scope.getNestingLevel()) + ":\n")
            for entity in scope.getEntityList():
                if entity.getOffset() == 8:
                    file1.write( entity.type + " : " + entity.name + "\n")
                elif entity.getFrameLength() > 0:
                    file1.write(entity.name + " : Type: " + entity.type +  ", FrameLength: " + str(entity.getFrameLength()) + ",startQuad: " + str(entity.getStartQuad()))
                    for argument in entity.getArgumentList():
                        file1.write(" , " + str(argument.getParMode()))
                    file1.write("\n")
                else:
                    file1.write(entity.name + " : Type: " + entity.type + " , Offset: " + str(entity.getOffset()) + "\n")

# ΣΗΜΑΣΙΟΛΟΓΙΚΗ ΑΝΑΛΥΣΗ
def getEntityFromScopeList(entityName):
    if entityName.isdigit():
        return entityName
    else:
        for scope in state.deletedScopes:
            for entity in scope.getEntityList():
                if entity.getName() == entityName:
                    return entity

def getEntityFromScopeList2(entityName):
    for scope in state.scopeList:
        for entity in scope.getEntityList():
            if entity.getName() == entityName:
                return entity

def resolveVariable(variable):
    foundVariable = False
    for scope in state.scopeList:
        for entity in scope.entityList:
            if entity.getName() == variable:
                foundVariable = True
                return foundVariable
    return foundVariable

def getFunctionVarialbles(function):
    entityList = state.scopeList[-1].entityList
    for entity in entityList:
        if entity.getName() == function:
            return entity.getNumOfParameters()
    return -1

def checkFunctionVariables(function, variables):
    entityList = state.scopeList[-1].entityList
    FunctionEntity = None
    for entity in entityList:
        if entity.getName() == function:
            FunctionEntity = entity

    CV_variables = FunctionEntity.getCvParameters()
    RET_variables = FunctionEntity.getRefParameters()

    argList = []
    for argument in FunctionEntity.getArgumentList():
        argList.append(str(argument.getParMode()))

    for variable in variables:
        if variable[0:2] == "CV"  and 'in' in argList:
            CV_variables -= 1
        elif variable[0:3] == "REF" and 'io' in argList:
            RET_variables -= 1

    if CV_variables == RET_variables == 0:
        return True
    else:
        return False