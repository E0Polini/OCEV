from random import *
import numpy as np
from matplotlib import pyplot as plt

#Gerador de população inicial
def generatePop(size, popSize):
    popList = []
    while len(popList) < 30:
        #Gerador de indivíduos
        popList.append(sample(range(size), size))

    return popList

#Gera lista de indivíduos com respectivo fitness
def popFitness(size, pop):
    fitnessList = []
    for sub in pop:
        fitnessList.append((subFitness(size, sub), sub))
    return fitnessList

#Calcula o fitness de cada indivíduo
def subFitness(size, sub):
    f1, f2 = [], []
    t1, t2 = 0, 0
    for i in range(size):
        f1.append(sub[i]-i)
        f2.append((1+size)-sub[i]-i)
    f1.sort()
    f2.sort()
    for i in range(size-1):
        if(f1[i] == f1[i+1]):
            t1 += 1
        if(f2[i] == f2[i+1]):
            t2 += 1
    return t1+t2

#Função de gerações
def startGen(gen, size, popSize, pop):
    bests = []
    for i in range(gen): #numero de geracoes
        
        #seção para salvar dados de cada geração
        order = sorted(pop)
        bests.append(order[0])
        if(order[0][0] == 0):
            break
        
        ##

        intermed = []
        for i in range(int((popSize/2)+1)): #numero de torneios = popSize/2
            intermed.append(select(popSize, pop))
            if(i%2 == 1):
                pmxCross(pop, size, intermed[i-1][1],intermed[i][1])
        
        popOrdered = sorted(pop)
        temp = []
        for j in range(popSize):
            temp.append(popOrdered[j])

        pop = [x for x in temp if x in pop] #retira os n piores elementos da populacao
        
    return pop, bests


#Torneio de seleção
def select(popSize, pop):
    idx1, idx2 = randrange(popSize), randrange(popSize)
    while(idx1 == idx2):
        idx2 = randrange(popSize)
    kp = randint(1, 100)

    #chosen1 é sempre o cara com fitness <= ao chosen2
    if(pop[idx1][0] > pop[idx2][0]):
        chosen1 = pop[idx2]
        chosen2 = pop[idx1]
    else:
        chosen1 = pop[idx1]
        chosen2 = pop[idx2]

    #90% de chance de retornar o melhor dois dois selecionados
    if(kp < 90):
        return chosen2
    else:
        return chosen1

def pmxCross(pop, size, parent1, parent2):
    point1 = randint(0,size-2)
    point2 = randint(point1+1,size-1)
    mut = randint(1, 100)

    parent1Mid = parent1[point1:point2]
    parent2Mid = parent2[point1:point2]

    temp_child1 = parent1[:point1] + parent2Mid + parent1[point2:]
    temp_child2 = parent2[:point1] + parent1Mid + parent2[point2:]

    relations = []
    for i in range(len(parent1Mid)):
        relations.append([parent2Mid[i], parent1Mid[i]])

    child1=recursion1(temp_child1,point1,point2,parent1,parent1Mid,parent2,parent2Mid, relations)
    child2=recursion2(temp_child2,point1,point2,parent1,parent1Mid,parent2,parent2Mid, relations)

    if(mut > 90):
        mutate(child1, child2, size)

    noFitPop = []
    for i in range(len(pop)):
        noFitPop = pop[i][1]

    if(child1 not in noFitPop):
        pop.append((subFitness(size,child1),child1))
    if(child2 not in noFitPop):
        pop.append((subFitness(size,child2),child2))


def recursion1 (temp_child, point1, point2, parent1, parent1Mid, parent2, parent2Mid, relations) :
    child = []
    for i in range(len(parent1)):
        child.append(0)
    for i,j in enumerate(temp_child[:point1]):
        c=0
        for x in relations:
            if j == x[0]:
                child[i]=x[1]
                c=1
                break
        if c==0:
            child[i]=j
    j=0
    for i in range(point1,point2):
        child[i]=parent2Mid[j]
        j+=1

    for i,j in enumerate(temp_child[point2:]):
        c=0
        for x in relations:
            if j == x[0]:
                child[i+point2]=x[1]
                c=1
                break
        if c==0:
            child[i+point2]=j
    child_unique=np.unique(child)
    if len(child)>len(child_unique):
        child=recursion1(child,point1,point2,parent1,parent1Mid,parent2,parent2Mid, relations)
    return(child)

def recursion2(temp_child, point1, point2, parent1, parent1Mid, parent2, parent2Mid, relations):
    child = []
    for i in range(len(parent1)):
        child.append(0)
    for i,j in enumerate(temp_child[:point1]):
        c=0
        for x in relations:
            if j == x[1]:
                child[i]=x[0]
                c=1
                break
        if c==0:
            child[i]=j
    j=0
    for i in range(point1,point2):
        child[i]=parent1Mid[j]
        j+=1

    for i,j in enumerate(temp_child[point2:]):
        c=0
        for x in relations:
            if j == x[1]:
                child[i+point2]=x[0]
                c=1
                break
        if c==0:
            child[i+point2]=j
    child_unique=np.unique(child)
    if len(child)>len(child_unique):
        child=recursion2(child,point1,point2,parent1,parent1Mid,parent2,parent2Mid, relations)
    return(child)

def mutate(child1, child2, size):
    allele1, allele2 = randrange(size), randrange(size)
    while(allele1 == allele2):
        allele2 = randrange(size)

    child1[allele1], child1[allele2] = child1[allele2], child1[allele1]
    child2[allele1], child2[allele2] = child2[allele2], child2[allele1]


popSize = 30 
size = int(input('Tamanho do tabuleiro: '))
gen = int(input('Numero de gerações: '))
for i in range(1):
    pop = generatePop(size, popSize)

    fitness = popFitness(size, pop)
    
    lastGen, bests = startGen(gen, size, popSize, fitness)
    lastGen.sort()

    x, y = [], []
    for i in range(len(bests)):
        x.append(int(i))
        y.append(int(bests[i][0]))

    bestFit = [lastGen[0]]
    for i in range(1, popSize):
        if(lastGen[i][0] == bestFit[0][0] and len(bestFit) < 10 ):
            bestFit.append(lastGen[i])
    
    print("O melhor fitness encontrado nessa execução é: ", lastGen[0][0])
    print(len(bests))
    print("Os elementos com esse fitness encontrados são: ")
    for i in range(len(bestFit)):
        print (bestFit[i][1])

    print()
    plt.title("Grafico Fitness")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.plot(x,y)
    plt.show()