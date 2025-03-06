################################################################################
# Read a raw image and find the bounding box with GPT provided solution.
################################################################################

import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_image(image_path):
    """Loads an image from a file path."""
    return cv2.imread(image_path)

def preprocess_image(image):
    """Converts the image to grayscale and applies thresholding."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)  # Adjust threshold if needed
    return thresh

def find_contours(thresh):
    """Finds contours from the thresholded image."""
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def merge_overlapping_boxes(contours, threshold=10):
    """Merges overlapping bounding boxes to prevent redundancy."""
    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    merged_boxes = []
    for x, y, w, h in bounding_boxes:
        merged = False
        for i, (mx, my, mw, mh) in enumerate(merged_boxes):
            # Check if boxes overlap or are within the threshold distance
            if not (x > mx + mw + threshold or mx > x + w + threshold or
                    y > my + mh + threshold or my > y + h + threshold):
                # Merge boxes by expanding boundaries
                new_x = min(x, mx)
                new_y = min(y, my)
                new_w = max(x + w, mx + mw) - new_x
                new_h = max(y + h, my + mh) - new_y
                merged_boxes[i] = (new_x, new_y, new_w, new_h)
                merged = True
                break
        if not merged:
            merged_boxes.append((x, y, w, h))
    return merged_boxes
    # return bounding_boxes

def draw_bounding_boxes(image, bounding_boxes):
    """Draws bounding boxes on the image."""
    image_with_boxes = image.copy()
    for x, y, w, h in bounding_boxes:
        cv2.rectangle(image_with_boxes, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red bounding boxes
    return image_with_boxes

def display_image(image, title="Image"):
    """Displays an image using matplotlib."""
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(8, 6))
    plt.imshow(image_rgb)
    plt.axis("off")
    plt.title(title)
    plt.tight_layout()
    plt.savefig('figs/gpt_box_2d.png')

if __name__ == "__main__":
    # Provide the path to your image
    image_path = "figs/raw_tf_2d.png"  # Update with the actual path
    # Load and process the image
    image = load_image(image_path)
    thresh = preprocess_image(image)
    contours = find_contours(thresh)
    merged_bounding_boxes = merge_overlapping_boxes(contours, threshold=15)
    # Draw and display the final bounding boxes
    image_with_boxes = draw_bounding_boxes(image, merged_bounding_boxes)
    display_image(image_with_boxes, title="Detected Blocks with Merged Bounding Boxes")
