def preprocess_text():
  text = input()
  text = text.lower()
  text = re.sub('[^A-Za-z0-9]+', ' ', text)
  return text
  
query_text = preprocess_text()
query_encoding = get_bert_embeddings(query_text, preprocessor, encoder)

df_yt['similarity_score'] = df_yt['encodings'].apply(lambda x: metrics.pairwise.cosine_similarity(x, query_encoding)[0][0])
df_results = df_yt.sort_values(by=['similarity_score'], ascending=False)