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
					#print("madeking")
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
						#print("madeking")
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
			#print(oldrow,oldcol,row,col,row_diff,col_diff)
			#print(state[oldrow+row_diff][oldcol+col_diff].piece.lower(),state[oldrow][oldcol].piece.lower())
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

	def computeHeuristic1(self, state):
		bp,wp,bkp,wkp,x,y = self.get_evaluation_count_on_board(state)
		if self.color == "BLACK":
			checkers_count,checkers_king_count,opponent_checkers_count,opponent_checkers_king_count = bp,bkp,wp,wkp
		else:
			checkers_count,checkers_king_count,opponent_checkers_count,opponent_checkers_king_count = wp,wkp,bp,bkp

		heurisitic = (checkers_count - opponent_checkers_count) * 50 + (checkers_king_count - opponent_checkers_king_count) * 100 + checkers_count
		#print("heuristic",heurisitic)
		return heurisitic

	def computeHeuristic(self, state):
		#pprint("compheuristic")
		#pprint(state)
		bp,wp,bkp,wkp,dbk,dwk = self.get_evaluation_count_on_board(state)
		#print(bp,wp,bkp,wkp,dbk,dwk)
		if self.color == "BLACK":
			checkers_count,checkers_king_count,opponent_checkers_count,opponent_checkers_king_count,dist_king = bp,bkp,wp,wkp,dbk
		else:
			checkers_count,checkers_king_count,opponent_checkers_count,opponent_checkers_king_count,dist_king = wp,wkp,bp,bkp,dwk
			
		heurisitic = (checkers_count - opponent_checkers_count) * 0.32 + (checkers_king_count - opponent_checkers_king_count) * 0.32*2 + dist_king*0.7
		#print("heuristic",heurisitic)
		return heurisitic

	def get_evaluation_count_on_board(self,state):
		#print("evalcount")
		#pprint(state)
		black_piece_count,white_piece_count = 0,0
		black_piece__king_count,white_piece_king_count = 0,0
		dist_to_become_white_king,dist_to_become_black_king = 0,0
		for row in state:
			for piece in row:
				#print(piece.color)
				if piece != EMPTY_SPOT:
					if piece.piece == 'w':
						white_piece_count = white_piece_count + 1
						dist_to_become_white_king = dist_to_become_white_king + (piece.row)
					elif piece.piece == 'b':
						black_piece_count = black_piece_count + 1
						dist_to_become_black_king = dist_to_become_black_king + (8 - piece.row)
					elif piece.piece == 'W':
						white_piece_king_count = white_piece_king_count + 1
					elif piece.piece == 'B':
						black_piece__king_count = black_piece__king_count + 1
				
		#print(pieces)
		return black_piece_count,white_piece_count,black_piece__king_count,white_piece_king_count,dist_to_become_black_king,dist_to_become_white_king


class AiAgent:
	def __init__(self,game,color):
		self.game = game
		self.color = color

	def get_best_next_move(self,state,depthLimit):
		next_move = self.alpha_beta(state,depthLimit)
		#pprint(state.board)
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
		#heur = set()
		v = self.maxValue(state.board, -10000000, 1000000, self.depthLimit)
		#print(heur)
		#print(self.maxDepth)
		#print(self.numNodes)
		#print(depthLimit)
		#print(is_jump)
		return self.best_move

	def maxValue(self, state, alpha, beta, depthLimit):
		#print("depth max Limit",depthLimit)
		heuristic = None
		# if state.terminal_test():
		# 	return state.computeUtilityValue()
		if depthLimit == 0:
			#print("depthLimit max is 0")
			#pprint(state)
			#heuristic = self.state.computeHeuristic(state)
			#print(heuristic)
			#heur.add(heuristic)
			return self.state.computeHeuristic(state)
		self.currentDepth += 1
		self.maxDepth = max(self.maxDepth, self.currentDepth)
		
		self.numNodes += 1

		actionList = self.state.getActions(state,True)[0]

		v = -math.inf
		if len(actionList) == 0:
			#print("actionList max is 0")
			#heuristic = self.state.computeHeuristic(state)
			#print("actionList == 0",move,heuristic)
			#heur.add(heuristic)
			return self.state.computeHeuristic(state)
		
		for state,move in actionList:
			# return captured checker if it is a capture move
			# state.printBoard()
			next = self.minValue(state, alpha, beta, depthLimit - 1)
			if next > v:
				v = next
				# Keep track of the best move so far at the top level
				if depthLimit == self.depthLimit:
					#pprint(state)
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
		#print("depth min Limit",depthLimit)
		# if state.terminalTest():
		#     return state.computeUtilityValue()
		if depthLimit == 0:
			#print("depthLimit is 0")
			#heuristic = self.state.computeHeuristic(state)
			#heur.add(heuristic)
			return self.state.computeHeuristic(state)

		# update statistics for the search
		self.currentDepth += 1
		self.maxDepth = max(self.maxDepth, self.currentDepth)
		self.numNodes += 1
		actionList = self.state.getActions(state,False)[0]
		#pprint(actionList)
		v = math.inf
		if len(actionList) == 0:
			#print("actionList is 0")
			#heuristic = self.state.computeHeuristic(state)
			#heur.add(heuristic)
			return self.state.computeHeuristic(state)

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


class Game:
	def __init__(self):
		self.start_time = time.time()
		self.inputs()
		

	def inputs(self):
		f = open("input.txt","r")
		game_type = f.readline().rstrip()
		color = f.readline().rstrip()
		remaining_playtime = f.readline().rstrip()
		board = []
		board_row = []
		#print(color)
		for i in range(0,ROWS):
			board.append([])
			board_row = list(f.readline().rstrip())
			for j in range(0,len(board_row)):
				board[i].append(Piece(i,j,board_row[j]))
		#print(board)
		f.close()
		if(game_type == 'GAME'):
			remaining_playtime = self.determinetimeforthisplay(remaining_playtime)
		self.playgame(board, color, remaining_playtime)

	def playgame(self,board,color,remaining_playtime):
		self.board = board
		#pprint(board)
		if color == "BLACK" :
			opponent_color = "WHITE"
		else:
			opponent_color = "BLACK"

		#print(self.board.winner())
		#value, new_board = AiAgent().minimax(self.board,4,color,color,opponent_color)
		max_player = AiAgent(self.board,color)
		state = GameState(self.board,color,opponent_color)
		next_move = max_player.get_best_next_move(state,6)
		#print(next_move)
		output = self.get_output_format(next_move)
		f = open("output.txt","w+")
		f.write(output)
		f.close()
		print(time.time() - self.start_time)
	
	def get_output_format(self,next_move):
		if len(next_move)>4:
			is_jump = True
		else:
			is_jump = False
		output = ""
		if is_jump:
			output = output + "J "
		else:
			output = output + "E "
		for i in range(0,len(next_move)):
			if i%2 == 0 :
				output += chr(next_move[i+1] + 97) + str(8 - next_move[i]) + " "
			if i%4 == 3 and i<(len(next_move) - 2):
				output = output + "\n"
				if is_jump:
					output = output + "J "
				else:
					output = output + "E "
		print(output)
		return output

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

