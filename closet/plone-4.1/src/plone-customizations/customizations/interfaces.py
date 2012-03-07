from zope.interface import Interface

class ICustomizationsLayer(Interface):
    """Browser layer marker interface which will be applied to the request
    when the package is installed.

    This can be used as the value of the ``layer`` attribute of ZCML
    directives like ``<browser:page />`` and ``<browser:viewlet />`` to
    register components that are only active when these customizations are in
    effect.
    """
