import time
import os
import math
from random import shuffle
import sys
from copy import deepcopy
ROWS, COLS = 8, 8
BLACK = ['b','B']
WHITE = ['w','W']
EMPTY_SPOT = '.'

class Piece:

	def __init__(self, row, col, piece):
		self.row = row
		self.col = col
		self.piece = piece
		if piece in WHITE:
			self.color = 'WHITE'
		elif piece in BLACK:
			self.color = 'BLACK'
		else:
			self.color = EMPTY_SPOT
		self.king = piece in ['B', 'W']
		
	def make_king(self):
		self.king = True
		self.piece = self.piece.upper()

	def move(self, row, col):
		self.row = row
		self.col = col

	def __repr__(self):
		return str(self.piece)


class GameState:
	
	def __init__(self,board,color,opponent_color):
		self.color = color
		self.opponent_color = opponent_color
		self.board = deepcopy(board)
		

	
	def get_all_pieces(self,state,color):
		pieces = []
		for row in state:
			for piece in row:
				if piece.piece != EMPTY_SPOT and piece.color == color:
					pieces.append(piece)
		return pieces

	def getActions(self,state,max_player):
		if max_player:
			playercolor = self.color
			coins = self.get_all_pieces(state,self.color)
		else:
			playercolor = self.opponent_color
			coins = self.get_all_pieces(state,self.opponent_color)

		regularMoves = []
		captureMoves = []
		for checker in coins:
			regularDirs,captureDirs = self.get_directions(checker.king,playercolor)
			actions, flag = self.recursive_check(regularDirs,captureDirs,checker,state,playercolor)
			# must take capture move if possible
			if flag:
				captureMoves.extend(actions)
			else:
				regularMoves.extend(actions)
			
		# must take capture move if possible
		if captureMoves:
			return captureMoves,True
		else:
			return regularMoves,False

	def get_directions(self,is_king,playercolor):
		if is_king:
			if playercolor == "BLACK":
					regularDirs = [[1, -1], [1, 1],[-1, -1], [-1, 1]]
					captureDirs = [[2, -2], [2, 2],[-2, -2], [-2, 2]]
			elif playercolor == "WHITE":
				regularDirs = [[-1, -1], [-1, 1],[1, -1], [1, 1]]
				captureDirs = [[-2, -2], [-2, 2],[2, -2], [2, 2]]
		else:
			if playercolor == "BLACK":
				regularDirs = [[1, -1], [1, 1]]
				captureDirs = [[2, -2], [2, 2]]
			elif playercolor == "WHITE":
				regularDirs = [[-1, -1], [-1, 1]]
				captureDirs = [[-2, -2], [-2, 2]]
		return regularDirs,captureDirs

	def recursive_check(self,regularDirs,captureDirs,checker,state,playercolor):
		oldrow,oldcol = checker.row,checker.col
		regularMoves = []
		captureMoves = []
		for dir in captureDirs:
			is_Valid,new_state = self.isValidMove(oldrow, oldcol, oldrow+dir[0], oldcol+dir[1],state)
			if is_Valid:
				if not checker.king and (( playercolor == "BLACK" and oldrow+dir[0] == 7)):
					new_state[oldrow+dir[0]][oldcol+dir[1]].make_king()
					captureMoves.append((new_state, [oldrow, oldcol, oldrow+dir[0], oldcol+dir[1]]))
				elif not checker.king and (( playercolor == "WHITE" and oldrow+dir[0] == 0)):
					new_state[oldrow+dir[0]][oldcol+dir[1]].make_king()
					captureMoves.append((new_state, [oldrow, oldcol, oldrow+dir[0], oldcol+dir[1]]))
				else:
					caplist,capflag = self.recursive_check(regularDirs,captureDirs,new_state[oldrow+dir[0]][oldcol+dir[1]],new_state,playercolor)
					if capflag:
						for cap in caplist:
							capmoveList = [oldrow, oldcol, oldrow+dir[0], oldcol+dir[1], *cap[1]]
							captureMoves.append((cap[0],capmoveList))
					else:
						captureMoves.append((new_state, [oldrow, oldcol, oldrow+dir[0], oldcol+dir[1]]))
		if not captureMoves:
			for dir in regularDirs:
				is_Valid,new_state = self.isValidMove(oldrow, oldcol, oldrow+dir[0], oldcol+dir[1],state)
				if is_Valid:
					if not checker.king and ((playercolor == "BLACK" and oldrow+dir[0] == 7 )):
						new_state[oldrow+dir[0]][oldcol+dir[1]].make_king()
					elif not checker.king and ((playercolor == "WHITE" and oldrow+dir[0] == 0)):
						new_state[oldrow+dir[0]][oldcol+dir[1]].make_king()
					regularMoves.append((new_state, [oldrow, oldcol, oldrow+dir[0], oldcol+dir[1]]))
		# must take capture move if possible
		if captureMoves:
			return captureMoves,True
		else:
			return regularMoves,False
	
	def isValidMove(self, oldrow, oldcol, row, col,state):
		# invalid index
		if oldrow < 0 or oldrow > 7 or oldcol < 0 or oldcol > 7 or row < 0 or row > 7 or col < 0 or col > 7:
			return False, None
		# No checker exists in original position
		if state[oldrow][oldcol].piece == '.':
			return False,None
		# Another checker exists in destination position
		if state[row][col].piece != '.':
			return False,None
		
		row_diff = row - oldrow
		abs_row_diff = abs(row_diff)
		if abs_row_diff == 1:   # regular move
			temp_board = deepcopy(state)

			temp_piece = temp_board[oldrow][oldcol].piece
			temp_board[oldrow][oldcol] = Piece(oldrow,oldcol,'.')
			temp_board[row][col].piece = temp_piece
			return True,temp_board
		elif abs_row_diff == 2:  # capture move
			#  \ direction or / direction
			row_diff = row_diff // 2
			col_diff = (col - oldcol) // 2
			if state[oldrow+row_diff][oldcol+col_diff].piece == '.' or (state[oldrow+row_diff][oldcol+col_diff].piece.lower() == state[oldrow][oldcol].piece.lower()):
				return False,None
			else:
				temp_board = deepcopy(state)
				temp_piece = temp_board[oldrow][oldcol].piece
				temp_board[oldrow][oldcol] = Piece(oldrow,oldcol,'.')
				temp_board[oldrow+row_diff][oldcol+col_diff].piece = '.' 
				temp_board[row][col].piece = temp_piece
				return True,temp_board
		else:
			 False,None

	def computeHeuristic(self,state):
		black_pawn,black_king,white_pawn,white_king,black_protected,white_protected,white_can_be_killed,black_can_be_killed = self.get_evaluation_count_on_board(state)
		
		heuristic = (white_pawn - black_pawn) * 12+(white_king - black_king) * 15+(white_can_be_killed - black_can_be_killed) * -3 + (white_protected - black_protected) * 9
		
		return heuristic if self.color == "WHITE" else -1*heuristic

	def get_evaluation_count_on_board(self,state):
		black_pawn,black_king,white_pawn,white_king = 0,0,0,0
		black_protected,white_protected = 0,0
		white_can_be_killed,black_can_be_killed = 0,0
		for row in state:
			for piece in row:
				if piece.piece == '.':
					continue

				if piece.piece == 'w' or piece.piece == 'W':
					if piece.king:
						white_king += 1
					else:
						white_pawn += 1
					# Protected
					if piece.row < 7:
						if piece.row == 0 or piece.col == 0 or piece.col == 7:
							white_protected += 1
						else:
							try:
								if (state[piece.row - 1][piece.col - 1].piece == 'b' or state[piece.row - 1][piece.col - 1].piece == 'B') and (state[piece.row + 1][piece.col + 1].piece == "."):
									white_can_be_killed += 1
								elif (state[piece.row - 1][piece.col - 1].piece == 'b' or state[piece.row - 1][piece.col + 1].piece == 'B') and (state[piece.row + 1][piece.col - 1].piece == "."):
									white_can_be_killed += 1
								elif (state[piece.row + 1][piece.col - 1].piece == 'b' or state[piece.row + 1][piece.col - 1].piece == 'B') and state[piece.row + 1][piece.col - 1].king and state[piece.row - 1][piece.col + 1].piece == ".":
									white_can_be_killed += 1
								elif (state[piece.row + 1][piece.col + 1].piece == 'b' or state[piece.row + 1][piece.col + 1].piece == 'B') and state[piece.row + 1][piece.col + 1].king and state[piece.row - 1][piece.col - 1].piece == ".":
									white_can_be_killed += 1
								else:
									white_protected += 1
							except:
								white_protected += 1
				else:
					if piece.king:
						black_king += 1
					else:
						black_pawn += 1
					# Protected
					if piece.row > 0:
						if piece.row == 7 or piece.col == 0 or piece.col == 7:
							black_protected += 1
						else:
							try:
								if (state[piece.row + 1][piece.col - 1].piece == 'w' or state[piece.row + 1][piece.col - 1].piece == 'W') and (state[piece.row - 1][piece.col + 1].piece == '.'):
									black_can_be_killed += 1
								elif (state[piece.row + 1][piece.col + 1].piece == 'w' or state[piece.row + 1][piece.col + 1].piece == 'W') and (state[piece.row - 1][piece.col - 1].piece == '.'):
									black_can_be_killed += 1
								elif (state[piece.row + 1][piece.col - 1].piece == 'w' or state[piece.row + 1][piece.col - 1].piece == 'W') and state[piece.row + 1][piece.col - 1].king and (state[piece.row - 1][piece.col + 1].piece == '.'):
									black_can_be_killed += 1
								elif (state[piece.row + 1][piece.col + 1].piece == 'w' or state[piece.row + 1][piece.col + 1].piece == 'W') and state[piece.row + 1][piece.col + 1].king and (state[piece.row - 1][piece.col - 1].piece == '.'):
									black_can_be_killed += 1
								else:
									black_protected += 1
							except:
								black_protected += 1	
		return 	black_pawn,black_king,white_pawn,white_king,black_protected,white_protected,white_can_be_killed,black_can_be_killed

class AiAgent:
	def __init__(self,game,color):
		self.game = game
		self.color = color

	def get_best_next_move(self,state,depthLimit):
		next_move = self.alpha_beta(state,depthLimit)
		return next_move
		

	def alpha_beta(self,state,depthLimit):
		self.state = state
		self.best_move = []
		self.depthLimit = depthLimit
		v = self.maxValue(state.board, -math.inf, math.inf, self.depthLimit)
		return self.best_move

	def maxValue(self, state, alpha, beta, depthLimit):
		if depthLimit == 0:
			return self.state.computeHeuristic(state)
		
		actionList = self.state.getActions(state,True)[0]
		shuffle(actionList)
		v = -math.inf
		if len(actionList) == 0:
			return self.state.computeHeuristic(state)
		
		for state,move in actionList:
			next = self.minValue(state, alpha, beta, depthLimit - 1)
			if next > v:
				v = next
				# Keep track of the best move so far at the top level
				if depthLimit == self.depthLimit:
					self.best_move = move
			elif next == v and depthLimit == self.depthLimit:
				self.best_move = move			
			# alpha-beta max pruning
			if v >= beta:
				return v
			alpha = max(alpha, v)

		return v

	def minValue(self, state, alpha, beta, depthLimit):
		if depthLimit == 0:
			return self.state.computeHeuristic(state)

		actionList = self.state.getActions(state,False)[0]
		shuffle(actionList)
		v = math.inf
		if len(actionList) == 0:
			return self.state.computeHeuristic(state)

		for state,moves in actionList:
			next = self.maxValue(state, alpha, beta, depthLimit - 1)
			
			if next < v:
				v = next
				
			#alpha-beta min pruning
			if v <= alpha:
				return v
			beta = min(beta, v)

		return v


class Game:
	def __init__(self):
		self.start_time = time.process_time()
		self.inputs()
		
	def inputs(self):
		f = open("input.txt","r")
		game_type = f.readline().rstrip()
		color = f.readline().rstrip()
		remaining_playtime = f.readline().rstrip()
		board = []
		board_row = []
		for i in range(0,ROWS):
			board.append([])
			board_row = list(f.readline().rstrip())
			for j in range(0,len(board_row)):
				board[i].append(Piece(i,j,board_row[j]))
		f.close()
		self.playgame(board, color, remaining_playtime,game_type)

	def playgame(self,board,color,remaining_playtime,game_type):
		self.board = board
		nummovesleft = 100
		if color == "BLACK" :
			opponent_color = "WHITE"
		elif color == "WHITE":
			opponent_color = "BLACK"
		if os.path.exists('playdata.txt'):
			nummovesleft = open("playdata.txt","r").readline()

		if not isinstance(nummovesleft,int):	
			nummovesleft = int(nummovesleft)
		if nummovesleft !=0:
			depthTiming = float(remaining_playtime)//nummovesleft
		else:
			depthTiming = 10
		f = open("calibration.txt","r")
		depthTL = f.readline().rstrip().split(",")
		f.close()
		depth = 5
		final_depth = 1000
		for i in range(1,len(depthTL)):
			if depthTiming < float(depthTL[i]):
				#print("i",i)
				final_depth = i-1
				break
			else:
				final_depth = 8
		if game_type == "SINGLE":
			depth = 1
		elif final_depth != 1000:
				depth = final_depth
	
		max_player = AiAgent(self.board,color)
		state = GameState(self.board,color,opponent_color)
		next_move = max_player.get_best_next_move(state,depth)
		output = self.get_output_format(next_move)
		f = open("output.txt","w+")
		f.write(output)
		f.close()
		f = open("playdata.txt","w")
		nummovesleft = nummovesleft - 1
		f.write(str(nummovesleft))
		f.close()
		
	def get_output_format(self,next_move):
		output = ""
		if next_move:
			if len(next_move)>4:
				is_jump = True
			elif abs(next_move[0] - next_move[2]) == 2:
				is_jump = True
			else:
				is_jump = False
			if is_jump:
				output = output + "J "
			else:
				output = output + "E "
			for i in range(0,len(next_move)):
				if i%2 == 0 :
					output += chr(next_move[i+1] + 97) + str(8 - next_move[i]) + " "
				if i%4 == 3 and i<(len(next_move) - 2):
					output = output.strip() + "\n"
					if is_jump:
						output = output + "J "
					else:
						output = output + "E "
		return output.strip()

c = Game()

