# ARTIFICIAL INTELLEGENCE OFFLINE 3
# Shaikh Islam
# Roll: 1205046

'''
Implementation of job scheduling via 1st choice hill climbing and simulated annealing
'''
import random
import math
import copy


# the node class
class JobSchedule:
    """docstring for JobSchedule"""

    def __init__(self, ara, state):
        self.jobSequence = copy.deepcopy(ara)
        self.C = [[0]*len(state[0]) for _ in range(len(state))]

    def MakeSpan(self, P):
        for i in range(len(P)):
            for j in range(len(P[0])):
                if i == 0 and self.jobSequence[j] == 0:
                    self.C[i][j] = P[i][self.jobSequence[j]]
                elif i == 0 and self.jobSequence[j] > 0:
                    self.C[i][j] = self.C[i][j - 1] + P[i][self.jobSequence[j]]
                elif i > 0 and j == 0:
                    self.C[i][j] = self.C[i - 1][j] + P[i][self.jobSequence[j]]
                else:
                    self.C[i][j] = (self.C[i - 1][j] if (self.C[i - 1][j] > self.C[i][j - 1]) else self.C[i][j - 1]) + P[i][self.jobSequence[j]]

        return self.C[-1][-1]   #self.C[len(self.C) - 1][len(self.C[0]) - 1]


# the hill climbing approach
def HillClimbing(sequence, A):
    current = sequence[:]
    currentNode = JobSchedule(current, A)
    currentNodeMakeSpan = currentNode.MakeSpan(A)
    count = 0
    max_limit = len(sequence)**3
    child_limit = len(sequence)**2
    for i in range(max_limit):
        for j in range(child_limit):
            last_point = j
            count += 1
            if random.random() < 0.5:
                child = current[:]
                #temp = child.pop(random.randrange(len(child)))
                #child.insert(random.randrange(len(child)), temp)
                random.shuffle(child)
                childNode = JobSchedule(child, A)
            else:
                child = current[:]
                i = random.randrange(len(child))
                j = random.randrange(len(child))
                child[i], child[j] = child[j], child[i]
                #random.shuffle(child)
                childNode = JobSchedule(child, A)
            if childNode.MakeSpan(A) < currentNodeMakeSpan:
                currentNode = copy.deepcopy(childNode)
                break
        if last_point == child_limit - 1:
            return currentNode, count
    return currentNode, count


# the simiulated annealing
def SimuAnneal(sequence, A):
    current = sequence[:]
    currentNode = JobSchedule(current, A)
    currentNodeMakeSpan = currentNode.MakeSpan(A)
    count = 0
    T = 1
    t = 1
    while T > .009:
        count+=1
        T = T - 0.001*t
        child = current[:]
        random.shuffle(child)
        childNode = JobSchedule(child, A)
        delE = childNode.MakeSpan(A) - currentNodeMakeSpan
        if delE < 0:
            currentNode = copy.deepcopy(childNode)
        else:
            prob = math.exp(-delE/T)
            #print("prob", prob)
            if random.random() < prob:
                currentNode = copy.deepcopy(childNode)

    return currentNode,count


def main():
    inputFiles = ['Carlier 7x7 instance.txt','Carlier 8x9 instance.txt','Carlier 11x5 instance.txt','Carlier 14x4 instance.txt','Reeves 20x5 type C.txt','Reeves 30x10 type C.txt']
    outFile = open('OutputFile.txt','w')
    outFile.write('{0:24s}  {1:1s}  {2:1s}  {3:1s}  {4:1s}  {5:1s}  {6:1s}  {7:1s}\n\n'.format('DataSet','t hill','AvgOfitrHill','AvgMakespanHill','MinMakespanHill','AvgitrSimu','AvgMakespansimu','MinMakespansimu'))
    for file in inputFiles:
        inFile = open(file,'r')
        jobNumber, machine = map(int, inFile.readline().split())
        Pstate = [list(map(int, inFile.readline().split()[1::2])) for i in range(jobNumber)]
        AvgHillMakeSpan = AvgSimuMakeSpan = AvgHillItr = 0
        minHillMakeSpan = minSimuMakeSpan = int(1e9)
        L=5
        for i in range(L):
            sequence = random.sample(range(machine), machine)
            hillClimbedSolution,countHill = HillClimbing(sequence, Pstate)
            simulatedAnnelSolution,countSim = SimuAnneal(sequence, Pstate)
            hillMakeSpan = hillClimbedSolution.MakeSpan(Pstate)
            simuMakeSpan = simulatedAnnelSolution.MakeSpan(Pstate)
            AvgHillMakeSpan += hillMakeSpan
            AvgSimuMakeSpan += simuMakeSpan
            AvgHillItr += countHill
            if hillMakeSpan < minHillMakeSpan:
                minHillMakeSpan = hillMakeSpan
            if simuMakeSpan < minSimuMakeSpan:
                minSimuMakeSpan = simuMakeSpan

        inFile.close()
        outFile.write('{0:24s}  {1:3d}\t\t{2:5.2f}\t\t{3:5.2f} \t{4:5d} \t{5:5d}\t\t{6:5.2f} \t{7:5d}\n'.format(file,len(sequence)**2,AvgHillItr/L,AvgHillMakeSpan/L,minHillMakeSpan,countSim,AvgSimuMakeSpan/L,minSimuMakeSpan))
    outFile.close()
    
main()
