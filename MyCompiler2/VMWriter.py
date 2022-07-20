class VMWriter:
  def __init__(self, outputFile):
    self.outfile = open(outputFile, 'w')

  def writePush(self):
    pass

  def writePop(self):
    pass

  def WriteArithmetic(self):
    pass

  def WriteLabel(self):
    pass

  def WriteGoto(self, label):
    pass

  def WriteIf(self, label):
    pass

  def WriteCall(self, label):
    pass

  def close(self):
    self.outfile.close()