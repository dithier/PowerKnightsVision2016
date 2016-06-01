import math

#distance to goal
distY = 85 #inches

#Goal dimensions
goalHeight = 24
goalWidth = 16

#tape dimensions
tapeHeight = 12
tapeWidth = 20
tapeEndMargin = 2

#ball dimensions
ballRadius = 5 #inches
ballDiameter = 10

#FOV, swapped because the camera is rotated 90 degrees on the robot
horizontalFOV = 36.5
verticalFOV = 47.0

#TODO find actual values

#Triangle to goal
#		  *		<-Robot
#		 /|\    
#		/ | \
#	   /  |  \  <-longLeg (side)
#	  /___|___\ <-shortLeg(bottom)
#longLeg = distD / math.cos(angleError)
#shortLeg = 2 * math.sin(angleError) * distD

#distX = distance along the ground to the goal
#correction = buffer on either ends of the goal to get the correct allowed width of the target for aiming
def calc_angle(distX, correction):	
	distD = math.sqrt(distX**2 + distY**2)

	angleError = math.atan(goalWidth / 2 / distD)
	correctedAngleError = math.atan((goalWidth - correction) / 2 / distD)

	return correctedAngleError, correctedAngleError * 180.0 / math.pi

def main():
	while True:
		distX = raw_input("Enter a distance from the goal to the robot in inches: ")
		correction = raw_input("Enter a correction amount in inches (suggested 10.5-12): ")
		correctAngleR, correctAngleD = calc_angle(int(distX), float(correction))
		print("Your corrected angle is [" + str(correctAngleR) + " radians|" + str(correctAngleD) + " degrees]\n")


if __name__ == "__main__":
	main()
