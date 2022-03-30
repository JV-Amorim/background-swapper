import cv2
import numpy as np
import sys


INPUT_IMG_DIR = 'input/'
OUTPUT_IMG_DIR = 'output/'
LOWER_MASK_BOUNDARY = np.array([40, 100, 20])
UPPER_MASK_BOUNDARY = np.array([75, 256, 256])


def main():
  input_img_name, background_img_name = get_files_names_from_arguments()
  input_img, background_img = read_required_images(input_img_name, background_img_name)

  result_img = swap_image_background(input_img, background_img)

  save_result_image_with_same_name_of_input_image(result_img, input_img_name)
  print('Success! The result image have been saved in output directory.')


def get_files_names_from_arguments():
  arguments = sys.argv[1:]

  if len(arguments) != 2:
    raise ValueError('Incorrect number of arguments.')

  input_img_name = arguments[0]
  background_img_name = arguments[1]

  return input_img_name,  background_img_name

def read_required_images(input_img_name, background_img_name):  
  input_img = cv2.imread(INPUT_IMG_DIR + input_img_name)
  background_img = cv2.imread(INPUT_IMG_DIR + background_img_name)

  if input_img is None:
    raise ValueError('Input image file not found.')
  if background_img is None:
    raise ValueError('Background image file not found.')

  return input_img, background_img


def swap_image_background(input_img, background_img):
  background_img = resize_background_image_to_same_size_of_input_image(background_img, input_img)

  hsv_input_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2HSV)
  hsv_background_img = cv2.cvtColor(background_img, cv2.COLOR_BGR2HSV)

  mask, inverted_mask = generate_masks_from_input_image(hsv_input_img)

  masked_hsv_input_img = apply_mask_to_input_image(inverted_mask, hsv_input_img)
  masked_hsv_background_img = apply_mask_to_background_image(mask, hsv_background_img)

  result_img = generate_result_image(masked_hsv_input_img, masked_hsv_background_img)

  return cv2.cvtColor(result_img, cv2.COLOR_HSV2BGR)


def resize_background_image_to_same_size_of_input_image(background_img, input_img):
  input_img_height = input_img.shape[0]
  input_img_width = input_img.shape[1]
  background_img_height = background_img.shape[0]

  aspect_ratio = input_img_height / background_img_height
  new_background_height = int(background_img_height * aspect_ratio)
  new_background_size = (input_img_width, new_background_height)

  return cv2.resize(background_img, new_background_size, interpolation=cv2.INTER_AREA)


def generate_masks_from_input_image(hsv_input_img):
  mask = cv2.inRange(hsv_input_img, LOWER_MASK_BOUNDARY, UPPER_MASK_BOUNDARY)
  inverted_mask = cv2.bitwise_not(mask)
  return mask, inverted_mask

def apply_mask_to_input_image(inverted_mask, hsv_input_img):
  return cv2.bitwise_and(hsv_input_img, hsv_input_img, mask=inverted_mask)

def apply_mask_to_background_image(mask, hsv_background_img):
  return cv2.bitwise_and(hsv_background_img, hsv_background_img, mask=mask)


def generate_result_image(masked_hsv_input_img, masked_hsv_background_img):
  return cv2.add(masked_hsv_input_img, masked_hsv_background_img)

def save_result_image_with_same_name_of_input_image(result_img, input_img_name):
  cv2.imwrite(OUTPUT_IMG_DIR + input_img_name, result_img)


if __name__ == '__main__':
  main()
