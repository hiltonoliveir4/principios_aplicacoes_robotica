#Codigo baseado em https://www.youtube.com/watch?v=zHboXMY45YU&list=WL&index=1

import pygame
import math

class Envir: # Environment class
    def __init__(self, dimentions):
        #Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)
        self.yel = (255, 255, 0)

        #Dimensions
        self.height = dimentions[0]
        self.width = dimentions[1]

        #Window settings
        pygame.display.set_caption("Mobile robot")
        self.map = pygame.display.set_mode((self.width, self.height))

        #Text configuration
        self.font=pygame.font.Font('freesansbold.ttf', 20)
        self.text=self.font.render('default', True, self.white, self.black)
        self.textRect=self.text.get_rect()
        self.textRect.center = (dimentions[1]-700,dimentions[0]-100)

        #Trail
        self.trail_set=[]
        
    def write_info(self, x, y, theta, v, gamma):
        Pose=f"x={x} y={y} theta={int(math.degrees(theta)):.2f} v={v:.2f} gamma={gamma:.2f}"
        self.text=self.font.render(Pose, True, self.white, self.black)
        self.map.blit(self.text, self.textRect)

    def trail(self, pos):
        for i in range(0, len(self.trail_set)-1):
            pygame.draw.line(self.map, self.yel, (self.trail_set[i][0], self.trail_set[i][1]), (self.trail_set[i+1][0], self.trail_set[i+1][1]))
            
        if self.trail_set.__sizeof__()>10000: #Numbe of elements on the trail
            self.trail_set.pop(0)
            
        self.trail_set.append(pos)

    def robot_frame(self, pos, rotation):
        n = 80
        centerx, centery = pos
        x_axis = (centerx + n * math.cos(-rotation),
                  centery + n * math.sin(-rotation))
        y_axis = (centerx + n * math.cos(-rotation + math.pi/2),
                  centery + n * math.sin(-rotation + math.pi/2))
        pygame.draw.line(self.map, self.red, (centerx, centery), x_axis, 3) # X axis in red
        pygame.draw.line(self.map, self.green, (centerx, centery), y_axis, 3) # Y axis in green
        
class Robot:
    def __init__(self, startpos, target_pos, robotImg, width):
      #Initial conditions
        self.w=width
        self.x=startpos[0]
        self.y=startpos[1]
        self.v=0
        self.gamma=0

        self.target_pos_x = target_pos[0]
        self.target_pos_y = target_pos[1]

        self.theta=0
        self.m2p = 3779.52 # meters to pixels

        #Robot
        self.img=pygame.image.load(robotImg)
        self.rotated=self.img
        self.rect=self.rotated.get_rect(center=(self.x, self.y))

    def draw(self, map):
        map.blit(self.rotated, self.rect)
        
    def calc_move_to_target(self):
        kv = 0.5
        kh = 4

        v_p = kv * math.sqrt((self.x - self.target_pos_x)**2 + (self.y - self.target_pos_y)**2)
        theta_p = math.atan((self.y - self.target_pos_y) / (self.x - self.target_pos_x))

        gamma = kh * (theta_p - self.theta)

        return [v_p, gamma]

    def move(self, event=None):
        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: 
                    # self.gamma += 0.5
                    pass
                elif event.key == pygame.K_a:
                    # self.gamma -= 0.5
                    pass
                elif event.key == pygame.K_w:
                    pass
                elif event.key == pygame.K_s:
                    pass

        control = self.calc_move_to_target()

        self.v = control[0]        
        self.gamma = control[1]

        self.x+=self.v*math.cos(self.theta)*dt
        self.y-=self.v*math.sin(self.theta)*dt
        self.theta+=(self.v/self.w)*math.tan(self.gamma)*dt

        #Reset theta
        if(self.theta>2*math.pi or self.theta<-2*math.pi):
          self.theta=0

        #Change in orientation
        self.rotated=pygame.transform.rotozoom(self.img, math.degrees(self.theta), 1) # Rotate image 'theta' with a scale operation of 1 - no change in size
        self.rect=self.rotated.get_rect(center=(self.x, self.y))
        
#Initialisation
pygame.init()

#Dimensions
dims = (800, 800)

#Status
running = True

#Environment
environment = Envir(dims)

#Robot
start_pos =(400,400)
target_pos = (0, 0) #posição alvo

img_add="robo.png"
robot_width = 8 # 8 pixels
robot = Robot(start_pos, target_pos, img_add, robot_width)

#dt
dt=0
lasttime=pygame.time.get_ticks()

#Simulation loop
while running:
    #Verify events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Quit the window
            running = False
        robot.move(event)

    #Time change
    dt = (pygame.time.get_ticks() - lasttime)/1000 # Current minus last time # Time in seconds
    lasttime=pygame.time.get_ticks() #Update last time
    
    #Update
    pygame.display.update()
    environment.map.fill(environment.black)
    robot.move()

    environment.write_info(int(robot.x), int(robot.y), robot.theta, robot.v, robot.gamma)

    robot.draw(environment.map)
    environment.robot_frame((robot.x, robot.y), robot.theta)
    
    environment.trail((robot.x, robot.y))

pygame.quit()