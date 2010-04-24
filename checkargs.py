class BadArgument(Exception):
 def __init__(self, value):
   self.parameter = value
 def __str__(self):
   return repr(self.parameter)


class check_args(object):
  def __init__(self, *args):
    self.types = args

  def __call__(self, function):
    def check_arguments(*args):
      for arg, curtype in zip(args,self.types):
        if type(arg) != curtype:
          raise BadArgument(str(arg) + " is not of type " + str(curtype)) 
      function(*args)
    return check_arguments


class check_args_ex(object):
  def __init__(self, *args):
    self.types = args

  def docondition(self, arg, condition):
    if type(condition) == xrange and (type(arg) != int or arg not in condition):
      raise BadArgument(str(arg) + " is not in " + str(condition)) 
    
    elif type(condition) in (list,tuple) and arg not in condition:
      raise BadArgument(str(arg) + " is not in " + str(condition)) 

    elif type(condition) == type and type(arg) != condition:
      raise BadArgument(str(arg) + " is not of type " + str(condition)) 
      

  def __call__(self, function):
    def check_arguments(*args):
      for arg, curtype in zip(args,self.types):
        if type(curtype) in (tuple,list):
          for condition in curtype:
            self.docondition(arg,condition)
        elif type(arg) != curtype:
          raise BadArgument(str(arg) + " is not of type " + str(curtype)) 
      function(*args)
    return check_arguments



@check_args(str,int,float)
@check_args_ex(str, (int,[1,2,3,4,5],xrange(3,8)), float)
def func(name,numstuff,percent):
  print "%s %d %f" % (name,numstuff,percent)


func("hello", 2, 1.5)





