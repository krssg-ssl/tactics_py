import sys
sys.path.append("/home/mehul/Documents/KRSSG/src/skills_py/scripts/skills")
sys.path.append("/home/mehul/KRSSG/src/scripts/utils")
sys.path.append("/home/mehul/Documents/KRSSG/src/plays_py/scripts/utils")

from tactic import Tactic
from geometry import Vector2D
import skills_union
import sKick
import sKickToPoint
from math import fabs,atan
from numpy import inf
from config import *
MAX_DRIBBLE_RANGE = 3
KICK_RANGE_THRESH = 3 * MAX_DRIBBLE_RANGE
THRES = 0.8
THETA_THRESH = 0.005
SHIFT = (HALF_FIELD_MAXX/9.0)

class TGoalie(Tactic):
	def __init__(self,botID,state,params=None):
		self.botID = botID
		self.ballAim = Vector2D()
		self.goalieTarget = Vector2D()
		self.ballPos = Vector2D(state.ballPos.x, state.ballPos.y)
		self.botPos = Vector2D(state.homePos[botID].x, state.homePos[botID].y)
		self.ballVel = Vector2D(state.ballVel.x , state.ballVel.y)
		self.sParams = skills_union.SParam()

	def execute(self,state , params, pub):
		dist = self.ballPos.dist(self.botPos)
		'''		
		if(sqrt(self.ballVel.absSq()) < 0.02*MAX_BOT_SPEED and  fabs(state.ballPos.y) < OUR_GOAL_MAXY and state.ballPos.x > (HALF_FIELD_MAXX- (2 * DBOX_WIDTH) (HALF_FIELD_MAXX/5.0)):
		'''
		if(sqrt(self.ballVel.absSq()) < 0.02*MAX_BOT_SPEED and fabs(state.ballPos.y) < OUR_GOAL_MAXY and state.ballPos.x > HALF_FIELD_MAXX - HALF_FIELD_MAXX/5.0):
		   if (dist >= DRIBBLER_BALL_THRESH):
			   self.sParams.GoToPoint.x = state.ballPos.x
			   self.sParams.GoToPoint.y = state.ballPos.y
			   self.sParams.GoToPoint.finalVelocity = 0
			   self.sParams.GoToPoint.finalslope = atan((state.ballPos.y - state.homePos[self.botID].y) , (state.ballPos.x - state.homePos[self.botID].x))
			   sGoToPoint.execute(self.sParams, state, self.botID, pub)
			   return
		   else:
			   self.sParams.Kick.power = 7.0
			   sKick.execute(self.sParams, state , self.botID, pub)
			   
		default_x = HALF_FIELD_MAXX + SHIFT
		
		if(state.ballPos.x >  (HALF_FIELD_MAXX - SHIFT) and state.ballPos.x < HALF_FIELD_MAXX):
			self.goalieTarget.x = HALF_FIELD_MAXX -SHIFT
		else:
			self.goalieTarget  = default_x
		
		striker = -1
		striker_dist = inf


		for oppID in xrange(5):
			if oppID == botID :
				continue
			oppPos = Vector2D(state.homePos[oppID].x, state.homePos[oppID].y)
			kick_range_test = sqrt((oppPos-self.ballPos).absSq())

			if(kick_range_test < KICK_RANGE_THRESH and kick_range_test < striker_dist):
					striker = oppID
					striker_dist = kick_range_test
		if(striker is not -1):
			goalieTarget.y = ( ((state.ballPos.y - state.homePos[striker].y) / (state.ballPos.x - state.homePos[striker].x)) * (goalieTarget.x - state.ballPos.x) ) + state.ballPos.y
		else :
			if(state.ballVel.x == 0):
				goalieTarget.y = state.ballPos.y
			else:
				if state.ballVel.x > 0:
					self.goalieTarget.y = (( state.ballVel.y / state.ballVel.x ) * ( self.goalieTarget.x \
					- state.ballPos.x ) ) + state.ballPos.y
				else:
					self.goalieTarget.y = 0
		if self.goalieTarget.y < OUR_GOAL_MINY/1.2 :
			self.goalieTarget.y = OUR_GOAL_MINY/1.2
		elif self.goalieTarget.y > OUR_GOAL_MAXY/1.2 :
			self.goalieTarget.y = OUR_GOAL_MAXY/1.2

		self.sParams.GoToPoint.x = goalieTarget.x
		self.sParams.GoToPoint.y = goalieTarget.y
		self.sParams.GoToPoint.finalVelocity = 0
		self.sParams.GoToPoint.finalslope = atan((state.ballPos.y - state.homePos[botID].y) , (state.ballPos.x - state.homePos[botID].x))
		sGoToPoint.execute(self.sParams, state, self.botID, pub)

	def isComplete(self, state):
		return False

	def updateParams(self, state):
		pass
