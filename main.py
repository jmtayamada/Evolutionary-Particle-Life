import pygame
from pygame.locals import *
import time
from torch import tensor, Tensor

from Particle import ParticleLife
from constants import *

def delete_values(tensor: Tensor, indices: []) -> Tensor:
    mask = torch.ones(tensor.numel(), dtype=torch.bool)
    mask[indices] = False
    return tensor.clone()[mask]

def main():
    running = True
    
    # list of particle games running
    lifeFormList: list[ParticleLife] = []
    
    # print what device the program is being run on
    if torch.backends.mps.is_available():
        print("running on MPS")
    elif torch.cuda.is_available():
        print("running on CUDA")
    else:
        print("running on cpu")
    
    # for measuring performance
    timeList = []
    
    # get total amount of particles
    totalParticles = k_maxCreatures*k_particlesPerCreature
    
    # initialize particles
    for x in range(k_maxCreatures - len(lifeFormList)):
        lifeFormList.append(ParticleLife(64, totalParticles/2))
        
    # main loop
    while running:
        start = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(black)
        
        # create new particleLifes if particleLifes have died
        for x in range(k_maxCreatures - len(lifeFormList)):
            lifeFormList.append(ParticleLife(k_particlesPerCreature, [1, 1, 1, 1], totalParticles/2))
                            
        for particleLife in lifeFormList:
            # create a tensor that stores other particle's positions
            tensorList = [tensor([], dtype=int, device=device) for x in range(8)]
            for obj in lifeFormList:
                if obj != particleLife:
                    tensorList[0] = torch.cat([tensorList[0], obj.xGpuTensorsRed])
                    tensorList[1] = torch.cat([tensorList[1], obj.yGpuTensorsRed])
                    tensorList[2] = torch.cat([tensorList[2], obj.xGpuTensorsBlue])
                    tensorList[3] = torch.cat([tensorList[3], obj.yGpuTensorsBlue])
                    tensorList[4] = torch.cat([tensorList[4], obj.xGpuTensorsGreen])
                    tensorList[5] = torch.cat([tensorList[5], obj.yGpuTensorsGreen])
                    tensorList[6] = torch.cat([tensorList[6], obj.xGpuTensorsYellow])
                    tensorList[7] = torch.cat([tensorList[7], obj.yGpuTensorsYellow])
            particleLife.updateVelocityOuter(tensorList)
            particleLife.updateVelocityInner()
            
        for particleLife in lifeFormList:
            particleLife.updatePosition()
        
        for particleLife in lifeFormList:
            particleLife.syncCpuTensors()
            
        for particleLife in lifeFormList:
            particleLife.draw()

        pygame.display.update()
        end = time.time()
        timeList.append(end-start)
        clock.tick(60)
    print("average time: " + str(sum(timeList)/len(timeList)))
    pygame.quit()
        
if __name__ == "__main__":
    main()