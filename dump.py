#encoding: utf8
import sys,os

def dump(o, methods=False):
    import exceptions,types
    for f in (f for f in dir(o) if not(f.startswith('__') and f.endswith('__'))):
        try:
            v=getattr(o,f)
        except Exception,e:
            if (type(e)==exceptions.SystemError \
                    and e[0]=='Указанный метод не поддерживается.')\
                    or type(e)==exceptions.AttributeError:
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
        limit=1024
        print f,':', v[:limit]+'...' if len(v)>limit else v

def enum(e):
    import System
    t = System.Reflection.TypeDelegator(e)
    for n in t.GetEnumNames():
        print n,'=',t.GetMember(n)[0].GetRawConstantValue()
        
def cls():
    os.system("cls")
