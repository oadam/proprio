# vim: ai ts=4 sts=4 et sw=4
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, ValidationError
from datetime import date
from collections import namedtuple
import itertools
from operator import attrgetter


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
        return '{0}\n{1}'.format(self.name, self.address)


def validate_month(value):
    if value is not None and value.day != 1:
        raise ValidationError(
            _("month expected. Please use first day of the month"))


class Tenant(models.Model):
    property = models.ForeignKey(
        Property,
        verbose_name=Property._meta.verbose_name,
        on_delete=models.PROTECT)
    name = models.CharField(_("name"), max_length=255)
    email = models.EmailField(_("email"), max_length=254, blank=True)
    tenancy_begin_date = models.DateField(
        _("tenancy begin date"), validators=[validate_month])
    tenancy_end_date = models.DateField(
        _("tenancy end date"), blank=True,
        null=True, validators=[validate_month])

    def cashflows(self):
        non_sorted = itertools.chain.from_iterable([
            payments_to_cashflows(date.today(),
                                  self.payment_set.all()),
            revisions_to_cashflows(
                date.today(),
                self.rentrevision_set.all()),
            fees_to_cashflows(date.today(), self.fee_set.all())
        ])
        date_sorted = sorted(non_sorted, key=attrgetter('date', 'amount'))
        result = []
        balance = 0
        for c in date_sorted:
            balance += c.amount
            result.append(
                CashflowAndBalance(c.date, c.amount, c.description, balance))
        return reversed(result)

    def balance(self):
        return sum([c.amount for c in self.cashflows()])

# Translators: This is the balance of the tenant's payments
    balance.short_description = _("balance")

    class Meta:
        verbose_name = _("tenant")

    def __unicode__(self):
        return "{0} {1}".format(self.name, self.property)


class RentRevision(models.Model):
    tenant = models.ForeignKey(Tenant, verbose_name=Tenant._meta.verbose_name)
    start_date = models.DateField(_("start date"), validators=[validate_month])
    end_date = models.DateField(
        _("end date"), validators=[validate_month],
        blank=True, null=True)
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
        return "{0} - {1}".format(self.start_date, self.end_date or "")


class Payment(models.Model):
    """money received from the tenant"""
    tenant = models.ForeignKey(Tenant, verbose_name=Tenant._meta.verbose_name)
    date = models.DateField(_("date"))
    amount = models.DecimalField(
        _("amount"), max_digits=7, decimal_places=2,
        validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = _("payment")

    def __unicode__(self):
        return "{0} - {1}".format(self.date, self.amount)


class Fee(models.Model):
    """a one-time fee (for example an end of year adjustment fee)"""
    description = models.CharField(_("description"), max_length=255)
    tenant = models.ForeignKey(Tenant, verbose_name=Tenant._meta.verbose_name)
    date = models.DateField(_("date"))
    amount = models.DecimalField(_("amount"), max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = _("one-time fee")

    def __unicode__(self):
        return "{0} - {1}".format(self.description, self.date)


Cashflow = namedtuple('Cashflow', ['date', 'amount', 'description'])
CashflowAndBalance = namedtuple('Cashflow',
                                ['date', 'amount', 'description', 'balance'])


def payments_to_cashflows(date, payments):
    return [Cashflow(x.date, x.amount, _('payment'))
            for x in payments if x.date <= date]


def fees_to_cashflows(date, fees):
    return [Cashflow(x.date, -x.amount, x.description)
            for x in fees if x.date <= date]


def revision_to_cashflows(rev, end_date):
    """Converts a revision to a list of cashflows
    end_date -- the first month we do not want to take into account
    """
    end_date = rev.end_date or end_date
    result = []
    month_range = xrange(
        12*rev.start_date.year + rev.start_date.month,
        12*end_date.year + end_date.month)
    for m in month_range:
        # because january is 1
        mm = m - 1
        d = date(mm / 12, mm % 12 + 1, 1)
        result.append(Cashflow(d, -rev.rent, _("rent")))
        if rev.provision != 0:
            result.append(Cashflow(d, -rev.provision, _("provision")))
    return result


def revisions_to_cashflows(date, revisions):
    date = next_month(date)
    result = map(lambda r: revision_to_cashflows(r, date), revisions)
    joined_result = itertools.chain.from_iterable(result)
    return [c for c in joined_result if c.date < date]


def next_month(date):
    date = date.replace(day=1)
    if date.month == 12:
        return date.replace(month=1, year=date.year + 1)
    else:
        return date.replace(month=date.month+1)
