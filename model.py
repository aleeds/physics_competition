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
    return (energy_received, energy_needed)
 
# Idea is that it calculates how energy heating takes
# modifies the heat level for the object, returns delta energy
def modelling_heat_metabolic(species, conditions):
    surface_area_heat_delta = species.surface_area * (conditions.temp() - species.temp)
    return surface_area_heat_delta / (species.volume * species.heat_efficiency)

# Calculates how much energy needs to go towards repairing bone fractures
def modelling_bone_stress(species,  movement_energy):
    mass = species.mass
    dia = species.bone_diameter 
    return species.bone_stress(mass, dia, energy)

# Calculates delta energy from oxygen consumption
def modelling_oxygen_consumption(species, conditions):
    return species.consume_oxygen(conditions)

# determines delta energy from giving birth
def modelling_birth(species, conditions):
    return species.reproduce(conditions)

class Species(object):
    def __init__(self, mass, energy_stores, max_energy_stores, temp):
        self.mass = mass 
        self.energy_stores = energy_stores
        self.max_energy_energy = max_energy_stores
        self.temp
        self.energy_needed = 0        

    def update_food(self, food_needed, food_present, dis):
        energy_needed = math.sqrt(food_present) * dis * dis * uniform(2./3., 3./2.)
        energy_received = (food_present - food_needed) * uniform(2./3.,3./2.)
        return (energy_received, energy_needed)

    def energy_consumption(self):
        return (self.energy_needed + min(0, self.energy_stores)) * uniform(2./3., 3./2.)

class Conditions(object):
    def __init__(self, weather, food_availability):
        self.food_availability = food_availability
    
    def generate_availability_food(self):
        return (self.food_availability * uniform(2./3., 3./2.), uniform(1, 3))

def model(species, conditions):
    for i in range(0, 1000):
        if species.dead():
            return species.statistics()
        (energy_c, movement_energy) = food_consumption(species, conditions)
        energy_heat = modelling_heat_metabolic(species, conditions)
        energy_bone_stress = modelling_bone_stress(species, movement_energy)
        energy_oxygen = modelling_oxygen_consumption(species, conditions)
        birth_energy = modelling_birth(species, conditions)
        total_energy = energy_c + energy_oxygen - (energy_heat + energy_bone_stress + birth_energy) 
        species.life += 1
    return species.statistics()


dinosaur = Species(1000, 100, 300)
conditions = Conditions(0, 200)
print(food_consumption(dinosaur, conditions))
