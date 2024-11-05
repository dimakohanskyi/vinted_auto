from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np
import cv2

# Get the image name from the user
image_name = input("Enter the image file name (including extension): ")
image_path = f"./{image_name}"

# Load the image
try:
    image = Image.open(image_path)
except FileNotFoundError:
    print(f"Error: The file '{image_name}' was not found.")
    exit()
except OSError:
    print(f"Error: Could not open the file '{image_name}'. Please check the file format and name.")
    exit()

# Display the original image
plt.figure(figsize=(6, 6))
plt.imshow(image)
plt.title("Original Image")
plt.axis("off")
plt.show()

# Define the cropping values
crop_top = 62
crop_left = 28

# Perform the cropping
width, height = image.size
cropped_image = image.crop((crop_left, crop_top, width, height))

# Adjust Brightness, Contrast, and Gamma
# Brightness: +1, Contrast: -1, Gamma: 1.00
enhancer_brightness = ImageEnhance.Brightness(cropped_image)
cropped_image = enhancer_brightness.enhance(1.1)  # Brightness slightly increased to better match XnView results
enhancer_contrast = ImageEnhance.Contrast(cropped_image)
cropped_image = enhancer_contrast.enhance(0.8)  # Contrast adjustment to better match XnView results

# Convert image to numpy array for gamma correction
image_np = np.array(cropped_image)

# Apply gamma correction
gamma = 1.0
inv_gamma = 1.0 / gamma
gamma_table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
image_np = cv2.LUT(image_np, gamma_table)

# Adjust levels for Red, Green, Blue channels
if len(image_np.shape) == 3:  # Ensure image has color channels
    # Use more precise level adjustments to match XnView results
    image_np[:, :, 0] = cv2.normalize(image_np[:, :, 0], None, 0, 253, cv2.NORM_MINMAX)  # Blue channel
    image_np[:, :, 1] = cv2.normalize(image_np[:, :, 1], None, 0, 253, cv2.NORM_MINMAX)  # Green channel
    image_np[:, :, 2] = cv2.normalize(image_np[:, :, 2], None, 0, 252, cv2.NORM_MINMAX)  # Red channel (slightly adjusted)

# Convert numpy array back to Image
cropped_image = Image.fromarray(image_np)

# Display the adjusted image
plt.figure(figsize=(6, 6))
plt.imshow(cropped_image)
plt.title("Cropped and Adjusted Image")
plt.axis("off")
plt.show()

# Save the adjusted image to the output file
output_path = "./cropped_image.png"
cropped_image.save(output_path)
