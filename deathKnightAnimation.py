import pygame as pg
import sys
from settings import *
from sprites import *
# Load death animation frames (replace with your image paths)
death_frames = [
    pygame.image.load("Knight.png"),
    pygame.image.load("knightDeath1.png"),
    pygame.image.load("deathSkull.png"),
    # ... add more frames as needed
]

# Set animation speed
animation_speed = 10 
current_frame = 0 

# Function to play a death animation
def play_death_animation(player_rect):
    global current_frame 
    
    # Loop through animation frames
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Update current frame
    current_frame = (current_frame + 1) % len(death_frames) 
    
    # Draw the current frame
    screen.blit(death_frames[current_frame], player_rect) 
    pygame.display.flip() 

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Trigger death animation when needed (replace with your game logic) 
    if player_hit: 
        play_death_animation(player_rect) 

pygame.quit() 



