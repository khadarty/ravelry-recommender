from ravtrykd import *
from ravfuncs import *
from sklearn.metrics.pairwise import cosine_similarity

#my favorites (stuff to train on)
kdfaves_train = meep.patternid_search(kdfavesid)
#pattern_pool --> first start with just a few patterns, about 1000 patterns...
patt_pool1 = meep.pattern_search(page = 4, page_size = 1000)
poolidsearch = meep.patternid_search(patt_pool1['id'].values)

non_string_mask = ~poolidsearch['notes'].apply(isinstance, args = (str, ))
non_string_values = poolidsearch[non_string_mask]
non_string_values['notes']

kdfaves_train = kdfaves_train.fillna('')
poolidsearch = poolidsearch.fillna('')
ftr = dropcols_cleannotes(kdfaves_train)
ptr = dropcols_cleannotes(poolidsearch)

# tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased',do_lower_case = True)
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')

# tokenizing first description
text = ptr.iloc[0].combo
tokens = tokenizer.tokenize(text)

# Create embeddings for each pattern
pattern_embeddings = [get_embeddings(desc) for desc in ptr['combo']]
user_embeddings = [get_embeddings(desc) for desc in ftr['combo']]

#mean of user embeddings to get average embedding
uemb = torch.mean(torch.stack(user_embeddings), dim=0)

##-----------------------> embeddings for each pattern in the pool and in favorites
ftr['embeddings'] = user_embeddings
ptr['embeddings'] = pattern_embeddings


ptr['similarity_score'] = ptr['embeddings'].apply(get_recs, args = (uemb, ))


