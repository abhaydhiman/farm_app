from django import template
from modules.imp_funcs import translator
from modules.diff_langs_texts import *

from user_home.views import *



register = template.Library()





@register.simple_tag(name = 'trans')
def trans( key , language ):
    dic = langs_dic[ language ]
    return dic[key]

# @register.simple_tag(name = 'transs')
# def transs( key , language ):
#     dic = langs_dic[ language ]
#     return dic[key]

@register.simple_tag(name = 'translate')
def translate( string , language ):

    translated_string = ''

    for word in string.split():
        translated_string += translator( word.lower() , to_langg = language) + ' '
    
    return translated_string
    



@register.simple_tag(name = 'transs')
def transs( key , language ):
    dic = langs_dic[ language ]
    return dic[key]



@register.filter
def modulo(num, val):
    return num % val