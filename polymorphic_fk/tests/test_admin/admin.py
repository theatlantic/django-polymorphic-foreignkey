from django.contrib import admin
from django.db import models
from django import forms

from polymorphic.admin import (
    PolymorphicParentModelAdmin, PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter)
import nested_admin

from .models import Base, A, B, C, Item, Group


class BaseChildAdmin(PolymorphicChildModelAdmin):
    base_model = Base
    base_fieldsets = [(None, {'fields': ['slug']})]


@admin.register(A)
class AAdmin(BaseChildAdmin):
    base_model = A
    base_fieldsets = [(None, {'fields': ['slug', 'a']})]
    show_in_index = True


@admin.register(B)
class BAdmin(BaseChildAdmin):
    base_model = B
    base_fieldsets = [(None, {'fields': ['slug', 'b']})]
    show_in_index = True


@admin.register(C)
class CAdmin(BaseChildAdmin):
    base_model = C
    base_fieldsets = [(None, {'fields': ['slug', 'c']})]
    show_in_index = True


@admin.register(Base)
class BaseParentAdmin(PolymorphicParentModelAdmin):
    base_model = Base
    child_models = (A, B, C)
    list_filter = (PolymorphicChildModelFilter,)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['slug', 'fk']})]


class ItemInline(nested_admin.NestedStackedInline):
    model = Item
    fieldsets = [(None, {'fields': ['position', 'slug', 'fk']})]
    sortable_field_name = 'position'
    formfield_overrides = {
        models.PositiveIntegerField: {'widget': forms.HiddenInput},
    }
    inline_classes = ['grp-open']


@admin.register(Group)
class GroupAdmin(nested_admin.NestedModelAdmin):
    inlines = [ItemInline]
    fieldsets = [(None, {'fields': ['slug']})]
