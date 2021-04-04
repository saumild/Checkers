import time
import math
import random
import sys
from copy import deepcopy
ROWS, COLS = 8, 8
BLACK = ['b','B']
WHITE = ['w','W']
EMPTY_SPOT = '.'
#w1,w2,w3,w4 = int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])

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
	def deepcopypickle(self, state):
		return pickle.loads(pickle.dumps(state, -1))


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
		#random.shuffle(captureDirs)
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
			#random.shuffle(regularDirs)
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

	def computeHeuristic(self, state):
		bp,wp,bkp,wkp,cbt,cwt,dbk,dwk,sbc,swc = self.get_evaluation_count_on_board(state)
		if self.color == "BLACK":
			checkers_count = bp
			checkers_king_count = bkp
			opponent_checkers_count = wp
			opponent_checkers_king_count = wkp
			dist_checker_king = dbk
			checkers_safe_count = sbc
			opponent_safe_count = swc
			checkers_triangle = cbt
			opponent_checkers_triangle = cwt
		elif self.color == "WHITE":
			checkers_count = wp
			checkers_king_count = wkp
			opponent_checkers_count = bp
			opponent_checkers_king_count = bkp
			dist_checker_king = dwk
			checkers_safe_count = swc
			opponent_safe_count = sbc
			checkers_triangle = cwt
			opponent_checkers_triangle = cbt
		
		heurisitic = (checkers_count - opponent_checkers_count)*15 + (checkers_king_count - opponent_checkers_king_count)*9+ (opponent_safe_count)*(-3) + (checkers_triangle)*6
		return heurisitic

	def get_evaluation_count_on_board(self,state):
		black_piece_count,white_piece_count = 0,0
		black_piece__king_count,white_piece_king_count = 0,0
		dist_to_become_white_king,dist_to_become_black_king = 0,0
		count_safe_white_checker,count_safe_black_checker = 0,0
		checkers_white_triangle,checkers_black_triangle = 0,0
		board = state
		for row in state:
			for piece in row:
				if piece.row >= 3 and piece.color == "BLACK":
					checkers_black_triangle = checkers_black_triangle + 7
				elif piece.color == "BLACK":
					checkers_black_triangle = checkers_black_triangle + 5
				elif piece.row < 3 and piece.color == "WHITE":
					checkers_white_triangle = checkers_white_triangle + 7
				elif piece.color == "WHITE":
					checkers_white_triangle = checkers_white_triangle + 5
				safe = False
				if piece.row == 0 or piece.row == 7 or piece.col == 0 or piece.col == 7:
				 	safe = True 

				if piece.piece != EMPTY_SPOT:
					if piece.piece == 'w':
						white_piece_count = white_piece_count + 1
						dist_to_become_white_king = dist_to_become_white_king + (piece.row)
						if safe:
						 	count_safe_white_checker += 1

					elif piece.piece == 'b':
						black_piece_count = black_piece_count + 1
						dist_to_become_black_king = dist_to_become_black_king + (7 - piece.row)
						if safe:
						 	count_safe_black_checker += 1

					elif piece.piece == 'W':
						white_piece_king_count = white_piece_king_count + 1
						if safe:
							count_safe_white_checker += 1

					elif piece.piece == 'B':
						black_piece__king_count = black_piece__king_count + 1
						if safe:
							count_safe_black_checker += 1

		return black_piece_count, white_piece_count, black_piece__king_count, white_piece_king_count,checkers_black_triangle,checkers_white_triangle,dist_to_become_black_king,dist_to_become_white_king,count_safe_black_checker,count_safe_white_checker

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
		random.shuffle(actionList)
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
			elif next == v and depthLimit == self.depthLimit and random.random() > 0.75:
				self.best_move = move			
			# alpha-beta max pruning
			if v >= beta:
				return v
			alpha = max(alpha, v)

		return v

	def minValue(self, state, alpha, beta, depthLimit):
		if depthLimit == 0:
			return self.state.computeHeuristic(state)

		# update statistics for the search
		actionList = self.state.getActions(state,False)[0]
		#random.shuffle(actionList)
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
		#p1,w1,w2,w3,w4,inp,op = args
		#print(w1,w2,w3,w4)

	def inputs(self):
		#f = open(sys.argv[1],"r")
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
		#pprint(board)
		if color == "BLACK" :
			opponent_color = "WHITE"
		elif color == "WHITE":
			opponent_color = "BLACK"

		if game_type == "SINGLE":
			depth = 1
		else:
			depth = 8
		max_player = AiAgent(self.board,color)
		state = GameState(self.board,color,opponent_color)
		next_move = max_player.get_best_next_move(state,depth)
		output = self.get_output_format(next_move)
		#f = open(sys.argv[2],"w+")
		f = open("output.txt","w+")
		f.write(output)
		f.close()
		# #print(time.process_time() - self.start_time)
	
	def make_move(self,next_move,board):
		for i in range(0,len(next_move),4):
			if i % 4 == 0:
				row_diff = (next_move[0] - next_move[2])
				if abs(row_diff) == 2:
					row_diff = row_diff // 2
					col_diff = (next_move[1] - next_move[3]) // 2		
				
					temp_piece = self.board[next_move[i]][next_move[i]].piece
					self.board[next_move[i]][next_move[i+1]] = Piece(next_move[i],next_move[i],'.')
					self.board[next_move[i]+row_diff][next_move[i+1]+col_diff].piece = '.' 
					self.board[next_move[i+2]][next_move[i+3]].piece = temp_piece
				else:
				#print(next_move)
					temp_piece = self.board[next_move[i]][next_move[i+1]].piece
					self.board[next_move[i]][next_move[i+1]] = Piece(next_move[i],next_move[i+1],'.')
					self.board[next_move[i+2]][next_move[i+3]].piece = temp_piece 
		output = ""
		for i in range(0,ROWS):
			board_row = self.board[i]
			for j in range(0,len(board_row)):
				output = output + str(self.board[i][j])
			output = output + "\n"
		#print(type(output))
		f = open("output.txt","w+")
		f.write(output.strip())
		f.close()
		
		# print(board)
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
		#print(output)
		return output.strip()

c = Game()

