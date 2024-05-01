from tqdm import tqdm
import pandas as pd
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def pipeline(df):
    indexes = list(df.keys())
    
    # Model
    from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

    inputs = tokenizer("I hate paolo", return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits

    predicted_class_id = logits.argmax().item()
    model.config.id2label[predicted_class_id]
    
    # Getting the amount of reviews
    total_reviews = []
    for k in range(len(indexes)):
        data = len([x.strip() for x in list(df[indexes[k]]['users_review'].values()) if len(x) >= 1])
        total_reviews.append(data)
    
    # Getting the positive reviews
    res_name, res_loc, res_catagory, reviews, res_rating = [], [], [], [], []
    for k in tqdm(range(len(indexes))):
        res_name.append(df[indexes[k]]['title']+", " + df[indexes[k]]['address'])
        res_loc.append(df[indexes[k]]['location'][0].split("destination=")[1])
        res_catagory.append(df[indexes[k]]['category'])
        data = [x.strip() for x in list(df[indexes[k]]['users_review'].values()) if len(x) >= 1]
        counter = 0
        for i in data:
            inputs = tokenizer(i, return_tensors="pt")
            with torch.no_grad():
                logits = model(**inputs).logits

            predicted_class_id = logits.argmax().item()
            score = model.config.id2label[predicted_class_id]
            if score == 'POSITIVE':
                counter += 1
        reviews.append(counter)
        res_rating.append(df[indexes[k]]['dining_rating'])
        
    # Creating a dataframe with information collected
    data_frame = pd.DataFrame({'res_name': res_name, 'res_loc': res_loc, 'res_catagory': res_catagory, 'total_no_reviews': total_reviews, 'positive_reviews': reviews, 'res_rating': res_rating})
    
    # Creating a new rating through the analysis of the NLP model
    data_frame['actual_rating'] = round(((( data_frame['positive_reviews'] / data_frame['total_no_reviews'] ) * 100) * 5 )/100,1)
    
    # Creating a new column with a consice description of the restaurant category
    temp =  [" ".join(x) for x in data_frame['res_catagory'] ]
    data_frame['bag_of_words'] = temp
    data_frame['res_name'] = data_frame['res_name'].apply(lambda x: x.split(',')[0])
    
    # Rounding and splitting the location
    data_frame['res_loc_x'] = data_frame['res_loc'].apply(lambda x: x.split(",")[0])
    data_frame['res_loc_y'] = data_frame['res_loc'].apply(lambda x: x.split(",")[1])
    
    # Creating a column for time
    data_frame['time'] = [df[x]['time'] for x in indexes]
    
    # Creating a column for the location link
    data_frame['location_link'] = [df[x]['location'] for x in indexes]
    
    # Creating a column for the zomato link
    links = list(df.keys())[0]
    data_frame['zomato_link'] = list(df.keys())[0]
    
    # Creating a column for the phone number
    data_frame['delivery_rating'] = [df[x]['delivery_rating'] for x in indexes]
    
    return data_frame

def analyze_recommendation(data_frame, category):
    message = ""
    ideal_restaurants = data_frame.copy()
    
    if len(ideal_restaurants) == 0:
        message = "No restaurants found near you"
    
    # Filtering the data by the category
    category_str = ' '.join(category)
    documents = [category_str] + ideal_restaurants['bag_of_words'].tolist()
    vectorizer = TfidfVectorizer().fit(documents)

    # Transform the user and restaurant 'documents' to TF-IDF vectors
    user_vector = vectorizer.transform(category)
    restaurant_vectors = vectorizer.transform(ideal_restaurants['bag_of_words'])
    similarities = cosine_similarity(user_vector, restaurant_vectors)
    
    # Sorting the data
    ideal_restaurants['similarity'] = similarities.mean(axis=0)
    ideal_restaurants = ideal_restaurants.sort_values(by='similarity', ascending=False)
    
    # Removing those not similar
    top_iqr = ideal_restaurants['similarity'].quantile(0.75)
    ideal_restaurants = ideal_restaurants[ideal_restaurants['similarity'] > top_iqr]
    
    # Using ranking to get the top 5 restaurants
    mean = ideal_restaurants['actual_rating'].mean()
    ideal_restaurants = ideal_restaurants[ideal_restaurants['actual_rating'] > mean]
    
    # Sorting by rating
    ideal_restaurants = ideal_restaurants.sort_values(by='actual_rating', ascending=False)
    
    # Getting the top 5
    ideal_restaurants = ideal_restaurants.head(10)
    
    return ideal_restaurants, message

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommendation(data_frame, title, total_result=5):
    tfid = TfidfVectorizer()
    tfid_matrix = tfid.fit_transform(data_frame['bag_of_words'])
    tfid.get_feature_names_out()
    
    cosine_sim = cosine_similarity(tfid_matrix, tfid_matrix)
    
    idx = data_frame[data_frame['res_name'] == title].index[0]
    data_frame['similarity'] = cosine_sim[idx]
    sort_final_df = data_frame.sort_values(by='similarity', ascending=False)[1:total_result+1]
    mean = sort_final_df['actual_rating'].mean()
    sort_final_df = sort_final_df[sort_final_df['actual_rating'] > mean]
    sort_final_df = sort_final_df.sort_values(by='actual_rating', ascending=False)
    sort_final_df = sort_final_df.head(5)
    names = sort_final_df['res_name']
    if len(names) != 0:
        print('Similar restraunt name(s) list:')
        for i, movie in enumerate(names):
            print('{}. {}'.format(i+1, movie))
        print()
    else:
        print('Similar restaurant name(s) list:')
        print('-\n')
    
    return sort_final_df