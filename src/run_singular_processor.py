import time
from processorFull.Processor import Processor

def main():
    processor = Processor(True)
    
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()

