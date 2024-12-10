import pygame as pg
import sys
from settings import *
from sprites import *
# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Idle Animation")

# Load the sprite sheet
sprite_sheet = pygame.image.load("sprite_sheet.png")  # Replace with your sprite sheet path

# Sprite dimensions
sprite_width = 32
sprite_height = 32

# Number of frames in the sprite sheet
num_frames = 4

# Create a list to store the individual frames
frames = []
for i in range(num_frames):
    frame = sprite_sheet.subsurface(i * sprite_width, 0, sprite_width, sprite_height)
    frames.append(frame)

# Current frame index
current_frame = 0

# Animation speed (frames per second)
animation_speed = 10
last_update = pygame.time.get_ticks()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the current frame
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= 1000 // animation_speed:
        current_frame = (current_frame + 1) % num_frames
        last_update = current_time

    # Draw the current frame
    screen.fill((255, 255, 255))  # Fill the screen with white
    screen.blit(frames[current_frame], (100, 100))  # Draw the sprite

    pygame.display.flip()

# Quit pygame
pygame.quit()