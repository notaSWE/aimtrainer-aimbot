from settings import *
import cv2, io, pygame
import numpy as np

class Aimbot():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.target_identified = False
        self.contours = None
        self.detectedX, self.detectedY = None, None

    def detect_target(self):
        screen_copy = pygame.surfarray.array3d(self.display_surface)
        screen_copy = cv2.cvtColor(screen_copy, cv2.COLOR_BGR2RGB)
        screen_copy = np.rot90(screen_copy)
        screen_copy = np.flipud(screen_copy)
        screen_copy = np.fliplr(screen_copy)

        _, buffer = cv2.imencode('.jpg', screen_copy)
        file_bytes = io.BytesIO(buffer)
        find_target = cv2.imdecode(np.frombuffer(file_bytes.getvalue(), np.uint8), cv2.IMREAD_COLOR)

        hsv_image = cv2.cvtColor(find_target, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv_image, lower_red, upper_red)
        self.contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in self.contours:
            # Get the rectangle bounding contour
            [x, y, w, h] = cv2.boundingRect(cnt)
            aspect_ratio = float(w) / h
            area = cv2.contourArea(cnt)
            if (aspect_ratio >= 0.9) and (aspect_ratio <= 1.1) and (area > 100):
                # Draw the rectangle on the original image
                cv2_rect = cv2.rectangle(find_target, (x, y), (x + w, y + h), (0, 255, 0), 2)
                detection_surface = pygame.image.load(DETECTION_IMAGE)
                detection_rect = detection_surface.get_rect(topleft=(1860 - x - 10, y - 10))
                self.detectedX, self.detectedY = (detection_rect.centerx, detection_rect.centery)
        self.target_identified = True

    def draw_outline(self, x, y):
        if x != None and y != None:
            detection_surface = pygame.image.load(DETECTION_IMAGE)
            detection_rect = detection_surface.get_rect(topleft=(x - 40, y - 40))
            self.display_surface.blit(detection_surface, detection_rect)
        if pygame.mouse.get_pressed()[0]:
            # Jump mouse to detected target
            pygame.mouse.set_pos(x, y)

    def reset_detection(self):
        self.target_identified = False
        self.contours = None
        self.detectedX, self.detectedY = None, None

    # "Read" display every tick and identify/highlight target.
    def update(self):
        if not self.target_identified:
            self.detect_target()
        elif self.target_identified and self.contours:
            self.draw_outline(self.detectedX, self.detectedY)