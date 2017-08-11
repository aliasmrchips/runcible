from django.test import TestCase
from spoons.models import Metadata, Source


class LayerTestCase(TestCase):
    fixtures = ['source.json', 'metadata.json']

    def setUp(self):
        pass

    def test_source(self):
        source = Source.objects.get(sat_id='LANDSAT_8')

        self.assertEqual(source.const_id, 'l8')

    def test_metadata(self):
        qs = Metadata.objects.all()

        self.assertEqual(qs.count(), 3)
