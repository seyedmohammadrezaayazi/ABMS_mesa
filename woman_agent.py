from human_agent import Human


class Woman(Human):
    def __init__(self, unique_id, model, age=0, sex='man', married='not married', number_child=0,
                 past_time_of_pregnancy=0):
        super().__init__(unique_id, model, age, sex, married)
        self._number_child = 0
        self._past_time_of_pregnancy = 1

    def marriage_rate(self):
        number_live = self.model.schedule.number_agent_by_age[type(self)][str(self.get_age())]
        number_marriage = self.model.schedule.get_number_of_married()+1
        marriage_rate = (number_marriage / (number_marriage+number_live))* self.model.get_evo_married()

        return marriage_rate

    def get_brith_rand(self):
        brith_rate = self.random.uniform(0, 1 / (self._number_child + 1)) * self._past_time_of_pregnancy / \
                     (3*self._number_child + 1)
        return brith_rate*self.model.get_evo_brith()

    def step(self):
        super().step()
        if self._married == "not married":
            if self._age > self.model.start_age_married:
                rand = self.random.uniform(0, 1)
                if self.marriage_rate() > rand:
                    self._married = "married"
                    self.model.schedule.increase_number_of_married()
        else:
            rand = self.random.uniform(0, 1)
            if self.get_brith_rand() > rand and self._past_time_of_pregnancy > 1:
                sex = self.random.choice([Human, Woman])
                married = "not married"
                self._number_child += 1
                self._past_time_of_pregnancy = 1
                if sex is Human:
                    human = Human(self.model.next_id(), self.model, 1, 'man', married)
                else:
                    human = Woman(self.model.next_id(), self.model, 1, 'woman', married)
                self.model.schedule.add(human)
            else:
                self._past_time_of_pregnancy += 1
