from __future__ import print_function
from django.contrib.gis.geos import GEOSGeometry, GEOSException
from django.contrib.gis.gdal import OGRGeometry
from django.apps import apps

import sys
import json
import operator
import functools

from spoons.models import *

from dateutil.parser import *
from datetime import datetime

def process(key, metadata):

    defaults = {}

    if 'geometry' in metadata:

        geom = OGRGeometry(json.dumps(metadata['geometry']))
        geom.coord_dim = 2

        defaults['geom'] = geom.geos
        # del metadata['geometry']

    if 'acquired' in metadata:
        defaults['acquired'] = parse(metadata['acquired'])

    if 'archived' in metadata:
        defaults['published'] = parse(metadata['archived'])

    if 'published' in metadata:
        defaults['published'] = parse(metadata['published'])

    if 'processed' in metadata:
        defaults['processed'] = datetime.utcfromtimestamp(metadata['processed'])

    if 'file_sizes' in metadata:
        defaults['bytes'] = functools.reduce(operator.add, metadata['file_sizes'])

    if 'raster_size' in metadata:
        defaults['pixels'] = functools.reduce(operator.mul, metadata['raster_size'])

    if 'cloud_fraction' in metadata:
        defaults['cloud_fraction'] = float(metadata['cloud_fraction'])

    if 'fill_fraction' in metadata:
        defaults['fill_fraction'] = float(metadata['fill_fraction'])

    defaults['data'] = metadata

    product_id = metadata.get('product','N/A')

    product, created = Product.objects.get_or_create(name=product_id, defaults={'groups':['public']})

    defaults['groups'] = product.groups

    instance, created = Metadata.objects.update_or_create(key=key, product=product, defaults=defaults)

    return instance, created
