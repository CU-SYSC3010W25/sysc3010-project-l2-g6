// please add your respective sections of code and set up instructions

# Setting up the GUI

To set up the GUI you will need to first make sure that the camera pi (streaming) runs their streaming py file. This is found in: (need to add this)
- Run the streaming python file by navigating to the directory where the file is located in your raspberry pi terminal, then running: python3 (camera_web_streamer.py) // replace with actual file name

Once we have this up and running, now we can run our firebase listener python file. This file is what allows our http server to listen and write to our firebase DB in real time. 
- Navigate to where the file Gui_listening_firebase.py is located (within src/GUI/frontend) and run: python3 Gui_listening_firebase.py

After this, we can finally run our http server. Navigate to where the interpreter and signer html files are located. (src/GUI/frontend)
- Be sure to update the IP addresses in intepreter.html line 158 to hold the IP address of the raspberry pi that is streaming its video, as well as lines 168, 183, and 193 to hold the IP address of the raspberry pi you are working on.
- Once these fixes are made all that is left to do is run: python3 -m http.server 8080
