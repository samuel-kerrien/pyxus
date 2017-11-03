import logging
import unittest

from hamcrest.library.number.ordering_comparison import greater_than

from pyxus.client import NexusClient
import pyxus.config as conf

from hamcrest import (assert_that, instance_of, has_properties, not_none, equal_to)


class TestSearchForItems(unittest.TestCase):
    client = {}

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.client = NexusClient(**conf.NEXUS_ENV_HBP_DEV)

    def test_search_items(self):
        """ This test assumes specific test data - we therefore do not apply assumptions but make this test rather a manual one until we can ensure a specific testdata set. """
        search = self.client.instances.list(full_text_query="interneuron")
        assert_that(len(search.results), greater_than(0))
        results = self.client.instances.resolve_all(search)
        print results
        for obj in results:
            data_url = obj.json["hbp:dataurl"]
            if data_url:
                print data_url["nxcv:downloadURL"]


    def test_get_self_link_with_https(self):
        self.client.api_root_dict = {'scheme': 'https',
                     'host': 'nexus-dev.humanbrainproject.org',
                     'prefix': 'v0'}
        self.client._http_client.api_root="https://nexus-dev.humanbrainproject.org/v0"
        self_link = self.client.instances._get_self_link("http://kg:8080/v0/data/hbp/core/celloptimization/v0.0.1/3fa38385-796d-4bf6-b692-55b9b2861a3c")
        assert_that(self_link, equal_to("https://nexus-dev.humanbrainproject.org/v0/data/hbp/core/celloptimization/v0.0.1/3fa38385-796d-4bf6-b692-55b9b2861a3c"))