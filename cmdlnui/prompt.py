##
## This module provides some standard prompts and cast functions
##
import Prompt from cmdlnui
import date from datetime
import timedelta from datetime

##
## Standard date prompt
##
class DatePrompt(Prompt):

    def __init__(self):
        Prompt.__init__(self, 'Date (yyyy-dd-mm):', strtodate)

    def strtodate(self, str):
        parts = str.split('-')
        return date(int(parts[0]), int(parts[1]), int(parts[2]))

##
## Prompt for a time delta
##
class TimeDeltaPrompt(Prompt):

    def __init__(self):
        Prompt.__init__(self, 'Time (#w #d hh:mm:ss.micro):', strtodelta)

    def strtodelta(self, str):
        args = {}
        parts = str.split(' ')
        if len(parts) == 3:
            args['weeks'] = int(parts.pop(0)[0:-1])

        if len(parts) == 2:
            args['days'] = int(parts.pop(0)[0:-1])

        parts = parts[0].split('.')
        if len(parts) == 2:
            args['microseconds'] = int(parts.pop())
        
        parts = parts[0].split(':')
        args['hours'] = int(parts[0])
        args['minutes'] = int(parts[1])
        args['seconds'] = int(parts[2])

        return timedelta(**args)

