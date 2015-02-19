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
            isinstance(v,(types.BuiltinFunctionType,types.FunctionType)): continue
        v=unicode(v)
        limit=1024
        print f,':', v[:limit]+'...' if len(v)>limit else v

def enum(e):
    import System
    t = System.Reflection.TypeDelegator(e)
    for n in t.GetEnumNames():
        print n,'=',t.GetMember(n)[0].GetRawConstantValue()
        
def cls():
    os.system("cls")
