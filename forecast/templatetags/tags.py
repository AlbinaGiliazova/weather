from django import template  
   
register = template.Library()  


@register.filter  
def index(sequence, position):  
    """Возвращает sequence[position] или пустую строку при ошибке."""  
    try:  
        return sequence[position]  
    except Exception:  
        return ''
