import numpy as np

from src.engine.base_culture import Culture


def test_culture():
    c = Culture([1, 0, 0], 0.5)

    vec = c.get_random_vector()

    print(c.angle_compute(vec))
    assert np.abs(c.angle_compute(vec)) < c.angle

    assert c.check_vector_in_culture(vec)
    print(c.check_vector_in_culture(vec))


if __name__ == '__main__':
    test_culture()