import cv2

def get_last_frame(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Set the video pointer to the last frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 1)

    # Read the last frame
    ret, last_frame = cap.read()

    # Release the video capture object
    cap.release()

    # If reading the frame was successful, return the last frame
    if ret:
        return last_frame
    else:
        return None

def save_last_frame(video_path, output_path):
    last_frame = get_last_frame(video_path)
    if last_frame is not None:
        # Save the last frame to the specified output path
        cv2.imwrite(output_path, last_frame)
        print("Last frame saved successfully at:", output_path)
    else:
        print("Error: Unable to read the last frame of the video.")
        
# Replace 'path_to_video.mp4' with the actual path to your video file
video_path = 'sculptures/videos/pink_ring_gen2.mp4'

# Replace 'output_last_frame.png' with the desired output filename and extension
output_path = 'sculptures/images/pink_ring_gen2_last_frame.png'

save_last_frame(video_path, output_path)
