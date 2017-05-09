# Super class for all the tactics

import sys
import time

sys.path.insert(0,'./../../../plays_py/scripts')

from abc import ABCMeta, abstractmethod
from utils import tactics_union

class Tactic(object):
	# this default time is in milliseconds
	__metaclass__ = ABCMeta

	DEFAULT_TIMEOUT_PERIOD = 50
	param = tactics_union.Param()
	def __init__(self, name, bot_id, time_out=DEFAULT_TIMEOUT_PERIOD):
		self.name       = name
		self.bot_id     = bot_id
		self.time_out   = time_out
		self.begin_time = time.time()
	
	@abstractmethod
	def execute(self,state):
		pass

	@abstractmethod
	def isComplete(self,state):
		pass

	@abstractmethod
	def updateParams(self,state):
		pass