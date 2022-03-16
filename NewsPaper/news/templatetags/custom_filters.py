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