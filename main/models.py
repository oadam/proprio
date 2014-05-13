from django.db import models
from django.contrib.auth.models import User

class Building(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return self.name
    def property_count(self):
        return self.property_set.count()

class Property(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    building = models.ForeignKey(Building, blank=True, null=True, on_delete=models.PROTECT)
    address = models.TextField()

    class Meta:
        verbose_name_plural = "properties"

    def __unicode__(self):
        return self.name + '\n' + self.address

