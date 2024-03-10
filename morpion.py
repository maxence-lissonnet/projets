import pygame

surf = pygame.display.set_mode((800,600))
run = True
n = 0

rect_1 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(30, 30, 150, 150))
rect_2 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(30, 190, 150, 150))
rect_3 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(30, 350, 150, 150))

rect_4 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(190, 30, 150, 150))
rect_5 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(350, 30, 150, 150))
    
rect_6 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(190, 190, 150, 150))
rect_7 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(190, 350, 150, 150))

rect_8 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(350, 350, 150, 150))
rect_9 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(350, 190, 150, 150))

L = [rect_1,rect_2,rect_3,rect_4,rect_5,rect_6,rect_7,rect_8,rect_9]


while run :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_r :
                rect_1 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(30, 30, 150, 150))
                rect_2 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(30, 190, 150, 150))
                rect_3 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(30, 350, 150, 150))

                rect_4 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(190, 30, 150, 150))
                rect_5 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(350, 30, 150, 150))
                    
                rect_6 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(190, 190, 150, 150))
                rect_7 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(190, 350, 150, 150))

                rect_8 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(350, 350, 150, 150))
                rect_9 = pygame.draw.rect(surf, (255,255,255),pygame.Rect(350, 190, 150, 150))

                L = [rect_1,rect_2,rect_3,rect_4,rect_5,rect_6,rect_7,rect_8,rect_9]
                n = 0

        if event.type == pygame.MOUSEBUTTONDOWN :
            if pygame.mouse.get_pressed() == (1,0,0) :
                pos = pygame.mouse.get_pos(),
                print(pos)
                if rect_1.collidepoint(pos):
                    print("Rectangle 1 a été cliqué")
                    if rect_1 in L :
                        if n%2 == 0 :
                            pygame.draw.line(surf,(0,0,0),(38,38),(166,166),2)
                            pygame.draw.line(surf,(0,0,0),(176,34),(34,176),2)
                            v_rect_1 = "x"
                            print("croix")
                            n = n + 1
                        else :
                            pygame.draw.circle(surf, (0,0,0), (102, 102), 50, 2)
                            print("rond")
                            n = n + 1
                        L.remove(rect_1)
                if rect_2.collidepoint(pos):
                    print("Rectangle 2 a été cliqué")
                    if rect_2 in L :
                        if n%2 == 0 :
                            pygame.draw.line(surf,(0,0,0),(38,200),(166,326),2)
                            pygame.draw.line(surf,(0,0,0),(176,200),(38,331),2)
                            v_rect_2 = "x"
                            print("croix")
                            n = n + 1
                        else :
                            pygame.draw.circle(surf, (0,0,0), (102, 268), 50, 2)
                            print("rond")
                            n = n + 1
                        L.remove(rect_2)
                if rect_3.collidepoint(pos):
                    print("Rectangle 3 a été cliqué")
                    if rect_3 in L :
                        if n%2 == 0 :
                            pygame.draw.line(surf,(0,0,0),(38,364),(166,478),2)
                            pygame.draw.line(surf,(0,0,0),(160,364),(34,489),2)
                            v_rect_3 = "x"
                            print("croix")
                            n = n + 1
                        else :
                            pygame.draw.circle(surf, (0,0,0), (102, 424), 50, 2)
                            print("rond")
                            n = n + 1
                        L.remove(rect_3)
                if rect_4.collidepoint(pos):
                    print("Rectangle 4 a été cliqué")
                    if rect_4 in L :
                        if n%2 == 0 :
                            pygame.draw.line(surf,(0,0,0),(200,38),(320,166),2)
                            pygame.draw.line(surf,(0,0,0),(331,38),(200,166),2)
                            v_rect_4 = "x"
                            print("croix")
                            n = n + 1
                        else :
                            pygame.draw.circle(surf, (0,0,0), (259, 102), 50, 2)
                            print("rond")
                            n = n + 1
                        L.remove(rect_4)
                if rect_5.collidepoint(pos):
                    print("Rectangle 5 a été cliqué")
                    if rect_5 in L :
                        if n%2 == 0 :
                            pygame.draw.line(surf,(0,0,0),(360,38),(480,166),2)
                            pygame.draw.line(surf,(0,0,0),(483,38),(365,166),2)
                            v_rect_5 = "x"
                            print("croix")
                            n = n + 1
                        else :
                            pygame.draw.circle(surf, (0,0,0), (425, 100), 50, 2)
                            print("rond")
                            n = n + 1
                        L.remove(rect_5)
                if rect_6.collidepoint(pos):
                    print("Rectangle 6 a été cliqué")
                    if rect_6 in L :
                        if n%2 == 0 :
                            pygame.draw.line(surf,(0,0,0),(200,200),(330,330),2)
                            pygame.draw.line(surf,(0,0,0),(335,200),(200,335),2)
                            v_rect_6 = "x"
                            print("croix")
                            n = n + 1
                        else :
                            pygame.draw.circle(surf, (0,0,0), (260, 260), 50, 2)
                            print("rond")
                            n = n + 1
                        L.remove(rect_6)
                if rect_7.collidepoint(pos):
                    print("Rectangle 7 a été cliqué")
                    if rect_7 in L :
                        if n%2 == 0 :
                            pygame.draw.line(surf,(0,0,0),(200,360),(320,480),2)
                            pygame.draw.line(surf,(0,0,0),(335,355),(200,480),2)
                            v_rect_7 = "x"
                            print("croix")
                            n = n + 1
                        else :
                            pygame.draw.circle(surf, (0,0,0), (260, 425), 50, 2)
                            print("rond")
                            n = n + 1
                        L.remove(rect_7)
                if rect_8.collidepoint(pos):
                    print("Rectangle 8 a été cliqué")
                    if rect_8 in L :
                        if n%2 == 0 :
                            pygame.draw.line(surf,(0,0,0),(360,360),(485,485),2)
                            pygame.draw.line(surf,(0,0,0),(490,355),(370,480),2)
                            v_rect_8 = "x"
                            print("croix")
                            n = n + 1
                        else :
                            pygame.draw.circle(surf, (0,0,0), (420, 420), 50, 2)
                            print("rond")
                            n = n + 1
                        L.remove(rect_8)
                if rect_9.collidepoint(pos):
                    print("Rectangle 9 a été cliqué")
                    if rect_9 in L :
                        if n%2 == 0 :
                            pygame.draw.line(surf,(0,0,0),(364,200),(480,320),2)
                            pygame.draw.line(surf,(0,0,0),(485,200),(360,335),2)
                            v_rect_9 = "x"
                            print("croix")
                            n = n + 1
                        else :
                            pygame.draw.circle(surf, (0,0,0), (420, 260), 50, 2)
                            print("rond")
                            n = n + 1
                        L.remove(rect_9)
                        
        """if L == [] :
            if v_rect_1 == "x" and v_rect_4 == "x" and v_rect_5 == "x" :
                print( "le joureur jouant les croix gagne")
            """

    pygame.display.flip()
pygame.quit()