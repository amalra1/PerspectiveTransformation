import cv2
import numpy as np
import sys
import os

CLICKED_POINTS = []
INSTRUCTION_HEIGHT = 50

def handle_mouse_click(event, x, y, flags, param):
    global CLICKED_POINTS, image_with_overlay
    if event == cv2.EVENT_LBUTTONDOWN and len(CLICKED_POINTS) < 4:
        corrected_y = y - INSTRUCTION_HEIGHT
        if corrected_y < 0:
            print("Click below the instruction bar.")
            return
        CLICKED_POINTS.append((x, corrected_y))
        print(f"Point {len(CLICKED_POINTS)}: ({x}, {corrected_y})")
        cv2.circle(image_with_overlay, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Select 4 corners", image_with_overlay)

def sort_points_clockwise(points):
    pts = np.array(points, dtype="float32")
    center = np.mean(pts, axis=0)

    def angle_from_center(p):
        return np.arctan2(p[1] - center[1], p[0] - center[0])

    sorted_pts = sorted(pts, key=angle_from_center)
    sorted_pts = np.array(sorted_pts)

    sum_pts = sorted_pts.sum(axis=1)
    diff_pts = np.diff(sorted_pts, axis=1)

    top_left = sorted_pts[np.argmin(sum_pts)]
    bottom_right = sorted_pts[np.argmax(sum_pts)]
    top_right = sorted_pts[np.argmin(diff_pts)]
    bottom_left = sorted_pts[np.argmax(diff_pts)]

    return np.array([top_left, top_right, bottom_right, bottom_left], dtype="float32")

def apply_perspective(image, source_points, output_size=(640, 480)):
    width, height = output_size
    destination_points = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype="float32")

    transform_matrix = cv2.getPerspectiveTransform(source_points, destination_points)
    return cv2.warpPerspective(image, transform_matrix, (width, height))

def add_title(image, title_text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    thickness = 2
    title_height = 40

    width = image.shape[1]
    title_bar = np.ones((title_height, width, 3), dtype=np.uint8) * 255
    text_size = cv2.getTextSize(title_text, font, font_scale, thickness)[0]
    x = (width - text_size[0]) // 2
    y = (title_height + text_size[1]) // 2
    cv2.putText(title_bar, title_text, (x, y), font, font_scale, (0, 0, 0), thickness)

    return np.vstack((title_bar, image))

def create_comparison_image(original, transformed):
    target_height = 500
    resized_original = cv2.resize(original, (int(original.shape[1] * target_height / original.shape[0]), target_height))
    resized_transformed = cv2.resize(transformed, (int(transformed.shape[1] * target_height / transformed.shape[0]), target_height))

    original_labeled = add_title(resized_original, "Original")
    transformed_labeled = add_title(resized_transformed, "Transformed")

    return np.hstack((original_labeled, transformed_labeled))

def show_instruction_overlay(image, instruction_text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    width = image.shape[1]

    overlay = np.ones((INSTRUCTION_HEIGHT, width, 3), dtype=np.uint8) * 255
    text_size = cv2.getTextSize(instruction_text, font, 0.7, 2)[0]
    x = (width - text_size[0]) // 2
    y = (INSTRUCTION_HEIGHT + text_size[1]) // 2
    cv2.putText(overlay, instruction_text, (x, y), font, 0.7, (0, 0, 0), 2)

    return np.vstack((overlay, image))

def main(image_path):
    global image_with_overlay, CLICKED_POINTS

    if not os.path.exists(image_path):
        print(f"Error: File '{image_path}' not found.")
        return

    image_original = cv2.imread(image_path)
    image_with_overlay = show_instruction_overlay(image_original.copy(), "Click the 4 screen corners. Press any key when done.")

    cv2.namedWindow("Select 4 corners", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Select 4 corners", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Select 4 corners", image_with_overlay)
    cv2.setMouseCallback("Select 4 corners", handle_mouse_click)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if len(CLICKED_POINTS) != 4:
        print("You must click exactly 4 points.")
        return

    ordered_points = sort_points_clockwise(CLICKED_POINTS)
    transformed = apply_perspective(image_original, ordered_points)
    comparison = create_comparison_image(image_original, transformed)

    output_filename = "comparison.jpg"
    cv2.imwrite(output_filename, comparison)
    print(f"Comparison image saved as: {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 perspective_transform.py <image_path>")
    else:
        main(sys.argv[1])
