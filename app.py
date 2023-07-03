from flask import Flask, render_template, request
from googletrans import Translator
translator = Translator()
from pyyoutube import Api
from transformers import pipeline
sent_pipeline = pipeline('sentiment-analysis')

app = Flask(__name__)
API_KEY = 'YOUR_API_KEY'
api = Api(api_key=API_KEY)


@app.route('/')
def send_index():
    return render_template("index.html", title='Projects')


@app.route('/api/comments', methods=['POST'])
def getComments():
    try:
        video_id = request.json.get('video_id')
        if video_id == None: return {'status': 'error', 'result': 'provide valid youtube video id'}, 400
        count = request.json.get('count')
        count = int(count) if count != None else 100
        count = 100 if count > 100 else count
    
        try:
            ct_by_video = api.get_comment_threads(
                video_id=video_id, count=count, return_json=True, order='relevance')
            return {'status': 'success', 'result': ct_by_video}, 200
        except:
            return {'status': 'error', 'result': 'provide valid youtube video id'}, 400
    except:
        return {'status': 'error', 'result': 'provide json body'}, 400


@app.route('/api/rating', methods=['POST'])
def getRating():
    try:
        comment_id = request.json.get('comment_id')
        textOriginal = request.json.get('text')
        if textOriginal == None: return {'status': 'error', 'result': 'provide text parameter'}, 400
        if comment_id == None: return {'status': 'error', 'result': 'provide comment_id parameter'}, 400
        result = translator.translate(textOriginal, dest='en')
        return {'status': 'success', 'result': { 'textTranslate': result.text, "comment_id": comment_id, "rating": sent_pipeline(result.text, truncation=True)}}, 200
    except:
        return {'status': 'error', 'result': 'provide json body'}, 400

if __name__ == '__main__':
    app.run(debug=True, port=4567)
