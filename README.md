# Parse-French-ID-Card
You give a French ID Card picture (scan, photo...). It reads the MRZ(Machine Readable Zone) and prints a Dictionnary with the informations of the card.
The names of the variables are globally in French but you have a commentary with the translation.
You can fork the repository to adapt the code for every country using EU ID Card.
# Compatibility
This repository works with a new or old **French** ID Card (Carte Nationale d'Identité or CNI).
You can provide as input the front of the old card or the back of the new card (Where you have the Machine Readable Zone/the long string beggining with "ID")

**IMPORTANT** : You can provide the front of the new card but Processing will be very uncertain and may fail, as it is based solely on the full OCR of the image, and unwanted characters are often detected, disrupting processing.
**So, providing the front of the new card is not recommended.**
# License
This repository is under MIT License. If you use this repository, please notify me at <a href="mailto:noctosnovan@gmail.com">this email</a> if it's possible.
# Sources
I used some tutorials where the code is explained and commented. It would be unfair not to mention them : 
  - https://www.geeksforgeeks.org/image-registration-using-opencv-python/
  - https://pysource.com/2018/07/20/find-similarities-between-two-images-with-opencv-and-python/
