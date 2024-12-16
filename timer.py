from pygame.time import get_ticks

class TimedEvent():
    def __init__(self, delay: int, active: bool = False):
        self.start = 0
        self.delay = delay
        self.active = active
        self.current_time = self.delay
    
    def off(self):
        self.active = False
        self.start = 0
    
    def on(self):
        self.active = True
        self.start = get_ticks()

    def update(self, expr: bool):
        if expr:
            current_time = get_ticks()

            if current_time - self.start >= self.delay:
                self.off()
        else:
            self.on()
            self.current_time = self.delay / 1000