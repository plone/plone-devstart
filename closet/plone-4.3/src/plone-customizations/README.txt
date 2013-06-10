plone-customizations
====================

This package contains project-specific customizations.

It should *not* be released to PyPI. Because its name is so generic, it is also
unlikely to be reusable across projects.

However, for simple projects, you may put all your customisations here.

* Template overrides using `z3c.jbot <http://pypi.python.org/pypi/z3c.jbot>`_ go
  in the folder ``customizations/overrides/``.
* Configuration profiles using GenericSetup go in
  ``customizations/profiles/default/``.
* Views, viewlets and portlets may be registered with a ``layer`` of
  ``customizations.interfaces.ICustomizationsLayer``, which will be applied
  when the product is installed through the Plone *Add-ons* control panel.
* Other Python and template code can be placed in the ``customizations``
  package.
* Configuration unit tests can be written in the ``customizations/tests/``
  sub-package. Test setup is done in ``customizations.testing``.

For customisations to take effect, this product (listed as *Project
customizations*) must be installed when a Plone site is created, or aftewards
in the *Add-ons* control panel in Plone.

If you want to create reusable packages, you should create new distributions
using ``ZopeSkel`` (the ``bin/zopeskel`` command in the buildout created by
``plone-devstart``).

You may then choose to have those packages be listed as dependencies of the
``plone-customizations`` package. To that, edit ``setup.py`` and modify the
``install_requires`` line::

    install_requires=[
          'setuptools',
          'Plone',
          'z3c.jbot',
          'acme.somepackage'
      ],

Here ``acme`` is an organisation-specific namespace and ``somepackage`` is a
package name in that namespace. This follows the conventions of namespacing
packages applied by ``ZopeSkel`` when using the ``plone_basic`` template.

If the package has a ``GenericSetup`` profile, you can ensure it is applied
when the *Project customizations* product is installed, by listing it in
``customizations/profiles/defaults/metadata.xml``::

    <?xml version="1.0"?>
    <metadata>
      <version>0001</version>
      <dependencies>
        <dependency>profile-acme.somepackage</dependency>
      </dependencies>
    </metadata>
