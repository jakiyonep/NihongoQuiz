from django import template

register = template.Library()

@register.simple_tag()
def my_url(value, filed_name, urlencode=None):
    url = '?{}={}'.format(filed_name, value)

    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0]!=filed_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)

    return url


