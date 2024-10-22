preprocessor = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3")
encoder = hub.KerasLayer("https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-128_A-2/1", trainable=True)

def get_bert_embeddings(text, preprocessor, encoder):

  text_input = tf.keras.layers.Input(shape=(), dtype=tf.string)
  encoder_inputs = preprocessor(text_input)
  outputs = encoder(encoder_inputs)
  embedding_model = tf.keras.Model(text_input, outputs['pooled_output'])
  sentences = tf.constant([text])
  return embedding_model(sentences)

df_yt['encodings'] = df_yt['cleaned_title'].apply(lambda x: get_bert_embeddings(x, preprocessor, encoder))