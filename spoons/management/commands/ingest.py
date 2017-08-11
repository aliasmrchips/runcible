from django.core.management.base import BaseCommand, CommandError

from spoons.models import Metadata, Source

import logging

logger = logging.getLogger('django')

from landsat.search import Search
from landsat.downloader import Downloader

class Command(BaseCommand):

    help = 'ingest'

    def add_arguments(self, parser):
        parser.add_argument('--paths_rows', type=str)
        parser.add_argument('--lat', type=float)
        parser.add_argument('--lon', type=float)
        parser.add_argument('--address', type=str)
        parser.add_argument('--start_date', type=str)
        parser.add_argument('--end_date', type=str)
        parser.add_argument('--cloud_min', type=int)
        parser.add_argument('--cloud_max', type=int)
        parser.add_argument('--limit', type=int)

    def handle(self, *args, **options):

        kwargs = {}

        if options['paths_rows']:
            kwargs['paths_rows'] = options['paths_rows']
        if options['lat']:
            kwargs['lat'] = options['lat']
        if options['lon']:
            kwargs['lon'] = options['lon']
        if options['address']:
            kwargs['address'] = options['address']
        if options['start_date']:
            kwargs['start_date'] = options['start_date']
        if options['end_date']:
            kwargs['end_date'] = options['end_date']
        if options['cloud_min']:
            kwargs['cloud_min'] = options['cloud_min']
        if options['cloud_max']:
            kwargs['cloud_max'] = options['cloud_max']
        if options['limit']:
            kwargs['limit'] = options['limit']

        search = Search()

        result = search.search(**kwargs)

        print 'total_returned:%s, total:%s' % (result['total_returned'], result['total'])

        for metadata in result['results']:

            sat_id = metadata['sat_type']
            const_id = metadata['sat_type']
            
            source, created = Source.objects.get_or_create(sat_id=sat_id, const_id=const_id, defaults={'groups':['public']})

        # logger.info('%s: %s/%s' % (key, source.sat_id, source.const_id))

        # metadata.source = source
        # metadata.sat_id = source.sat_id
        # metadata.const_id = source.const_id

        # metadata.save()
