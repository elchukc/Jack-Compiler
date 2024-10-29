import re
import SymbolTable
# for now just a parsing process
class CompilationEngine:
  def __init__(self, inputFile, outputFile): #inputFile, outputFile):
    self.infile = open(inputFile, 'r')
    self.outfile = open(outputFile, 'w')
    self.symTable = SymbolTable.SymbolTable()
    self.CompileClass()

  def adv(self):
    x = self.infile.readline()
    self.outfile.write(f"{x}")
    return x
  # for identifier, write 1) identifier category (var, argument, static, field, class, subroutine)
  #                       2) whether it's being DEFINED or USED
  #                       3) whether it represents a variable of the four kinds (var, argument, static, field)
  #                           and the running index assigned to that identifier
  def CompileClass(self):
    # class classname { classVarDec* subroutineDec* }
    # <class>
    #   <keyword> class </keyword>
    #   <identifier> className </identifier>
    #   <symbol> { </symbol>
    #   <classVarDec></classVarDec>* NOW THIS IS THE PART YOU MUST CHECK to see if there's classVarDecs
    #   <subroutineDec></subroutineDec>* NOW THIS IS THE PART YOU MUST CHECK whether there's subroutineDecs
    #   <symbol> } </symbol>
    # </class>
    # classVarDec: static | field
    # subroutineDec: constructor | function | method

    # so that should be keyword, identifier, symbol, ****, symbol
    self.infile.readline() # just to get past token line
    self.outfile.write(f"<class>\n")
    # there are three elements before we have to make looping choices: class, className, symbol
    for i in range(3):
      x = self.adv()
      if i == 1:
        name = x.split()[1]
        self.printIdentifier(name, kind='class')
        self.writeIdentifier(name, kind='class')
    
    # NOW time to check if we need to call compileClassVarDec and CompileSubroutine
    x = self.peek()
    while x.split()[1] != "}":
      if x.split()[1] in ("static", "field"):
        self.CompileClassVarDec()
        x = self.peek()
      elif x.split()[1] in ("constructor", "function", "method"):
        self.CompileSubroutine()
        x = self.peek()
      x = self.peek()

    self.adv() # for the last closing bracket
    self.outfile.write("</class>")
    self.symTable.PrintTable(title="FINAL")

  def CompileClassVarDec(self):
    #  (static|field) type varName, varName, varName, varName, varName, varName;
    #           (int char boolean className)
    #     this field is always being defined, and it's always class scope
    #   field int x, y, z, a;  kind type name, name, name, name;
    self.outfile.write("<classVarDec>\n")
    x = self.adv() # (static field)
    kind = x.split()[1]
    x = self.adv() # type -> (int char boolean className)
    if x.split()[0] == "<identifier>": # then it's className. And it's being referenced, not declared
      self.outfile.write(f"{x.split()[1]}.     category: className, USED, NOT IN SYMBOL TABLE")
    idtype = x.split()[1]

    #  // end of our new alternative to the commented out for loop #TODO
    while x.split()[1] != ";":
      x = self.adv()
      if x.split()[0] == "<identifier>": # this is how we do identifier stuff for Ch11 Symbol Table
        name = x.split()[1]
        self.symTable.Define(name, idtype, kind)
        self.outfile.write(f"{name}.     category: {kind}, DEFINED, {self.symTable.IndexOf(name) if self.symTable.KindOf(name)!= None else 'NOT IN TABLE'}")
    self.outfile.write("</classVarDec>\n")

  def CompileSubroutine(self):
    #   subroutineDec: constructor | function | method
    #   ( void | type ) subroutineName ( parameterlist ) subroutineBody
    self.symTable.PrintTable()
    self.symTable.startSubroutine()
    self.outfile.write("<subroutineDec>\n")
    # up to initial ( before parameterlist
    for i in range(4):
      x = self.adv()
      if i == 1: # is type
        idtype = x.split()[1]
        if x.split()[0] == "<identifier>": 
          self.printIdentifier(x.split()[1], None, isClassName=True)
          name = x.split()[1]
          self.outfile.write(f"{x.split()[1]}.     category: className, USED, NOT IN SYMBOL TABLE")
      elif i == 2 and x.split()[0] == "<identifier>":
        name = x.split()[1]
        # THERE'S NO DEFINING A METHOD FOR SYMBOL TABLE 
        # EXCEPT THE HIDDEN SELF ARGUMENT?? TODO
        # bht the categories are var, argument, static, field, class, subroutine
        kind = 'subroutine'
        self.printIdentifier(name, kind)
        self.writeIdentifier(name, kind)
        #print(f"{name}.     category: {kind}, DEFINED, {self.symTable.IndexOf(name) if self.symTable.KindOf(name)!= None else 'NOT IN TABLE'}")
        #self.outfile.write(f"{name}.     category: {kind}, DEFINED, {self.symTable.IndexOf(name) if self.symTable.KindOf(name)!= None else 'NOT IN TABLE'}")

    self.compileParameterList()
    self.adv() # closing bracket )
    # now for subroutineBody, which it appears doesn't have a method
    # subroutineBody:
    #     { varDec* statements }
    self.outfile.write("<subroutineBody>\n")

    self.adv() # for the opening brace {
    x = self.peek()
    while x.split()[1] == 'var':
      self.compileVarDec()
      x = self.peek()
    self.compileStatements()
    self.adv() # just the closing bracket
    self.outfile.write("</subroutineBody>\n")
    self.outfile.write("</subroutineDec>\n")

  def compileParameterList(self):
    self.outfile.write("<parameterList>\n")
    #x = self.peek()
    #while x.split()[1] != ")":
    #  self.adv()
    #  x = self.peek()
    # ((type varName)(, type varName)*)?
    x = self.peek()
    while x.split()[1] != ")":
      x = self.adv()
      idtype = x.split()[1] # type
      if x.split()[0] == '<identifier>':
        self.printIdentifier(idtype, None, isClassName=True)
      name = self.adv().split()[1] # varName
      kind = 'argument'

      self.symTable.Define(name, idtype, kind)
      self.printIdentifier(name, kind)
      self.outfile.write(f"{name}.     category: {kind}, DEFINED, {self.symTable.IndexOf(name) if self.symTable.KindOf(name)!= None else 'NOT IN TABLE'}")
      x = self.peek()
      if x.split()[1] == ',': self.adv()
    self.outfile.write(" </parameterList>\n")

  def printIdentifier(self, name, kind, isClassName=False):
    #if isClassName:
    #  print(f"{'{:<14}'.format(name)} category: className, USED, NOT IN SYMBOL TABLE")
    #else:
    #  print(f"{'{:<14}'.format(name)} category: {kind}, DEFINED, {self.symTable.IndexOf(name) if self.symTable.KindOf(name)!= None else 'NOT IN TABLE'}")
    return
  
  def writeIdentifier(self, name, kind, using=False, isClassName=False):
    if isClassName:
      self.outfile.write(f"{name} category: className, USED, NOT IN SYMBOL TABLE")
    else:
      self.outfile.write(f"{name} category: {kind}, {'USED' if using else 'DEFINED'}, {self.symTable.IndexOf(name) if self.symTable.KindOf(name)!= None else 'NOT IN TABLE'}")
    
  def compileVarDec(self):
    # varDec:   var type varName (, varName)*;
    self.outfile.write("<varDec>\n")
    kind = 'var'
    #for i in range(4): # it always has at least 4 tokens. The 4th is either , or ;
    #  x = self.adv()
    #while x.split()[1] != ";":
    #  x = self.adv()
    self.adv()
    x = self.adv()
    idtype = x.split()[1]
    # TODO perhaps some method for writeIdentifier, like printIdentifier
    #      and a getType() that splits x for you and writes Identifier if it's a className
    if x.split()[0] == '<identifier>':
      name = x.split()[1]
      self.printIdentifier(name, kind)
      self.outfile.write(f"{name}.     category: className, USED, NOT IN SYMBOL TABLE")
    
    while x.split()[1] != ";":
      name = self.adv().split()[1]
      self.symTable.Define(name, idtype, kind)
      self.outfile.write(f"{name}.     category: {kind}, DEFINED, {self.symTable.IndexOf(name) if self.symTable.KindOf(name)!= None else 'NOT IN TABLE'}")
      # it goes identifier, , or ;, identifier, , or ; .....
      x = self.adv()
      
    
    self.outfile.write("</varDec>\n")

  def compileStatements(self):
    statements = {
      "let" : self.compileLet,
      "if" : self.compileIf,
      "while" : self.compileWhile,
      "do" : self.compileDo,
      "return" : self.compileReturn, }
    self.outfile.write("<statements>\n")
    x = self.peek()
    while x.split()[1] in statements.keys():
      statements[x.split()[1]]()
      x = self.peek()
      
    self.outfile.write("</statements>\n")

  def compileDo(self):
    self.outfile.write("<doStatement>\n")
    self.adv() # for do
    # then, always subroutineCall
    self._subroutinecall(wroteFirstIdentifier=False)
    self.adv() # for ;
    self.outfile.write("</doStatement>\n")

  def compileLet(self):
    # let varName ([ expression ])? = expression ;
    self.outfile.write("<letStatement>\n")
    for i in range(2):
      x = self.adv()
    name = x.split()[1] # varName
    kind = self.symTable.KindOf(name)
    self.writeIdentifier(name, kind, using=True) # TODO wrap in the part where you add it into symboltable
    x = self.adv() # this is either [ or =
    if x.split()[1] == "[": # if we just wrote [
      self.compileExpression()
      for i in range(2):
        self.adv() # and cap off the square brackets ] and =
    self.compileExpression()
    self.adv() # for the last ;
    self.outfile.write("</letStatement>\n")

  def compileWhile(self):
    self.outfile.write("<whileStatement>\n")
    # while ( expression ) { statements }
    for i in range(2):
      self.adv()
    self.compileExpression()
    for i in range(2):
      self.adv() # for closing bracket ) and opening brace {
    self.compileStatements()
    self.adv() # for closing brace }

    self.outfile.write("</whileStatement>\n")

  def compileReturn(self):
    self.outfile.write("<returnStatement>\n")
    self.adv()
    if self.peek().split()[1] != ';':
      self.compileExpression()
    
    self.adv()
    self.outfile.write("</returnStatement>\n")

  def compileIf(self):
    self.outfile.write("<ifStatement>\n")
    # if ( expression ) { statements } ( else { statements } )?
    for i in range(2):
      self.adv()
    self.compileExpression()
    for i in range(2):
      self.adv()
    self.compileStatements()

    self.adv() # closing brace }
    # else block
    x = self.peek()
    if x.split()[1] == "else":
      for i in range(2):
        self.adv() # for else and opening brace {
      self.compileStatements()
      # for final closing brace
      self.adv()

    self.outfile.write("</ifStatement>\n")

  def compileExpression(self):
    self.outfile.write("<expression>\n")
    self.compileTerm()
    x = self.peek()
    while x.split()[1] in ('+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '='): # or, while the next token is an expression, so an identifier or an opening bracket
      self.adv()
      self.compileTerm()
      x = self.peek()
    self.outfile.write("</expression>\n")

  def _subroutinecall(self, wroteFirstIdentifier=False): # Subroutinecall is called from compileDo or compileTerm
    # la can be ( or . for    subroutineName(expressionList) | className|varName.subroutineName( expressionList )
    # ASSUMING the initial identifier has not already been written
    if not wroteFirstIdentifier:
      x = self.adv()
      name = x.split()[1]
      kind = self.symTable.KindOf(name)
      isClassName = False if kind == 'var' else True
      #print(f"IS IT A VAR? {not isClassName}, {kind} {name}")
      self.printIdentifier(name, kind, isClassName=isClassName)
      self.writeIdentifier(name, kind, using=True, isClassName=isClassName)
      self.outfile.write("\nthis is where")

    x = self.adv() # this will either be ( or .

    if x.split()[1] == '(':   #  className|varName.subroutineName( expressionList )
      r = 0
    else:  # x == '.'   #  subroutineName( expressionList )
      r = 2

    for i in range(r):
      if i == 1:
        name = x.split()[1]
        self.writeIdentifier(name, kind='subroutine', using=True)
      x = self.adv()
    self.compileExpressionList()
    self.adv()

  def compileTerm(self):
    # integerConstant | stringConstant | keywordConstant | varName | varName [ expression ] |
    #       | subroutineCall | ( expression ) | unaryOp term
    self.outfile.write("<term>\n")
    
    x = self.adv() # for single-token integerConstant | stringConstant | keywordConstant | varName 
    if x.split()[0] == '<identifier>':
      # "If the current token is an identifier, the routine must distinguish between 
      # a variable, an array entry, and a subroutine call. A single look-ahead token,
      # which may be [, (, or . suffices. Any other token is not part of this term and should not be advanced over"

      # first we must record the first identifier, be it subroutineName, varName or className
      name = x.split()[1]
      self.writeIdentifier(name, self.symTable.KindOf(name), using=True)
      #self.printIdentifier(name, self.symTable.KindOf(name))
      #self.writeIdentifier(name, self.symTable.KindOf(name), using=True,)
      la = self.peek().split()[1]
      if (la == '('): # it is a subroutine call subroutineName( expressionList )
        kind = None
        # then we just wrote was subroutineName
        self.writeIdentifier(name, None, using=True)
        self._subroutinecall(wroteFirstIdentifier=True)
      elif (la == '['): # it's an array varName[ expression ]
        kind = 'var' # !!!!!!
        self.writeIdentifier(name, kind, using=True)
        self.adv() # for [
        self.compileExpression()
        self.adv() # for ]
      elif (la == '.'): # subroutine call className|varName.subroutineName ( expressionList )
        # then it was a className or varName. 
        kind = self.symTable.KindOf(name)
        isClassName = kind == None
        #print(f"{name} isClassName is {isClassName}.  {self.symTable.KindOf(name)}")
        self.writeIdentifier(name, kind, using=True, isClassName=isClassName)
        self._subroutinecall(wroteFirstIdentifier=True)
      # else it's not part of the term and should not be advanced on
    else:
      # this leaves integerConstant | stringConstant | keywordConstant |  ( expression ) | unaryOp term
      if x.split()[1] == '(':
        # then it's ( expression )
        self.compileExpression()
        self.adv()
      elif x.split()[1] in '-~':
        self.compileTerm()
      
    self.outfile.write("</term>\n")

  def compileExpressionList(self):
    # [totally empty]
    # expression, expression, expression
    # (expression (, expression)*)?
    self.outfile.write("<expressionList>\n")
    x = self.peek()
    while x.split()[1] != ")":

      self.compileExpression()
      x = self.peek()
      if x.split()[1] == ",":
        self.adv()
      x = self.peek()
    self.outfile.write(" </expressionList>\n")

  # looks ahead one line. Don't know how this handles end-of-file
  def peek(self):
    pos = self.infile.tell()
    line = self.infile.readline()
    self.infile.seek(pos)
    return line

  # not in specs but needed for now
  def Close(self):
    self.infile.close()
    self.outfile.close()
  