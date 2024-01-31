import torch
from torch import tensor, float16, Tensor
import math
import random
import pygame

from constants import *


# class for a particle sim
class ParticleLife():
    
    def __init__(self, size: int, colorRatios: [], velocityMultiplyer: float) -> None: 
        # velocity multiplyer
        self.velocityMultiplyer = velocityMultiplyer
        # creating color ratios for particles
        tot = colorRatios[0] + colorRatios[1] + colorRatios[2] + colorRatios[3]
        redRatio = (colorRatios[0]/tot)
        blueRatio = (colorRatios[1]/tot)
        greenRatio = (colorRatios[2]/tot)
        yellowRatio = (colorRatios[3]/tot)
        
        # create tensors for x and y values for each color on cpu
        self.xTensorsRed = tensor([random.randint(0, width) for x in range(math.floor(redRatio * size))], dtype=int)
        self.xTensorsBlue = tensor([random.randint(0, width) for x in range(math.floor(blueRatio * size))], dtype=int)
        self.xTensorsGreen = tensor([random.randint(0, width) for x in range(math.floor(greenRatio * size))], dtype=int)
        self.xTensorsYellow = tensor([random.randint(0, width) for x in range(math.floor(yellowRatio * size))], dtype=int)
        self.yTensorsRed = tensor([random.randint(0, height) for x in range(math.floor(redRatio * size))], dtype=int)
        self.yTensorsBlue = tensor([random.randint(0, height) for x in range(math.floor(blueRatio * size))], dtype=int)
        self.yTensorsGreen = tensor([random.randint(0, height) for x in range(math.floor(greenRatio * size))], dtype=int)
        self.yTensorsYellow = tensor([random.randint(0, height) for x in range(math.floor(yellowRatio * size))], dtype=int)
                
        # make sure total particle num equals the total particles
        for num in range(tot - (math.floor(redRatio * size) + math.floor(blueRatio * size) + math.floor(greenRatio * size) + math.floor(yellowRatio * size))):
            if num == 0:
                self.xTensorsRed = torch.cat((self.xTensorsRed, tensor([random.randint(0, width)], dtype=int)))
                self.yTensorsRed = torch.cat((self.yTensorsRed, tensor([random.randint(0, height)], dtype=int)))
            elif num == 1:
                self.xTensorsBlue = torch.cat((self.xTensorsBlue, tensor([random.randint(0, width)], dtype=int)))
                self.yTensorsBlue = torch.cat((self.yTensorsBlue, tensor([random.randint(0, height)], dtype=int)))
            else:
                self.xTensorsGreen = torch.cat((self.xTensorsGreen, tensor([random.randint(0, width)], dtype=int)))
                self.yTensorsGreen = torch.cat((self.yTensorsGreen, tensor([random.randint(0, height)], dtype=int)))
                
        self.xGpuTensorsRed = self.xTensorsRed.to(device)
        self.xGpuTensorsBlue = self.xTensorsBlue.to(device)
        self.xGpuTensorsGreen = self.xTensorsGreen.to(device)
        self.xGpuTensorsYellow = self.xTensorsYellow.to(device)
        self.yGpuTensorsRed = self.yTensorsRed.to(device)
        self.yGpuTensorsBlue = self.yTensorsBlue.to(device)
        self.yGpuTensorsGreen = self.yTensorsGreen.to(device)
        self.yGpuTensorsYellow = self.yTensorsYellow.to(device)
        
        # create vx and vy tensors for each color on device
        self.vxTensorsRed = torch.zeros([self.xTensorsRed.size(dim=0),], dtype=float16, device=device)
        self.vyTensorsRed = torch.zeros([self.yTensorsRed.size(dim=0),], dtype=float16, device=device)
        self.vxTensorsBlue = torch.zeros([self.xTensorsBlue.size(dim=0),], dtype=float16, device=device)
        self.vyTensorsBlue = torch.zeros([self.yTensorsBlue.size(dim=0),], dtype=float16, device=device)
        self.vxTensorsGreen = torch.zeros([self.xTensorsGreen.size(dim=0),], dtype=float16, device=device)
        self.vyTensorsGreen = torch.zeros([self.yTensorsGreen.size(dim=0),], dtype=float16, device=device)
        self.vxTensorsYellow = torch.zeros([self.xTensorsYellow.size(dim=0),], dtype=float16, device=device)
        self.vyTensorsYellow = torch.zeros([self.yTensorsYellow.size(dim=0),], dtype=float16, device=device)
        
        # rules
        self.RedRed = random.randint(-100, 80)/self.velocityMultiplyer
        self.RedBlue = random.randint(-100, 80)/self.velocityMultiplyer
        self.RedGreen = random.randint(-100, 80)/self.velocityMultiplyer
        self.RedYellow = random.randint(-100, 80)/self.velocityMultiplyer
        self.BlueRed = random.randint(-100, 80)/self.velocityMultiplyer
        self.BlueBlue = random.randint(-100, 80)/self.velocityMultiplyer
        self.BlueGreen = random.randint(-100, 80)/self.velocityMultiplyer
        self.BlueYellow = random.randint(-100, 80)/self.velocityMultiplyer
        self.GreenRed = random.randint(-100, 80)/self.velocityMultiplyer
        self.GreenBlue = random.randint(-100, 80)/self.velocityMultiplyer
        self.GreenGreen = random.randint(-100, 80)/self.velocityMultiplyer
        self.GreenYellow = random.randint(-100, 80)/self.velocityMultiplyer
        self.YellowRed = random.randint(-100, 80)/self.velocityMultiplyer
        self.YellowBlue = random.randint(-100, 80)/self.velocityMultiplyer
        self.YellowGreen = random.randint(-100, 80)/self.velocityMultiplyer
        self.YellowYellow = random.randint(-100, 80)/self.velocityMultiplyer
        
        self.ExteriorRedRed = random.randint(-90, 100)/self.velocityMultiplyer
        self.ExteriorRedBlue = random.randint(-90, 100)/self.velocityMultiplyer
        self.ExteriorRedGreen = random.randint(-90, 100)/self.velocityMultiplyer
        self.ExteriorRedYellow = random.randint(-90, 100)/self.velocityMultiplyer
        self.ExteriorBlueRed = random.randint(-90, 100)/self.velocityMultiplyer
        self.ExteriorBlueBlue = random.randint(-90, 100)/self.velocityMultiplyer
        self.ExteriorBlueGreen = random.randint(-90, 100)/self.velocityMultiplyer
        self.ExteriorBlueYellow = random.randint(-90, 100)/self.velocityMultiplyer
        self.ExteriorGreenRed = random.randint(-90, 100)/self.velocityMultiplyer
        self.ExteriorGreenBlue = random.randint(-90, 100)/self.velocityMultiplyer
        self.ExteriorGreenGreen = random.randint(-90, 100)/self.velocityMultiplyer
        self.ExteriorGreenYellow = random.randint(-90, 100)/self.velocityMultiplyer
        self.ExteriorYellowRed = random.randint(-90, 100)/self.velocityMultiplyer
        self.ExteriorYellowBlue = random.randint(-90, 100)/self.velocityMultiplyer
        self.ExteriorYellowGreen = random.randint(-90, 100)/self.velocityMultiplyer
        self.ExteriorYellowYellow = random.randint(-90, 100)/self.velocityMultiplyer
        
        # create numpy arrays from position tensors which will make it faster to iterate over the arrays when drawing the particles
        self.xArrayRed = self.xTensorsRed.numpy()
        self.xArrayBlue = self.xTensorsBlue.numpy()
        self.xArrayGreen = self.xTensorsGreen.numpy()
        self.xArrayYellow = self.xTensorsYellow.numpy()
        self.yArrayRed = self.yTensorsRed.numpy()
        self.yArrayBlue = self.yTensorsBlue.numpy()
        self.yArrayGreen = self.yTensorsGreen.numpy()
        self.yArrayYellow = self.yTensorsYellow.numpy()
                
    def syncCpuTensors(self):
        self.xTensorsRed.copy_(self.xGpuTensorsRed)
        self.xTensorsBlue.copy_(self.xGpuTensorsBlue)
        self.xTensorsGreen.copy_(self.xGpuTensorsGreen)
        self.xTensorsYellow.copy_(self.xGpuTensorsYellow)
        self.yTensorsRed.copy_(self.yGpuTensorsRed)
        self.yTensorsBlue.copy_(self.yGpuTensorsBlue)
        self.yTensorsGreen.copy_(self.yGpuTensorsGreen)
        self.yTensorsYellow.copy_(self.yGpuTensorsYellow)
        
    def calculateForces(self, xTensor1: Tensor, yTensor1: Tensor, vxTensor1: Tensor, vyTensor1: Tensor, xTensor2: Tensor, yTensor2: Tensor, rule: int):
        # create new tensors for x and y tensors
        xTensors1 = xTensor1.repeat(xTensor2.size(dim=0),)
        yTensors1 = yTensor1.repeat(yTensor2.size(dim=0),)
        
        # create new tensors for x2 and y2 tensors
        xTensors2 = xTensor2.repeat_interleave(xTensor1.size(dim=0))
        yTensors2 = yTensor2.repeat_interleave(yTensor1.size(dim=0))
        
        # create tensors for fx and fy of particles
        fxTensor = torch.zeros((xTensors1.size(dim=0),), device=device)
        fyTensor = torch.zeros((yTensors1.size(dim=0),), device=device)
        
        # calculate distance between particles
        dx = xTensors1.sub(xTensors2)
        dy = yTensors1.sub(yTensors2)
        dis = (dx**2 + dy**2)**.5
        
        # calculate forces
        F = tensor(torch.reciprocal((dis + .0001)) * rule, dtype=float16, device=device)
        fxTensor += F*dx
        fyTensor += F*dy
        # reshape fx and fy tensors to match with xTensor1 and yTensor1, then add the different rows to get tensors with the same shape as x and y tensor
        fxTensor = fxTensor.reshape(xTensor1.size(dim=0), xTensor2.size(dim=0))
        fxTensor = torch.sum(fxTensor, 1)
        fyTensor = fyTensor.reshape(yTensor1.size(dim=0), yTensor2.size(dim=0))
        fyTensor = torch.sum(fyTensor, 1)
        
        # forces to velocity
        vxTensor1.copy_((vxTensor1 + fxTensor)*0.5)
        vyTensor1.copy_((vyTensor1 + fyTensor)*0.5)
                
    def draw(self):
        for i in range(len(self.xArrayRed)):
            pygame.draw.rect(screen, red, (self.xArrayRed[i] - 1, self.yArrayRed[i] - 1, 3, 3))
        for i in range(self.xTensorsBlue.size(dim=0)):
            pygame.draw.rect(screen, blue, (self.xArrayBlue[i] - 1, self.yArrayBlue[i] - 1, 3, 3))
        for i in range(self.xTensorsGreen.size(dim=0)):
            pygame.draw.rect(screen, green, (self.xArrayGreen[i] - 1, self.yArrayGreen[i] - 1, 3, 3))
        for i in range(self.xTensorsYellow.size(dim=0)):
            pygame.draw.rect(screen, yellow, (self.xArrayYellow[i] - 1, self.yArrayYellow[i] - 1, 3, 3))
        
    def VelocityToPos(self, xTensor1: Tensor, yTensor1: Tensor, vxTensor1: Tensor, vyTensor1: Tensor):
        # velocity to postion
        xTensor1.add_(vxTensor1.long())
        yTensor1.add_(vyTensor1.long())
        
        # make sure particles stay on screen
        xTensor1.clamp_(0, 700)
        yTensor1.clamp_(0, 500)
        
        # reverse velocity if object is outside of the bounds
        vxTensor1.multiply_(torch.where(xTensor1 == width, -1.0, 1.0))
        vyTensor1.multiply_(torch.where(yTensor1 == height, -1.0, 1.0))
        vxTensor1.multiply_(torch.where(xTensor1 == 0, -1.0, 1.0))
        vyTensor1.multiply_(torch.where(yTensor1 == 0, -1.0, 1.0))
        
    def updateVelocityInner(self):
        self.calculateForces(self.xGpuTensorsRed, self.yGpuTensorsRed, self.vxTensorsRed, self.vyTensorsRed, self.xGpuTensorsRed, self.yGpuTensorsRed, self.RedRed)
        self.calculateForces(self.xGpuTensorsRed, self.yGpuTensorsRed, self.vxTensorsRed, self.vyTensorsRed, self.xGpuTensorsBlue, self.yGpuTensorsBlue, self.RedBlue)
        self.calculateForces(self.xGpuTensorsRed, self.yGpuTensorsRed, self.vxTensorsRed, self.vyTensorsRed, self.xGpuTensorsGreen, self.yGpuTensorsGreen, self.RedGreen)
        self.calculateForces(self.xGpuTensorsRed, self.yGpuTensorsRed, self.vxTensorsRed, self.vyTensorsRed, self.xGpuTensorsYellow, self.yGpuTensorsYellow, self.RedYellow)
        self.calculateForces(self.xGpuTensorsBlue, self.yGpuTensorsBlue, self.vxTensorsBlue, self.vyTensorsBlue, self.xGpuTensorsRed, self.yGpuTensorsRed, self.BlueRed)
        self.calculateForces(self.xGpuTensorsBlue, self.yGpuTensorsBlue, self.vxTensorsBlue, self.vyTensorsBlue, self.xGpuTensorsBlue, self.yGpuTensorsBlue, self.BlueBlue)
        self.calculateForces(self.xGpuTensorsBlue, self.yGpuTensorsBlue, self.vxTensorsBlue, self.vyTensorsBlue, self.xGpuTensorsGreen, self.yGpuTensorsGreen, self.BlueGreen)
        self.calculateForces(self.xGpuTensorsBlue, self.yGpuTensorsBlue, self.vxTensorsBlue, self.vyTensorsBlue, self.xGpuTensorsYellow, self.yGpuTensorsYellow, self.BlueYellow)
        self.calculateForces(self.xGpuTensorsGreen, self.yGpuTensorsGreen, self.vxTensorsGreen, self.vyTensorsGreen, self.xGpuTensorsRed, self.yGpuTensorsRed, self.GreenRed)
        self.calculateForces(self.xGpuTensorsGreen, self.yGpuTensorsGreen, self.vxTensorsGreen, self.vyTensorsGreen, self.xGpuTensorsBlue, self.yGpuTensorsBlue, self.GreenBlue)
        self.calculateForces(self.xGpuTensorsGreen, self.yGpuTensorsGreen, self.vxTensorsGreen, self.vyTensorsGreen, self.xGpuTensorsGreen, self.yGpuTensorsGreen, self.GreenGreen)
        self.calculateForces(self.xGpuTensorsGreen, self.yGpuTensorsGreen, self.vxTensorsGreen, self.vyTensorsGreen, self.xGpuTensorsYellow, self.yGpuTensorsYellow, self.GreenYellow)
        self.calculateForces(self.xGpuTensorsYellow, self.yGpuTensorsYellow, self.vxTensorsYellow, self.vyTensorsYellow, self.xGpuTensorsRed, self.yGpuTensorsRed, self.YellowRed)
        self.calculateForces(self.xGpuTensorsYellow, self.yGpuTensorsYellow, self.vxTensorsYellow, self.vyTensorsYellow, self.xGpuTensorsBlue, self.yGpuTensorsBlue, self.YellowBlue)
        self.calculateForces(self.xGpuTensorsYellow, self.yGpuTensorsYellow, self.vxTensorsYellow, self.vyTensorsYellow, self.xGpuTensorsGreen, self.yGpuTensorsGreen, self.YellowGreen)
        self.calculateForces(self.xGpuTensorsYellow, self.yGpuTensorsYellow, self.vxTensorsYellow, self.vyTensorsYellow, self.xGpuTensorsYellow, self.yGpuTensorsYellow, self.YellowYellow)
        
    # main loop for a particle sim
    def updateVelocityOuter(self, outsideTensors: list[Tensor]):
        """
        outsideTensors should contain 8 tensors
        [xTensorRed, yTensorRed, xTensorBlue, yTensorBlue, xTensorGreen, yTensorGreen, xTensorYellow, yTensorYellow]
        """
        self.calculateForces(self.xGpuTensorsRed, self.yGpuTensorsRed, self.vxTensorsRed, self.vyTensorsRed, outsideTensors[0], outsideTensors[1], self.ExteriorRedRed)
        self.calculateForces(self.xGpuTensorsRed, self.yGpuTensorsRed, self.vxTensorsRed, self.vyTensorsRed, outsideTensors[2], outsideTensors[3], self.ExteriorRedBlue)
        self.calculateForces(self.xGpuTensorsRed, self.yGpuTensorsRed, self.vxTensorsRed, self.vyTensorsRed, outsideTensors[4], outsideTensors[5], self.ExteriorRedGreen)
        self.calculateForces(self.xGpuTensorsRed, self.yGpuTensorsRed, self.vxTensorsRed, self.vyTensorsRed, outsideTensors[6], outsideTensors[7], self.ExteriorRedYellow)
        self.calculateForces(self.xGpuTensorsBlue, self.yGpuTensorsBlue, self.vxTensorsBlue, self.vyTensorsBlue, outsideTensors[0], outsideTensors[1], self.ExteriorBlueRed)
        self.calculateForces(self.xGpuTensorsBlue, self.yGpuTensorsBlue, self.vxTensorsBlue, self.vyTensorsBlue, outsideTensors[2], outsideTensors[3], self.ExteriorBlueBlue)
        self.calculateForces(self.xGpuTensorsBlue, self.yGpuTensorsBlue, self.vxTensorsBlue, self.vyTensorsBlue, outsideTensors[4], outsideTensors[5], self.ExteriorBlueGreen)
        self.calculateForces(self.xGpuTensorsBlue, self.yGpuTensorsBlue, self.vxTensorsBlue, self.vyTensorsBlue, outsideTensors[6], outsideTensors[7], self.ExteriorBlueYellow)
        self.calculateForces(self.xGpuTensorsGreen, self.yGpuTensorsGreen, self.vxTensorsGreen, self.vyTensorsGreen, outsideTensors[0], outsideTensors[1], self.ExteriorGreenRed)
        self.calculateForces(self.xGpuTensorsGreen, self.yGpuTensorsGreen, self.vxTensorsGreen, self.vyTensorsGreen, outsideTensors[2], outsideTensors[3], self.ExteriorGreenBlue)
        self.calculateForces(self.xGpuTensorsGreen, self.yGpuTensorsGreen, self.vxTensorsGreen, self.vyTensorsGreen, outsideTensors[4], outsideTensors[5], self.ExteriorGreenGreen)
        self.calculateForces(self.xGpuTensorsGreen, self.yGpuTensorsGreen, self.vxTensorsGreen, self.vyTensorsGreen, outsideTensors[6], outsideTensors[7], self.ExteriorGreenYellow)
        self.calculateForces(self.xGpuTensorsYellow, self.yGpuTensorsYellow, self.vxTensorsYellow, self.vyTensorsYellow, outsideTensors[0], outsideTensors[1], self.ExteriorYellowRed)
        self.calculateForces(self.xGpuTensorsYellow, self.yGpuTensorsYellow, self.vxTensorsYellow, self.vyTensorsYellow, outsideTensors[2], outsideTensors[3], self.ExteriorYellowBlue)
        self.calculateForces(self.xGpuTensorsYellow, self.yGpuTensorsYellow, self.vxTensorsYellow, self.vyTensorsYellow, outsideTensors[4], outsideTensors[5], self.ExteriorYellowGreen)
        self.calculateForces(self.xGpuTensorsYellow, self.yGpuTensorsYellow, self.vxTensorsYellow, self.vyTensorsYellow, outsideTensors[6], outsideTensors[7], self.ExteriorYellowYellow)

    def updatePosition(self):
        self.VelocityToPos(self.xGpuTensorsRed, self.yGpuTensorsRed, self.vxTensorsRed, self.vyTensorsRed)
        self.VelocityToPos(self.xGpuTensorsBlue, self.yGpuTensorsBlue, self.vxTensorsBlue, self.vyTensorsBlue)
        self.VelocityToPos(self.xGpuTensorsGreen, self.yGpuTensorsGreen, self.vxTensorsGreen, self.vyTensorsGreen)
        self.VelocityToPos(self.xGpuTensorsYellow, self.yGpuTensorsYellow, self.vxTensorsYellow, self.vyTensorsYellow)
