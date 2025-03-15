from mesa import Agent


class Human(Agent):
    def __init__(self, unique_id, model, age=0, sex='man', married='not married'):
        super(Human, self).__init__(unique_id, model)
        self._age = age
        self._sex = sex
        self._married = married

    def get_age(self):
        return self._age

    def get_death_rate(self):
        pass

    def is_married(self):
        if self._married == "married":
            return True
        else:
            return False

    def death_rnd(self):
        number_live = self.model.schedule.number_agent_by_age[type(self)][str(self.get_age())]
        number_death = self.model.schedule.last_number_death_agent_by_age[type(self)][str(self.get_age())]
        death_rate = (number_death / (number_death + number_live)) * \
                     self.model.get_evo_death(self.get_age(), self._sex)
        return death_rate

    def step(self):
        rand = self.random.uniform(0, 1)
        if self.death_rnd() > rand:
            self.model.schedule.remove(self)
        else:
            if self._age == self.model.end_age:
                self.model.schedule.remove(self)
            else:
                self._age += 1
