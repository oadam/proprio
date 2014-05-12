from django.db import models
from django.contrib.auth.models import User

class Building(models.Model):
    user = models.ForeignKey(User)
    address = models.TextField()
    notes = models.TextField(blank=True)
    def __unicode__(self):
        a = self.address
        return a[:100] + '...' if len(a) > 100 else a
    def property_count(self):
        return self.property_set.count()

class Property(models.Model):
    building = models.ForeignKey(Building)
    address_prefix = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "properties"

    def __unicode__(self):
        a = self.address_prefix
        return a[:100] + '...' if len(a) > 100 else a

