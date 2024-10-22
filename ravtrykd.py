from ravfuncs import *
from IPython.display import display

#allowing me to see all rows and columns in a dataframe
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

#creating instance of thingy thing 
meep = ravutils(authUsername, authPassword)

# display(meep.get_user(rav_username = 'khadarty'))

# display(meep.get_projects(rav_username = 'khadarty'))

# searching for patterns with ids
idsearch1 = meep.patternid_search([523829,7364422,857493])
# getting my favorites, i specified patterns, but you can get all favorites
kdfaves = meep.get_favorites(rav_username = 'khadarty')
# getting ids of my faves
kdfavesid = kdfaves['favorited.id'].values
# getting the notes of all of the patterns in my favorites list by doing an id search
kdfavesnotes = meep.patternid_search(kdfavesid)[['notes']]
#getting my queue
kdqueue = meep.get_queue(rav_username = 'khadarty')
#get ids of queue
kdqueueid = kdqueue['pattern_id'].values
#getting notes of queue patterns 
kdqueuenotes = meep.patternid_search(kdqueueid)[['notes']]

#converting strings to datetime objects, plotting histogram of dates --> shows how many patterns i favorited every months
kdfaves['datetime'] = pd.to_datetime(kdfaves['created_at'], errors='coerce', utc = True)
kdfaves['datetime']
kdfaves['date'] = kdfaves['datetime'].dt.date
kdfaves['month'] = kdfaves['datetime'].dt.month
plt.hist(kdfaves['date'])
plt.xlabel('Date')
plt.ylabel('Counts')
plt.title('Counts of patterns favorited over time')
plt.xticks(rotation = 270)
plt.show()