import pygame, sys
from pygame.locals import *
import numpy as np

def iRangdZero(posx,posy,board,N):
	return (posx < N and posx >= 0 and posy < N and posy >= 0 and board[posx][posy] == 0)

def getAbility(x,y,moves,board,N):
	axbility = 0
	for i in range(8):
		if iRangdZero(x+moves[i][0],y+moves[i][1],board,N):
			axbility += 1
	return axbility

def getNextIteration(move,moves,board,N):
	posX = move[0]
	posY = move[1]
	axbility = 8
	for i in range(8):
		newx = posX + moves[i][0]
		newy = posY + moves[i][1]
		newacc = getAbility(newx,newy,moves,board,N)
		if iRangdZero(newx,newy,board,N) and newacc < axbility:
			move[0] = newx
			move[1] = newy
			axbility = newacc
	return

def gDis(N,L_coor):
	horse = pygame.image.load("s")
	pygame.init()
	window = pygame.display.set_mode((32*N,32*N))
	pygame.display.set_caption("Knight's Tour")
	index = 0
	font = pygame.font.SysFont("ActionIsShaded",40)
	text = []
	surface = []

	while True:
		window.blit(background,(0,0))
		if index < N*N:
			window.blit(horse,(L_coor[index][0]*32,L_coor[index][1]*32))
			text.append(font.render(str(index+1),True,(255,255,255)))
			surface.append(text[index].get_rect())
			surface[index].center = (L_coor[index][0]*32+16,L_coor[index][1]*32+16)
			index += 1
		else:
			window.blit(horse,(L_coor[index-1][0]*32,L_coor[index-1][1]*32))
		for x in range(1000000):
			pass
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == 27:
					pygame.quit()
					sys.exit()

		for i in range(index):
			window.blit(text[i],surface[i])

		pygame.display.update()

def ifSolution(Board,N):
	for i in range(N):
		for j in range(N):
			if Board[i][j] == 0:
				return False
	return True

N = int(input("NxN Board Size of N: "))
posX = int(input("Start Location - X: "))%N
posY = int(input("Start Location - Y: "))%N
x = posX
y = posY
moveNumber = 2
move = [posX,posY]
moves = [[2,1],[2,-1],[1,2],[1,-2],[-1,2],[-1,-2],[-2,1],[-2,-1]]
Board = np.zeros([N,N])
Board[posX][posY] = 1
L = []
for i in range(N*N):
	move[0] = posX
	move[1] = posY
	getNextIteration(move,moves,Board,N)
	posX = move[0]
	posY = move[1]
	Board[posX][posY] = moveNumber
	moveNumber += 1
Board[posX][posY] -= 1

sol = ifSolution(Board,N)
if sol:
	k = 1
	while k <= N*N:
		for i in range(N):
			for j in range(N):
				if Board[i][j] == k:
					L.append([i,j])
					k += 1
	print(Board)
else:
	moves = [[2,1],[-2,1],[2,-1],[-2,-1],[1,2],[-1,2],[1,-2],[-1,-2]]
	Board = np.zeros([N,N])
	posX = x
	posY = y
	Board[posX][posY] = 1
	L = []
	moveNumber = 2
	move = [posX,posY]
	for i in range(N*N):
		move[0] = posX
		move[1] = posY
		getNextIteration(move,moves,Board,N)
		posX = move[0]
		posY = move[1]
		Board[posX][posY] = moveNumber
		moveNumber += 1
	Board[posX][posY] -= 1

	sol = ifSolution(Board,N)
	if sol:
		k = 1
		while k <= N*N:
			for i in range(N):
				for j in range(N):
					if Board[i][j] == k:
						L.append([i,j])
						k += 1
		print(Board)
if len(L) == 0:
	print("Solutions Not Found")
print("Optimal Knight Start: ", L)

if N <= 32 and sol:
	gDis(N,L)
