from random import uniform
import math

# NOTE
#     Each species method does not update energy, only internal variables
#     related to stress, etc.

# Figures out how much food it can get from the environment if the 
# species needs a certain amount of food, has certain mass, etc.
# Has been reasonably fudged
def food_consumption(species, conditions):
    food_needed = species.energy_consumption()
    (food_present, dis) = conditions.generate_availability_food()
    (energy_received, energy_needed) = species.update_food(food_needed, food_present, dis)
    return (energy_received, energy_needed, dis)
 
# Idea is that it calculates how energy heating takes
# modifies the heat level for the object, returns delta energy
# Has been reasonably fudged
def modelling_heat_metabolic(species, conditions, movement_energy):
    t = abs(conditions.get_temp() - species.temp)
    surface_area_heat_delta = species.surface_area * (2 ** t)
    return surface_area_heat_delta * species.heat_efficiency / species.volume + math.sqrt(movement_energy)

# Calculates how much energy needs to go towards repairing bone fractures
# Has been reaosnably fudged, needs to take into account the 
# various mass, size, etc.
def modelling_bone_stress(species,  movement_energy, dis):
    return species.bone_stress(movement_energy, dis)

# Calculates delta energy from oxygen consumption
# Total garbage right now, but has been fudged. 
def modelling_oxygen_consumption(species, conditions, dis):
    return species.consume_oxygen(conditions)

# determines delta energy from giving birth
def modelling_birth(species, conditions):
    return species.reproduce(conditions)

class Species(object):
    def __init__(self, mass, energy_stores, max_energy_stores, temp, length, heat_efficiency, oxygen_efficiency):
        self.mass = mass 
        self.energy_stores = energy_stores
        self.max_energy_energy = max_energy_stores
        self.temp = temp
        self.surface_area = math.pi * length * length
        self.volume = math.pi * length * length
        self.heat_efficiency = heat_efficiency
        self.energy_needed = 0        
        self.bone_health = 1
        self.oxygen_efficiency = oxygen_efficiency

    def update_food(self, food_needed, food_present, dis):
        energy_needed = math.sqrt(food_present) * dis * dis * uniform(2./3., 3./2.)
        energy_received = (food_present - food_needed) * uniform(2./3.,3./2.)
        return (energy_received, energy_needed)

    def bone_stress(self, movement_energy, dis):
        self.bone_health -= math.log(dis)
        self.bone_health = max(1, self.bone_health + uniform(0, math.log(dis) * 2))
        return 10

    def energy_consumption(self):
        return (self.energy_needed + min(0, self.energy_stores)) * uniform(2./3., 3./2.)

    def consume_oxygen(self, conditions): 
        return self.mass * 3./4 * 100 * (1/(dis ** 5)) * conditions.oxygen * self.oxygen_efficiency

class Conditions(object):
    def __init__(self, temp, food_availability, oxygen):
        self.temp = temp
        self.cur_temp = temp
        self.food_availability = food_availability
        self.oxygen = oxygen

   
    def get_temp(self):
        if (self.temp == self.cur_temp):
            self.cur_temp += uniform(-5,5)
        elif (self.temp > self.cur_temp):
            self.cur_temp += uniform(-5, (self.temp - self.cur_temp) * 1.5)
        else:
            self.cur_temp += uniform((self.temp - self.cur_temp) * 1.5, 5)
        return self.cur_temp
 
    def generate_availability_food(self):
        return (self.food_availability * uniform(2./3., 3./2.), uniform(1, 3))

def model(species, conditions):
    for i in range(0, 1000):
        if species.dead():
            return species.statistics()
        (energy_c, movement_energy, dis) = food_consumption(species, conditions)
        energy_heat = modelling_heat_metabolic(species, conditions, movement_energy)
        energy_bone_stress = modelling_bone_stress(species, movement_energy, dis)
        energy_oxygen = modelling_oxygen_consumption(species, conditions)
        birth_energy = modelling_birth(species, conditions)
        total_energy = energy_c + energy_oxygen - (energy_heat + energy_bone_stress + birth_energy) 
        species.life += 1
    return species.statistics()


dinosaur = Species(1000, 100, 300, 100, 1000, 1, .3)
conditions = Conditions(100, 200, .3)

(energyc, movement_energy, dis) = food_consumption(dinosaur, conditions)
print((energyc, movement_energy, dis)) 
print(modelling_heat_metabolic(dinosaur, conditions, movement_energy))
print(modelling_bone_stress(dinosaur, movement_energy, dis))
print(modelling_oxygen_consumption(dinosaur, conditions, dis))
