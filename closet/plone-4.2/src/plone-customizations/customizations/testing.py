from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile
from plone.testing.z2 import installProduct, uninstallProduct

from zope.configuration import xmlconfig

class Customizations(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import customizations
        xmlconfig.file('configure.zcml', customizations,
                context=configurationContext)

        installProduct(app, 'customizations')

    def tearDownZope(self, app):
        uninstallProduct(app, 'customizations')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'customizations:default')

CUSTOMIZATIONS_FIXTURE = Customizations()
CUSTOMIZATIONS_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(CUSTOMIZATIONS_FIXTURE, ),
                       name="Customizations:Integration")
CUSTOMIZATIONS_FUNCTIONAL_TESTING = \
    FunctionalTesting(bases=(CUSTOMIZATIONS_FIXTURE, ),
                       name="Customizations:Functional")
