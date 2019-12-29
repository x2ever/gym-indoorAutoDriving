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
