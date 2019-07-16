from django.urls import path
from django.contrib import admin
from django import forms
from django.contrib.admin import helpers
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Photo, Gallery
from .forms import UploadZipForm


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Админ фото"""
    list_display = ('name', 'captions', 'get_mini_html', 'create_date', 'id')
    search_fields = ('name', )
    # admin.site.disable_action('delete_selected')
    readonly_fields = ["get_mini_html"]
    list_filter = ('create_date', )
    prepopulated_fields = {'slug': ('name',)}

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def full_delete_selected(self, request, obj):
        for o in obj.all():
            o.delete()
    full_delete_selected.short_description = 'Удалить выбранные иллюстрации'
    actions = ['full_delete_selected']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('immortal/', self.upload_zip, name="oms_upload_zip"),
        ]
        return my_urls + urls
    change_list_template = "oms_gallery/admin/change_list.html"

    def upload_zip(self, request):

        context = {
            'title': 'Загрузка изображений zip-архивом',
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }

        # Handle form request
        if request.method == 'POST':
            form = UploadZipForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(request=request)
                return HttpResponseRedirect('..')
        else:
            form = UploadZipForm()
        context['form'] = form
        context['adminform'] = helpers.AdminForm(form, list([(None, {'fields': form.base_fields})]), {})
        return render(request, 'oms_gallery/admin/upload_zip.html', context)


class PhotoChoiceField(forms.ModelMultipleChoiceField):
    """Виджет checkbox с отображением миниатюр"""
    def label_from_instance(self, obj):
        return obj.get_mini_html()


class GalleryForm(forms.ModelForm):
    """Форма для галереи с виджетом"""
    images = PhotoChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Photo.objects.all(), required=True)

    class Meta:
        model = Gallery
        fields = ('__all__')


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    """Админ галереи"""
    list_display = ('name', 'captions', 'create_date', 'id')
    list_filter = ('create_date',)
    prepopulated_fields = {'slug': ('name',)}
    form = GalleryForm





