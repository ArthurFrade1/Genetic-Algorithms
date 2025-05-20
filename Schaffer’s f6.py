import random
import math

numberOfPoints = 100                # tamanho da população
points = []                         # população
sumImage = 0                        # soma das imagens da população
generations = 100                   # número de gerações

class Point:
    def __init__(self):
        self.coord=[]
        self.image = 0
   
    def addPoint(self, x1, x2):
        self.coord.append(x1)
        self.coord.append(x2)

    def getPoint(self, index):
        return self.coord[index]
       

def schaffers_f6(x):
    x1, x2 = x[0], x[1]
    numerator = math.sin(math.sqrt(x1**2 + x2**2))**2 - 0.5
    denominator = (1 + 0.001 * (x1**2 + x2**2))**2
    return 0.5 - numerator / denominator

# gera população inicial
def firstPopulation():
    for i in range (numberOfPoints):
        # coordenada aléatoria entre -10 e 10
        point = Point()
        x1 = random.uniform(-10, 10)
        x2 = random.uniform(-10, 10)
        point.addPoint(x1, x2)

        point.image = schaffers_f6([x1, x2])
        points.append(point)

def selection():
    total = sum(point.image for point in points)
    n = random.uniform(0, total)
    soma = 0
    for point in points:
        soma += point.image
        if soma >= n:
            return point
    return points[-1]

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
        # media das coordenadas dos pais
        x1 = (pointFather.coord[0] + pointMother.coord[0]) / 2
        x2 = (pointFather.coord[1] + pointMother.coord[1]) / 2

        pointChild.image = schaffers_f6([x1, x2])
        pointChild.addPoint ( x1, x2)
        newGeneration.append(pointChild)
   
    points = newGeneration.copy()

    # Recalcula a imagem após mutar
    point.image = schaffers_f6(point.coord)

print("F([0,0]) é:",schaffers_f6([0,0]))

# gerar população inicial
firstPopulation()

# escreve os pontos iniciais
print("Geração: 1")
contador_ponto = 1
for point in points:
    print(f"Ponto: {contador_ponto}")
    print(f"x1: {point.getPoint(0):.3f}")
    print(f"x2: {point.getPoint(1):.3f}")
    print(f"Imagem: {point.image:.3f}")
    contador_ponto+=1

# gera as pŕoximas gerações
contador_geração = 2
for i in range (generations):
    soma=0
    print("---------------\nGeração:", contador_geração)
    crossover()
    contador_ponto = 1
    for point in points:
        print(f"Ponto: {contador_ponto}")
        print(f"x1: {point.getPoint(0):.3f}")
        print(f"x2: {point.getPoint(1):.3f}")
        print(f"Imagem: {point.image:.3f}")
        soma+=point.image

        contador_ponto+=1
    print(f"\033[91mMedia: {soma/numberOfPoints:.2f}\033[0m")
    print("Melhor:")
    print(f"\033[91mX: {elitePoint.coord[0]:.2f}\033[0m")
    print(f"\033[91mY: {elitePoint.coord[1]:.2f}\033[0m")
    print(f"\033[91mImagem: {elitePoint.image:.2f}\033[0m")
