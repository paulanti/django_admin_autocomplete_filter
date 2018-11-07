import operator

from django import forms
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.widgets import AutocompleteSelect


class AutocompleteFilter(SimpleListFilter):
    template = 'autocomplete_filter.html'
    title = ''
    field_name = ''

    def __init__(self, request, params, model, model_admin):
        self.parameter_name = f'{self.field_name}__id__exact'
        super().__init__(request, params, model, model_admin)

        self.field = forms.ModelChoiceField(
            queryset=getattr(model, self.field_name).get_queryset(),
        )
        self.field.widget = AutocompleteSelect(
            rel=operator.attrgetter(
                f"{self.field_name}.field.remote_field"
            )(model),
            admin_site=model_admin.admin_site, choices=self.field.choices,
        )

        self.rendered_widget = self.field.widget.render(
            name=self.parameter_name,
            value=self.used_parameters.get(self.parameter_name, ''),
        )

    def has_output(self):
        return True

    def lookups(self, request, model_admin):
        return ()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{self.parameter_name: self.value()})
        return queryset
