import numpy as np
import warnings

class Obstacle(object):
    obstacle_type = "default"

    def __init__(self, start_coordinate, intensity):
        self.x, self.y = start_coordinate
        self.intensity = intensity
        self.coordinates = [func(self.x, self.y) for func in self.size_info_functions]
        self.size_info_functions = [
            self.create_size_info_function(0, 0)
        ]

    def create_size_info_function(self, dx, dy):

        def size_info_function(x, y):
            return (x + dx, y + dy)

        return size_info_function

class StaticObstacle(Obstacle):
    obstacle_type = "static"
    def __init__(self, start_coordinate, intensity):
        self.x, self.y = start_coordinate
        self.intensity = intensity
        self.coordinates = [func(self.x, self.y) for func in self.size_info_functions]


class TableObstacle(StaticObstacle):
    intensity = 0.5

    def __init__(self, start_coordinate):
        self.x, self.y = start_coordinate
        self.size_info_functions = [
            self.create_size_info_function(0, 0),
            self.create_size_info_function(1, 0),
            self.create_size_info_function(1, 1),
            self.create_size_info_function(0, 1),
            self.create_size_info_function(1, -1),
            self.create_size_info_function(-1, 0),
            self.create_size_info_function(-1, 1),
            self.create_size_info_function(0, -1),
            self.create_size_info_function(-1, -1),
        ]

        self.coordinates = [func(self.x, self.y) for func in self.size_info_functions]

class WallObstacle(StaticObstacle):
    intensity = 0.7

    def __init__(self, start_coordinate, width=1, height=1):
        self.x, self.y = start_coordinate
        self.size_info_functions = [
            self.create_size_info_function(i, j) for i in range(height) for j in range(width)
        ]

        self.coordinates = [func(self.x, self.y) for func in self.size_info_functions]


class DynamicObstacle(Obstacle):
    obstacle_type = "dynamic"
    def __init__(self, center_coordinate, intensity):
        self.x, self.y = center_coordinate
        self.intensity = intensity
        self.coordinates = [func(self.x, self.y) for func in self.size_info_functions]

class Map(object):
    def __init__(self, size=32):
        self.size = size
        self.__data = np.zeros((size, size))
        self.static_obstacles = list()
        self.dynamic_obstacles = list()

    def addObstacle(self, obstacle: Obstacle):
        if obstacle.obstacle_type == "static":
            self.static_obstacles.append(obstacle)
            intensity = obstacle.intensity

            for x, y in obstacle.coordinates:
                if 0 <= x < self.size and 0 <= y < self.size:
                    self.__data[x, y] = intensity
        else:
            warnings.warn("Not implemented yet")

    def update(self):
        warnings.warn("Not implemented yet")

    @property
    def data(self):
        return np.copy(self.__data)

if __name__ == "__main__":
    m = Map()
    t1 = TableObstacle((2, 2))
    t2 = TableObstacle((3, 6))
    w1 = WallObstacle((0, 0), height=32)
    w2 = WallObstacle((0, 0), width=32)
    w3 = WallObstacle((0, 31), height=32)
    w4 = WallObstacle((31, 0), width=32)

    m.addObstacle(t1)
    m.addObstacle(t2)
    m.addObstacle(w1)
    m.addObstacle(w2)
    m.addObstacle(w3)
    m.addObstacle(w4)
    print(m.data)
