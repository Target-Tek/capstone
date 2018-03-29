from math import pi, sin, cos, atan, atan2, sqrt
from numpy import array, matmul

pi = 3.14159265358979 #better accuracy value for pi

#===================test values=======================
plat = 41.590833
plon = -111.3952778
palt = 5281

roll = 3
pitch = -10
heading = 140

t1lat = 42.6049294
t1lon = -113.8423461
t1alt = 12000

t2lat = 43.3831003
t2lon = -109.9647447
t2alt = 12000

t3lat = 39.6328939
t3lon = -112.3186589
t3alt = 12000

t4lat = 40.5264822
t4lon = -109.0257347
t4alt = 12000

pTESTlat = 40.236283
pTESTlon = -111.694184
pTESTalt = 4468.02822

tarTESTlat = 40.2361734
tarTESTlon = -111.6946300
tarTESTalt = 4469.72769

TESTroll = 0
TESTpitch = 0
TESTheading = 0
#=====================================================

#================for testing purposes=================
class CreateLLA:
	def __init__(self,lat, lon, alt):
		self.lat = lat
		self.lon = lon
		self.alt = alt

class CreateAngles:
	def __init__(self,roll, pitch, heading):
		self.roll = roll
		self.pitch = pitch
		self.heading = heading
#====================================================

class Angles:
	def __init__(self,angles):
		self.rollD = angles.roll
		self.pitchD = angles.pitch
		self.headingD = angles.heading
		self.rollR = angles.roll*pi/180
		self.pitchR = angles.pitch*pi/180
		self.headingR = angles.heading*pi/180

	def display(self):
		print('degrees')
		print(self.rollD)
		print(self.pitchD)
		print(self.headingD)
		print('radians')
		print(self.rollR)
		print(self.pitchR)
		print(self.headingR)

class LLA:
	def __init__(self,llacoords):
		self.latD = llacoords.lat
		self.lonD = llacoords.lon
		self.altFt = llacoords.alt
		self.latR = llacoords.lat*pi/180
		self.lonR = llacoords.lon*pi/180
		self.altM = llacoords.alt*.3048

	def display(self):
		print('degrees:')
		print(self.latD)
		print(self.lonD)
		print(self.altFt)
		print('radians:')
		print(self.latR)
		print(self.lonR)
		print(self.altM)

class ECEFvector:
	WGS84_a = 6378137 #semi-major
	WGS84_b = 6356752.3149622 #semi-minor
	WSG84_f = .0033528105523341 #flattening
	#N = not sure if needed...

	def N_val(self, latD):
		output= self.WGS84_a**2/sqrt(self.WGS84_a**2*(cos(latD*pi/180))**2 + self.WGS84_b**2*(sin(latD*pi/180))**2)	#this line might have problems
		return output

	def __init__(self, llacoord):
		self.x = (self.N_val(llacoord.latD) + llacoord.altM)*cos(llacoord.latR)*cos(llacoord.lonR)
		self.y = (self.N_val(llacoord.latD) + llacoord.altM)*cos(llacoord.latR)*sin(llacoord.lonR)
		self.z = ((self.WGS84_b**2/self.WGS84_a**2)*self.N_val(llacoord.latD)+llacoord.altM)*sin(llacoord.latR)#!!!The resulting vector component is incorrect


	def display(self):
		#print('ECEF vector')
		print(self.x)
		print(self.y)
		print(self.z)

class LOSvector:
	def __init__(self, pedestalECEF, targetECEF):
		self.x = targetECEF.x-pedestalECEF.x
		self.y = targetECEF.y-pedestalECEF.y
		self.z = targetECEF.z-pedestalECEF.z

	def display(self):
		#print('LOS vector')
		print(self.x)
		print(self.y)
		print(self.z)

class LLvector:
	def __init__(self, tarLOS, pedLLA):
		self.rotMatrix = array([[-sin(pedLLA.latR)*cos(pedLLA.lonR), -sin(pedLLA.latR)*sin(pedLLA.lonR), cos(pedLLA.latR)],[-sin(pedLLA.lonR), cos(pedLLA.lonR), 0],[-cos(pedLLA.latR)*cos(pedLLA.lonR), -cos(pedLLA.latR)*sin(pedLLA.lonR), -sin(pedLLA.latR)]])
		LOSmatrix = array([[tarLOS.x],[tarLOS.y],[tarLOS.z]])
		self.LLmatrix = matmul(self.rotMatrix,LOSmatrix)
		self.xLL = self.LLmatrix[0,0]
		self.yLL = self.LLmatrix[1,0]
		self.zLL = self.LLmatrix[2,0]

	def display(self):
		#print('LLvector')
		print(self.LLmatrix)

	def displayRotMatrix(self):
		print('rotMatrix')
		print(self.rotMatrix)

class PBvector:
	def __init__(self,LLvector,angles):
		self.rollMatrix = array([[1,0,0],[0,cos(angles.rollR),sin(angles.rollR)],[0,-sin(angles.rollR),cos(angles.rollR)]])
		self.pitchMatrix = array([[cos(angles.pitchR),0,-sin(angles.pitchR)],[0,1,0],[sin(angles.pitchR),0,cos(angles.pitchR)]])
		self.headingMatrix = array([[cos(angles.headingR),sin(angles.headingR),0],[-sin(angles.headingR),cos(angles.headingR),0],[0,0,1]])
		self.PBmatrix = matmul(matmul(matmul(self.rollMatrix,self.pitchMatrix),self.headingMatrix),LLvector.LLmatrix)
		self.xPB = self.PBmatrix[0,0]
		self.yPB = self.PBmatrix[1,0]
		self.zPB = self.PBmatrix[2,0]

	def display(self):
		print('PBmatrix')
		print(self.PBmatrix)

class Solution:
	def __init__(self, LLvector, PBvector):
		total = 0
		for x in range(len(LLvector.LLmatrix)):
			total = total + LLvector.LLmatrix[x,0]**2
		self.rangeNmi = sqrt(total)/1852
		self.range = self.range*6076.11549
		if (atan2(LLvector.yLL,LLvector.xLL)*180/pi) < 0:
			self.trueAz = atan2(LLvector.yLL,LLvector.xLL)*180/pi+360
		else:
			self.trueAz = atan2(LLvector.yLL,LLvector.xLL)*180/pi
		self.trueEl = (atan(-LLvector.zLL/(sqrt(LLvector.xLL**2 + LLvector.yLL**2))))*180/pi
		if (atan2(PBvector.yPB,PBvector.xPB)*180/pi) < 0:
			self.relAz = atan2(PBvector.yPB,PBvector.xPB)*180/pi+360
		else:
			self.relAz = atan2(PBvector.yPB,PBvector.xPB)*180/pi
		self.relEl = (atan(-PBvector.zPB/(sqrt(PBvector.xPB**2 + PBvector.yPB**2))))*180/pi

	def display(self):
		print('Range = ' + str(self.range) + ' feet')  #change to self.rangeNmi if you want to display Nmi units
		print('True Az = ' + str(self.trueAz) + ' degrees')
		print('True El = ' + str(self.trueEl) + ' degrees')
		print('Rel Az = ' + str(self.relAz) + ' degrees')
		print('Rel El = ' + str(self.relEl) + ' degrees')

	def getRange(self):
		return self.range

	def getTrueAz(self):
		return self.trueAz

	def getTrueEl(self):
		return self.trueEl

	def getRelAz(self):
		return self.trueAz

	def getRelEl(self):
		return self.RelEl

class AzEl:
	def __init__(self, pedestal, angles, target):
		self.pedLLA = LLA(pedestal)
		self.pedAngles = Angles(angles)
		self.tarLLA = LLA(target)
		self.pedECEF = ECEFvector(self.pedLLA)
		self.tarECEF = ECEFvector(self.tarLLA)
		self.tarLOS = LOSvector(self.pedECEF,self.tarECEF)
		self.tarLL = LLvector(self.tarLOS,self.pedLLA)
		self.tarPB = PBvector(self.tarLL,self.pedAngles)
		self.tarSol = Solution(self.tarLL,self.tarPB)

	def displaySol(self):
		print('Target Solutions')
		self.tarSol.display()

	def getRange(self):
		return self.range.getRange()

	def getTrueAz(self):
		return self.tarSol.getTrueAz()

	def getTrueEl(self):
		return self.tarSol.getTrueEl()

	def getRelAz(self):
		return self.tarSol.getRelAz()

	def getRelEl(self):
		return self.tarSol.getRelEl()

print('-----------Starting script-----------')
#=============for testing purposes===================
ped_lla = CreateLLA(plat,plon,palt)
tar1_lla = CreateLLA(t1lat,t1lon,t1alt)
tar2_lla = CreateLLA(t2lat,t2lon,t2alt)
tar3_lla = CreateLLA(t3lat,t3lon,t3alt)
tar4_lla = CreateLLA(t4lat,t4lon,t4alt)
ped_angles = CreateAngles(roll, pitch, heading)
pedTEST_lla = CreateLLA(pTESTlat, pTESTlon, pTESTalt)
tarTEST_lla = CreateLLA(tarTESTlat,tarTESTlon,tarTESTalt)
pedTEST_angles = CreateAngles(TESTroll,TESTpitch,TESTheading)
sol1 = AzEl(ped_lla,ped_angles,tar1_lla)
sol2 = AzEl(ped_lla,ped_angles,tar2_lla)
sol3 = AzEl(ped_lla,ped_angles,tar3_lla)
sol4 = AzEl(ped_lla,ped_angles,tar4_lla)
solTEST = AzEl(pedTEST_lla,pedTEST_angles,tarTEST_lla)
sol1.displaySol()
sol2.displaySol()
sol3.displaySol()
sol4.displaySol()
solTEST.displaySol()
#====================================================
print('------------Ending script------------')
