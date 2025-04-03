# interprePi - Setting up the System
// please add your respective sections of code and set up instructions

## Within the src folder:
The src folder contains all source code. It is divided into sub folders: GUI, camera, output, pi3, and processorFull. 
- GUI: This folder contains the GUI to firebase listener file, both the interpreter and signer html files, our local database to hold the chat log (conversation.db), and a folder containing the interprePi icons for when we navigate to the site on our browser.

## Within the EndToEndDemo folder:
This folder contains all of our listener and writing files for our end to end demo. We have a listener and writer file for each pi that is connected to the firebase. 

## Within the UnitTestsDemo folder:
This folder contains all the files we used for our unit test demo. This folder is divided into sub folders as well: GUI, camera, ethernet_connection, pi3, processor, and servo. 
- GUI: this folder contains a test file to check that the speaker and microphone buttons on the GUI update the firebase accordingly, another test file to ensure that the GUI is grabbing the current gesture and displaying it on the GUI, a test file to validate the stream is being displayed on our GUI, and a test to validate that our web server is up and running.

## Within the config folder:
This folder contains the access key JSON file for our firebase DB.

## Within the WeeklyUpdates folder:
This folder contains all of our WIPURs. This folder is divided into subfolders containing our team's WIPUR from every week.

## Setting up the GUI

To set up the GUI, we need to start by running our firebase listener python file. This file is what allows our http server to listen and write to our firebase DB in real time and updates the web server accordingly. 
- Navigate to where the file Gui_listening_firebase.py is located (within src/GUI/frontend) and run: python3 Gui_listening_firebase.py

After this, we can run our http server. Navigate to where the interpreter and signer html files are located. (src/GUI/frontend)
- Be sure to update the IP addresses in intepreter.html line 158 to hold the IP address of the raspberry pi that is streaming its video, as well as lines 168, 183, and 193 to hold the IP address of the raspberry pi you are working on.
- Once these fixes are made all that is left to do is run: python3 -m http.server 8080

## Running GUI Unit Tests

To run the GUI unit tests the files are all located in the UnitTestsDemo/GUI folder. After navigating to this folder in your raspberry pi terminal you can run any of the tests using this command:
python3 (test_file_name_).py
- ex: python3 audio_mic_test.py

  
