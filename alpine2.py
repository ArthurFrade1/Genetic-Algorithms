import random
import math

numberOfPoints = 100
points = []
sumImage = 0
generations = 100

class Point:
    def __init__(self):
        self.coord=[]
        self.image = 0
    
    def addPoint(self, x1, x2):
        self.coord.append(x1)
        self.coord.append(x2)

    def getPoint(self, index):
        return self.coord[index]
        
def alpine2(x):
    return sum(math.sqrt(abs(xi)) * math.sin(xi) for xi in x)

def firstPopulation():
    
    for i in range (numberOfPoints):
        # Calcula ponto coordenada aléatoria entre 0 e 10
        point = Point()
        x1 = random.uniform(0, 10)
        x2 = random.uniform(0, 10)
        point.addPoint(x1, x2)

        point.image = alpine2([x1, x2])
        points.append(point)

def selection():
    total = sum(point.image for point in points)
    n = random.uniform(0, total)
    soma = 0
    for point in points:
        soma += point.image
        if soma >= n:
            return point
    return points[-1]  # fallback (caso nenhuma seja retornada)

def mutation(point, mutation_rate=0.01, mutation_strength=1):
    # Para cada coordenada, com uma certa chance, aplica uma pequena alteração
    for i in range(len(point.coord)):
        if random.random() < mutation_rate:
            mutation = random.uniform(-mutation_strength, mutation_strength)
            point.coord[i] += mutation

            # Garante que continue no intervalo válido (0 a 10)
            point.coord[i] = max(0, min(10, point.coord[i]))

    # Recalcula a imagem após mutar
    point.image = alpine2(point.coord)

elitePoint = Point()
def crossover():
    global points, sumImage
    newGeneration = []

    global elitePoint
    elitePoint = points[0]
    for point in points:
        if point.image > elitePoint.image:
            elitePoint = point

    newGeneration.append(elitePoint)

    while len(newGeneration) < numberOfPoints:
        # Seleciona pais
        pointFather = selection()
        pointMother = selection()
        pointChild = Point()
        #Troca de genes, media das coordenadas dos pais
        x1 = (pointFather.coord[0] + pointMother.coord[0]) / 2
        x2 = (pointFather.coord[1] + pointMother.coord[1]) / 2

        pointChild.image = alpine2([x1, x2])
        pointChild.addPoint ( x1, x2)
        mutation(pointChild)
        newGeneration.append(pointChild)

    points = newGeneration.copy()

firstPopulation()

for i in range (generations+1):
    soma=0
    print("---------------")
    count = 1
    for point in points:
        print(f"Ponto: {count}")
        print(f"x1: {point.getPoint(0):.3f}")
        print(f"x2: {point.getPoint(1):.3f}")
        print(f"image: {point.image:.3f}")
        soma+=point.image

        count+=1
    print(f"\033[91mMelhor: {elitePoint.image:.2f}\033[0m")
    crossover()