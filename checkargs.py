class BadArgument(Exception):
 def __init__(self, value):
   self.parameter = value
 def __str__(self):
   return repr(self.parameter)




class checkargs(object):
  def __init__(self, *args):
    self.types = args

  def __call__(self, function):
    def check_arguments(*args):
      for arg, curtype in zip(args,self.types):
        if type(arg) != curtype:
          raise BadArgument(str(arg) + " is not of type " + str(curtype)) 
      function(*args)
    return check_arguments

@checkargs(str,int,float)
def func(name,numstuff,percent):
  print "%s %d %f" % (name,numstuff,percent)


func("hello", 1.2, 1.5)





