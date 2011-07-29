# PyCmdLn
Phython 3 utility for building command line interfaces

 * * *

## API

**cmdlnui.py**

cmdlnui.py provides a set of classes for building command line interfaces.
Building an interface consists of populating a Shell object with a set of
Command objects.  Command objects consist of a description, one or more aliases
for invoking the command, an handler function for executing the command and a
series of Prompt objects used to collect the parameters to pass to the handler.

### Command

A Command object represents a command that can be invoked rom the main
interface by the user.  It consists of one or aliases, a description, a set
of parameters (defined as prompts) and a handler.
  
**`__init__(default_alias, description, handler)`**

Initializes a command object with the given alias, description and handler.

 - *default_alias* The default alias for the command.  This is the alias shown when the list
   of available commands is displayed.
 - *description* A description of the command.
 - *handler* The function to invoke in order to process the desired command.

**`add_alias(alias)`**

Aliases can be added to Commands in order to make the UI more intuitive and
easier to use.  E.g. Some users prefer quit while others prefer exit, so the
exit command has both as aliases.

 - *alias* An alias that can be used to invoke the command.

**`add_parameter(prompt, name=None, cast=None)`**

Parameters are stored as Prompt objects which consist of a message to the
user and a function which converts the input into a data type/structure that
is appropriate for the handler.  

 - *prompt* The prompt for the user&#146;s input.  Either a Prompt object, a string or
   a parameterless function that returns a string.
 - *name* The name of the parameter.  This needs to match the name of the parameter
   in the command&#146;s handler function.  If not provided, the value
   returned by the prompt will be passed to the handler in the order it was
   added to the command, before any named parameters.
 - *cast* A function which transforms the string input by the user into a form that
   is recognized by the command&#146;s handler function.  If not provided
   then the default cast is used which simply returns the input string.  If
   *prompt* is a Prompt object then *cast* will be ignored.

### Prompt 

A Prompt object encapsulates a Command parameter for which the value is to
be provided by the user.  A Prompt consists of the text with which to prompt
the user, (optionally) the name of the parameter in the handler function of
the Command to which the Prompt is attached and (optionally) a cast function
used to transform the input value into a type/structure that will be
recognized by the handler function.

**`__init__(prompt, name, cast_fn)`**

Create a new Prompt.

 - *prompt* A string, or parameterless function that return a string, with which to prompt the user.
 - *name* (optional) The name of the parameter in the Command's handler function for which this prompt provides a value.
 - *cast_fn* (optional) A function which transforms the input value into a type/structure recognized by the Command's handler function.

**`prompt()`**

Prompt the user input the return the given value, and pass it through any
defined cast function.

### Shell

The Shell class encapsulates a set of commands from which the user is
continuously prompted to select.  The Shell provides two built in commands:

 - quit (exit)
 - command (cmds, show commands)

**`__init__(name=None)`**

Create a new, empty shell.

 - *name* (optional) An optional name for the shell which will be displayed when the shell is started.

**`add_command(command)`**

Add a command to the shell.

 - *command* A Command object.

**`set_global(name, value)`**

Shells provide the capacity to set named values which are global to all
commands.  If a command defines a parameter with the same name as a global
value, then the value input for the parameter's prompt will override the
global value with the same name for that command invocation.

 - *name* The name of the global value.
 - *value* The value to assign to the given name.

**`start()`**

Continuously prompt the user for commands until they invoke the quit command
using any of its aliases.

 * * *

**cmdlnprompt.py**

cmdlnprompt.py provides a set of common prompts.

 - ### DatePrompt:
   Prompts the user to input a date using yyyy-mm-dd format and
   returns a datetime.date object.

 - ### TimeDeltaPrompt: 
   Prompts the user to input a time delta in the format #w #d hh:mm:ss.micro and
   returns a datetime.timedelta object.

