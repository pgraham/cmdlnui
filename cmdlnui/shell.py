"""This module provides classes for building a command line interface.

The main interface is encapsulated in a Shell object to which Command objects
are added.  Command objects consist of a description, one or more aliases for
invoking the command, a handler function for executing the command and a series
of Prompt objects used to collect the parameters to pass to the handler.
"""
import collections

class Command(object):
    """This class encapsulates a command that can be invoked from the main
    interface by the user.

    Commands can be assigned one or more aliases for invocation and may contain
    Prompt objects used to collect the parameters to pass to the command's
    handler function.
    """

    def __init__(self, defaultAlias, description, handler):
        """Inits a Command object with the given alias, description and handler.
        Args:
            defaultAlias: The default alias for the command.
            description: A description of the command.
            handler: Function to invoke to perform the described command
        """
        self.aliases = []
        self.params = []

        self.aliases.append(defaultAlias)
        self.desc = description
        self.fn = handler

    def addAlias(self, alias):
        """Add an alias that can be used to invoke the command.

        Aliases can be added to Commands in order to make the UI more intuitive,
        e.g. Some users prefer quit, others exit so the exit command has both as
        aliases.

        Args:
            alias: The alias that can be used to invoke the command.

        Returns: self
        """
        self.aliases.append(alias)
        return self

    def addParameter(self, prompt, name=None, cast=None):
        """Adds a parameter to pass to the command handler.

        Parameters are stored as Prompt objects which consist of a message to
        the user and a function which converts the inputted string into a data
        type/structure that will be recognized by the handler.  A Prompt object
        can be added directly, a string with which to prompt the user or a
        function with no parameters which returns a string.  The default cast
        function simply returns the input string.  If Prompt object is provided
        then the cast parameter is ignored.

        Args:
            prompt: The prompt for the user's input.  Either a Prompt object, a
                string or a parameterless function that returns a string.
            name: The name of the parameter.  This needs to match the name of
                the parameter in the commands handler function to which the
                input corresponds.  If not provided the parameter will be passed
                to the handler in the order it was added before any named
                parameters.
            cast: Function which transforms the string input by the user into
                a form that is recognized by the command's handler function.

        Returns: self
        """
        if cast is None:
            cast = lambda x: x

        if isinstance(prompt, Prompt):
            prmt = prompt
        else:
            prmt = Prompt(prompt, name, cast)

        self.params.append(prmt)
        return self

    def invoke(self, globals=None):
        """Prompts for arguments, if necessary, and invokes the encapsulated
        function.

        Prompts are shown in the order they were added to command.  Unnamed
        prompts are passed to the function first, in the order they were added
        followed by any named prompts.

        Returns: self
        """
        unnamedArgs = []
        namedArgs = {}
        if globals is not None:
            for k, v in globals.items():
                namedArgs[k] = v

        for prompt in self.params:
            val = prompt.prompt(*unnamedArgs, **namedArgs)
            if prompt.name is not None:
                namedArgs[prompt.name] = val
            else:
                unnamedArgs.append(val)

        self.fn(*unnamedArgs, **namedArgs)
        return self

class InvalidCommand(Exception):
    """Exception for when the user attempts to invoke a command with an alias
    that is not associated with any commands.
    """

    def __init__(self, message=None):
        """Creates a new InvalidCommand exception with an optional message

        Args:
            message: An optional message
        """
        self.message = "Invalid Command"
        if message is not None:
            self.message += ": " + message

class Prompt(object):
    """This class encapsulates a prompt to the user.

    A Prompt consists of the text with which to prompt the user, the name of
    the parameter for which this prompt provides a value (can be None) and an
    optional function that casts the input string into the appropriate type for
    the function parameter.  The given prompt can be a parameterless function
    which returns a string.
    """
    
    def __init__(self, prompt, name=None, cast=None):
        """Create a new prompt.

        Args:
            prompt: A string or a parameterless function that returns a string
            name: The name of the parameter for which the prompt provides a
                value
            cast: A function which takes a single paramter, the string input
                by the user, and returns a value of the appropriate type for the
                parameter to which the value is assigned.
        """
        if cast is None:
            cast = lambda x: x

        self.prmt = prompt
        self.name = name
        self.fn = cast

    def prompt(self, *args, **kwargs):
        """Prompt the user for input and return the cast value.

        Returns: the value input by the user after it has been passed through
            any provided cast function.
        """
        if isinstance(self.prmt, collections.Callable):
            inpt = input(self.prmt(*args, **kwargs))
        else:
            inpt = input(self.prmt)

        return self.fn(inpt)

class Shell(object):
    """This class encapsulates a list of commands and continuously asks the user
    to input a new command until the user enters either exit or quit.

    Instances also provide a special command for listing all of the commands.
    """

    def __init__(self, name=None):
        """Create a new, empty shell.

        Args:
            name: An optional name for the shell.  If given it will be displayed
                to the user when the shell is started.
        """
        self.cmds = []
        self.name = name
        self.globals = {}
        
    def addCommand(self, command):
        """Add the given command to the shell.

        Args:
            command: The command to add to the shell.
        """
        self.cmds.append(command)

    def setGlobal(self, name, value):
        """Set a value that is passed in with the dictionary values to each
        command invocation.  A command parameter prompt with the same name will
        override a global value.

        Args:
            name: The name of the parameter.
            value: The value of the parameter.
        """
        self.globals[name] = value
        
    def start(self):
        """Continuously prompt the user for commands until they invoke the quit
        command using either the 'quit' or 'exit' alias.
        """
        if self.name is not None:
            print("You have entered the " + self.name)
            print("Type 'cmds' to see the list of available commands")

        show = Command('commands', 'Show available commands', self._show)
        show.addAlias('cmds')
        show.addAlias('show commands')
        self.addCommand(show)

        quit = Command('quit', 'Quit', self._quit)
        quit.addAlias('exit')
        self.addCommand(quit)

        self.again = True
        while self.again:
            cmd = input(' # ')

            foundCmd = False
            for command in self.cmds:
                if cmd in command.aliases:
                    foundCmd = True
                    try:
                        command.invoke(self.globals)
                        break
                    except InvalidCommand as e:
                        print(e.message)
                   # except Exception as e:
                   #     print('An unexpected condition was encountered '
                   #           'processing your command: {}'.format(e))

            if not foundCmd:
                print("Invalid command: ", cmd)

    def _quit(self, **globals):
        # Since any defined globals are passed to all functions we define an
        # unused keywords parameters to avoid errors
        if self.name is not None:
            print("Leaving the " + self.name)
        else:
            print("See YA!")
        self.again = False

    def _show(self, **globals):
        # Since any defined globals are passed to all functions we define an
        # unused keywords parameters to avoid errors
        for cmd in self.cmds:
            print(cmd.aliases[0], ': ', cmd.desc)
                    
