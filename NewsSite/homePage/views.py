from django.shortcuts import render
from django.http import JsonResponse
from keras.utils import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import load_model


model = load_model("C:\\Users\\Admin\\Downloads\\yt_balanced_lstm.h5")


import preprocess_kgptalkie as ps


tokenizer = Tokenizer()  

def NewsDisplay(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')

        if user_input:
            # Tokenize user input using the same logic as during training
            tokenizer.fit_on_texts([user_input])  # Fit on user input
            user_input_sequence = tokenizer.texts_to_sequences([user_input])  # Tokenize the user input

            # Pad sequence to match the model's input length
            maxlen = 1000  
            user_input_padded = pad_sequences(user_input_sequence, maxlen=maxlen)

            # Make predictions
            prediction = model.predict(user_input_padded)[0, 0]

            # Display the prediction
            if prediction >0.5:
                result = 'This news is likely real.'
            else:
                result = 'This news is likely fake.'
        

        return render(request, 'homePage/result.html', {'result': result,'prediction':prediction})


    return render(request, "homePage/homeindex.html")
    
