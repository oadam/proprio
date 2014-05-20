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
    property_count.short_description = _("number of properties")

class Property(models.Model):
    name = models.CharField(_("name"), max_length=255)
    building = models.ForeignKey(Building, verbose_name=Building._meta.verbose_name, blank=True, null=True, on_delete=models.PROTECT)
    address = models.TextField(_("address"))
    class Meta:
        verbose_name = _("property")
        verbose_name_plural = _("properties")
    def __unicode__(self):
        return self.name + '\n' + self.address

class Tenancy(models.Model):
    property = models.ForeignKey(Property, verbose_name=Property._meta.verbose_name, on_delete=models.PROTECT)
    tenant_name = models.CharField(_("tenant name"), max_length=255)
    tenant_email = models.EmailField(_("tenant email"), max_length=254, blank=True)
    #begin date is inferred from first rent revision
    end_date = models.DateField(_("end date"), blank=True, null=True)
    class Meta:
        verbose_name = _("tenancy")
        verbose_name_plural = _("tenancies")
    def __unicode__(self):
        return self.tenant_name + ' ' + unicode(self.property)

class RentRevision(models.Model):
    tenancy = models.ForeignKey(Tenancy, verbose_name=Tenancy._meta.verbose_name, on_delete=models.PROTECT)
    date = models.DateField(_("start date"))
    rent = models.DecimalField(_("monthly rent"), max_digits=7, decimal_places=2)
    provision = models.DecimalField(_("monthly provision"), max_digits=7, decimal_places=2)
    class Meta:
        verbose_name = _("rent revision")
    def __unicode__(self):
        return self.date

