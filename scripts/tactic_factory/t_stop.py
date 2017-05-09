from tactic import Tactic
from utils import tactics_union
import time

class TStop(Tactic):

	def __init__(self, name, bot_id):
		super(TStop, self).__init__(name, bot_id)

		# TODO: Need to set these threshold velocity values
		self.vel_x_threshold = 0.0
		self.vel_y_threshold = 0.0

	def execute(self, state):
		# TODO: call the skill execute instance here
		pass

	def isComplete(self, state):
		if state.homeVel[self.bot_id].x <= self.vel_x_threshold and state.homeVel[self.bot_id].y <= self.vel_y_threshold:
			return True
		elif time.time()-self.begin_time > self.time_out:
			return True
		else:
			return False

	def updateParams(self, state):
		# No parameter to update here
		pass
