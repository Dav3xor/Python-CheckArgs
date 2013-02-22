import types
from pprint import pprint

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

# need a function for raising exceptions inside of
# list comprehensions, etc.
def bail(error):
  raise BadArgument(error)

class check_args_ex(object):
  """
  Extended version of check_args, you can allow multiple types
  for each argument (both int and float for instance), and
  also specify conditions for each argument.

  conditional checking can check to see if an integer is
  within an xrange, or in a list/tuple/dictionary.

  WARNING:  If you want to pass in a single list or tuple,
  it must be enclosed in another list or tuple
  
  >>> @check_args_ex((str,None),
  ...                (int, (xrange(10),(5,9))),
  ...                ((str,int),[('Jan','Feb','Mar','Apr','May')]))
  ... def dostuff2(name, age, month):
  ...     print "name = %s age = %d month = %s" % (name,age,month)
 
  >>> dostuff2("Dave",5,'May')
  name = Dave age = 5 month = May
  
  >>> dostuff2("Dave",12,'May')
  Traceback (most recent call last):
      ...
  BadArgument: '12 is not in xrange(10)'
  
  >>> dostuff2("Dave",9,'Mayx')
  Traceback (most recent call last):
      ...
  BadArgument: "Mayx is not in ('Jan', 'Feb', 'Mar', 'Apr', 'May')"

  You can also use a function:

  >>> def isvalid(arg):
  ...   if arg in (1,2,5,"hello"):
  ...     return True
  ...   else:
  ...     return False

  >>> @check_args_ex(([],[isvalid]))
  ... def dostuff3(greeting):
  ...     print greeting

  >>> dostuff3('hello')
  hello
  >>> dostuff3('goodbye')
  Traceback (most recent call last):
      ...
  BadArgument: 'goodbye fails function isvalid'

  """

  def __init__(self, *args):
    self.types, self.conditions = zip(*args)
    
    # the decorator depends on these being a list of lists (or tuples)...
    self.types = [(i,) if type(i) not in (list, tuple) else i 
                       for i in self.types]
    self.conditions = [(i,) if type(i) not in (list, tuple) else i 
                       for i in self.conditions]

  condition_functions = {
    types.FunctionType: lambda arg, condition: \
                        (bail("%s fails function %s" % (str(arg),condition.func_name)) \
                        if not condition(arg) else 1),
    types.NoneType:     lambda arg, conditions: \
                        True,
    xrange:   lambda arg, condition: \
              (bail("%s is not in %s" % (str(arg),str(condition))) 
              if arg not in condition else 1),
    list:     lambda arg, condition: \
              (bail("%s is not in %s" % (str(arg),str(condition))) 
              if arg not in condition else 1),
    tuple:    lambda arg, condition: \
              (bail("%s is not in %s" % (str(arg),str(condition))) 
              if arg not in condition else 1)
  }

  def docondition(self, arg, condition):
    self.condition_functions[type(condition)](arg,condition)

  def doconditionals(self, arg, conditionals):
    [self.docondition(arg,conditional) for conditional in conditionals]

  def dotypes(self, arg, types):
    if len(types) and type(arg) not in types:
      bail("%s is illegal type %s, legal types are: %s" % \
           (str(arg), type(arg).__name__,
            str([type(i).__name__ for i in types])))

  def __call__(self, function):
    def check_arguments(*args):
      [self.dotypes(arg,types) for arg, types in zip(args,self.types)]
      [self.doconditionals(arg,cond) for arg, cond in zip(args,self.conditions)]
      function(*args)
    return check_arguments


if __name__ == "__main__":
  import doctest
  doctest.testmod()






