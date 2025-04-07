# SYSC 3010 - interprePi - Setting up the System
![alt text](https://github.com/CU-SYSC3010W25/sysc3010-project-l2-g6/blob/main/misc/logo.jpg "Logo Title Text 1")

**Project Members:**
- Alec Tratnik
- Andrew Rivera
- Divya Dushyanthan
- Kyle Mathias
- Vaanathy Thaneskumar

**TA: Afsoon Khodaee**
InterprePi is a modular, real-time sign language interpretation system built on Raspberry Pi hardware to facilitate seamless communication between Deaf and Hard-of-Hearing (DHH) individuals and non-signers. By leveraging edge computing, computer vision, and machine learning, InterprePi captures and interprets sign language gestures locally, converting them into text and optionally speech. Conversely, spoken or typed responses from non-signers are transcribed and displayed for DHH users, enabling fully bidirectional interaction.

The system is composed of independently functioning Raspberry Pi nodes, each responsible for a specific task such as video capture, gesture recognition, speech processing, and GUI display. Inter-node communication is managed through lightweight HTTP and WebSocket protocols, with Firebase used only for synchronizing application state. This hybrid local-cloud approach ensures low-latency performance while maintaining user privacy.

Designed for flexibility and scalability, InterprePi can be deployed across multiple devices or locations, making it ideal for use in classrooms, hospitals, workplaces, and other accessibility-critical environments. It offers an inclusive, privacy-conscious, and cost-effective alternative to traditional interpretation services.

# Repo Structure of Relevant Folders:
  - Folder Descriptions:
      - src
      - EndtoEndDemo
      - UnitTestDemo
      - config
      - WeeklyUpdates
    
  - Setup Descriptions

# Folders
## src folder:
The src folder contains all source code. It is divided into sub folders: GUI, camera, output, pi3, and processorFull. 
- **GUI:** This folder contains the GUI to firebase listener file, both the interpreter and signer html files, our local database to hold the chat log (conversation.db), and a folder containing the interprePi icons for when we navigate to the site on our browser.

- **camera:** This directory contains the camera and servo implementations alongside the firebase listener file, config file and addip shell script. The servo implementation is wihtin the Camera.py file to ensure that both devices can work asynchronously and prevent GPIO conflicts. The Listener.py file is used to listen to changes on the database such as servo direction and stream state.

- **pi3:** This directory contains the code for the text to speech and speech to text. This is found in the audio.py file.

- **output:** This directory contains the code to initialize the output devices. The code is found in the _init_.py file.

## EndToEndDemo folder:
This folder contains all of our listener and writing files for our end to end demo. We have a listener and writer file for each pi that is connected to the firebase. 

## UnitTestsDemo folder:
This folder contains all the files we used for our unit test demo. This folder is divided into sub folders as well: GUI, camera, ethernet_connection, pi3, processor, and servo. 
- **GUI:** This folder contains a test file to check that the speaker and microphone buttons on the GUI update the firebase accordingly, another test file to ensure that the GUI is grabbing the current gesture and displaying it on the GUI, a test file to validate the stream is being displayed on our GUI, and a test to validate that our web server is up and running.

- **camera:** This directory contains the test file for the camera component, test_camera.py. It verifies the cameras connection with the Raspberry Pi and runs a script to preview the camera's input for 5 seconds to visually see it working.

- **ethernet_connection:** This directory contains the test file for the connection between the camera and proccesor node, test_ethernet.py and test_receive_ethernet.py. It verifies the physical connection between the two nodes by checking if the correct ips are added to each device and checks to see if it able to send and receive (ping) data between thetwo nodes.

- **servo:** This directory contains the test file for the servo, test_servo.py. It tests the functionality of the hardware devices by checking the max, min, and out of range angle values. As well as testing for the correct GPIO connection, max and min duty cycles.

- **pi3:** This directory contains the test files for the text to speech and speech to text functionalities, as well as the LED display. pi3_audio_test.py tests the microphone and speaker output devices, and pi3_led_test.py tests the LED display of what is being said into the microphone. 

## config folder:
This folder contains the access key JSON file for our firebase DB.

## WeeklyUpdates folder:
This folder contains all of our WIPURs. This folder is divided into subfolders containing our team's WIPUR from every week.

# Setup Instructions:

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

## Setting up the Camera and Servo

To set up the camera and servo components:
1. Start by runnning the run_camera.py script inside sysc3010-project-l2-g6/src folder (python3 run_camera.py). From here, the servo is ready to go, however for the camera requires further set up.
2. To start streaming the video, it has to be manually turned on within the database to prevent unwanted to changes to it. From the database, navitage to settings -> 0 -> Stream and toggle it from false to true (or true to false then to true again if it was initially at true). After that the camera is ready to go, and is sending its video input to the processor node.
   
    - In the rare case that it is not streaming after these steps, the issue is most likely due to the ip configuration. In that case, open the linux terminal and navigate to sysc3010-project-l2-g6/src/camera and run the command "sh addip.sh". Verify that the ip is added by running the command "hostname -I".
  
## Running the servo, camera and ethernet Unit Tests

To run these unit steps:
1. Navigate to the sysc3010-project-l2-g6/UnitTestsDemo. You will see all the folders each resprective test cases for the servo, camera and ethernet.
2. Run each test file separately (python3 run_camera.py). Ensure that you are in the correct directory when running the test files. 
Running all these tests should all pass. 

  
