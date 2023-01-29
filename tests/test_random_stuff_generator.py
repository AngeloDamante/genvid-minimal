import unittest
import json
from src.LoggingManager import configure_logging
from create_random_route import generate_number_with_sum, routes_generator
from create_random_sequence import json_generator


class TestRandomRouteGenerator(unittest.TestCase):
    def test_generate_number_with_sum(self):
        configure_logging()
        for n in range(1, 100):
            for sigma in range(n, 1000):
                values = generate_number_with_sum(n, sigma)
                self.assertEqual(sum(values), sigma)
                self.assertEqual(len(values), n)
                self.assertEqual(all([val > 0 for val in values]), True)

        # case sum < n
        values = generate_number_with_sum(5, 3)
        self.assertEqual(sum(values), 3)

        # with min_value
        values = generate_number_with_sum(5, 1000, 100)
        self.assertEqual(sum(values), 1000)
        self.assertEqual(min(values) >= 100, True)
        values = generate_number_with_sum(5, 1000, 300)
        self.assertEqual(min(values) >= 300, True)

    def test_routes_generator(self):
        num_instructions = 10
        duration = 2000
        frame_size = (720, 640)
        instructions = routes_generator(num_instructions, duration, frame_size)

        # take into account the origin
        self.assertEqual(len(instructions), num_instructions + 1)

        # save file
        with open(f"../routes/test_routes.txt", 'w+') as outfile:
            outfile.writelines(instructions)


class TestRandomSequenceGenerator(unittest.TestCase):
    def test_json_generator(self):
        sequence = json_generator(5)
        self.assertEqual(len(sequence), 5)
        with open(f"../sequences/test_sequence.json", 'w+') as outfile:
            json.dump(sequence, outfile)


if __name__ == '__main__':
    unittest.main()
