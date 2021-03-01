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

authenticator = IAMAuthenticator('1er7KcbcUw91tYVf3_MhdYVBnhBRrq3reSwN8dHdV3CJ')
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)

text_to_speech.set_service_url(
    'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/e0f75cef-dcf8-4cb9-98c3-b465561e068a')

with open('audiobook.wav', 'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize(
            text,
            voice='en-US_AllisonV3Voice',
            accept='audio/wav'
        ).get_result().content)