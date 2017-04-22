#encoding: utf8
from __future__ import print_function
import sys,os
ironpython=hasattr(Exception,'clsException')    #the feature that interests us

import types
if ironpython: import System
import six
unicode=six.text_type
str=six.binary_type
basestring=six.string_types

limit=1024  #truncate values after this many characters

def dump(o, system=False, methods=False):
    """Dump object's contents.

    :param system: include members with names starting and ending with double-underscore
    :param methods: include functions

    Always skips members that yield AttrbiuteError or (in IronPython) NotSupportedException.
    For other exceptions, prints the exception alongside the member.
    Truncates long output (signified by ellipsis) for readability.
    Prints national characters unless this would yield a transcoding error.
    Non-printable characters are replaced with escape-sequences.
    """
    
    for f in (f for f in dir(o) if system or (not(f.startswith('__') and f.endswith('__')))):
        try:
            v=getattr(o,f)
        except Exception as e:
            if (ironpython and type(e)==SystemError \
                        and isinstance(e.clsException,System.NotSupportedException))\
                    or type(e)==AttributeError:
                continue
            else: v=unicode(e)
        if (not methods) and \
            isinstance(v,(types.BuiltinFunctionType,types.FunctionType,types.MethodType)): continue
        #escape terminal-control characters - they'd break the output
        if isinstance(v,basestring):
            hexpat = u'\\u%04x' if isinstance(v,unicode) else '\\x%02x'
            v = type(v)('').join(c if ord(c)>=20 else hexpat%ord(c) for c in v)
        try: v=unicode(v)   #for readability
        except UnicodeDecodeError: pass     #If it fails, never mind
        except AttributeError: v=str(v)     #for some objects that don't have __unicode__
        print(f,':', v[:limit]+'...' if len(v)>limit else v)

if ironpython:
    def enum(e):
        """Dump .NET enum members and their values."""
        import System
        t = System.Reflection.TypeDelegator(e)
        for n in t.GetEnumNames():
            print(n,'=',t.GetMember(n)[0].GetRawConstantValue())
            
    def cls():
        """clear console window and its buffer"""
        os.system("cls")
