![Parse French ID Card](https://i.postimg.cc/T35jgMqj/download.png)
<p align="left">
  "Parse French ID Card" is an <b>open-source French Identity Card(CNI) parser</b>. You give a French ID Card picture (scan, photo...) using Tesseract OCR and OpenCV. It reads the MRZ(Machine Readable Zone) and prints a Dictionnary with the informations of the card.
  The names of the variables are in French in extract-infos.py but you have a commentary with the translation. Else, the names of the variables are in English.
  You can fork the repository to adapt the code for every country using EU ID Card.
</p>

![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/N0ct0s/Parse-French-ID-Card)
![Static Badge](https://img.shields.io/badge/language-python-blue)
![GitHub](https://img.shields.io/github/license/N0ct0s/Parse-French-ID-Card)
![GitHub repo size](https://img.shields.io/github/repo-size/N0ct0s/Parse-French-ID-Card)
![GitHub Repo stars](https://img.shields.io/github/stars/N0ct0s/Parse-French-ID-Card)
![Static Badge](https://img.shields.io/badge/requirements-tesseract_ocr_%7C_opencv_%7C_pycountry-8A2BE2)
  
# Compatibility
This repository works with a new or old **French** ID Card (Carte Nationale d'Identité or CNI).
You can provide as input the front of the old card or the back of the new card (Where you have the Machine Readable Zone/the long string beggining with "ID")

**IMPORTANT** : You can provide the front of the new card but processing will be very uncertain and may fail, as it is based solely on the full OCR of the image, and unwanted characters are often detected, disrupting processing.
**So, providing the front of the new card is not recommended.**
# License
This repository is under MIT License. If you use this repository, please notify me at <a href="mailto:noctosnovan@gmail.com">this email</a> if it's possible.
# Sources
I used some tutorials where the code is explained and commented. It would be unfair not to mention them : 
  - https://www.geeksforgeeks.org/image-registration-using-opencv-python/
  - https://pysource.com/2018/07/20/find-similarities-between-two-images-with-opencv-and-python/
