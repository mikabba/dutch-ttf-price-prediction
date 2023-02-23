# Predizione Dell’indice Dutch TTF Combinando Embedding Testuali Di News E Tweet Con La Serie Storica Dei Dati
Questo è un project work sviluppato per il corso di Artificial Intelligence e Machine Learning del Politecnico di Bari.

Il lavoro svolto è stato utile a sviluppare un approccio che combini tecniche di deep learning per il processing di input testuali (BERT) con reti neurali ricorrenti per l’analisi di serie temporali quali BiLSTM e GRU, con l’obiettivo di aumentare l’accuratezza delle previsioni a breve termine dei prezzi del gas naturale. Il modello proposto è in grado di ottenere delle predizioni elevatamente accurate. Tuttavia, dai risultati ottenuti si è evinto che l’utilizzo di embedding testuali di news e tweets non è in grado di migliorare le performance rispetto al solo utilizzo della serie storica.

Utilizzo:
* Specificare la configurazione desiderata all'interno del file `config.py`
* Lo script può essere lanciato tramite riga di comando: `python main.py` oppure tramite un IDE compatibile
* L'output delle predizioni si troverà al percorso `/output/predictions.csv`
