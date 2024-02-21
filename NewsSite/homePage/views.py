from django.shortcuts import render
from django.http import JsonResponse
from keras.utils import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import load_model
from django import forms
import preprocess_kgptalkie as ps
model = load_model("C:\\Users\\Admin\\Downloads\\yt_balanced_lstm1.h5")






tokenizer = Tokenizer()  

def NewsDisplay(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')

        if user_input:
            # Tokenize user ko input same as during training
            tokenizer.fit_on_texts([user_input])  # Fit on user input
            user_input_sequence = tokenizer.texts_to_sequences([user_input])  # Tokenize the user input

            #Adding Pad sequence to match the model's input
            maxlen = 1000  
            user_input_padded = pad_sequences(user_input_sequence, maxlen=maxlen)

            # Make predictions
            prediction = model.predict(user_input_padded)[0, 0]

            # Display the prediction 
            if prediction >0.8:
                result = 'This news is likely real.'
            else:
                result = 'This news is likely fake.'
        

        return render(request, 'homePage/homeindex.html', {'result': result,'prediction':prediction})


    return render(request, "homePage/homeindex.html")
    


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from pygooglenews import GoogleNews
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import spacy

# Load English language model for NER
nlp = spacy.load('en_core_web_sm')
nltk.download('punkt')
nltk.download('stopwords')
def preprocess_text(text):
    # Tokenize the text
    tokens = nltk.word_tokenize(text.lower())
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

def calculate_similarity(claim, articles):
    # Preprocess the claim
    processed_claim = preprocess_text(claim)
    # Preprocess and tokenize the articles
    processed_articles = [preprocess_text(article) for article in articles]
    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    # Fit and transform the processed articles
    tfidf_matrix = vectorizer.fit_transform([processed_claim] + processed_articles)
    # Calculate cosine similarity between the claim and each article
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
    return similarity_scores

def verify_claim(claim_text):
    print("Claim Text:", claim_text)  # Print the claim text for debugging purposes
    
    # Initialize PyGoogleNews
    gn = GoogleNews(lang='en', country='US')

    # Fetch relevant articles using PyGoogleNews
    search_results = gn.search(preprocess_text(claim_text))
    articles = [entry['title'] for entry in search_results['entries']]

    # Calculate similarity between claim and articles
    similarity_scores = calculate_similarity(claim_text, articles)

    # Combine articles with their similarity scores
    claim_results = list(zip(articles, similarity_scores))

    # Sort articles by similarity score (descending order)
    claim_results = sorted(claim_results, key=lambda x: x[1], reverse=True)

    return claim_results

def ClaimCheck(request):
    if request.method == 'POST':
        claim_text = request.POST.get('user_input')
        
        if claim_text:
            # Perform claim verification using the claim text
            claim_results = verify_claim(claim_text)
            
            # Pass the claim verification results to the template
            context = {'claim_results': claim_results}
            return render(request, "homePage/claimchecking.html", context)

    return render(request, "homePage/claimchecking.html")