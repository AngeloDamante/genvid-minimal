
class BackgroundIterator:
    index: int

    def __init__(self, frames: list):
        self.frames = frames
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.frames) - 1:
            self.index = len(self.frames) - 1
        frame = self.frames[self.index].copy()
        self.index += 1
        return frame
