from evolver import Evolver
import cv2

frame_w = 720
frame_h = 1280
origin_w = 200
origin_h = 400
patch = cv2.imread('/home/angelo/Development/uni/genvid-minimal/patches/circle.png')
# route = [[300, 500, "linear", 500]]
fps = 30


route = [[300, 500, "linear", 1000], 
         [400, 500, "linear", 3000]]

print(type(patch))
evolver = Evolver(frame_w, frame_h, origin_w, origin_h, patch, fps)
frames, gth = evolver.compute_evolutions(route)

print(len(frames))
print(frames[0].shape)

frameSize = frames[0].shape[1], frames[0].shape[0]
codec = cv2.VideoWriter_fourcc(*"mp4v")
video = cv2.VideoWriter("video_output.mp4", codec, fps, frameSize)

for frame in frames:
    video.write(frame.astype('uint8'))
video.release()
