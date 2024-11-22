import pygame
import os

# Initialize Pygame
pygame.init()

# Set up the window
window = pygame.display.set_mode((1200, 400))
pygame.display.set_caption("Self-Driving Car Simulation")

# Load assets with proper error handling
try:
    # Change the working directory to ensure correct file paths
    os.chdir("C:/Users/Ram/Desktop/projects/tesla")
    track = pygame.image.load("track.png")
    car = pygame.image.load("tesla.png")
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Ensure 'track.png' and 'tesla.png' are in the specified directory.")
    pygame.quit()
    exit()

# Scale the car image
car = pygame.transform.scale(car, (30, 60))

# Car and Camera Parameters
car_x = 155
car_y = 300
focal_dis = 25
cam_x_offset = 0
cam_y_offset = 0
direction = "up"

# Main Loop Parameters
drive = True
clock = pygame.time.Clock()

# Main Loop
while drive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            drive = False

    clock.tick(60)

    # Camera position
    cam_x = car_x + cam_x_offset + 15
    cam_y = car_y + cam_y_offset + 15

    # Get pixel colors at the camera's focal points
    try:
        up_px = window.get_at((cam_x, cam_y - focal_dis))[0]
        down_px = window.get_at((cam_x, cam_y + focal_dis))[0]
        right_px = window.get_at((cam_x + focal_dis, cam_y))[0]
    except IndexError:
        print("Camera position out of bounds! Ensure the car stays on track.")
        break

    # Debugging pixel values
    print(up_px, right_px, down_px)

    # Change direction (take turns)
    if direction == "up" and up_px != 255 and right_px == 255:
        direction = "right"
        cam_x_offset = 30
        car = pygame.transform.rotate(car, -90)
    elif direction == "right" and right_px != 255 and down_px == 255:
        direction = "down"
        car_x += 30
        cam_x_offset = 0
        cam_y_offset = 30
        car = pygame.transform.rotate(car, -90)
    elif direction == "down" and down_px != 255 and right_px == 255:
        direction = "right"
        car_y += 30
        cam_x_offset = 30
        cam_y_offset = 0
        car = pygame.transform.rotate(car, 90)
    elif direction == "right" and right_px != 255 and up_px == 255:
        direction = "up"
        car_x += 30
        cam_x_offset = 0
        car = pygame.transform.rotate(car, 90)

    # Drive in the current direction
    if direction == "up" and up_px == 255:
        car_y -= 2
    elif direction == "right" and right_px == 255:
        car_x += 2
    elif direction == "down" and down_px == 255:
        car_y += 2

    # Render the track, car, and camera point
    window.blit(track, (0, 0))
    window.blit(car, (car_x, car_y))
    pygame.draw.circle(window, (0, 255, 0), (cam_x, cam_y), 5, 5)
    pygame.display.update()

# Quit Pygame
pygame.quit()
