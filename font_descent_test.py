import pygame
import asyncio

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((640, 480))

# Load a font
font = pygame.font.Font("font.otf", 10)

# Get the descent of the font
descent = font.get_descent()
print(f"Font descent: {descent}")

# Main loop
async def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        text = font.render(f"Hello, Pygbag! & I like {font.get_descent()}/{font.get_height()}/24", True, (0, 0, 0))
        screen.blit(text, (100, 100))

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
