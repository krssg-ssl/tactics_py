from tactic import Tactic
import time
import sys

sys.path.append('/home/ss/robocup/src/skills_py/scripts/skills')
sys.path.append('/home/ss/robocup/src/plays_py/scripts/utils/')
from geometry import Vector2D 
import skills_union

class TKickToGoal(Tactic):
	def __init__(self, bot_id, state, param=None):
		super(TPosition, self).__init__( bot_id, state, param)
		self.sParam = skills_union.SParam()
		self.destination = Vector2D(int(self.param.PositionP.x), int(self.param.PositionP.y))
		self.threshold = 20.0

	def execute(self, state, pub):
	  
	  ballPos=Vector2D(state.ballPos.x, state.ballPos.y)
	  botPos=Vector2D(state.homePos[bot_id].x, state.homePos[bot_id].y)
	  oppPos=[]    # array storing positions of opponents
	  for i in xrange(0,6):
	    oppPos.append([state.awayPos[i].x,state.awayPos[i].y])
	  dist=ballPos.dist(botPos)
	  
	  goalMax=Vector2D(HALF_FIELD_MAXX, OPP_GOAL_MAXY)
	  goalMin=Vector2D(HALF_FIELD_MAXX, OPP_GOAL_MINY)
	  angleMax = goalMax.angle(botPos)
	  angleMin = goalMin.angle(botPos)
    
    	  destination=Vector2D()
	  iState=""
	  if (dist >= DRIBBLER_BALL_THRESH):
      		iState="GO TO BALL"
    	  elif(state.homePos[bot_id].theta >= angleMax or state.homePos[botID].theta <= angleMin):
      		iState = "DRIBBLE AND TURN"
     	   #f<< "TURN TO FACE BALL THEN DRIBBLE TURN TO FACE GOAL\n";
	  else:
	    # Shoot
	    Angles=[]
	    for opp in oppPos:
	      Angles.append(opp.angle(botPos))
	    flag=True; maxmin=0
	    while(1):
	      for angle in Angles:
	        if angle<=angleMax and angle>=angleMin:
	          flag=False
	        if angle>angleMax and angle<angleMin:
	          angleMax, angleMin=angleMin, angleMax
	          maxmin=1
	      if maxmin==0: break
	    if flag==False:
	      iState="CANT SHOOT"
	    else:
	      ballangle=ballPos.angle(botPos)
	      if ballangle<=angleMax and ballangle>=angleMin:
	        iState("SHOOT")
	      else:
	        iState("TURN TO BALL")
	    
	  if iState=="GO TO BALL":
	    self.sParam.GoToPointP.x = ballPos.x
	    self.sParam.GoToPointP.y = ballPos.y
	    self.sParam.GoToPointP.align = True # needs verification
	    import sGoToPoint
	    sGoToPoint.execute(self.sParam, state, self.bot_id, pub)
	    
	  elif iState=="DRIBBLE AND TURN":
	    # first sDribbleTurn needs to be rectified
	    pass
	    
	  elif iState=="TURN TO BALL":
	    self.sParam.TurnToAngleP.finalslope=ballPos.angle(botPos)
	    import sTurnToAngle
	    sTurnToAngle.execute(self.sParam, state, self.bot_id, pub)
	    
	  elif iState=="SHOOT":
      		self.Sparam.KickToPointP = Vector2D(HALF_FIELD_MAXX, (OPP_GOAL_MAXY+OPP_GOAL_MINY)/2)
     		import sKickToPoint
      		sKickToPoint.execute(self.sParam, state, self.bot_id, pub)
    	  else:
     	    #Yet to be written
     	     pass
		
		
		
	def isComplete(self, state):
		# TO DO use threshold distance instead of actual co ordinates
		if ballPos.x>=HALF_FIELD_MAXX and ballPos.y >= OPP_GOAL_MAXY and ballPos.y <= OPP_GOAL_MINY:
			return True
		elif time.time()-self.begin_time > self.time_out:
			return True
		else:
			return False

	def updateParams(self, state):
		# No parameter to update here
		pass
