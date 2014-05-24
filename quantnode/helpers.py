import os
import sys

def attach_parameters(obj, params):
    """
    Ataches common parameters to the data provider
    """
    obj.timestamp = params.get('timestamp')
    obj.instrument = params.get('instrument')
    obj.pricebar = params.get('pricebar')

    if hasattr(obj, 'algorithm') and not getattr(obj, 'algorithm'):
        obj.algorithm = params.get('algorithm')


def importall(projpath):
    for path, dirs, files in os.walk(projpath):
        pathparts = path.split('/')
        if '.git' in pathparts or 'venv' in pathparts or 'virtualenv' in pathparts or 'site-packages' in pathparts:
            continue

        sys.path.insert(0, path)

        for f in files:
            if not f.endswith('.py'):
                continue

            try:
                filename = f
                modname = f.replace('.py', '')
                mod = __import__(modname, globals(), locals(), [''])
            except Exception:
                continue

        sys.path.pop(0)


def _get_subclass_info(parentcls):
    ls = []
    for cls in parentcls.__subclasses__():
        ls.append({
            'name': cls.__name__,
            'methods': cls.methods_implemented()
        })

    return {
        parentcls.__name__: ls
    }


def get_implementation_info(projpath):
    from actors import Calculator, Algorithm

    if not projpath:
        raise AttributeError('get_implementation_info requires the path of the project')

    importall(projpath)

    info = dict()
    info.update(_get_subclass_info(Calculator))
    info.update(_get_subclass_info(Algorithm))

    return info


def get_user_implementation_class(mod, clsname, modulename='quantnode.actors'):
    """
    Get the user's implementation of the class corresponding to clsname
    """
    if not clsname:
        return None

    for attrname in dir(mod):
        if '__' in attrname:
            continue

        attr = getattr(mod, attrname)

        if not hasattr(attr, '__bases__'):
            continue

        for parent in attr.__bases__:
            if getattr(parent, '__module__', '') == modulename and getattr(parent, '__name__', '') == clsname:
                return attr

    return None


def find_implementation(repopath, clsname, modulename='quantnode.actors'):
    useralgo_cls = None

    for path, dirs, files in os.walk(repopath):
        pathparts = path.split('/')
        if '.git' in pathparts or 'venv' in pathparts or 'virtualenv' in pathparts or 'site-packages' in pathparts:
            continue

        sys.path.insert(0, path)

        for f in files:
            if not f.endswith('.py'):
                continue

            try:
                filename = f
                modname = f.replace('.py', '')
                mod = __import__(modname, globals(), locals(), [''])
                useralgo_cls = get_user_implementation_class(mod, clsname, modulename = modulename)
                if useralgo_cls:
                    break

            except Exception, e:
                continue

        sys.path.pop(0)
        if useralgo_cls:
            break

    return useralgo_cls

