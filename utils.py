import nltk
import re
from urllib.parse import unquote
import tensorflow as tf
import keras.backend.tensorflow_backend as ktf
def URLDECODE(XSS):
    
    XSS=XSS.lower()
    XSS=unquote(unquote(XSS))
    XSS,num=re.subn(r'\d+',"0",XSS)
    
    XSS,num=re.subn(r'(http|https)://[a-zA-Z0-9\.@&/#!#\?]+', "http://u", XSS)
    
    r = '''
        (?x)[\w\.]+?\(
        |\)
        |"\w+?"
        |'\w+?'
        |http://\w
        |</\w+>
        |<\w+>
        |<\w+
        |\w+=
        |>
        |[\w\.]+
    '''
    return nltk.regexp_tokenize(XSS, r)
def init_session():
    ktf.set_session(tf.Session())
