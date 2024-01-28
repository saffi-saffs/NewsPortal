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
    
