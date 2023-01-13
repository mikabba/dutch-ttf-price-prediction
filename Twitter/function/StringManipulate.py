import re


def preprocessing_tweet(text):
    """
    Rimuove emoticon unicode, link, simboli @ e #, numeri di telefono internazionali, simboli $ e CRLF dal testo del tweet.

    Authors:
        Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
    """
    text = remove_unicode_emot(text)
    text = remove_links(text)
    text = remove_at_hashtags(text)
    text = remove_international_phones(text)
    text = remove_dollar_symbol_conditional(text)
    text = remove_crlf(text)
    return text


def remove_crlf(text):
    """
    Rimuove i caratteri CRLF (carriage return e line feed) dal testo.

    Authors:
        Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
    """
    return text.replace("\n", "")


def remove_dollar_symbol_conditional(text):
    """
    Rimuove tutti i simboli $ che non sono preceduti da un numero.

    Authors:
        Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
    """
    return re.sub(r'\$(?=\D)', '', text)


def remove_international_phones(text):
    """
    Rimuove i numeri di telefono internazionali dal testo.

    Authors:
        Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
    """
    return re.sub(r'(\+\d{1,3}\s)?\d{3}\s\d{3}\s\d{4}','', text)


def remove_unicode_emot(text):
    """
    Rimuove gli emoticon unicode dal testo.

    Authors:
        Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
    """
    return re.sub(r'[^\x00-\x7F]+','', text)


def remove_links(text):
    """
    Rimuove i link dal testo.

    Authors:
        Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
    """
    return re.sub(r'https?:\/\/\S+', '', text)


def remove_at_hashtags(text):
    """
    Rimuove i simboli @ e # dal testo.

    Authors:
        Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
    """
    return re.sub(r'(#|@)', '', text)


def remove_at_hashtags_after(text):
    """
    Rimuove i simboli @ e # e le parola che precedono dal testo.

    Authors:
        Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
    """
    return re.sub(r'(#|@)\w+', '', text)


def remove_dollar_symbol_conditional(text):
    """
    Rimuove tutti i simboli $ che non sono preceduti da un numero.
    Args:
        text (str): Il testo da elaborare.
    Returns:
        str: Il testo elaborato con i simboli $ non preceduti da un numero rimossi.

    Authors:
        Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
    """
    return re.sub(r'\$(?=\D)', '', text)