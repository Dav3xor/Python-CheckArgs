class BadArgument(Exception):
 def __init__(self, value):
   self.parameter = value
 def __str__(self):
   return repr(self.parameter)


class check_args(object):
  """
  check_args allows you to simply type check arguments passed
  into a function, without writing a lot of error prone
  type checking code.

  >>> @check_args(str,int)
  ... def dostuff(name, age):
  ...     print "name = %s age = %d" % (name,age)
  >>> dostuff("Dave",5)
  name = Dave age = 5
  """
  def __init__(self, *args):
    self.types = args

  def __call__(self, function):
    def check_arguments(*args):
      for arg, curtype in zip(args,self.types):
        if type(arg) != curtype:
          raise BadArgument(str(arg) + " is not of type " + str(curtype)) 
      function(*args)
    return check_arguments

def bail(error):
  raise BadArgument(error)

class check_args_ex(object):
  """
  Extended version of check_args, it allows you to test against multiple
  conditions.  Handier, but takes more time.

  >>> @check_args_ex(str,(int,xrange(10)))
  ... def dostuff2(name, age):
  ...     print "name = %s age = %d" % (name,age)
 
  >>> dostuff2("Dave",5)
  name = Dave age = 5
  
  >>> dostuff2("Dave",12)
  Traceback (most recent call last):
  BadArgument: '12 is not in xrange(10)'
  """

  def __init__(self, *args):
    self.types = args


  conditions = {
    xrange: lambda arg, condition: (bail("%s is not in %s" % (str(arg),str(condition))) if arg not in condition else 1),
    list:   lambda arg, condition: (bail("%s is not in %s" % (str(arg),str(condition))) if arg not in condition else 1),
    tuple:  lambda arg, condition: (bail("%s is not in %s" % (str(arg),str(condition))) if arg not in condition else 1),
    type:   lambda arg, condition: (bail("%s is not of type %s" % (str(arg),str(condition))) if type(arg) != condition else 1)
  }

  def docondition(self, arg, condition):
    self.conditions[type(condition)](arg,condition)
    """
    if type(condition) == xrange and (type(arg) != int or arg not in condition):
      raise BadArgument(str(arg) + " is not in " + str(condition)) 
    
    elif type(condition) in (list,tuple) and arg not in condition:
      raise BadArgument(str(arg) + " is not in " + str(condition)) 

    elif type(condition) == type and type(arg) != condition:
      raise BadArgument(str(arg) + " is not of type " + str(condition)) 
    """ 

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


if __name__ == "__main__":
  import doctest
  doctest.testmod()






