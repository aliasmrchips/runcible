from django.test import TestCase, Client
import json

from spoons.models import Metadata, Source

sample_key = 'meta_2016-10-24_5363511_RE3_v0'
sample_data = {"groups": "[\"descartes:team\"]", "acquired": "2016-10-24T02:35:46Z", "cs_code": "EPSG:32653",
               "bits_per_pixel": [1.86, 2.19, 1.34], "fill_fraction": 0.2187, "cloud_fraction": -1.0,
               "solar_azimuth_angle": 176.36746, "archived": "2016-10-26T18:24:11Z", "file_sizes": [6367335],
               "area": 136.7, "cloud_fraction_0": 0.03, "raster_size": [5000, 5000],
               "reflectance_scale": [0.3638, 0.39, 0.4658, 0.521, 0.6464], "files": ["2016-10-24_5363511_RE3.jp2"],
               "solar_elevation_angle": 25.30383, "bright_fraction": 0.9829, "descartes_version": "satin-0.8.6",
               "view_angle": 10.32567, "tile_id": "5363511", "identifier": "20161024_023546_5363511_RapidEye-3",
               "projcs": "WGS 84 / UTM zone 53N", "geometry": {"type": "Polygon", "coordinates": [
        [[133.59814887438813, 52.84092026667005], [133.5673014, 52.8405962], [133.5598556, 53.0652632],
         [133.6930608295916, 53.0666665609444], [133.626965399316, 52.9098581774291],
         [133.59814887438813, 52.84092026667005]]]}, "bucket": "gs://descartes-re/",
               "file_md5s": ["7079395892efb6e0a0111f47b90fb6af"], "processed": 1477516675, "sat_id": "RE-3",
               "geotrans": [403500.0, 5.0, 0.0, 5880500.0, 0.0, -5.0]}

token_descartes_team = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImV4cCI6OTk5OTk5OTk5OSwiaWF0IjowLCJncm91cHMiOlsiZGVzY2FydGVzOnRlYW0iLCJwdWJsaWMiXSwiYXVkIjoiWk9CQWk0VVJPbDVnS1pJcHh4bHdPRWZ4OEtwcVhmMmMiLCJpc3MiOiJodHRwczovL2Rlc2NhcnRlc2xhYnMuYXV0aDAuY29tLyJ9.cnsoRk3fzqFVmuNKY4eBuZuuPfKka0RPXKXmEAwBOyo"



class ViewTestCase(TestCase):
    fixtures = ['lookup.json', 'source.json', 'metadata.json']

    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        super(ViewTestCase, cls).setUpClass()

    def setUp(self):
        self.client = ViewTestCase.client

    def test_metadata_list(self):
        response = self.client.post("/search", data=json.dumps({}), content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json.loads(response.content)), Metadata.objects.all().count())

    def test_metadata_list_offset(self):
        response = self.client.post("/search", data=json.dumps({'offset': '0'}),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json.loads(response.content)), Metadata.objects.all().count())

        response = self.client.post("/search", data=json.dumps({'offset': '1'}),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json.loads(response.content)), Metadata.objects.all().count() - 1)

    def test_metadata_list_limit(self):
        response = self.client.post("/search", data=json.dumps({'limit': '0'}),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json.loads(response.content)), 0)

        response = self.client.post("/search", data=json.dumps({'limit': '1'}),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_metadata_list_limit_offset(self):
        response = self.client.post("/search", data=json.dumps({'offset': '1', 'limit': '0'}),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json.loads(response.content)), 0)

        response = self.client.post("/search", data=json.dumps({'offset': '1', 'limit': '1'}),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_metadata_summary(self):
        response = self.client.post("/summary", content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content)['count'], 3)

    def test_source_list(self):
        response = self.client.get("/sources", HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json.loads(response.content)), Source.objects.all().count())

    def test_get(self):

        response = self.client.get("/get/meta_LC80270312016188_v1", HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)

        response = self.client.get("/get/meta_SRTMGL1003_4096:16:15.0:15:-4:80_v0",
                                   HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)

    def test_search_geojson(self):
        geometry = {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        -95.2734375,
                        31.952162238024975
                    ],
                    [
                        -94.21875,
                        31.952162238024975
                    ],
                    [
                        -94.21875,
                        32.84267363195431
                    ],
                    [
                        -95.2734375,
                        32.84267363195431
                    ],
                    [
                        -95.2734375,
                        31.952162238024975
                    ]
                ]
            ]
        }

        response = self.client.post("/search", data=json.dumps(dict(geom=json.dumps(geometry))),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)

        feature = {"type": "Feature", "geometry": geometry}

        response = self.client.post("/search", data=json.dumps(dict(geom=json.dumps(feature))),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)

        feature_collection = {
            "type": "FeatureCollection",
            "features": [feature, feature]}

        response = self.client.post("/search", data=json.dumps(dict(geom=json.dumps(feature_collection))),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(400, response.status_code)

    def test_search_wkt(self):
        wkt_polygon = "POLYGON ((35 10, 45 45, 15 40, 10 20, 35 10),(20 30, 35 35, 30 20, 20 30))"

        response = self.client.post("/search", data=json.dumps(dict(geom=wkt_polygon)),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)

        wkt_multipolygon_with_holes = "MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40)),((20 35, 10 30, 10 10, 30 5, 45 20, 20 35),(30 20, 20 15, 20 25, 30 20)))"

        response = self.client.post("/search", data=json.dumps(dict(geom=wkt_multipolygon_with_holes)),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)

        wkt_bad = "(((40 40, 20 45, 45 30, 40 40)),((20 35, 10 30, 10 10, 30 5, 45 20, 20 35),(30 20, 20 15, 20 25, 30 20)))"

        response = self.client.post("/search", data=json.dumps(dict(geom=wkt_bad)),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(400, response.status_code)


    def test_summary_geojson(self):
        geometry = {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        -95.2734375,
                        31.952162238024975
                    ],
                    [
                        -94.21875,
                        31.952162238024975
                    ],
                    [
                        -94.21875,
                        32.84267363195431
                    ],
                    [
                        -95.2734375,
                        32.84267363195431
                    ],
                    [
                        -95.2734375,
                        31.952162238024975
                    ]
                ]
            ]
        }

        response = self.client.post("/summary", data=json.dumps(dict(geom=json.dumps(geometry))),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)

        feature = {"type": "Feature", "geometry": geometry}

        response = self.client.post("/summary", data=json.dumps(dict(geom=json.dumps(feature))),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)

        feature_collection = {
            "type": "FeatureCollection",
            "features": [feature, feature]}

        response = self.client.post("/summary", data=json.dumps(dict(geom=json.dumps(feature_collection))),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(400, response.status_code)

    def test_summary_wkt(self):
        wkt_polygon = "POLYGON ((35 10, 45 45, 15 40, 10 20, 35 10),(20 30, 35 35, 30 20, 20 30))"

        response = self.client.post("/summary", data=json.dumps(dict(geom=wkt_polygon)),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)

        wkt_multipolygon_with_holes = "MULTIPOLYGON (((40 40, 20 45, 45 30, 40 40)),((20 35, 10 30, 10 10, 30 5, 45 20, 20 35),(30 20, 20 15, 20 25, 30 20)))"

        response = self.client.post("/summary", data=json.dumps(dict(geom=wkt_multipolygon_with_holes)),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)

        wkt_bad = "(((40 40, 20 45, 45 30, 40 40)),((20 35, 10 30, 10 10, 30 5, 45 20, 20 35),(30 20, 20 15, 20 25, 30 20)))"

        response = self.client.post("/summary", data=json.dumps(dict(geom=wkt_bad)),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(400, response.status_code)

    def test_cloud_fraction(self):
        # test cloud_fraction_0
        response = self.client.post("/search", data=json.dumps({'cloud_fraction_0': "0.0"}),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json.loads(response.content)), 1)

        response = self.client.post("/search", data=json.dumps({'cloud_fraction_0': "0.9"}),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json.loads(response.content)), 2)

        # test cloud_fraction
        response = self.client.post("/search", data=json.dumps({'cloud_fraction': "0.0"}),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json.loads(response.content)), 0)

        response = self.client.post("/search", data=json.dumps({'cloud_fraction': "0.9"}),
                                    content_type='application/x-www-form-urlencoded',
                                    HTTP_AUTHORIZATION=token_descartes_team)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(json.loads(response.content)), 1)




