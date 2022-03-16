from django import template
 
register = template.Library()  

ban_words = ['nigga', 'amogus', 'fuck']

@register.filter(name='censor')  
def censor(value):  
    for i in ban_words:
        value = value.replace(i, '*' * len(i) )
    return value 
