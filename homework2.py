import time
from pprint import pprint
import math
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
		self.board = deepcopy(board)
		self.color = color
		self.opponent_color = opponent_color
		

	def get_all_pieces(self,color):
		#print("inside get all pieces")
		pieces = []
		for row in self.board:
			for piece in row:
				#print(piece.color)
				if piece != EMPTY_SPOT and piece.color == color:
					pieces.append(piece)
		#print(pieces)
		return pieces
#king check
	def getActions(self,state,max_player):
		if max_player:
			playercolor = self.color
			coins = self.get_all_pieces(self.color)
		else:
			playercolor = self.opponent_color
			coins = self.get_all_pieces(self.opponent_color)

		if playercolor == "BLACK":
			regularDirs = [[1, -1], [1, 1]]
			captureDirs = [[2, -2], [2, 2]]
		else:
			regularDirs = [[-1, -1], [-1, 1]]
			captureDirs = [[-2, -2], [-2, 2]]

		regularMoves = []
		captureMoves = []
		for checker in coins:
			if checker.king:
				regularDirs = [[1, -1], [1, 1],[-1, -1], [-1, 1]]
				captureDirs = [[2, -2], [2, 2],[-2, -2], [-2, 2]]

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

	def recursive_check(self,regularDirs,captureDirs,checker,state,playercolor):
		oldrow,oldcol = checker.row,checker.col
		regularMoves = []
		captureMoves = []
		for dir in captureDirs:
			is_Valid,new_state = self.isValidMove(oldrow, oldcol, oldrow+dir[0], oldcol+dir[1],state)
			if is_Valid:
				if not checker.king and ((oldrow+dir[0] == 7 and playercolor == "BLACK") or (oldrow+dir[0] == 0 and playercolor == "WHITE")):
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
					if not checker.king and ((oldrow+dir[0] == 7 and playercolor == "BLACK") or (oldrow+dir[0] == 0 and playercolor == "WHITE")):
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
			# if !checker.king and (row == 7 and self.color == "BLACK") or (row == 0 and self.color == "WHITE"):
			#     temp_board[row][col].make_king()
			return True,temp_board
		elif abs_row_diff == 2:  # capture move
			#  \ direction or / direction
			row_diff = row_diff // 2
			col_diff = (col - oldcol) // 2
			print(oldrow,oldcol,row,col,row_diff,col_diff)
			print(state[oldrow+row_diff][oldcol+col_diff].piece.lower(),state[oldrow][oldcol].piece.lower())
			if state[oldrow+row_diff][oldcol+col_diff].piece == '.' or (state[oldrow+row_diff][oldcol+col_diff].piece.lower() == state[oldrow][oldcol].piece.lower()):
				return False,None
			else:
				temp_board = deepcopy(state)
				temp_piece = temp_board[oldrow][oldcol].piece
				temp_board[oldrow][oldcol] = Piece(oldrow,oldcol,'.')
				temp_board[oldrow+row_diff][oldcol+col_diff].piece = '.' 
				temp_board[row][col].piece = temp_piece
				# if !checker.king and (row == 7 and self.color == "BLACK") or (row == 0 and self.color == "WHITE"):
				#     temp_board[row][col].make_king()
				return True,temp_board
		else:
			 False,None

	# def applyAction(self,state,):

	# def terminal_test(self):
	# 	if(len(self.checkers) == 0 or len(self.opponent_checkers) == 0) :
	# 		return True
	
	def computeUtilityValue(self, state):
		# utility = (len(self.checkers) - len(self.opponent_heckers)) * 500 + len(self.checkers) * 50
		return 1000

	def computeHeuristic(self, state):
		#  heurisitc = (len(self.checkers) - len(self.opponent_checkers)) * 50 + self.countSafecheckers() * 10 + len(self.checkers)
		 return 1000


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
		self.currentDepth = 0
		self.maxDepth = 0
		self.numNodes = 0
		self.maxPruning = 0
		self.minPruning = 0
		self.depthLimit = depthLimit

		v = self.maxValue(state.board, -1000, 1000, self.depthLimit)

		return self.best_move

	def maxValue(self, state, alpha, beta, depthLimit):
		# if state.terminal_test():
		# 	return state.computeUtilityValue()
		if depthLimit == 0:
			return self.state.computeHeuristic(state)
		self.currentDepth += 1
		self.maxDepth = max(self.maxDepth, self.currentDepth)
		self.numNodes += 1

		actionList = self.state.getActions(state,True)[0]
		pprint(actionList)
		v = -math.inf
		if len(actionList) == 0:
			return self.state.computeUtilityValue(state)
		
		for state,move in actionList:
			# return captured checker if it is a capture move
			# state.printBoard()
			next = self.minValue(state, alpha, beta, depthLimit - 1)
			if next > v:
				v = next
				# Keep track of the best move so far at the top level
				if depthLimit == self.depthLimit:
					self.best_move = move
			
			# alpha-beta max pruning
			if v >= beta:
				self.maxPruning += 1
				self.currentDepth -= 1
				return v
			alpha = max(alpha, v)

		self.currentDepth -= 1

		return v

	def minValue(self, state, alpha, beta, depthLimit):
		# if state.terminalTest():
		#     return state.computeUtilityValue()
		if depthLimit == 0:
			return self.state.computeHeuristic(state)

		# update statistics for the search
		self.currentDepth += 1
		self.maxDepth = max(self.maxDepth, self.currentDepth)
		self.numNodes += 1
		actionList = self.state.getActions(state,False)[0]
		v = math.inf
		if len(actionList) == 0:
			return self.state.computeUtilityValue(state)
		for state,moves in actionList:
			next = self.maxValue(state, alpha, beta, depthLimit - 1)
			
			if next < v:
				v = next
			
			#alpha-beta min pruning
			if v <= alpha:
				self.minPruning += 1
				self.currentDepth -= 1
				return v
			beta = min(beta, v)

		self.currentDepth -= 1
		return v

	
	# def minimax(self,position, depth, max_player,color, opponent_color):
	# 	if depth == 0 or position.winner() != None:
	# 		print("start",position.evaluate())
	# 		return position.evaluate(), position
		
	# 	if max_player:
	# 		print("inside max")
	# 		maxEval = float('-inf')
	# 		best_move = None
	# 		for move in self.get_all_moves(position, color):
	# 			evaluation = self.minimax(move, depth-1, False,color,opponent_color)[0]
	# 			print("max",evaluation)
	# 			maxEval = max(maxEval, evaluation)
	# 			if maxEval == evaluation:
	# 				best_move = move
	# 		print(maxEval)	        
	# 		return maxEval, best_move
	# 	else:
	# 		print("inside min")
	# 		minEval = float('inf')
	# 		best_move = None
	# 		for move in self.get_all_moves(position, opponent_color):
	# 			evaluation = self.minimax(move, depth-1, True, color, opponent_color)[0]
	# 			print("min", evaluation)
	# 			minEval = min(minEval, evaluation)
	# 			if minEval == evaluation:
	# 				best_move = move
	# 		print(minEval)
	# 		return minEval, best_move

	# def get_all_moves(self,board, color):
	# 	moves = []
	# 	#print("inside getallmoves")
	# 	for piece in board.get_all_pieces(color):
	# 		print(piece.color)
	# 		valid_moves = board.get_valid_moves(piece)
	# 		#print(valid_moves)
	# 		for move, skip in valid_moves.items():
	# 			print(move[0],move[1])
	# 			temp_board = deepcopy(board)
	# 			temp_piece = temp_board.get_piece(piece.row, piece.col)
	# 			new_board = self.simulate_move(temp_piece, move, temp_board, skip)
	# 			moves.append(new_board)
	# 	return moves

	# def simulate_move(self, move, board, piece):
	# 	oldrow,oldcol,row,col = move
	# 	board[row][col] = piece
	# 	board[oldrow][oldcol] = Piece(oldrow,oldcol,'.')
	# 	return board


class Game:
	def __init__(self):
		start_time = time.time()
		self.inputs()
		print(time.time() - start_time)

	def inputs(self):
		f = open("input.txt","r")
		game_type = f.readline().rstrip()
		color = f.readline().rstrip()
		remaining_playtime = f.readline().rstrip()
		board = []
		board_row = []
		print(color)
		for i in range(0,ROWS):
			board.append([])
			board_row = list(f.readline().rstrip())
			for j in range(0,len(board_row)):
				board[i].append(Piece(i,j,board_row[j]))
		#print(board)
		if(game_type == 'GAME'):
			remaining_playtime = self.determinetimeforthisplay(remaining_playtime)
		self.playgame(board, color, remaining_playtime)

	def playgame(self,board,color,remaining_playtime):
		self.board = board
		pprint(board)
		if color == BLACK :
			opponent_color = WHITE
		else:
			opponent_color = BLACK

		#print(self.board.winner())
		#value, new_board = AiAgent().minimax(self.board,4,color,color,opponent_color)
		max_player = AiAgent(self.board,color)
		state = GameState(self.board,color,opponent_color)
		next_move = max_player.get_best_next_move(state,1)
		print(next_move)

	#TODO
	def winner():
		return self.board.winner()

	def ai_move():
		pass

	def get_board(self,board):
		return self.board

	def determinetimeforthisplay(self,remaining_playtime):
		#TODO heuristic to decide playtime for current play in game mode
		return remaining_playtime

c = Game()

