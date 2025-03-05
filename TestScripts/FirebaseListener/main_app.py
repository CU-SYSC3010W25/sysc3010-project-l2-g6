from multiprocessing import Process, Value
import time

def main_app(shared_state):
    """Reads the shared state and acts on it."""
    while True:
        current_state = shared_state.value
        print(f"🔄 Main App: Current Stream Enabled State = {current_state}")

        if current_state == 1:
            print("✅ Main App: Starting RTSP Stream...")
            # Start streaming logic here
        else:
            print("⛔ Main App: Stopping RTSP Stream...")
            # Stop streaming logic here

        time.sleep(5)  # Simulate ongoing task

if __name__ == "__main__":
    # Create a shared variable to store the state
    shared_state = Value('i', 0)  # 'i' for integer, initial value 0

    # Start the main app in a separate process
    app_process = Process(target=main_app, args=(shared_state,))
    app_process.start()

    # Keep the main app process running
    app_process.join()
