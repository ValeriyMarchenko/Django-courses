from django import template
 
register = template.Library()  

ban_words = ['nigga', 'amogus', 'fuck']

@register.filter(name='censor')  
def censor(value): 
    if not isinstance(value, str):
        raise ValueError('Cant censor not str object') 
    for i in ban_words:
        value = value.replace(i[0:], '*' * len(i) )
    return value 

# alternative var. :  value = value.replace(i[1:], '*' * (len(i) - 1) )


@register.filter(name='update_page')
def update_page(full_path:str, page:int):
    try:
        params_list = full_path.split('?')[1].split('&')
        params = dict([tuple(str(param).split('=')) for param  in params_list])
        params.update({'page' : page})
        link = ''
        for key, value in params.items():
            link += (f"{key}={value}&")
        return link[:-1]
    except:
        return f"page={page}"