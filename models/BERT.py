from scipy.special import softmax
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import torch
import pandas as pd
import glob
import os
from transformers import BertTokenizer, BertModel
import config

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')


def split_into_chunks(df):

    # Split text dataframe into chunks to avoid running out of memory while processing it with BERT
    if config == 'news':
        text = [x[:201] + x[201:] for x in df.CONTENT.values]
    else:
        text = [x for x in df.CONTENT.values]

    chunks = [text[x:x + 25] for x in range(0, len(text), 25)]
    return chunks


def process_chunks(chunks):

    # Delete already existing files
    print('Deleting Files in path: \'/data/bert_outputs/\'')
    files = glob.glob('./data/bert_outputs/*')
    if len(files) > 0:
        for f in files:
            os.remove(f)

    # Processes every chunk with BERT and saves the embeddings in a file to be used later
    for i in range(len(chunks)):
        print(f"Chunk: {i + 1}/{len(chunks)}")
        inputs = tokenizer(chunks[i], add_special_tokens=True,
                           truncation=True, padding="max_length",
                           # return_attention_mask = True,
                           return_tensors="pt")

        model = BertModel.from_pretrained("bert-base-uncased")
        outputs = model(**inputs).pooler_output

        with open(f"./data/bert_outputs/chunk{i+1 if i+1 > 9 else f'0{i + 1}'}.pt", 'wb') as file:
            torch.save(outputs, file)

        del inputs, model, outputs


def apply_attention(x, method='cos', seed=None):

    # Ensures the repeatability of the experiment
    if seed:
        np.random.seed(seed)

    if torch.is_tensor(x):
        x = x.detach()

    # X is of shape (n,768) where n is the number of tweets/news in a day and 768 is the embedding length
    # Weight matrices are instead of shape (768, n)
    W_Q = np.random.random(size=(x.shape[1], x.shape[0]))
    W_K = np.random.random(size=(x.shape[1], x.shape[0]))
    W_V = np.random.random(size=(x.shape[1], x.shape[0]))

    querys = np.dot(x, W_Q)
    keys = np.dot(x, W_K)
    values = np.dot(x, W_V)

    # for context embedding, cosine similarity is often preferred to dot product
    if method == 'dot':
        scores = querys @ keys
    elif method == 'cos':
        scores = cosine_similarity(querys, keys)

    # scores are divided by sqrt(768) to keep gradients stable
    weights = softmax(scores / np.sqrt(x.shape[1]), axis=1)

    # the attention coefficient is obtained by sum. This is preferred to give more importance to days with more news.
    return np.sum(weights @ values)


def add_attention_to_df(df, price_df):

    # Reads the text embeddings then joins them in a single structure
    lista = [x for x in glob.glob("./data/bert_outputs/chunk[0-9][0-9].pt")]
    lista.sort()
    exes = []
    for el in lista:
        with open(f"./{el}", "rb") as file:
            ex = torch.load(file)
            exes.append(ex)
    tupla = tuple([x for x in exes])

    # Tensors are joint together in a list and then added as a column of the text source df
    # This lets every text entry have its corresponding embeddings
    prova = torch.cat(tupla)
    test = [prova[i, :].detach() for i in range(prova.shape[0])]
    df['Tensor'] = test
    new_df = pd.DataFrame(columns=['Date', 'Attention'])
    new_df.Date = df.DATE.unique()
    new_df = new_df.sort_values('Date').reset_index(drop=True)

    # Applies attention to embeddings, grouped by date. Finally adds the data as a feature of the price df
    new_df['Attention'] = new_df.apply(
        lambda x: apply_attention(torch.stack(tuple(df.loc[df.DATE == x.Date].Tensor.values)), seed=42), axis=1)
    temp = price_df.merge(new_df, on='Date', how='left')

    # attention values for days where no text is found are filled with mean value
    temp['Attention'] = temp.Attention.fillna(np.mean(temp.Attention))
    return temp


def process_text(df, text_source):

    chunks = split_into_chunks(text_source)
    process_chunks(chunks)
    output_df = add_attention_to_df(text_source, df)
    return output_df
