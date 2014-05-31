from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, ValidationError
from datetime import date
from collections import namedtuple


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
    building = models.ForeignKey(
        Building,
        verbose_name=Building._meta.verbose_name,
        blank=True, null=True, on_delete=models.PROTECT)
    address = models.TextField(_("address"))

    class Meta:
        verbose_name = _("property")
        verbose_name_plural = _("properties")

    def __unicode__(self):
        return self.name + '\n' + self.address


class Tenant(models.Model):
    property = models.ForeignKey(
        Property,
        verbose_name=Property._meta.verbose_name,
        on_delete=models.PROTECT)
    name = models.CharField(_("name"), max_length=255)
    email = models.EmailField(_("email"), max_length=254, blank=True)
    #begin date is inferred from first rent revision
    tenancy_end_date = models.DateField(
        _("tenancy end date"), blank=True, null=True)

    class Meta:
        verbose_name = _("tenant")

    def __unicode__(self):
        return self.tenant_name + ' ' + unicode(self.property)


def validate_month(value):
    if value.day != 1:
        raise ValidationError(
            _("month expected. Please use first day of the month"))


class RentRevision(models.Model):
    tenant = models.ForeignKey(Tenant, verbose_name=Tenant._meta.verbose_name)
    date = models.DateField(_("start date"), validators=[validate_month])
    rent = models.DecimalField(
        _("monthly rent"), max_digits=7, decimal_places=2,
        validators=[MinValueValidator(0)])
    provision = models.DecimalField(
        _("monthly provision"), max_digits=7, decimal_places=2,
        validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = _("rent revision")
        verbose_name_plural = _("rent revisions")

    def __unicode__(self):
        return self.date


class Payment(models.Model):
    help_text = _("money received from the tenant")
    tenant = models.ForeignKey(Tenant, verbose_name=Tenant._meta.verbose_name)
    date = models.DateField(_("date"))
    amount = models.DecimalField(
        _("amount"), max_digits=7, decimal_places=2,
        validators=[MinValueValidator(0)])

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


Cashflow = namedtuple('Cashflow', ['date', 'amount', 'description'])

def payments_to_cashflows(date, payments):
    return [Cashflow(x.date, x.amount, _('payment')) for x in payments if x.date <= date]


def fees_to_cashflows(date, fees):
    month_start = date.replace(day=1)
    return [Cashflow(x.date, -x.amount, x.description) for x in fees if x.date <= month_start]


def revision_to_cashflows(rev, end_date):
    start_date = rev.date
    if (end_date <= start_date):
        return []
    result = []
    month_range = xrange(
        12*start_date.year + start_date.month,
        12*end_date.year + end_date.month)
    for m in month_range:
        d = date(m / 12, m % 12 + 1, 1)
        result.append(Cashflow(d, -rev.rent, _("rent")))
        if rev.provision != 0:
            result.append(Cashflow(d, -rev.provision, _("provision")))
    return result


def next_month_start(date):
    if date.month == 12:
        return date.replace(year=date.year + 1, month=1, day=1)
    else:
        return date.replace(month=date.month + 1, day=1)


def revisions_to_cashflows(date, revisions, end_date):
    if end_date is None:
        end_date = date
    next_month = next_month_start(end_date)
    filtered_revisions = [r for r in revisions if r.date < next_month]
    if len(filtered_revisions) == 0:
        return []
    sorted_revisions = sorted(filtered_revisions, key=lambda r: r.date)
    result = []
    for i in range(0, len(sorted_revisions) - 1):
        cashflows = revision_to_cashflows(
            sorted_revisions[i],
            sorted_revisions[i + 1].date)
        result.extend(cashflows)
    cashflows = revision_to_cashflows(
        sorted_revisions[len(sorted_revisions) - 1],
        end_date.replace(day=1))
    result.extend(cashflows)
    return result
