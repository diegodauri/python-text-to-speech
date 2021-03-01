import tkinter as tk
from tkinter import filedialog
import PyPDF2
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

text = []

pdfFileObj = open(file_path, 'rb')

pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

pages = pdfReader.numPages

for page in range(pages):
    pageObj = pdfReader.getPage(page)

    text.append(pageObj.extractText())

# closing the pdf file object
pdfFileObj.close()

text = "".join(text)

authenticator = IAMAuthenticator('')
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)

text_to_speech.set_service_url('')

with open('audiobook.wav', 'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize(
            text,
            voice='en-US_AllisonV3Voice',
            accept='audio/wav'
        ).get_result().content)
