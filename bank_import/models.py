from collections import namedtuple
from django.db import models
from django.utils.translation import ugettext_lazy as _


ImportLine = namedtuple('ImportLine', ['date', 'amount', 'caption'])


class ImportedLine(models.Model):
    date = models.DateField(_("date"))
    amount = models.DecimalField(
        _("amount"), max_digits=7, decimal_places=2)
    caption = models.CharField(_("caption"), max_length=1024)
    mapping = models.CharField(_("mapping"), max_length=1024)
