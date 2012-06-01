import random

def gen_scramble_str( nturns, dt_prob=0.3 ):
	'''Function to generate a Rubik's cube scrambling sequence
	with nturns turns. Generates double face turns with a probability
	of dt_prob. An inverse move is equally likely to come up as
	a normal move.'''

	faces = ['U','D','F','B','L','R']
	complements = ['D','U','B','F','R','L']
	face_seq = []
	scramblestr = ""

	lastface = None
	nextlastface = None
	for n in range(nturns):
		# Generate a valid face (not equal to last face, and if last two faces
		# were complements (e.g. 'U' and 'D'), not equal to second to last face)
		facenum = int( random.uniform( 0, len( faces ) ) )
		if n == 0:
			lastface = facenum
		elif n == 1:
			while facenum == lastface:
				facenum = int( random.uniform( 0, len( faces ) ) )
			nextlastface, lastface = lastface, facenum
		else:
			while (facenum == lastface) or ( (faces[lastface] == complements[nextlastface]) and (facenum == nextlastface) ):
				facenum = int( random.uniform( 0, len( faces ) ) )
			nextlastface, lastface = lastface, facenum
		# Initialize turn string
		str = faces[facenum]
		# Decide whether it's a single or double face turn
		double = random.uniform( 0, 1 ) <= dt_prob
		# Append modifiers to turn string
		if double:
			str += "2"
		else:
			if random.uniform( 0, 1 ) <= 0.5:
				str += "\'"
		#	else: str += " "
		str += " "
		scramblestr += str
	
	return scramblestr

def gen_scrambles( nscrambles, nturns ):
	scrambles = []
	for i in range(nscrambles):
		scrambles.append( gen_scramble_str( nturns ) )
	return scrambles

def print_scrambles( nscrambles, nturns=25 ):
	scrambles = gen_scrambles( nscrambles, nturns )
	for i in range( len( scrambles ) ):
		print scrambles[i]

