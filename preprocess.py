from ravtrykd import *

#my favorites (stuff to train on)
kdfaves_train = meep.patternid_search(kdfavesid)
#pattern_pool --> first start with just a few patterns, about 1000 patterns...
patt_pool1 = meep.pattern_search(page = 5, page_size = 1000)
poolidsearch = meep.patternid_search(patt_pool1['id'].values)

#REMEMBER TO REMOVE THE URLS -------------------------->



def dropcols_cleannotes(new_df):
    
   
    def rmurls(text):
        if isinstance(text, str):
            #removing urls, [1]:, and non english characters from text 
            #i'm gonna have to hard code special characters r'[^a-zA-Z\s\.,!?;:]' --> so i'll leave this out for now
            patterns = [r'\[\d+\]:', r'https?://\S+|www\.\S+', r'\[\d+\]']
            combined_pattern = '|'.join(patterns)
            cleaned_text = re.sub(combined_pattern, '', text)
            # url_patt = re.compile(r'https?://\S+|www\.\S+')
            return cleaned_text
        else:
            return ''
    
    new_df['notes'] = new_df['notes'].str.replace('\r', ' ').str.replace('\n', ' ').str.replace('*', ' ').str.replace('>', ' ') #i removed '#' from this list
    # new_df['notes'] = new_df['notes'].apply(rmbracurls)
    new_df['notes'] = new_df['notes'].apply(rmurls)
    new_df['combo'] = new_df['gauge_pattern'] + ' ' + new_df['name_1'] + ' ' + new_df['sizes_available'] + ' ' + new_df['gauge_description'] + ' ' + new_df['yardage_description'] + ' ' + new_df['notes'] + ' ' + new_df['name_2'] + ' ' + new_df['name_3'] + ' '  + new_df['name_5'] 
    # + new_df['name_4'] + ' '
    return new_df

