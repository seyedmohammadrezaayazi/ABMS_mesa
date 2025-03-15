from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from human_agent import Human
from schedule import RandomActivationBySex
from woman_agent import Woman


class HumanModel(Model):
    verbose = False
    description = (
        "A model for Iran Demography simulation."
    )

    def __init__(self, initial_man=100, initial_woman=100,
                 probability_of_having_children=1,
                 number_of_children=2, maternal_age_at_birth=12,
                 start_age=15, end_age=49,
                 evo_death='last years', initial_death_rate=0.5,
                 initial_evo_marriage=0.4, evo_brith=0.45,
                 last_years_marriage=5000, reg_dead_b=2500,
                 reg_dead_a1=1200, reg_dead_a2=10, start_age_married=21):
        super().__init__()
        self.start_age_married = start_age_married
        self.reg_dead_b = reg_dead_b
        self.reg_dead_a1 = reg_dead_a1
        self.reg_dead_a2 = reg_dead_a2
        self.initial_evo_marriage = initial_evo_marriage
        self.initial_death_rate = initial_death_rate
        self.evo_brith = evo_brith
        self.last_years_marriage = last_years_marriage
        self.start_age = start_age
        self.end_age = end_age
        self.initial_man = initial_man
        self.evo_death = evo_death
        self.initial_woman = initial_woman
        self.probability_of_having_children = probability_of_having_children
        self.number_of_children = number_of_children
        self.maternal_age_at_birth = maternal_age_at_birth
        self.schedule = RandomActivationBySex(self, self.initial_death_rate,
                                              self.initial_evo_marriage)

        self.datacollector = DataCollector(
            {
                "Men": lambda m: m.schedule.get_sex_count(Human),
                "Women": lambda m: m.schedule.get_sex_count(Woman),
                "total population": lambda m: m.schedule.get_sex_count(Woman) +
                                              m.schedule.get_sex_count(Human),
                "Married Woman": lambda m: m.schedule.get_married(Woman),
                "New Married Woman": lambda m: m.schedule.get_number_of_married(),
                "Dead in the year": lambda m: m.schedule.get_last_dead(),
            }
        )

        # self.grid = MultiGrid(self.height, self.width, torus=True)
        for i in range(self.initial_man):
            age = self.random.randint(0, self.end_age)

            married = self.random.choice(["married", "not married"])
            man = Human(self.next_id(), self, age, 'man', married)
            self.schedule.add(man)

        # Create woman
        for i in range(self.initial_woman):
            age = self.random.randint(0, self.end_age)
            # print(f"age :{age}")

            married = self.random.choice(["married", "not married"])
            if married == "married":
                past_time_of_pregnancy = self.random.randint(0, 10)
                number_children = self.random.randint(0, 4)
            else:
                past_time_of_pregnancy = 0
                number_children = 0
            woman = Woman(self.next_id(), self, age, 'woman', married, number_children, past_time_of_pregnancy)
            self.schedule.add(woman)
        self.running = True
        self.datacollector.collect(self)

    def get_last_years_marriage(self):
        return self.last_years_marriage

    def get_initial_woman(self):
        return self.initial_woman

    def get_evo_brith(self):
        return self.evo_brith

    def get_initial_man(self):
        return self.initial_man

    def get_end_age(self):
        return self.end_age

    def step(self):
        self.schedule.step()
        self.schedule.get_age()
        self.datacollector.collect(self)

    def run_model(self, step_count=200):

        if self.verbose:
            print("Initial number Men: ", self.schedule.get_breed_count(Human))
            print("Initial number Women: ", self.schedule.get_breed_count(Woman))

        for i in range(step_count):
            self.step()
            print(self.schedule.get_breed_count(Woman))

        if self.verbose:
            print("")
            print("Final number Men: ", self.schedule.get_breed_count(Human))
            print("Final number Women: ", self.schedule.get_breed_count(Woman))

    def get_evo_death(self, age, sex):
        if self.evo_death == 'last years':
            return self.schedule.get_death_rate()
        elif self.evo_death == 'Liner regression':
            cal = float(self.reg_dead_a1) * int(age)
            if (sex == 'man'):
                cal += float(self.reg_dead_a2)
            cal += float(self.reg_dead_b)
            return float(cal)
        else:
            return self.schedule.get_death_rate()

    def get_evo_married(self):
        if self.evo_death == 'last years':
            return self.schedule.get_marriage_rate()
        else:
            return self.schedule.get_marriage_rate()
