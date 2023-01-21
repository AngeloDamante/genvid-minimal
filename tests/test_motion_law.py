import unittest
import numpy as np
from src.motion_law import urm, uarm, trapezoidal_profile

# global
origin = np.array([400, 200], dtype=float)
dest = np.array([300, 500], dtype=float)
tf = 10  # [s]
f = 30  # [hz]
step = 1 / f
num_step = f * tf


class TestMotionLaw(unittest.TestCase):

    def test_urm(self):
        x1_val, x2_val = [], []
        v = (dest - origin) / tf
        x = np.zeros(2)
        for i in range(num_step + 1):
            t = i * step
            x[0] = urm(origin[0], v[0], t)
            x[1] = urm(origin[1], v[1], t)
            x1_val.append(x[0])
            x2_val.append(x[1])
        self.assertEqual(origin[0], x1_val[0])
        self.assertEqual(origin[1], x2_val[0])
        self.assertEqual(dest[0], x1_val[-1])
        self.assertEqual(dest[1], x2_val[-1])

    def test_uarm(self):
        x1_val, x2_val = [], []
        v0 = 1  # HARD CODED
        acc = 2 * (dest - origin - v0 * tf) / (tf ** 2)
        x = np.zeros(2)
        for i in range(num_step + 1):
            t = i * step
            x[0] = uarm(origin[0], v0, acc[0], t)
            x[1] = uarm(origin[1], v0, acc[1], t)
            x1_val.append(x[0])
            x2_val.append(x[1])
        self.assertEqual(origin[0], x1_val[0])
        self.assertEqual(origin[1], x2_val[0])
        self.assertEqual(dest[0], x1_val[-1])
        self.assertEqual(dest[1], x2_val[-1])

    def test_trapezoidal(self):
        # compute vc
        vc = np.sign((dest - origin) / tf)
        vc = vc * np.random.uniform(abs(dest - origin) / tf + 0.001, 2 * abs(dest - origin) / tf)

        t_val, x1_val, x2_val = [], [], []
        x = np.zeros(2)
        flag = [False, False]
        for i in range(num_step + 1):
            t = i * step
            flag[0], x[0] = trapezoidal_profile(origin[0], dest[0], tf, vc[0], t)
            flag[1], x[1] = trapezoidal_profile(origin[1], dest[1], tf, vc[1], t)
            x1_val.append(x[0])
            x2_val.append(x[1])
        self.assertEqual(all(flag), True)
        self.assertEqual(origin[0], x1_val[0])
        self.assertEqual(origin[1], x2_val[0])
        self.assertEqual(dest[0], x1_val[-1])
        self.assertEqual(dest[1], x2_val[-1])

    def test_trapezoidal_failure(self):
        vc = np.random.uniform(2 * abs(dest - origin) / tf, 2 * abs(dest - origin) / tf + 1)
        flag = [False, False]
        flag[0], _ = trapezoidal_profile(origin[0], dest[0], tf, vc[0], 1)
        flag[1], _ = trapezoidal_profile(origin[1], dest[1], tf, vc[1], 1)
        self.assertEqual(all(flag), False)
        pass


if __name__ == '__main__':
    unittest.main()
