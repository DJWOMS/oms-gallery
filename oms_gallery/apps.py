from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class GalleryConfig(AppConfig):
    name = 'oms_gallery'
    verbose_name = _("Галерея")
