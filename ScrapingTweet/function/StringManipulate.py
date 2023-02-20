import re
from html import unescape

def preprocessing_tweet(text):
    """
    Rimuove emoticon unicode, link, menzioni e hashtag, numeri di telefono internazionali, simboli $ e CRLF dal testo del tweet.
    """
    text = remove_unicode_emot(text)
    text = remove_links(text)
    text = remove_hashtag(text)
    text = remove_at_after(text)
    text = remove_international_phones(text)
    text = remove_dollar_symbol_conditional(text)
    text = remove_crlf(text)
    text = translate_html(text)
    return text


def translate_html(text):
    return unescape(text)


def remove_crlf(text):
    """
    Rimuove i caratteri CRLF (carriage return e line feed) dal testo.

    """
    return text.replace("\n", "")


def remove_dollar_symbol_conditional(text):
    """
    Rimuove tutti i simboli $ che non sono preceduti da un numero.

    """
    return re.sub(r'\$(?=\D)', '', text)


def remove_international_phones(text):
    """
    Rimuove i numeri di telefono internazionali dal testo.


    """
    return re.sub(r'\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}','', text)


def remove_unicode_emot(text):
    """
    Rimuove gli emoticon unicode dal testo.

    """
    return re.sub(r'[^\x00-\x7F]+','', text)


def remove_links(text):
    """
    Rimuove i link dal testo.


    """
    return re.sub(r'https?:\/\/\S+', '', text)


def remove_at_hashtags(text):
    """
    Rimuove i simboli @ e # dal testo.

    """
    return re.sub(r'(#|@)', '', text)


def remove_hashtag(text):
    """
        Rimuove il simbolo # dal testo.

        """
    return re.sub(r'(#)', '', text)


def remove_at_after(text):
    """
        Rimuove il simboli @ e la parola che esso precede

    """
    return re.sub(r'(@)\w+', '', text)


def remove_at_hashtags_after(text):
    """
    Rimuove i simboli @ e # e le parola che essi precedono dal testo.

    """
    return re.sub(r'(#|@)\w+', '', text)


def remove_dollar_symbol_conditional(text):
    """
    Rimuove tutti i simboli $ che non sono seguiti da un numero.

    """
    return re.sub(r'\$(?=\D)', '', text)