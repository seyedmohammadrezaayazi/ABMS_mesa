from collections import defaultdict
from mesa.time import RandomActivation
from human_agent import Human
from woman_agent import Woman
import random


class RandomActivationBySex(RandomActivation):

    def __init__(self, model, death_rate, marriage_rate):
        self.random = random.random()
        super().__init__(model)
        self.marriage_rate = marriage_rate
        self.agents_by_sex = defaultdict(dict)
        self.number_agent_by_age = defaultdict(dict)
        self.number_death_agent_by_age = defaultdict(dict)
        self.last_number_death_agent_by_age = defaultdict(dict)
        self.death_rate = death_rate
        self.dead_men = 0
        self.dead_women = 0
        self.last_dead_men = 0
        self.last_dead_women = 0
        self.last_year_number_of_married = self.model.get_last_years_marriage()
        self.number_of_married = 0
        for x in range(0, self.model.get_end_age() + 1):
            self.number_agent_by_age[Human][str(x)] = 0
            self.number_agent_by_age[Woman][str(x)] = 0
            self.number_death_agent_by_age[Human][str(x)] = 0
            self.number_death_agent_by_age[Woman][str(x)] = 0
            self.last_number_death_agent_by_age[Human][str(x)] = \
                self.model.get_initial_man() / (
                            self.model.get_initial_man() * (1-random.uniform(0, x / self.model.get_end_age()+1)))
            self.last_number_death_agent_by_age[Woman][str(x)] = \
                self.model.get_initial_woman() / (
                            self.model.get_initial_woman() * (1-random.uniform(0, x / self.model.get_end_age()+1)))

    def get_last_dead(self):
        return self.last_dead_men + self.last_dead_women

    def cal_death_rate(self):
        self.last_dead_men = self.dead_men
        self.last_dead_women = self.dead_women
        self.death_rate = (self.dead_men + self.dead_women) / (self.get_sex_count(Human) + self.get_sex_count(Woman))
        self.dead_men = 0
        self.dead_women = 0

    def increase_number_of_married(self):
        self.number_of_married += 1

    def get_number_of_married(self):
        return self.last_year_number_of_married

    def get_marriage_rate(self):
        return self.marriage_rate

    def add(self, agent):
        self._agents[agent.unique_id] = agent
        # print(type(agent))
        agent_class = type(agent)
        self.number_agent_by_age[agent_class][str(agent.get_age())] += 1
        self.agents_by_sex[agent_class][agent.unique_id] = agent

    def set_death_rate(self, value):
        self.death_rate = value

    def get_death_rate(self):
        return self.death_rate

    def set_marriage_rate(self, value):
        self.marriage_rate = value

    def remove(self, agent):
        del self._agents[agent.unique_id]
        agent_class = type(agent)
        if agent_class == Woman:
            self.dead_women += 1
        else:
            self.dead_men += 1
        self.number_death_agent_by_age[agent_class][str(agent.get_age())] += 1
        del self.agents_by_sex[agent_class][agent.unique_id]

    def step(self, by_breed=True):
        if by_breed:
            for agent_class in self.agents_by_sex:
                self.step_sex(agent_class)
            self.steps += 1
            self.time += 1
            self.last_year_number_of_married = self.number_of_married
            self.last_number_death_agent_by_age = self.number_death_agent_by_age
            self.number_of_married = 0
            self.cal_death_rate()
            for x in range(0, self.model.get_end_age() + 1):
                self.number_death_agent_by_age[Human][str(x)] = 0
                self.number_death_agent_by_age[Woman][str(x)] = 0


        else:
            super().step()

    def step_sex(self, sex):
        """
        Shuffle order and run all agents of a given breed.
        Args:
            sex: Class object of the breed to run.
        """
        agent_keys = list(self.agents_by_sex[sex].keys())
        self.model.random.shuffle(agent_keys)
        for agent_key in agent_keys:
            self.agents_by_sex[sex][agent_key].step()

    def get_sex_count(self, sex_class):
        return len(self.agents_by_sex[sex_class].values())

    def get_married(self, sex_class):
        agent_keys = list(self.agents_by_sex[sex_class].keys())
        self.model.random.shuffle(agent_keys)
        num = 0
        for agent_key in agent_keys:
            if self.agents_by_sex[sex_class][agent_key].is_married():
                num += 1
        return num

    def get_age(self):
        for x in range(0, self.model.get_end_age() + 1):
            self.number_agent_by_age[Human][str(x)] = 0
            self.number_agent_by_age[Woman][str(x)] = 0

        agents = list(self.agents_by_sex[Woman].keys())
        for agent_key in agents:
            # print(str(self.agents_by_sex[Woman][agent_key].age))
            self.number_agent_by_age[Woman][str(self.agents_by_sex[Woman][agent_key].get_age())] += 1
        agents = list(self.agents_by_sex[Human].keys())
        for agent_key in agents:
            self.number_agent_by_age[Human][str(self.agents_by_sex[Human][agent_key].get_age())] += 1
