import json


class Auth:
    """
    Classe per la gestione delle chiavi di autenticazione per l'API di Twitter.
    :Authors:
        Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
    """
    def __init__(self):
        """
        Inizializza la classe leggendo le chiavi di autenticazione dal file config/config.json
        :Authors:
            Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
        """
        with open("config/config.json") as config_file:
            config = json.load(config_file)
        self.consumer_key = config["consumer_key"]
        self.consumer_secret = config["consumer_secret"]
        self.access_token = config["access_token"]
        self.access_token_secret = config["access_token_secret"]

    def get_consumer_key(self):
        """
        Restituisce la chiave consumer_key.
        :Authors:
            Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
        """
        return self.consumer_key

    def get_consumer_secret(self):
        """
        Restituisce la chiave consumer_secret.
        :Authors:
            Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
        """
        return self.consumer_secret

    def get_access_token(self):
        """
        Restituisce la chiave access_token.
        :Authors:
            Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
        """
        return self.access_token

    def get_access_token_secret(self):
        """
        Restituisce la chiave access_token_secret.
        :Authors:
            Michele Abbaticchio <m.abbaticchio@studenti.poliba.it>
        """
        return self.access_token_secret
