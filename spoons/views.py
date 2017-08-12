from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geometry.regex import wkt_regex
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, render
from django.apps import apps

from dateutil.parser import parse
from datetime import datetime, timedelta

import json

from spoons import logger
from spoons.models import Product, Metadata

import os
import time
from operator import itemgetter


def products(request, groups=['public']):

    result = []

    for product in Product.objects.filter(groups__overlap=groups):
        result.append({'product_id': product.product_id, 'value': source.pk})

    return HttpResponse(json.dumps(result), content_type='application/json')

def search(request, groups=['public']):

    data = {}

    if request.body:
        data = json.loads(request.body)

    sat_id = data.get('sat_id',[])
    const_id = data.get('const_id',[])

    if 'MO' in const_id:
        sat_id.append('Terra')
        const_id.append('modis09')
        const_id.remove('MO')

    if 'MY' in const_id:
        sat_id.append('Aqua')
        const_id.append('modis09')
        const_id.remove('MY')

    geom = data.get('geom')
    date = data.get('date','acquired')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    cloud_fraction = data.get('cloud_fraction')
    cloud_fraction_0 = data.get('cloud_fraction_0')
    fill_fraction = data.get('fill_fraction')
    offset = int(data.get('offset', '0'))
    limit = int(data.get('limit', '100'))
    params = data.get('params')
    sort = data.get('sort',False)
    bbox = data.get('bbox',False)

    limit = min(limit, 10000)

    sources = Source.objects.filter(groups__overlap=groups)

    if const_id:
        sources = sources.filter(const_id__in=const_id)

    if sat_id:
        sources = sources.filter(sat_id__in=sat_id)

    features = []

    if sources.exists():

        qs = Metadata.objects.filter(source__in=sources).filter(groups__overlap=groups).only('id', date)

        if geom:
            # first check if wkt string
            if not wkt_regex.match(geom):
                try:
                    geom_tmp = json.loads(geom)
                except ValueError as e:
                    return HttpResponseBadRequest(e.message)
                else:
                    if 'geometry' in geom_tmp:
                        geom = json.dumps(geom_tmp['geometry'])
                    elif 'coordinates' not in geom_tmp:
                        return HttpResponseBadRequest('supported geojson types include: Feature and Geometry Primitives')
            try:
                geos_geom = GEOSGeometry(geom)
            except:
                return HttpResponseBadRequest("invalid geometry")

            if bbox in ['true', True]:
                qs = qs.filter(geom__bboverlaps=geos_geom)
            else:
                qs = qs.filter(geom__intersects=geos_geom)

        if start_time:
            try:
                qs = qs.filter(**{ '%s__gte' % date: parse(start_time)})
            except:
                return HttpResponseBadRequest('invalid start_time')

        if end_time:
            try:
                qs = qs.filter(**{ '%s__lte' % date: parse(end_time)})
            except:
                return HttpResponseBadRequest('invalid end_time')

        if cloud_fraction is not None:
            try:
                qs = qs.filter(cloud_fraction__gte=0).filter(cloud_fraction__lte=float(cloud_fraction))
            except:
                return HttpResponseBadRequest('invalid cloud_fraction')

        if cloud_fraction_0 is not None:
            try:
                qs = qs.filter(cloud_fraction_0__gte=0).filter(cloud_fraction_0__lte=float(cloud_fraction_0))
            except:
                return HttpResponseBadRequest('invalid cloud_fraction_0')

        if fill_fraction is not None:
            try:
                qs = qs.filter(fill_fraction__gte=float(fill_fraction))
            except:
                return HttpResponseBadRequest('invalid fill_fraction')

        if params:
            qs = qs.filter(data__contains=params)

        if sort in ['true', True]:
            qs = qs.order_by('%s' % date)
        else:
            qs = qs.order_by('id')

        for metadata in Metadata.objects.filter(id__in=qs.values_list('id')[:1000]).only('key','geom','data')[offset:limit + offset]:

            feature = {}

            feature['id'] = metadata.key
            feature['type'] = 'Feature'
            feature['bbox'] = metadata.geom.extent
            feature['properties'] = metadata.data
            feature['geometry'] = json.loads(metadata.geom.json)

            features.append(feature)

    return HttpResponse(json.dumps(features), content_type='application/json')

def summary(request, groups=['public']):

    data = {}

    if request.body:
        data = json.loads(request.body)

    sat_id = data.get('sat_id',[])
    const_id = data.get('const_id',[])
    geom = data.get('geom')
    date = data.get('date','acquired')
    part = data.get('part')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    cloud_fraction = data.get('cloud_fraction')
    cloud_fraction_0 = data.get('cloud_fraction_0')
    fill_fraction = data.get('fill_fraction')
    params = data.get('params')
    bbox = data.get('bbox',False)

    result = {}

    sources = Source.objects.filter(groups__overlap=groups)

    if const_id:
        sources = sources.filter(const_id__in=const_id)

    if sat_id:
        sources = sources.filter(sat_id__in=sat_id)

    if sources.exists():

        qs = Metadata.objects.filter(source__in=sources).filter(groups__overlap=groups)

        if geom:
            # first check if wkt string
            if not wkt_regex.match(geom):
                try:
                    geom_tmp = json.loads(geom)
                except ValueError as e:
                    return HttpResponseBadRequest(e.message)
                else:
                    if 'geometry' in geom_tmp:
                        geom = json.dumps(geom_tmp['geometry'])
                    elif 'coordinates' not in geom_tmp:
                        return HttpResponseBadRequest('supported geojson types include: Feature and Geometry Primitives')

            try:
                geos_geom = GEOSGeometry(geom)
            except:
                return HttpResponseBadRequest("invalid geometry")

            if bbox in ['true', True]:
                qs = qs.filter(geom__bboverlaps=geos_geom)
            else:
                qs = qs.filter(geom__intersects=geos_geom)

        if start_time:
            try:
                qs = qs.filter(**{ '%s__gte' % date: parse(start_time)})
            except:
                return HttpResponseBadRequest('invalid start_time')

        if end_time:
            try:
                qs = qs.filter(**{ '%s__lte' % date: parse(end_time)})
            except:
                return HttpResponseBadRequest('invalid end_time')

        if cloud_fraction is not None:
            try:
                qs = qs.filter(cloud_fraction__gte=0).filter(cloud_fraction__lte=float(cloud_fraction))
            except:
                return HttpResponseBadRequest('invalid cloud_fraction')

        if cloud_fraction_0 is not None:
            try:
                qs = qs.filter(cloud_fraction_0__gte=0).filter(cloud_fraction_0__lte=float(cloud_fraction_0))
            except:
                return HttpResponseBadRequest('invalid cloud_fraction_0')

        if fill_fraction is not None:
            try:
                qs = qs.filter(fill_fraction__gte=float(fill_fraction))
            except:
                return HttpResponseBadRequest('invalid fill_fraction')

        if params:
            qs = qs.filter(data__contains=params)

        if part:

            result['items'] = sorted([{'date':datetime.strftime(d['date'],'%Y-%m-%dT%H:%M:00'), 'bytes': d['bytes'], 'pixels': d['pixels'], 'count': d['count']} for d in qs.extra({'date': "date_trunc('%s', %s)" % (part, date)}).values('date').annotate(count=Count('pk'), bytes=Sum('bytes'), pixels=Sum('pixels'))], key=itemgetter('date'))

            result['count'] = sum([d['count'] for d in result['items']])
            result['bytes'] = sum([d['bytes'] for d in result['items']])
            result['pixels'] = sum([d['pixels'] for d in result['items']])

            result['const_id'] = const_id

        else:

            result = qs.aggregate(count=Count('pk'), bytes=Sum('bytes'), pixels=Sum('pixels'))

            result['const_id'] = const_id

    return HttpResponse(json.dumps(result), content_type='application/json')


def get(request, key, groups=['public']):

    for metadata in Metadata.objects.filter(key=key, groups__overlap=groups):
        return HttpResponse(json.dumps(metadata.data), content_type='application/json')

    return HttpResponse(status=404)
