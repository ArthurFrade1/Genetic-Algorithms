import random
# What's the sense :/
# Problem configuration
capacity = 50
itens = 30
maxWeightItens = 20
minValueItens = 10
maxValueItens = 100

# Problem variables

backpacks = []
quantityBackpacks = 50
sumPontuation = 0
generations = 100

class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value
        self.numberItens = 0

class Backpack:
    def __init__(self):
        self.itens = []
        self.sumValue = 0 
        self.sumWeight = 0
        self.pontuation = 0
        self.numberItens = 0

    def addItem(self, item):
        self.sumValue += item.value
        self.sumWeight += item.weight 
        self.numberItens += 1
        self.itens.append(item)

    def getItem(self, index):
        return self.itens[index]

def createItem(): #Definindindo o peso e o valor aleatoriamente

    weight = random.randint(1, maxWeightItens) 
    value = random.randint(minValueItens, maxValueItens)

    return Item(weight, value)

def fitness(backpack): # Avalia o quanto pontua
    backpack.pontuation = backpack.sumValue
    
def firstPopulation():
    global sumPontuation
    while len(backpacks) < quantityBackpacks:

        backpack = Backpack()
        numberItens = random.randint(1, itens) # Crio o número de itens aleatoriamente

        for j in range(numberItens): # Rodar o número de itens
            item = createItem() # Crio o número item de itens e incluo no objeto 
            backpack.addItem(item)

        if backpack.sumWeight <= capacity: # Adiciono na população somente as mochilas que tem a capacidade inferior a determinada
            backpacks.append(backpack)

            fitness(backpack) # Com a backback incluida na população, faço a avaliação da sua pontuação
            sumPontuation += backpack.pontuation

def selection(): # Seleciona os pais a partir da seleção por roleta
    n = random.uniform(0, sumPontuation)
    soma =0 
    for backpack in backpacks:
        soma+=backpack.pontuation
        if soma>=n:
            return backpack

def mutation(backpack, mutation_rate=0.1):

    if random.random() > mutation_rate:
        return backpack  # não ocorre mutação

    if backpack.numberItens <= 1:
        return backpack  # Não dá pra mutar com menos de 2 itens

    # Seleciona dois índices distintos
    index1 = random.randint(0, backpack.numberItens - 1)
    index2 = random.randint(0, backpack.numberItens - 1)
    while index2 == index1:
        index2 = random.randint(0, backpack.numberItens - 1)

    # Faz o swap
    temp1 = backpack.getItem(index1)
    temp2 = backpack.getItem(index2)

    backpack.itens[index1] = temp2
    backpack.itens[index2] = temp1

    return backpack

eliteBackpack = Backpack()
        
def crossover(): # Seleciona os pais e cruza os genes(no caso, itens)
    newGenBackpacks = []
    newSumPontuation=0
    global backpacks

    global eliteBackpack
    eliteBackpack = backpacks[0]
    for backpack in backpacks:
        if backpack.pontuation > eliteBackpack.pontuation:
            eliteBackpack = backpack
    
    newGenBackpacks.append(eliteBackpack)
    newSumPontuation+=eliteBackpack.pontuation

    while len(newGenBackpacks) < quantityBackpacks: # Faz o crossover pra obter o mesmo número de backpacks que tinha antes
        backpackFather = selection()
        backpackMother = selection()
        backpackChildren = Backpack()

        minCount = 0
        parent = ""
        if backpackFather.numberItens <= backpackMother.numberItens:
            minCount  = backpackFather.numberItens
            parent = "mother"
        if backpackMother.numberItens < backpackFather.numberItens:
            minCount  = backpackMother.numberItens
            parent = "father"

        cutPoint = random.randint(0, minCount) #Cria o ponto de corte aleatoriamente
         
        #Pega os itens do pai que estão antes do cutPoit e os da mãe que estão depois
        cutPointFather = 0
        while cutPointFather < cutPoint:
            backpackChildren.addItem(backpackFather.getItem(cutPointFather))
            cutPointFather+=1

        cutPointMother = cutPoint
        while cutPointMother < minCount:
            backpackChildren.addItem(backpackMother.getItem(cutPointMother))
            cutPointMother+=1

        #Momento de colocar os itens do parent dominante faltante
        i = minCount
        if parent == "father":
            while i  < (len(backpackFather.itens)):
                backpackChildren.addItem(backpackFather.itens[i])
                i+=1

        if parent == "mother":
            while i < (len(backpackMother.itens)):
                backpackChildren.addItem(backpackMother.itens[i])
                i+=1


        if backpackChildren.sumWeight < capacity :

            backpackChildren = mutation(backpackChildren)
            newGenBackpacks.append(backpackChildren) #Adiciona filho na nova geração
            fitness(backpackChildren) # Com a backback incluida na população, faço a avaliação da sua pontuação
            newSumPontuation += backpackChildren.pontuation
    
    global sumPontuation
    sumPontuation =newSumPontuation
    backpacks = newGenBackpacks.copy() # Geração atual recebe nova geração 

firstPopulation()

for i in range(generations+1):
    conta=1
    mediaPontuation = 0
    print("-------")
    for backpack in backpacks: 
        numItens=0
        print(f"Mochila {conta}")
        conta+=1
        for i in backpack.itens:
            print(f"item {i.weight} - {i.value}")
            numItens+=1
        print(f"soma - {backpack.sumValue}")
        print(f"peso - {backpack.sumWeight}")
        print(f"itens - {numItens}")
        print(f"pontuação - {backpack.pontuation:.2f}")
        print("-----------------------------")
        mediaPontuation += backpack.pontuation
    print(f"\033[91mMelhor - {eliteBackpack.pontuation:.2f}\033[0m")
    crossover()