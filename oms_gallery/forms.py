import zipfile
from zipfile import BadZipFile
import os
from io import BytesIO

from PIL import Image

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile

from .models import Gallery, Photo


class UploadZipForm(forms.Form):
    zip_file = forms.FileField()

    name = forms.CharField(label=_('Имя'), max_length=250, required=False)
    gallery = forms.ModelChoiceField(Gallery.objects.all(), label=_('Галерея'), required=False)
    caption = forms.CharField(label=_('Подпись'), required=False)

    def clean_zip_file(self):
        """Открываю zip-архив, чтобы убедиться, что это действительный zip-архив."""
        zip_file = self.cleaned_data['zip_file']
        try:
            zip = zipfile.ZipFile(zip_file)
        except BadZipFile as e:
            raise forms.ValidationError(str(e))
        bad_file = zip.testzip()
        if bad_file:
            zip.close()
            raise forms.ValidationError('"%s" архив .zip поврежден.' % bad_file)
        zip.close()
        return zip_file

    def clean_title(self):
        name = self.cleaned_data['name']
        if name and Gallery.objects.filter(title=name).exists():
            raise forms.ValidationError(_('Галерея с таким названием уже существует.'))
        return name

    def clean(self):
        cleaned_data = super(UploadZipForm, self).clean()
        if not self['name'].errors:
            if not cleaned_data.get('name', None) and not cleaned_data['gallery']:
                raise forms.ValidationError(
                    _('Выберите существующую галерею или введите название для новой галереи.'))
        return cleaned_data

    def save(self, request=None, zip_file=None):
        if not zip_file:
            zip_file = self.cleaned_data['zip_file']
        zip = zipfile.ZipFile(zip_file)
        count = 1
        if self.cleaned_data['gallery']:
            gallery = self.cleaned_data['gallery']
        else:
            gallery = Gallery.objects.create(name=self.cleaned_data['name'], slug=slugify(self.cleaned_data['name']))
        for filename in sorted(zip.namelist()):

            if filename.startswith('__') or filename.startswith('.'):
                continue

            if os.path.dirname(filename):
                if request:
                    messages.warning(request,
                                     _('Игнорирование файла "{filename}" который в подпапке; все изображения должны '
                                       'быть в корене zip.').format(filename=filename), fail_silently=True)
                continue

            data = zip.read(filename)

            if not len(data):
                continue

            photo_title_root = self.cleaned_data['name'] if self.cleaned_data['name'] else gallery.title

            # Возможно, фотография уже существует с тем же слагом
            # делаю петлю, пока не найдем slug, который доступен.
            while True:
                img_title = ' '.join([photo_title_root, str(count)])
                slug = slugify(img_title)
                if Photo.objects.filter(slug=slug).exists():
                    count += 1
                    continue
                break

            photo = Photo(name=img_title, slug=slug, captions=self.cleaned_data['caption'])

            # Основная проверка, что это изображение.
            try:
                file = BytesIO(data)
                opened = Image.open(file)
                opened.verify()
            except Exception:
                # Pillow не распознает изображение.
                # Если «плохой» файл найден, мы просто пропускаем его.
                # Сообщаю это пользователю.
                if request:
                    messages.warning(request,
                                     _('Не удалось обработать файл "{0}" в архиве .zip.').format(
                                         filename),
                                     fail_silently=True)
                continue

            contentfile = ContentFile(data)
            photo.image.save(filename, contentfile)
            photo.save()
            gallery.images.add(photo)
            count += 1

        zip.close()

        if request:
            messages.success(request,
                             _('Фотографии были добавлены в галерею "{0}".').format(
                                 gallery.name),
                             fail_silently=True)