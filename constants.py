import torch
import pygame

# variable for use in second version of this project
k_maxCreatures = 1

# define colors
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)
black = (0, 0, 0)
grey = (122, 122, 122)

# init pygame
pygame.init()
width = 700
height = 500
screen = pygame.display.set_mode((width + 1, height + 1))
pygame.display.set_caption("Particle Life")
screen.fill(black)

clock = pygame.time.Clock()

# set up device
device = torch.device("cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu")