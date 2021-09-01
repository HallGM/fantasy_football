class Player:
    def __init__(self, name, team, points, cost, position):
        self.name = name
        self.team = team
        self.points = int(float(points) * 10)
        self.cost = int(float(cost) * 10)
        if position in ("FOR", "MID", "DEF", "GK"):
            self.position = position
        else:
            raise ValueError('Position must be one of FOR, MID, DEF or GK')

    def get_points(self):
        return float(self.points) / 10

    def get_cost(self):
        return float(self.cost) / 10
