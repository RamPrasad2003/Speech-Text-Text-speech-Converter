import speech_recognition as sr
from flask import *
from gtts import gTTS
import os
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/text')
def text():
    return render_template('text.html')
@app.route('/download',methods=['POST'])
def download():
    if request.method=='POST':
        return send_file('welcome.mp3',as_attachment=True)
@app.route('/convert',methods=['POST'])
def convert():
    if request.method=='POST':
        data=request.form.get("data")
        lan="en"
        myobj=gTTS(text=data,lang=lan,slow=False)
        myobj.save("welcome.mp3")

    return render_template('download.html')
@app.route('/speech',methods=["GET","POST"])
def speech(): 
    transcript=""
    if request.method=="POST":

        if "file" not in request.files:
            return redirect(request.url)

        file=request.files["file"]

        if file.filename=="":
            return redirect(request.url)

        if file:
            recognizer=sr.Recognizer()
            audioFile=sr.AudioFile(file)
            with audioFile as source:
                data=recognizer.record(source)
            transcript=recognizer.recognize_google(data,key=None)
            
    return render_template('speech.html',transcript=transcript)

if __name__ == "__main__":
    app.run(debug=True)
