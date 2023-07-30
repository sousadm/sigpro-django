from urllib.parse import urlencode


def get_page(data, params):
    number = data.get('number')
    totalPages = data.get('totalPages', 0)
    return  {
        'object_list': data.get('content'),
        'number': number - 1,
        'has_other_pages': totalPages > 0,
        'has_previous': not data.get('first'),
        'has_next': not data.get('last'),
        'next_page_url': page_url(params, (data.get('number') + 1)),
        'next_page_number': data.get('number') + 1,
        'next_page_url': page_url(params, (data.get('number') + 1)),
        'previous_page_number': data.get('number') - 1,
        'previous_page_url': page_url(params, (data.get('number') - 1)),
        'page_range': range(0, totalPages - 1),
    }


def get_param(data, size):
    params = {}
    params['page'] = data.get('page', 0)
    params['size'] = data.get('size', size)
    params['sort'] = 'descricao,asc'
    return params

def page_url(params, page):
    params['page'] = page
    return urlencode(params)