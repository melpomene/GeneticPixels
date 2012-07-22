from PIL import Image
from random import randint, random


class Picture:
    def __init__(self, original):
         self.method = "square"
         self.original = original
         self.image = Image.new("RGB", original.size)
         self.fitness = self.calculate_fitness()
         
    def random(self):
        size = self.image.size
        if self.method == "pixel":
            for x in range(size[0]):
                for y in range(size[1]):
                    p0 = randint(0, 255)
                    p1 = randint(0, 255)
                    p2 = randint(0, 255)
                    self.image.putpixel((x,y),(p0,p1,p2))
        elif self.method == "square":
            for x in range(0, size[0], 30):
                for y in range(0, size[1], 10):
                    pos = (x, y, x+30, y+10)
                    p0 = randint(0, 255)
                    p1 = randint(0, 255)
                    p2 = randint(0, 255)
                    self.image.paste((p0,p1,p2), pos)

        self.fitness = self.calculate_fitness()
    def create_from(self, individual1, individual2, mutation_risk=0.01):
        size = self.image.size
        
        if self.method=="pixel": 
            for x in range(size[0]):
                for y in range(size[1]):
                    if randint(0,99) < mutation_risk * 100:
                        #print "Mutating"
                        self.image.putpixel((x,y), (randint(0,255), randint(0,255), randint(0,255)))
                    elif randint(0,1) == 1: 
                        self.image.putpixel((x,y), individual1.image.getpixel((x,y)))
                    else:
                        self.image.putpixel((x,y), individual2.image.getpixel((x,y)))
        elif self.method == "square":

            for x in range(0, size[0], 30):
                for y in range(0, size[1], 10):
                    pos = (x, y, x+30, y+10)
                    
                    if randint(0,99) < mutation_risk * 100:
                        #print "Mutating"
                        self.image.paste((randint(0,255), randint(0,255), randint(0,255)), pos)
                    elif randint(0,1) == 1: 
                        self.image.paste(individual1.image.getpixel((x,y)), pos)
                    else:
                        self.image.paste(individual2.image.getpixel((x,y)), pos)

        self.fitness = self.calculate_fitness()

    def save(self):
        self.image.save(str(self.fitness)+".jpg")

    def __repr__(self):
        return str(self.fitness)

    def calculate_fitness(self):
        def compare_pixel(p1, p2):
            """ Compare two pixels, the lower the value the better """

            r = abs(p1[0] - p2[0])
            g = abs(p1[1] - p2[1])
            b = abs(p1[2] - p2[2])
            #return abs(p1[0]+p1[1]+p1[2]-(p2[0]+p2[1]+p2[2]))
            return r + g + b

        def compare_image(img1, img2):
            """ 
                Returns a value describing the pixel liknes between two images.
                Lower is closer
            """

            img1_data = img1.getdata()
            img2_data = img2.getdata()
            diff_value = 0
            for i in range(len(img1_data)):
                diff_value += compare_pixel(img1_data[i], img2_data[i])
            return diff_value
            
        return compare_image(self.image, self.original)

def spawn_start_gen(nbr_individuals, original):
    generation = []
    for i in range(nbr_individuals):
        pic = Picture(original)
        pic.random()
        generation.append(pic)
    return generation

def save_gen_to_file(gen, verbose=True, show=False):
    for individual in gen: 
        individual.save()
        if verbose:
            print " fitness: " + str(individual.fitness)
        if show: 
            individual.image.show()




def generate_children(gen, nbr_survivors, mutation_risk):
    #select the best half and reporduce. 
    
    
    children = []
    
    mating_pairs = []
    for i in range(len(gen[:len(gen)/2])):
        mating_pairs.append((gen[i], gen[i+1]))
        mating_pairs.append((gen[i], gen[i+1]))


    for (i1, i2) in mating_pairs:
        child = Picture(i1.original)
        child.create_from(i1, i2, mutation_risk)
        children.append(child)

    children = children[:len(gen) - nbr_survivors] # no need for the unlucky
    children = children + gen[:nbr_survivors]
    children = sorted(children, key=lambda individual: individual.fitness)
    return children


def run(iterations_max, nbr_individuals, nbr_survivors, mutation_risk, original):

    print "Image size: " + str(original.size)
    print "Generating first generation"
    gen = spawn_start_gen(nbr_individuals, original) # returns
    print "Done generating. Starting Darwinism"
    iteration = 0
    best_individual = 0
    stagnation = 0
    try:
        while iteration < iterations_max:
            mates =  generate_children(gen, nbr_survivors, mutation_risk)
            gen = mates

            print str(iteration) + " " + str(gen)
            if gen[0] == best_individual:
                stagnation += 1
            else: 
                best_individual = gen[0]
                stagnation = 0

            if stagnation > 100: # If generation seems to have stagnated. Introduce new ind to pack
                lone_wolf = Picture(gen[0].original)
                lone_wolf.random()
                gen.append(lone_wolf)
                stagnation = 0



            iteration += 1
    except KeyboardInterrupt:
        pass
    save_gen_to_file(gen[:10], True, True)


if __name__ == "__main__":
    iterations_max = 5000
    nbr_individuals = 5
    nbr_survivors = 1
    mutation_risk = 0.12
    original = Image.open("test_small.jpg")
     
    run(iterations_max, nbr_individuals, nbr_survivors, mutation_risk, original)
    exit()
    while(True):
        iterations_max = randint(1, 1000)
        nbr_individuals = randint(2,100)
        nbr_survivors= randint(0,nbr_individuals-1)
        mutation_risk = random()
        print "iterations: " + str(iterations_max) + " # individual: " + str(nbr_individuals) + " Survivors: " + str(nbr_survivors) + " Mutationrisk: " + str(mutation_risk)
        run(iterations_max, nbr_individuals, nbr_survivors, mutation_risk, original)
