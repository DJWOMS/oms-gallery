from django import template

from oms_gallery.models import Gallery, Photo

register = template.Library()


@register.simple_tag()
def for_gallery(name=None, pk=None):
    """Вывод галереи по имени или id"""
    if name is not None:
        gallery = Gallery.objects.filter(name=name)
    elif pk is not None:
        gallery = Gallery.objects.filter(id=pk)
    else:
        gallery = Gallery.objects.all()
    return gallery


@register.simple_tag()
def get_photo(name=None, pk=None):
    """Вывод фото по имени или id"""
    if name is not None:
        photo = Photo.objects.filter(name=name).first()
    elif pk is not None:
        photo = Photo.objects.filter(id=pk).first()
    else:
        photo = None
    return photo


@register.simple_tag()
def for_photo(gallery=None):
    """Вывод фото имени галереи"""
    if gallery is not None:
        photos = Photo.objects.filter(gallery__name=gallery)
    else:
        photos = Photo.objects.all()
    return photos
