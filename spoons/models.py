from django.db import models
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField, ArrayField

class Source(models.Model):

    """
    A Source is the imagery provider.

    **Examples**

    Retrieve a Source object using the const_id:

        >>> Source.objects.filter(const_id='L8').count()

    **Parameters**

    sat_id: string
        Also known as 'sat_id' in image metadata schema
    const_id: string
        An abbreviation, for example: L7, L8, etc.
    groups: list
        Access control list
    """
    sat_id = models.CharField(max_length=80)
    const_id = models.CharField(max_length=256, blank=True, null=True)
    groups = ArrayField(models.CharField(max_length=80, blank=True))

    def __unicode__(self):
        return self.sat_id

    class Meta:
        db_table = 'source'
        unique_together = ('sat_id','const_id')

class Base(models.Model):
    """
    Base model

    **Parameters**
    created: datetime
        A timestamp that will be set to the current server time when an instance is created
    modified: datetime
        A timestamp that will be updated whenever the instance is updated
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Metadata(Base):
    """
    Image metadata

    **Parameters**
    key: string
        A unique identifier for the data
    acquired: datetime
        Timestamp for when the data was collected
    published: datetime
        Timestamp for when the data was published
    processed: datetime
        Timestamp for when the data was processed
    source: int
        A foreign key to the :py:class:`Source` for this data
    bytes: long
        Total bytes
    pixels: long
        Total pixels
    cloud_fraction: float
        Percentage of cloud free pixels
    fill_fraction: float
        Percentage of (not) nodata pixels
    geom: geometry
        Shape for the geometry
    data: dict
        Everything
    groups: list
        Access control list
    """
    key = models.CharField(max_length=256)

    acquired = models.DateTimeField(db_index=True, null=True)
    published = models.DateTimeField(db_index=True, null=True)
    processed = models.DateTimeField(db_index=True, null=True)

    source = models.ForeignKey(Source, db_index=True)

    bytes = models.BigIntegerField(blank=True, null=True)
    pixels = models.BigIntegerField(blank=True, null=True)

    cloud_fraction = models.FloatField(db_index=True, null=True)
    fill_fraction = models.FloatField(db_index=True, null=True)

    geom = models.GeometryField(null=True)

    data = JSONField()

    groups = ArrayField(models.CharField(max_length=80, blank=True))

    def __unicode__(self):
        return self.key

    class Meta:
        db_table = 'metadata'
        unique_together = ('key', 'source')

