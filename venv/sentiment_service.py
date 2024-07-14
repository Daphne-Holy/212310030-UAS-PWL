import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from flask import Flask, request, jsonify
from flask_cors import CORS

# Buat stemmer Sastrawi
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Muat kamus sentimen
def load_lexicon(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lexicon = set(file.read().split())
    return lexicon

# positif_lexicon = load_lexicon('positif.txt')
# negatif_lexicon = load_lexicon('negatif.txt')

senang_lexicon = load_lexicon('senang.txt')
sedih_lexicon = load_lexicon('sedih.txt')
marah_lexicon = load_lexicon('marah.txt')
takut_lexicon = load_lexicon('takut.txt')

# Peta label perasaan ke URL gambar
emotion_to_image_map = {
    "senang": "/images/happy.jpg",
    "sedih": "/images/sad.jpg",
    "marah": "/images/angry.jpg",
    "takut": "/images/fear.jpg"
}

# Fungsi praproses teks
def preprocess_text(text):
    # Mengubah teks menjadi huruf kecil
    text = text.lower()
    
    # Menghapus tanda baca
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenisasi
    words = text.split()
    
    # Stemming
    stemmed_words = [stemmer.stem(word) for word in words]
    
    # # Gabungkan kembali menjadi teks
    # processed_text = ' '.join(stemmed_words)
    
    return stemmed_words

# Analisis Sentimen
def analyze_sentiment(text):
    # processed_text = preprocess_text(text)
    tokens = preprocess_text(text)
    emotions = []

    for token in tokens:
        if token in senang_lexicon:
            emotions.append({"word": token, "emotion": "senang", "image": emotion_to_image_map["senang"]})
        elif token in sedih_lexicon:
            emotions.append({"word": token, "emotion": "sedih", "image": emotion_to_image_map["sedih"]})
        elif token in marah_lexicon:
            emotions.append({"word": token, "emotion": "marah", "image": emotion_to_image_map["marah"]})
        elif token in takut_lexicon:
            emotions.append({"word": token, "emotion": "takut", "image": emotion_to_image_map["takut"]})

    return {'emotions': emotions}


# Flask API
app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Bad Request, 'text' field is missing"}), 400
    text = data['text']
    result = analyze_sentiment(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# Contoh penggunaan
# if __name__ == '__main__':
#     text = "Saya sangat senang dan bahagia hari ini, cuaca luar biasa!"
#     result = analyze_sentiment(text)
#     print(result)
