from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from PIL import Image
import os

from django.utils.safestring import mark_safe


class Photo(models.Model):
    """Класс модели галереи"""
    name = models.CharField(_("Название"), max_length=250)
    image = models.ImageField(_("Изображение"), upload_to='gallery')
    captions = models.TextField(_("Подпись"), blank=True)
    сopyright = models.CharField(_("Автор"), max_length=250, blank=True, null=True)
    create_date = models.DateTimeField(_("Дата добавления"), auto_now_add=True)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name

    # Добавляем к свойствам объектов модели путь к миниатюре
    def _get_mini_path(self):
        return self._add_mini(self.image.path)

    mini_path = property(_get_mini_path)

    # Добавляем к свойствам объектов модели урл миниатюры
    def _get_mini_url(self):
        return self._add_mini(self.image.url)

    mini_url = property(_get_mini_url)

    # Добавляем к свойствам объектов модели html код для отображения миниатюры
    # Сделано в модели для упрощения вывода в админке. Смотрим далее.
    def get_mini_html(self):
        return mark_safe('<a class="image-picker" href="{}"><img src="{}" alt="{}"/></a>'.format(
            self.image.url, self._add_mini(self.image.url), self.captions
        ))

    mini_html = property(get_mini_html)
    get_mini_html.short_description = _('Изображение')
    get_mini_html.allow_tags = True

    # def to_internal_value(self, value):
    #     f = value.split("/").pop().split(".").pop(1)
    #     if f == "jpeg" or f == "jpg" or f == "webp":
    #         way = "tmp/img{}.j2p".format(value.split("/").pop().split(".").pop(0))
    #         outputPath = os.path.join(settings.MEDIA_ROOT, way)
    #         # quality = 50
    #         try:
    #             Image.open(settings.MEDIA_ROOT + "/" + way)
    #         except:
    #             im = Image.open(settings.BASE_DIR + value[value.rfind('/media'):])
    #             im.save(outputPath, 'JPEG', optimize=True, quality=60)
    #         path = settings.MEDIA_URL[:settings.MEDIA_URL.find('media')] + outputPath[outputPath.rfind('media'):]
    #         return path
    #     else:
    #         return value

    # Создаем свою save
    # Добавляем:
    # - создание миниатюры
    # - удаление миниатюры и основного изображения
    #   при попытке записи поверх существующей записи
    def save(self, **kwargs):
        try:
            obj = Photo.objects.get(id=self.id)
            if obj.image.path != self.image.path:
                self._del_mini(obj.image.path)
                obj.image.delete()
        except:
            pass
        super(Photo, self).save(**kwargs)
        img = Image.open(self.image.path)
        img.thumbnail(
            (128, 128),
            Image.ANTIALIAS
        )

        f = self.image.name.split(".").pop(1)
        if f == "jpeg" or f == "jpg":
            img.save(self.mini_path, "JPEG")
        else:
            img.save(self.mini_path, f)

    # Делаем свою delete с учетом миниатюры
    def delete(self, using=None):
        try:
            obj = Photo.objects.get(id=self.id)
            self._del_mini(obj.image.path)
            obj.image.delete()
        except (Photo.DoesNotExist, ValueError):
            pass
        super(Photo, self).delete()

    def _add_mini(self, s):
        """Изменение (filename, URL) вставкой '.mini' и изменение расширения на jpg"""
        parts = s.split(".")
        parts.insert(-1, "mini")
        if parts[-1].lower() not in ['jpeg', 'jpg']:
            parts[-1] = 'jpg'
        return ".".join(parts)

    def _del_mini(self, p):
        """Удаление миниатюры с физического носителя"""
        mini_path = self._add_mini(p)
        if os.path.exists(mini_path):
            os.remove(mini_path)

    def get_absolute_url(self):
        return reverse('photo_detail', kwargs={'object_id': self.id})

    class Meta:
        verbose_name = _('Изображение')
        verbose_name_plural = _('Изображения')
        ordering = ['name']


class Gallery(models.Model):
    """Модель галереи"""
    name = models.CharField(_("Название"), max_length=250)
    images = models.ManyToManyField(Photo, verbose_name=_("Изображение"))
    captions = models.TextField(_("Описание"), max_length=250, blank=True)
    create_date = models.DateTimeField(_("Дата добавления"), auto_now_add=True)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Галерея')
        verbose_name_plural = _('Галереи')
        ordering = ['name']
