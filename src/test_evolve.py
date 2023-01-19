from evolver import Evolver
from MovementType import MovementType
import cv2

frame_w = 720
frame_h = 1280
origin_w = 0
origin_h = 0
patch = cv2.imread('../patches/circle.png')
fps = 30


route = [[300, 500, MovementType.urm, 1000],
         [400, 500, MovementType.urm, 3000],
         [600, 700, MovementType.uarm, 5000],
         [800, 750, MovementType.uarm, 2000]]

# route = [[300, 500, MovementType.mru, 1000], 
#          [400, 500, MovementType.mru, 3000]]

# route = [[800, 750, MovementType.acc, 2000]]

evolver = Evolver(frame_w, frame_h, origin_w, origin_h, patch, fps)
frames, gth = evolver.compute_evolutions(route)

# print(gth)

# create video
frameSize = frames[0].shape[1], frames[0].shape[0]
codec = cv2.VideoWriter_fourcc(*"mp4v")
video = cv2.VideoWriter("video_output.mp4", codec, fps, frameSize)

for frame in frames:
    video.write(frame.astype('uint8'))
video.release()
