from enum import Enum

class Kind(Enum):
  STATIC = 1,
  FIELD = 2,
  ARG = 3,
  VAR = 4,

class SymbolTable:
  ## TIP: The Symbol Table abstraction can be implemented using
  #     two separate hash tables: one for the class scope and 
  #     another for the subroutine scope. When a new subroutine
  #     is started, the subroutine scope table can be cleared.
  def __init__(self):
    # creates a new empty symbol table
    # self.indexes = { Kind.STATIC : 0, Kind.FIELD: 0, Kind.ARG: 0, Kind.VAR: 0}
    self.indexes = { 'static' : 0, 'field': 0, 'argument': 0, 'var': 0} # this is wrong bc argument doesn't map to it
    self.classTable = {  } # new empty dict (Hash Table in python) (static, field)
    self.subroutineTable = { } # method, function, or constructor (arg, var)
    #     format of dictionary entries will be { name: (type, kind, #) }
  ## starts a new subroutine scope (i.e. resets the
  #     subroutine's symbol table)
  def startSubroutine(self):
    self.indexes['argument'] = 0
    self.indexes['var'] = 0
    self.subroutineTable.clear()
  
  ## Useful for debugging. Delete later
  def PrintTable(self, title="Printing Table"):
    print(f"       {title}")
    print(self.classTable)
    print(self.subroutineTable)
    print(self.indexes)
    print()

  def Define(self, name, idtype, kind):
    # any identifier not found in the symbol table may be assumed to be a
    #     subroutine name or class name
    # rn doesn't distinguish whether it's a class table or a subroutine table
    #print("Define called")
    if kind in ('static', 'field'):
      self.classTable[name] = (idtype, kind, self.indexes[kind])
    elif kind in ('argument', 'var'):
      self.subroutineTable[name] = (idtype, kind, self.indexes[kind])
    self.indexes[kind] += 1

  ## Returns # of variable of the given kind already
  #     defined in the current scope
  def VarCount(self, kind):
    # could just go through the table and count every time...
    print(f"{kind}: {self.indexes[kind]}")
    return self.indexes[kind]

  def KindOf(self, name):
    if name in self.subroutineTable.keys():
      return self.subroutineTable[name][1]  
    elif name in self.classTable.keys():
      return self.classTable[name][1]
    else:
      #print("name was in neither table (kind)", name)
      return None

  def TypeOf(self, name):
    if name in self.subroutineTable.keys():
      return self.subroutineTable[name][0]  
    elif name in self.classTable.keys():
      return self.classTable[name][0]
    else:
      print("name was in neither table (type)")

  def IndexOf(self, name):
    # { name : (type kind #) }  { name: (type kind)}
    #always check narrowest scope first
    if name in self.subroutineTable.keys():
      return self.subroutineTable[name][2]  
    elif name in self.classTable.keys():
      return self.classTable[name][2]
    else:
      print("name was in neither table (index)")