

# Initialize pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Attack Animation")

# Load the sprite sheet
sprite_sheet = pygame.image.load("attack_sprite_sheet.png")  # Replace with your sprite sheet path

# Sprite dimensions
sprite_width = 32
sprite_height = 32

# Number of frames in the sprite sheet
num_frames = 6  # Adjust based on your attack animation

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

# Attack flag
is_attacking = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Trigger attack on spacebar press
                is_attacking = True

    # Update the current frame if attacking
    if is_attacking:
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= 1000 // animation_speed:
            current_frame = (current_frame + 1) % num_frames
            last_update = current_time

            # Reset attack flag after the animation finishes
            if current_frame == num_frames - 1:  # Last frame of the animation
                is_attacking = False
                current_frame = 0  # Reset frame index

    # Draw the current frame
    screen.fill((255, 255, 255))  # Fill the screen with white
    if is_attacking:
        screen.blit(frames[current_frame], (100, 100))  # Draw the attack frame

    pygame.display.flip()

# Quit pygame
pygame.quit()
