schema = {
    "type": "object",
    "properties": {
        "key": {
            "type": "string"
        },
        "acquired": {
            "type": "string"
        },
        "cs_code": {
            "type": "string"
        },
        "bits_per_pixel": {
            "items": {
                "type": "number"
            },
            "type": "array"
        },
        "fill_fraction": {
            "type": "number"
        },
        "cloud_fraction": {
            "type": "number"
        },
        "solar_azimuth_angle": {
            "type": "number"
        },
        "bright_fraction": {
            "type": "number"
        },
        "file_sizes": {
            "items": {
                "type": "integer"
            },
            "type": "array"
        },
        "area": {
            "type": "number"
        },
        "terrain_correction": {
            "type": "string"
        },
        "cloud_fraction_0": {
            "type": "number"
        },
        "raster_size": {
            "items": {
                "type": "integer"
            },
            "type": "array"
        },
        "reflectance_scale": {
            "items": {
                "type": "number"
            },
            "type": "array"
        },
        "files": {
            "items": {
                "type": "string"
            },
            "type": "array"
        },
        "geolocation_accuracy": {
            "type": "number"
        },
        "solar_elevation_angle": {
            "type": "number"
        },
        "descartes_version": {
            "type": "string"
        },
        "roll_angle": {
            "type": "number"
        },
        "anyOf": {
            "tile_id": {
                "type": "string"
            },
            "tile_id": {
                "type": "integer"
            }
        },
        "sw_version": {
            "type": "string"
        },
        "identifier": {
            "type": "string"
        },
        "projcs": {
            "type": "string"
        },
        "bucket": {
            "type": "string"
        },
        "file_md5s": {
            "items": {
                "type": "string"
            },
            "type": "array"
        },
        "processed": {
            "type": "integer"
        },
        "published": {
            "type": "string"
        },
        "sat_id": {
            "type": "string"
        },
        "item_type": {
            "type": "string"
        },
        "geotrans": {
            "items": {
                "type": "number"
            },
            "type": "array"
        }
    }
}
