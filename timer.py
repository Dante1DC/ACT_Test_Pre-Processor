import time

class IterationTimer:
    def __init__(self):
        self.start_time = None
    
    def start(self, message="Time for the last iteration:"):
        if self.start_time is not None:
            iteration_time = time.time() - self.start_time
            print(f"{message}: {iteration_time:.4f} seconds")

        self.start_time = time.time()
