import cv2
import sys
from background_swapper import INPUT_IMG_DIR, OUTPUT_IMG_DIR, swap_image_background


def main():
  input_video_name, background_img_name = get_files_names_from_arguments()
  input_video, background_img = read_required_files(input_video_name, background_img_name)
  swap_video_background_and_save_output_video(input_video, background_img, input_video_name)

def get_files_names_from_arguments():
  arguments = sys.argv[1:]

  if len(arguments) != 2:
    raise ValueError('Incorrect number of arguments.')

  input_video_name = arguments[0]
  background_img_name = arguments[1]

  return input_video_name,  background_img_name

def read_required_files(input_video_name, background_img_name):  
  input_video = cv2.VideoCapture(INPUT_IMG_DIR + input_video_name)
  background_img = cv2.imread(INPUT_IMG_DIR + background_img_name)

  if input_video is None or input_video.isOpened() == False:
    raise ValueError('Error when opening the video file.')
  if background_img is None:
    raise ValueError('Background image file not found.')

  return input_video, background_img


def swap_video_background_and_save_output_video(input_video, background_img, output_video_name):
  frame_width = int(input_video.get(3))
  frame_height = int(input_video.get(4))
  frame_rate = int(input_video.get(cv2.CAP_PROP_FPS))
  
  output_video = cv2.VideoWriter(
    OUTPUT_IMG_DIR + output_video_name,
    cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
    frame_rate,
    (frame_width,frame_height)
  )

  while(input_video.isOpened()):
    ret, img = input_video.read()

    if not ret:
      break

    result_img = swap_image_background(img, background_img)
    output_video.write(result_img)

  input_video.release()
  output_video.release()  


if __name__ == '__main__':
  main()
