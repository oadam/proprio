from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator

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

class Tenant(models.Model):
    property = models.ForeignKey(Property, verbose_name=Property._meta.verbose_name, on_delete=models.PROTECT)
    name = models.CharField(_("name"), max_length=255)
    email = models.EmailField(_("email"), max_length=254, blank=True)
    #begin date is inferred from first rent revision
    tenancy_end_date = models.DateField(_("tenancy end date"), blank=True, null=True)
    class Meta:
        verbose_name = _("tenant")
    def __unicode__(self):
        return self.tenant_name + ' ' + unicode(self.property)

class RentRevision(models.Model):
    tenant = models.ForeignKey(Tenant, verbose_name=Tenant._meta.verbose_name)
    date = models.DateField(_("start date"))
    rent = models.DecimalField(_("monthly rent"), max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    provision = models.DecimalField(_("monthly provision"), max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    class Meta:
        verbose_name = _("rent revision")
        verbose_name_plural = _("rent revisions")
    def __unicode__(self):
        return self.date

class Payment(models.Model):
    help_text = _("money received from the tenant")
    tenant = models.ForeignKey(Tenant, verbose_name=Tenant._meta.verbose_name)
    date = models.DateField(_("date"))
    amount = models.DecimalField(_("amount"), max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    class Meta:
        verbose_name = _("payment")
    def __unicode__(self):
        return unicode(self.date) + ' - ' + unicode(self.amount)

class Fee(models.Model):
    help_text = _("a one-time fee (for example an end of year adjustment fee)")
    description = models.CharField(_("description"), max_length=255)
    tenant = models.ForeignKey(Tenant, verbose_name=Tenant._meta.verbose_name)
    date = models.DateField(_("date"))
    amount = models.DecimalField(_("amount"), max_digits=7, decimal_places=2)
    class Meta:
        verbose_name = _("one-time fee")
    def __unicode__(self):
        return unicode(self.description) + ' - ' + unicode(self.date)

