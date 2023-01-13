from function import twitter_get_post
from function import log
from Class import Post

query = "#gas OR #price OR #gasprice"
min_date = "2023-01-01"
max_date = "2023-01-12"
max_post = 2

# Inizializzazione e autenticazione dell'api di twitter
api = twitter_get_post.initialize_api()

# Prelievo dei post e generazione del json che rappresenta un dizionario la cui chiave è un intero che identifica il
# post, e la entry è un array di stringhe che compongono ciascun post
twitter_get_post.get_post_from_europe(api, query, min_date, max_date, max_post)

# Oggetto di classe Post che permette di manipolare il file Json
posts = Post.Post()
# get_post(key): permette di ottenere l'array di stringhe del post key-esimo
# remove_post(key): permette di rimuovere l'array di stringhe e la relativa chiave dall'attributo contenente il
# dizionario
log.info(posts.get_post(2))


