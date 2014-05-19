from django.db import models
from django.utils.translation import ugettext_lazy as _

class Building(models.Model):
    name = models.CharField(_("name"), max_length=255)

    class Meta:
        verbose_name = _("building")

    def __unicode__(self):
        return self.name
    def property_count(self):
        return self.property_set.count()

class Property(models.Model):
    name = models.CharField(_("name"), max_length=255)
    building = models.ForeignKey(Building, verbose_name=Building._meta.verbose_name, blank=True, null=True, on_delete=models.PROTECT)
    address = models.TextField(_("address"))

    class Meta:
        verbose_name = _("property")
        verbose_name_plural = _("properties")

    def __unicode__(self):
        return self.name + '\n' + self.address

