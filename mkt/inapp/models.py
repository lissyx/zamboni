from django.core.urlresolvers import reverse
from django.db import models

from amo.models import ModelBase
from apps.translations.fields import save_signal, TranslatedField


class InAppProduct(ModelBase):
    """
    An item which is purchaseable from within a marketplace app.
    """
    webapp = models.ForeignKey('webapps.WebApp')
    price = models.ForeignKey('market.Price')
    name = TranslatedField(require_locale=False)
    logo_url = models.URLField(max_length=1024, null=True, blank=True)

    class Meta:
        db_table = 'inapp_products'

    def __unicode__(self):
        return u'%s: %s' % (self.webapp.name, self.name)

    @property
    def icon_url(self):
        return self.logo_url or self.webapp.get_icon_url(64)

    @property
    def buy_url(self):
        # FIXME: This should accept the id in the url instead of from JSON.
        return reverse('webpay-prepare-inapp')


models.signals.pre_save.connect(save_signal, sender=InAppProduct,
                                dispatch_uid='inapp_products_translations')
