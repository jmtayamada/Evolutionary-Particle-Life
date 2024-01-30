import pygame
from pygame.locals import *
import time

from Particle import ParticleLife
from constants import *

# list of particle games running for the second version of this project
lifeFormList = []

def main():
    running = True
    if torch.backends.mps.is_available():
        print("running on MPS")
    elif torch.cuda.is_available():
        print("running on CUDA")
    else:
        print("running on cpu")
    timeList = []
    while running:
        start = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(black)
        
        for x in range(k_maxCreatures - len(lifeFormList)):
            lifeFormList.append(ParticleLife(64, [1, 1, 1, 1]))
        
        for particleLife in lifeFormList:
            particleLife.update()

        pygame.display.update()
        end = time.time()
        timeList.append(end-start)
        clock.tick(60)
    print("average time: " + str(sum(timeList)/len(timeList)))
    pygame.quit()
        
if __name__ == "__main__":
    main()