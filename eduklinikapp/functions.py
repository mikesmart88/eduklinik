# create your fuction here

import random,string
from ast import literal_eval

def rand_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
     """
     used to generate random  string with a given lenght.
     """
     return ''.join(random.choice(chars) for _ in range(size))


def s_remove(txt):
     
     main = str((txt))
     
     if ' ' in main:
          'is not in text'
     main = main.replace(' ', '_')
     return main
          
          
def loop_mode(model):
     for i in model:
          print(i)
          return i