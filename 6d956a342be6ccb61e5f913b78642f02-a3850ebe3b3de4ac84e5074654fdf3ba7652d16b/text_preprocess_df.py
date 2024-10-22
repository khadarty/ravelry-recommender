df_yt = pd.read_csv('/content/GB_videos_data.csv')
df_yt = df_yt.drop_duplicates(subset = ['title'])
df_yt = df_yt[['title', 'description']]
df_yt.columns = ['Title', 'Description']
df_yt['cleaned_title'] = df_yt['Title'].apply(lambda x: x.lower())
df_yt['cleaned_title'] = df_yt['cleaned_title'].apply(lambda x: re.sub('[^A-Za-z0-9]+', ' ', x))