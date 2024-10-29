# Very similar to parser from MyVM
from enum import Enum

class TokenType(Enum):
  KEYWORD = 1,
  SYMBOL = 2,
  IDENTIFIER = 3,
  INT_CONST = 4,
  STRING_CONST = 5
class KeyWord(Enum):
  CLASS = 1,
  METHOD = 2,
  FUNCTION = 3,
  CONSTRUCTOR = 4,
  INT = 5,
  BOOLEAN = 6,
  CHAR = 7,
  VOID = 8,
  VAR = 9,
  STATIC = 10,
  FIELD = 11,
  LET = 12,
  DO = 13,
  IF = 14,
  ELSE = 15,
  WHILE = 16,
  RETURN = 17,
  TRUE = 18,
  FALSE = 19,
  NULL = 20,
  THIS = 21
class JackTokenizer:
  def __init__(self, inputFile, outputFile):
    self.file = open(inputFile, 'r')
    self.outfile = open(outputFile, 'w') # this isn't meant to be in the final version, but the book calls for it
    self.currToken = ""
    self.currLine = "can't be blank"
    self.tokens = [] # maybe should be like a stack?
    self.outStack = [] # holds the th

  def hasMoreTokens(self):
    if self.currLine == '' and len(self.tokens) == 0:
      self.file.close()
      self.outFin()
      self.outfile.close()
      return False
    return True

  def advance(self):
    if len(self.tokens) == 0:
      self.advanceLine()
    if len(self.tokens) != 0:
      self.currToken = self.tokens.pop(0)
    else:
      self.currToken = " "
    
  def advanceLine(self):
    next = " "
    while next != '' and (next.isspace() or next.startswith('//')):
      next = self.file.readline()
      if next.lstrip().startswith("*"):
        next = self.stripToClose(next)
      if '/*' in next:
        # before /* + after */
        next = next[:next.index('/*')] + self.stripToClose(next[next.index('/*'):]) + " "
    # now, strip off any end-of-line comments
    if '//' in next:
      next = next[:next.index('//')]
    self.currLine = next
    self.tokens.extend(self.separateTokens2(next))
    #self.tokens.extend(self.separateTokens(next))
  
  def separateTokens2(self, line):
    # TODO this will probably replace separateTokens()
    ts = []
    i = 0
    j = 0
    line = line.strip()
    while i < len(line):
      if line[i].isspace():
        i += 1
      elif line[i].isdecimal():
        j = i
        while line[i].isdecimal() and i < len(line):
          i += 1
        ts.append(line[j:i] if j != i else line[j])
      elif line[i].isalpha():
        j = i
        while (line[i].isalnum() or line[i] == '_') and i < len(line):
          i += 1
        ts.append(line[j:i] if j != i else line[j])
      elif line[i] == "\"":
        j = i
        i += 1
        found = False
        while found == False and i < len(line):
        #while i < len(line) and (line[i] != "\""):
          if line[i] == "\"":
            found = True
          i += 1
        ts.append(line[j:i] if j != i else line[j])
      
      elif line[i] in ( '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*',
                        '/', '&', '|', '<', '>', '=', '~' ):
        ts.append(line[i])
        i += 1
    return ts
  
  ## Takes a line of text and splits it into tokens
  #TODO PROBABly delete this
  def separateTokens(self, line):
    temp = line.split()
    tlist = []
    for s in temp:
      #if not s.isalnum(): #or len(s) == 1: # TODO RESOLVE THIS
      if not s.isalnum() or len(s) == 1: # TODO RESOLVE THIS
        splitSymbols = self.splitSymbols(s)
        tlist.extend(splitSymbols)
      else:
        tlist.append(s)
    return tlist

  def splitSymbols(self, word):
    symbols = ( '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*',
                '/', '&', '|', '<', '>', '=', '~' )
    final = []
    # get indices of any symbols in the term
    i = 0
    j = 0
    k = -1
    while i < len(word):
      #if word[i] in symbols or word[i] == '\"':
      if word[i] in symbols:
        if i != j: # or i == len(word) ?? 
          final.append(word[j:i])
        final.append(word[i])
        j = i + 1
        k = -1
      elif word[i].isalnum() and k == -1:
        k = i
      i += 1
    # finally, if there's any words on the end of the chunk
    if k != -1:
      final.append(word[k:])
    return final
    
  def stripToClose(self, line):
    if '*/' in line: # assuming only one open-close bracket in line
      return line[line.index('*/') + 2:]
    return ' '

  ## Returns the type of the current token
  # Jack is LL(1) except for expressions
  def tokenType(self):
    lexicalElements = {
      'keyword' : ('class', 'constructor', 'function', 'method', 'field', 'static',
                    'var', 'int', 'char', 'boolean', 'void', 'true', 'false',
                    'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return'),
      'symbol' : ('{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*',
                    '/', '&', '|', '<', '>', '=', '~'),
      'identifier' : (''), # A sequence of letters, digits, and underscores not starting with digit
      'StringConstant' : ("\"" + "A sequence of Unicode characters not including double quote or newline" + "\""),
      'Statements' : ('statements', 'statement', 'letStatement', 'ifStatement', 'whileStatement', 'doStatement', 'ReturnStatement'),
      'Expressions' : ('expression', 'term', 'subroutineCall', 'expressionList', 'op', 'unaryOp', 'KeywordConstant'),
    }
    if self.currToken in lexicalElements['keyword']:
      return TokenType.KEYWORD
    elif self.currToken in lexicalElements['symbol']:
      return TokenType.SYMBOL
    elif self.currToken.isdecimal():
      return TokenType.INT_CONST
    elif self.currToken[0] == "\"" or self.currToken[-1] == "\"":
      return TokenType.STRING_CONST
    else:
      # if it's not anything else, it's an identifier
      return TokenType.IDENTIFIER

  def keyWord(self):
    return self.currToken
  
  def symbol(self):
    return self.currToken

  def identifier(self):
    return self.currToken

  def intVal(self):
    return self.currToken

  def stringVal(self):
    return self.currToken.strip("\"")

  # under this comment are methods for outputting the xml
  def outInit(self):
    self.outfile.write(f"<tokens>")
  
  def xmlOut(self, tokenType):
    tokenDict = {
      TokenType.KEYWORD : "keyword",
      TokenType.SYMBOL : "symbol",
      TokenType.IDENTIFIER : "identifier",
      TokenType.INT_CONST : "integerConstant",
      TokenType.STRING_CONST : "stringConstant",
    }
    tempToken = self.currToken
    # if the current token is empty, don't write
    if tempToken != " ":
      if tempToken == "<":
        tempToken = "&lt;"
      elif tempToken == ">":
        tempToken = "&gt;"
      elif tempToken == "&":
        tempToken = "&amp;"
      elif tempToken[0] == "\"":
        tempToken = tempToken.strip("\"")
      self.outfile.write(f"\n  <{tokenDict[tokenType]}> {tempToken} </{tokenDict[tokenType]}>")
  
  def outFin(self):
    self.outfile.write("\n</tokens>")