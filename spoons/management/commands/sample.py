from django.core.management.base import BaseCommand, CommandError

from spoons.models import Metadata, Product

import json
import logging

logger = logging.getLogger('django')

import descarteslabs as dl

from spoons.utilities import process

class Command(BaseCommand):

    help = 'ingest'

    def add_arguments(self, parser):
        parser.add_argument('--start_date', type=str)
        parser.add_argument('--end_date', type=str)
        parser.add_argument('--cloud_fraction', type=int)
        parser.add_argument('--fill_fraction', type=int)
        parser.add_argument('--limit', type=int)
        parser.add_argument('--offset', type=int)

    def handle(self, *args, **options):

        kwargs = {}

        if options['start_date']:
            kwargs['start_date'] = options['start_date']
        if options['end_date']:
            kwargs['end_date'] = options['end_date']
        if options['cloud_fraction']:
            kwargs['cloud_fraction'] = options['cloud_fraction']
        if options['fill_fraction']:
            kwargs['fill_fraction'] = options['fill_fraction']
        if options['limit']:
            kwargs['limit'] = options['limit']
        if options['offset']:
            kwargs['offset'] = options['offset']

        for product in dl.metadata.available_products():

            kwargs['products'] = [product]

            features = dl.metadata.search(**kwargs)

            for feature in features['features']:

                properties = feature['properties']
                properties['geometry'] = feature['geometry']
                key = properties['key']

                metadata, created = process(key, properties)

                if created:
                    logger.info('created: %s' % key)
                else:
                    logger.info('updated: %s' % key)
