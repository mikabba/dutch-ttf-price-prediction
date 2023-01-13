import json
from function import log


class Post:
    """
    Classe per la gestione dei post.
    Questa classe consente di aggiungere, recuperare e rimuovere i post da un dizionario inizializzato con il contenuto
    di un file JSON.
    I post sono rappresentati da array di stringhe
    :param key: chiave del post
    :param value: valore del post

    Authors:
        Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
    """
    def __init__(self):
        """
        Costruttore della classe.
        Apre il file JSON contenente i post e li carica come un dizionario dove ogni chiave è un identificativo univoco
        del post e il valore associato è un array di stringhe che rappresentano il contenuto del post.

        Authors:
            Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
        """
        with open("file/json_posts_string.json") as posts_file:
            self.posts = json.load(posts_file, object_hook=keystoint)

    def add_post(self, key, value):
        """
        Aggiunge un array di stringhe che rappresenta un post al dizionario dei post.
        Se la chiave non esiste, la crea.

        :param key: chiave del post
        :param value: valore del post

        Authors:
            Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
        """
        if key not in list(self.posts.keys()):
            self.posts[key] = []
        self.posts[key].append(value)

    def get_post(self, key):
        """
        Recupera un array di stringhe che rappresenta il post dal dizionario dei post in base alla chiave.

        :param key: chiave del post
        :return: valore del post se esiste, altrimenti None

        Authors:
            Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
        """
        if key in list(self.posts.keys()):
            return self.posts[key]
        else:
            log.warning(f'Non esiste alcuna entry identificata dalla chiave:{key}')
            return None

    def remove_post(self, key):
        """
        Rimuove un array di stringhe post dal dizionario dei post in base alla chiave.

        :param key: chiave del post

        Authors:
            Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
        """
        if key in list(self.posts.keys()):
            del self.posts[key]

    def __str__(self):
        """
        Restituisce una rappresentazione testuale del dizionario dei post.

        :return: stringa contenente la rappresentazione del dizionario

        Authors:
            Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
        """
        return str(self.posts)


def keystoint(x):
    """
    Converte le chiavi di un dizionario in interi.

    :param x: dizionario da convertire
    :return: dizionario con chiavi convertite in interi

    Authors:
        Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
    """

    return {int(k): v for k, v in x.items()}

