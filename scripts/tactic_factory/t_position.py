from tactic import Tactic
import time

class TPosition(Tactic):

	def __init__(self, bot_id, state, param=None):
		super(TPosition, self).__init__( bot_id, state, param)
		self.param = param

	def execute(self, state):
		# TODO: call the skill execute instance here
		pass

	def isComplete(self, state):
		# TO DO use threshold distance instead of actual co ordinates
		if state.homeVel[self.bot_id].x == self.param.PositonP.x and state.homeVel[self.bot_id].y == self.param.PositonP.y:
			return True
		elif time.time()-self.begin_time > self.time_out:
			return True
		else:
			return False

	def updateParams(self, state):
		# No parameter to update here
		pass
