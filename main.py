
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



if __name__ == '__main__':
    num = 1
    for i in range(10):
        file_name = "level" + str(num) + ".txt"
        f = open(file_name, "r")
        content = f.read()
        print(content)