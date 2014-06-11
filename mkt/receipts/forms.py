from urlparse import urlparse

from django import forms

from tower import ugettext_lazy as _lazy

import amo
from mkt.api.forms import SluggableModelChoiceField
from mkt.webapps.models import Addon


class ReceiptForm(forms.Form):
    app = SluggableModelChoiceField(
        queryset=Addon.objects.filter(type=amo.ADDON_WEBAPP),
        sluggable_to_field_name='app_slug')


class TestInstall(forms.Form):
    TYPE_CHOICES = (('none', _lazy('No receipt')),
                    ('ok', _lazy(u'Test receipt')),
                    ('expired', _lazy(u'Expired test receipt')),
                    ('invalid', _lazy(u'Invalid test receipt')),
                    ('refunded', _lazy(u'Refunded test receipt')))

    receipt_type = forms.ChoiceField(choices=TYPE_CHOICES)
    manifest_url = forms.URLField()

    def clean(self):
        data = self.cleaned_data
        url = data.get('manifest_url')
        if url:
            parsed = urlparse(url)
            data['root'] = '%s://%s' % (parsed.scheme, parsed.netloc)
        return data
