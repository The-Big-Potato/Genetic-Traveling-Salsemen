import random

#DistanceMatrix is used to create a dict object that acts as the distance matrix.
#This stores the cities and the cost or distance to get from one city to another.
class DistanceMatrix:
	def __init__(self):
		self.pathMatrix = {}

	#setTripCost is used to populate the matrix with the cities and the distances.
	#This is done through using nested dict objects.
	#Note that entering in the cost for going from city A to B also enters in the cost
	# for going from city B to A.
	def setTripCost(self, city, otherCity, units):
		if city not in self.pathMatrix.keys():
			self.pathMatrix[city] = {}
		if otherCity not in self.pathMatrix.keys():
			self.pathMatrix[otherCity] = {}

		self.pathMatrix[city][otherCity] = units
		self.pathMatrix[otherCity][city] = units
		return self

	#getTripCost is used to calcualte the distance or cost of a trip and returns it.
	def getTripCost(self, path):
		pathCost = 0
		for city, otherCity in zip(path, path[1:]):
			pathCost += self.pathMatrix[city][otherCity]
		return pathCost

	#printMatrix prints out the matrix. Note that there is no distance from a city to itself.
	#Since it would be pointless, that distance is not added.
	def printMatrix(self):
		for city in self.getCities():
			for otherCity in self.pathMatrix[city]:
				print('[',city, '->', otherCity,':',self.pathMatrix[city][otherCity],']', end = " ")
			print('\n')
	
	#getCities returns a list of all the keys, in this case the cities in the matrix.
	def getCities(self):
		return list(self.pathMatrix.keys())


class TravelingSalesmenGenetic:
	#There are four values that must be passed to initilize the class:
	# generations: The number of generations to be created for testing.
	# numTrips: The number of trips per generation.
	# mutationRate: A value from 0.0 to 1.0, determines the percentage chance of a mutation to occur in a child.
	# pathMatrix: The matrix containing the distance data. 
	def __init__(self, generations, numTrips, mutationRate, pathMatrix):
		self.generations = generations
		self.numTrips = numTrips
		self.mutationRate = mutationRate
		self.pathMatrix = pathMatrix

	#findShortestPath is the main function of the class.
	#It accepts a distance matrix of the type DistanceMatrix, simulates multiple generations, 
	# and returns the shortest trip found along with its cost.
	def findShortestPath(self):
		self.pathMatrix.printMatrix()
		
		#Generating the first generation of trips to test
		roundTrips = self.generateTrips(self.pathMatrix.getCities())

		for genNum in range(self.generations):
			print(' ')
			print ('Generation: ',(genNum + 1))
			print ('Round Trips: ',roundTrips)

			fitness = self.measureFitness(roundTrips)
			mostFit = fitness.index(min(fitness))
			print ('Trip Costs:  ',fitness)
			print ('Shortest Trip: ',roundTrips[mostFit], ', Trip Cost: ', fitness[mostFit])

			#generating a new list of trips from the previous generation of trips
			newRoundTrips = []
			for i in range(self.numTrips):
				parentA = self.selectParent(roundTrips)
				parentB = self.selectParent(roundTrips)
				child = self.crossover(parentA, parentB)
				newRoundTrips.append(child)

			#running the mutation function on the round trips
			for j in range(self.numTrips):
				newRoundTrips[j] = self.mutate(newRoundTrips[j])

			roundTrips = newRoundTrips

		return (roundTrips[mostFit], fitness[mostFit])


	#fitness function
	#measureFitness accepts a list of trips and the distance matrix and returns a list of the costs or distance of the trips.
	#A smaller number means the trip is considered more "fit". 
	def measureFitness(self, roundTrips):
		fitnessList = []
		for path in roundTrips:
			fitnessList.append(self.pathMatrix.getTripCost(path))
		return fitnessList

	#selectParent semi-randomly selects a parent to help produce offspring.
	#From roundTrips, about 1/3 (at least one) of the trips are randomly selected.
	#From the trips selected, the most fit trip(the one with the smallest cost) is chosen as the parent and is returned.
	def selectParent(self, roundTrips): # 1/3rd chosen
		size = len(roundTrips)//3
		if size<1:
			size = 1
		
		potentialParent = random.choices(roundTrips, k = size)
		parentFitness = self.measureFitness(potentialParent)
		
		return potentialParent[parentFitness.index(min(parentFitness))]

	#crossover is used to generate a child from two parents. 
	#A child is created with blank spaces is created same size as the parents.
	#From parentA, a subset of random size(2 elements min) is taken. This is placed in the same index location as parentA.
	#For every blank space in the child, an element from parentB is placed in it if it is not already present.
	def crossover(self, parentA, parentB):
		child = []
		for i in range(len(parentA)):
			child.append('')
			
		lowBound, highBound = self.generateTripBounds(parentA)

		child[lowBound:highBound+1] = list(parentA)[lowBound:highBound+1]
		childRemainder = list(range(0, lowBound)) + list(range(highBound+1, len(parentA)))
		for city in parentB:
			if '' not in child:
				break
			if city not in child:
				child[childRemainder.pop(0)] = city
		return ''.join(child)

	#mutate function
	#mutate is used to alter children and add randomness to the child creation process.
	#The mutationRate adjusts the rate of mutations occuring in teh children. 
	#A low index and a high index is generated. The values at these two locations are swapped.
	#The new trip is returned.
	def mutate(self, trip):
		if random.uniform(0.0,1.0) < self.mutationRate:
			lowIndex,highIndex = self.generateTripBounds(trip)
			temp = list(trip)
			temp[lowIndex],temp[highIndex] = temp[highIndex],temp[lowIndex]
			return ''.join(temp)
		else:
			return trip

	#generateTrips generates the first generation of trips to be tested.
	#Gets the list of cities, shuffles them, joins them together into one string, adds to a list. Returns list.
	def generateTrips(self, city):
		trip = []
		for i in range(self.numTrips):
			trip.append(''.join(random.sample(city,len(city))))
		return trip

	#generateBounds returns two index values, one lower and one higher, within the bounds of trip.
	#This is used for the crossver and mutate functions.
	def generateTripBounds(self, trip):
		lowBound = random.randint(0, len(trip)-2)
		highBound = random.randint(lowBound+1, len(trip)-1)
		
		while highBound - lowBound > (len(trip)//2):
			try:
				lowBound = random.randint(0, len(trip)-1)
				highBound = random.randint(lowBound+1, len(trip)-1)
			except ValueError:
				pass
		return (lowBound, highBound)




pathMatrix = DistanceMatrix()

pathMatrix.setTripCost('1', '2', 2)
pathMatrix.setTripCost('1', '3', 11)
pathMatrix.setTripCost('1', '4', 3)
pathMatrix.setTripCost('1', '5', 18)
pathMatrix.setTripCost('1', '6', 14)
pathMatrix.setTripCost('1', '7', 20)
pathMatrix.setTripCost('1', '8', 12)
pathMatrix.setTripCost('1', '9', 5)
pathMatrix.setTripCost('2', '3', 13)
pathMatrix.setTripCost('2', '4', 10)
pathMatrix.setTripCost('2', '5', 5)
pathMatrix.setTripCost('2', '6', 3)
pathMatrix.setTripCost('2', '7', 8)
pathMatrix.setTripCost('2', '8', 20)
pathMatrix.setTripCost('2', '9', 17)
pathMatrix.setTripCost('3', '4', 5)
pathMatrix.setTripCost('3', '5', 19)
pathMatrix.setTripCost('3', '6', 21)
pathMatrix.setTripCost('3', '7', 2)
pathMatrix.setTripCost('3', '8', 5)
pathMatrix.setTripCost('3', '9', 8)
pathMatrix.setTripCost('4', '5', 6)
pathMatrix.setTripCost('4', '6', 4)
pathMatrix.setTripCost('4', '7', 12)
pathMatrix.setTripCost('4', '8', 15)
pathMatrix.setTripCost('4', '9', 1)
pathMatrix.setTripCost('5', '6', 12)
pathMatrix.setTripCost('5', '7', 6)
pathMatrix.setTripCost('5', '8', 9)
pathMatrix.setTripCost('5', '9', 7)
pathMatrix.setTripCost('6', '7', 19)
pathMatrix.setTripCost('6', '8', 7)
pathMatrix.setTripCost('6', '9', 4)
pathMatrix.setTripCost('7', '8', 21)
pathMatrix.setTripCost('7', '9', 13)
pathMatrix.setTripCost('8', '9', 6)


#TravelingSalesmenGenetic(number of generations, population per generation, mutation rate (0.0 to 1.0))
shortestTrip, shortestTripCost = TravelingSalesmenGenetic(5,6,0.3,pathMatrix).findShortestPath()
print (' ')
print ('Shortest Trip:',shortestTrip, '| Trip Cost:',shortestTripCost)

#Running program 12 times with different values for generations and population per generations (all have mutation rate of 0.3)

#4,6 Shortest Trip: 386942175 | Trip Cost: 36
#4,6 Shortest Trip: 731846592 | Trip Cost: 71
#8,6 Shortest Trip: 641385297 | Trip Cost: 61
#8,6 Shortest Trip: 385769421 | Trip Cost: 49
#10,6 Shortest Trip: 973865241 | Trip Cost: 59
#10,6 Shortest Trip: 962547831 | Trip Cost: 40

#4,8 Shortest Trip: 619473258 | Trip Cost: 50
#4,8 Shortest Trip: 851732496 | Trip Cost: 48
#8,8 Shortest Trip: 785693142 | Trip Cost: 56
#8,8 Shortest Trip: 856143927 | Trip Cost: 42
#10,8 Shortest Trip: 852469731 | Trip Cost: 38
#10,8 Shortest Trip: 857394621 | Trip Cost: 35

#Of the 12 test runs, best result is:
#10,8 Shortest Trip: 857394621 | Trip Cost: 35

#More generations and higher populations appear to generate better results, may then be limited by computer memory and processing time.
#Inherit randomness of genetic algorithims means that multiple runs of program must be done.
#Some runs may be worse or better than other by chance.
#Seeding first generation with known good paths may improve perfomance vs using random values.



