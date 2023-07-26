import os
import cv2
import numpy as np
import argparse


def enhance_image(image, brightness, contrast, sharpness, saturation, noise_reduction):
    enhanced_image = cv2.convertScaleAbs(image, alpha=brightness, beta=0)
    enhanced_image = cv2.addWeighted(enhanced_image, contrast, np.zeros_like(enhanced_image), 0, 0)

    # Perform sharpening using Laplacian operator
    laplacian = cv2.Laplacian(enhanced_image, cv2.CV_64F)
    sharpened_image = cv2.convertScaleAbs(enhanced_image - sharpness * laplacian)

    # Convert image to HSV color space and modify saturation
    hsv = cv2.cvtColor(sharpened_image, cv2.COLOR_BGR2HSV)
    hsv[..., 1] = saturation * hsv[..., 1]
    enhanced_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Apply noise reduction using bilateral filter
    enhanced_image = cv2.bilateralFilter(enhanced_image, 9, noise_reduction, noise_reduction)

    return enhanced_image


def process_image(image_path, brightness, contrast, sharpness, saturation, noise_reduction):
    image = cv2.imread(image_path)

    # Enhance the image
    enhanced_image = enhance_image(image, brightness, contrast, sharpness, saturation, noise_reduction)

    # Display before-after comparison
    cv2.imshow("Original Image", image)
    cv2.imshow("Enhanced Image", enhanced_image)
    cv2.waitKey(0)


def batch_process_images(directory, brightness, contrast, sharpness, saturation, noise_reduction):
    # Get a list of image files in the directory
    image_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.lower().endswith(('.jpg', '.jpeg', '.png'))]
    for image_file in image_files:
        process_image(image_file, brightness, contrast, sharpness, saturation, noise_reduction)


def main():
    # Initialize argparse
    parser = argparse.ArgumentParser(description='AI Image Enhancer')

    # Add command-line arguments
    parser.add_argument('directory', type=str, help='Directory containing the images')
    parser.add_argument('--brightness', type=float, default=1.0, help='Brightness value (default: 1.0)')
    parser.add_argument('--contrast', type=float, default=1.0, help='Contrast value (default: 1.0)')
    parser.add_argument('--sharpness', type=float, default=0.5, help='Sharpness value (default: 0.5)')
    parser.add_argument('--saturation', type=float, default=1.0, help='Saturation value (default: 1.0)')
    parser.add_argument('--noise_reduction', type=float, default=10.0, help='Noise reduction value (default: 10.0)')

    # Parse command-line arguments
    args = parser.parse_args()

    # Check if the input directory exists
    if not os.path.exists(args.directory):
        print("Invalid directory path.")
        return

    # Process single image or batch process images
    if os.path.isfile(args.directory):
        # Process single image
        process_image(args.directory, args.brightness, args.contrast, args.sharpness, args.saturation,
                      args.noise_reduction)
    elif os.path.isdir(args.directory):
        # Batch process images
        batch_process_images(args.directory, args.brightness, args.contrast, args.sharpness, args.saturation,
                             args.noise_reduction)
    else:
        print("Invalid directory or file path.")
        return


if __name__ == '__main__':
    main()