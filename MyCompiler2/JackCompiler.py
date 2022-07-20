import os, sys
from JackTokenizer import JackTokenizer, TokenType
from CompilationEngine import CompilationEngine

sourcedir = ''
if os.path.isdir(sys.argv[1]):
  sourcedir = sys.argv[1]
else:
  sourcedir = os.path.dirname(sys.argv[1])
# make a subfolder for the output
newdirpath = sourcedir + '/AnalyzerOutput'
if not os.path.exists(newdirpath):
  os.mkdir(newdirpath) 

# we make a separate xml file for each input
for jack in os.listdir(sourcedir):
  if jack.endswith(".jack"):
    tokenizer = JackTokenizer(sourcedir + "/" + jack, newdirpath + '/' + jack[:jack.rindex('.')] + 'T.xml')
    print("STARTING CLASS", jack)
    tokenizer.outInit()
    tokenizer.advance()
    while tokenizer.hasMoreTokens():
      tokenType = tokenizer.tokenType()
      token = tokenizer.currToken
      if tokenType == TokenType.KEYWORD:
        token = tokenizer.keyWord()
      elif tokenType == TokenType.SYMBOL:
        token = tokenizer.symbol()
      elif tokenType == TokenType.IDENTIFIER:
        token = tokenizer.identifier()
      elif tokenType == TokenType.INT_CONST:
        token = tokenizer.intVal()
      elif tokenType == TokenType.STRING_CONST:
        token = tokenizer.stringVal()
      tokenizer.xmlOut(tokenType)
      tokenizer.advance()
    
    compileEngine = CompilationEngine(newdirpath + '/' + jack[:jack.rindex('.')] + 'T.xml', 
                                      newdirpath + '/' + jack[:jack.rindex('.')] + '.xml')
    
    
    
    compileEngine.Close()