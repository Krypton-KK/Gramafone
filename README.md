# Gramafone
my school project which focused on using csv, txt, yaml, sql and python to create a end to end encrypted chat client using sockets.

My school project (Gramafone) uses csv files to store data and keys on a physical drive and store the codes of these on a (home) sql server over the internet using sockets.
it took me about 4 months to start and end this project. with 1000s of lines of code i was able to implement:
- store and retrive data
- use encryption using cryptography module.
- add excess manual encyption by shifting ascii values of the keys themselves and decrypting the keys.
- transfer files in an encrypted manner by using read() and write() functions
- use sockets to transport the data
- finally used custom tkinter to create a ui to display it.

Fails:
- tried to open and close ports using python code and making the code work even when it is used with others on the internet in other local networks and using public ip addresses.
- tried to send and receive mail (because we cannot use pop3 with mail anymore as it is considered unsafe)
- tried to use "sent" and "recived" reciepts but it happened to be too intensive and almost lost my mind coding it with a deadline of 1 day
- make immages to appear in the way whatsapp and telegram display them but this ended up consuming almost a week without fruition
  
I would like to improve this code and later publish it as an app.
