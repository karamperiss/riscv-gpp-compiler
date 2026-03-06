import state

class Quad:
    def __init__(self, ID, op, x, y, z):
        self.ID = ID
        self.op = op
        self.x = x
        self.y = y
        self.z = z

    def myfunc(self):
        print(self.ID, ":" + self.op, self.x, self.y, self.z )

    def toString(self):
        return str(self.ID) + ": " + str(self.op) + " , " + str(self.x) + " , " +  str(self.y) + " , " + str(self.z)

def nextquad():
    return state.counter_nextquad + 1

def genquad(op, x, y, z):
    state.counter_nextquad += 1
    state.quadList.append(Quad(state.counter_nextquad, op, x, y, z))

def newtemp():
    state.T_i_counter += 1
    temp_name = "t@" + str(state.T_i_counter)
    state.listOfVariables.append(temp_name)
    return temp_name

def emptyList():
    return []

def makeList(x):
    return [x]

def mergeList(list1, list2):
    return list1 + list2

def backPatch(lst, z):
    for quad in state.quadList:
        if quad.ID in lst and quad.z == "_":
            quad.z = str(z)

def intermediateCodeGenerator(filename):
    with open(filename, "w", encoding="utf-8") as f:
        for i in range(len(state.quadList)):
            f.write(str(state.quadList[i].toString()) + '\n')