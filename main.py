import random
from matplotlib import pyplot as plt

class Chromosome:
    def __init__(self, length):
        self.chromosome_cell = []
        self.chromosomes = []
        self.n = length



    def build_chromosome(self):
        self.chromosome_cell = []
        choice = [0, 2]
        for i in range(self.n):
            temp = random.randint(0, 2)
            if i > 0 and self.chromosome_cell[i - 1] == 1 and temp == 1:
                temp = random.choice(choice)
            self.chromosome_cell.append(temp)
        return self.chromosome_cell


    def build_all_chromosomes(self):
        for i in range(200):
            each_chromosome = self.build_chromosome()
            self.chromosomes.append(each_chromosome)
        return self.chromosomes



class Heuristic:
    def __init__(self, levels):
        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0



    def load_next_level(self):
        self.current_level_index += 1
        self.current_level_len = len(self.levels[self.current_level_index])


    def get_score(self, actions):
        current_level = self.levels[self.current_level_index]
        steps, max = 0, 0
        win = True
        for i in range(self.current_level_len):
            current_step = current_level[i]
            if current_step == '_':
                steps += 1
                if i > 1 and actions[i - 2] == '1':
                    steps -= 0.5
            elif current_step == 'M':
                if (i > 0 and actions[i - 1] != '1') or i == 0:
                    steps += 3
                if i > 1 and actions[i - 2] == "1":
                    steps -= 0.5
            elif current_step == 'G' and actions[i - 2] == '1' and i > 1:
                steps += 3
            elif current_step == 'G' and actions[i - 1] == '1':
                steps += 1
            elif current_step == 'L' and actions[i - 1] == '2':
                steps += 1
            else:
                steps = 0
                win = False
            if max < steps:
                max = steps
        if steps == self.current_level_len:
            max += 5
        if actions[len(actions) - 1] == '1':
            max += 1
        return max, win


class Game:
    def __init__(self, heuristic, chromosome):
        self.heuristic = heuristic
        self.chromosome = chromosome
        self.chromosomes = chromosome.build_all_chromosomes()
        self.average = 0
        self.avg_plot = []
        self.best = []
        self.worst = []

    def score_all(self):
        population = []
        for i in range(len(self.chromosomes)):
            string_chromosome = ''
            for j in range(len(self.chromosomes[i])):
                string_chromosome += str(self.chromosomes[i][j])
            population.append([string_chromosome, self.heuristic.get_score(string_chromosome)])
        population = self.sort(population)
        return population


    def sort(self, population):
        for i in range(len(population)):
            for j in range(len(population) - i - 1):
                if population[j][1] < population[j + 1][1]:
                    temp = population[j]
                    population[j] = population[j + 1]
                    population[j + 1] = temp
        return population



    def choose(self, children):
        grandchildren = []
        for i in range(int(len(children) / 2)):
            child1, child2 = self.cross_over(children)
            grandchildren.append(child1)
            grandchildren.append(child2)
        children = self.next_generation(children, grandchildren)
        children = self.mutation(children)
        self.game_over(children)
        return children


    def build_children(self, population, children):
        for i in range(int(len(population) / 2)):
            children.append(population[i])
        self.choose(children)


    def cross_over(self, children):
        random1 = random.randint(0, len(children) - 1)
        random2 = random.randint(0, len(children) - 1)
        chromosome1 = list(children[random1][0])
        chromosome2 = list(children[random2][0])
        for i in range(int(len(children[0][0]) / 2), len(children[0][0])):
            chromosome1[i], chromosome2[i] = chromosome2[i], chromosome1[i]
        chromosome1 = ''.join(chromosome1)
        chromosome2 = ''.join(chromosome2)
        return [chromosome1, h.get_score(chromosome1)], [chromosome2, h.get_score(chromosome2)]


    def next_generation(self, children, grandchildren):
        for i in range(len(children)):
            grandchildren.append(children[i])
        grandchildren = self.sort(grandchildren)
        children = []
        for i in range(int(len(grandchildren) / 2)):
            children.append(grandchildren[i])
        return children


if __name__ == '__main__':
    num = 1
    for i in range(10):
        file_name = "level" + str(num) + ".txt"
        f = open(file_name, "r")
        content = f.read()
        print(content)
        h = Heuristic([content])
        h.load_next_level()
