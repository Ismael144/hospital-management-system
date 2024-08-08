from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """Add CSS class to form field."""
    attrs = value.field.widget.attrs
    css_class = attrs.get('class', '')
    if css_class:
        attrs['class'] = f'{css_class} {arg}'
    else:
        attrs['class'] = arg
    return value

@register.filter(name='add_required_class')
def add_required_class(field):
    if field.field.required:
        return field.as_widget(attrs={'class': 'form-control required-field'})
    return field.as_widget(attrs={'class': 'form-control'})