import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

from customizations.testing import CUSTOMIZATIONS_INTEGRATION_TESTING


class TestSetup(unittest.TestCase):

    layer = CUSTOMIZATIONS_INTEGRATION_TESTING

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        portal = self.layer['portal']
        qi_tool = getToolByName(portal, 'portal_quickinstaller')

        pid = 'customizations'
        installed = [p['id'] for p in qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed, 'package appears not to have been installed')
