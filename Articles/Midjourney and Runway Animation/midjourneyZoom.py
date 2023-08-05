import os
import cv2
import matplotlib.pyplot as plt



def generate_zoom_video(image_directory, output_filename, fps, duration, zoom_start, zoom_end, zoom_steps, reverse_zoom=False):
    # Get a sorted list of image filenames
    image_filenames = os.listdir(image_directory)
    image_filenames = sorted([filename for filename in image_filenames if filename.endswith('.png')],
                             reverse=reverse_zoom)  # Reverse the order if reverse_zoom is True


    # Calculate the number of frames and frame duration
    num_frames = int(fps * duration)
    frame_duration = 1 / fps

    # Get the center coordinates of the images
    image_size = plt.imread(os.path.join(image_directory, image_filenames[0])).shape[:2]
    center_x = image_size[1] // 2
    center_y = image_size[0] // 2

    # Create the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or use 'XVID'
    video_writer = cv2.VideoWriter(output_filename, fourcc, fps, image_size[::-1])



    # Generate each frame
    for image_filename in image_filenames:
        image_path = os.path.join(image_directory, image_filename)
        image = plt.imread(image_path)

        # Set initial zoom factor
        zoom_factor = zoom_start
        zoom_step = (zoom_start - zoom_end) / zoom_steps

        if reverse_zoom:
            zoom_factor = zoom_end
            zoom_step = (zoom_end - zoom_start) / zoom_steps
        else:
            zoom_factor = zoom_start
            zoom_step = (zoom_start - zoom_end) / zoom_steps

        # Generate frames for zooming out
        for _ in range(zoom_steps):
            # Calculate the current zoom level
            current_zoom = max(zoom_factor, 1.0)

            # Calculate the zoomed image size
            zoomed_size = (int(image_size[1] / current_zoom), int(image_size[0] / current_zoom))

            # Calculate the top-left corner of the zoomed image
            x = center_x - zoomed_size[0] // 2
            y = center_y - zoomed_size[1] // 2

            # Zoom out the image
            zoomed_image = cv2.resize(image[y:y+zoomed_size[1], x:x+zoomed_size[0]], image_size[::-1])
            zoomed_image_bgr = cv2.cvtColor((zoomed_image * 255).astype('uint8'), cv2.COLOR_RGB2BGR)

            # Write the frame to the video
            video_writer.write(zoomed_image_bgr)

            # Update the zoom factor for the next frame
            zoom_factor -= zoom_step

            # Make sure the zoom factor does not go below 1.0
            zoom_factor = max(zoom_factor, zoom_end)
        
        zoomed_image = cv2.resize(image, image_size[::-1])
        zoomed_image_bgr = cv2.cvtColor((zoomed_image * 255).astype('uint8'), cv2.COLOR_RGB2BGR)
        for _ in range(num_frames - zoom_steps):
            video_writer.write(zoomed_image_bgr)

    # Release the video writer and close the video file
    video_writer.release()



# Directory containing the images
image_directory = 'rootFolder/zoom'

# Output video filename
output_filename = 'rootFolder/videos/output.mp4'

fps = 30
duration = 6
zoom_start = 2
zoom_end = 1
zoom_steps = int(duration * fps)
reverse_zoom = True  # Set this to True to reverse the zoom direction

generate_zoom_video(image_directory, output_filename, fps, duration, zoom_start, zoom_end, zoom_steps, reverse_zoom)