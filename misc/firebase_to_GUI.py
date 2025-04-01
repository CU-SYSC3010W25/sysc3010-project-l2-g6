from GUI_to_firebase import clearTestMessages, writeTestMessages, readTestMessages, db
import time 


def triggerUIUpdate():
    """ Simulate a UI event by updating Firebase messages """
    test_message = {"gesture": "UI Update Test"}
    db.child("ui_events").push(test_message)  # Store new event

    print("UI update event triggered in Firebase.")

def main():
    clearTestMessages()
    writeTestMessages()
    readTestMessages()
    time.sleep(2)  # Give UI time to sync
    triggerUIUpdate()

main()
