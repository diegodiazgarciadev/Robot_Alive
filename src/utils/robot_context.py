
class RobotContext:
    cycle_id = None
    action_counter = 0

    @classmethod
    def set_cycle_id(cls, id):
        cls.cycle_id = id
        cls.action_counter = 0

    @classmethod
    def get_cycle_id(cls):
        return cls.cycle_id

    @classmethod
    def increment_action_counter(cls):
        cls.action_counter += 1
        return cls.action_counter

    @classmethod
    def get_action_counter(cls):
        return cls.action_counter
