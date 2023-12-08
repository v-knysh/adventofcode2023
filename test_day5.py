import unittest
from day5 import MapFunction, Range, RangeMap

# Create a test class that inherits from unittest.TestCase
class TestRanges(unittest.TestCase):

    # def test_1(self):
    #     rm = RangeMap.from_str('1000 100 100')
    #     r = Range(110, 120)
    #     spl = rm.split_values_range(r)
    #     self.assertEqual(len(spl), 1)
    #     self.assertEqual(spl[0].start, 110)
    #     self.assertEqual(spl[0].end, 120)
        
    # def test_2(self):
    #     rm = RangeMap.from_str('1000 100 100')
    #     r = Range(50, 150)
    #     spl = rm.split_values_range(r)
    #     self.assertEqual(len(spl), 2)
    #     self.assertEqual(spl[0], Range(50, 99))
    #     self.assertEqual(spl[1], Range(100, 150))
    
    # def test_3(self):
    #     rm = RangeMap.from_str('1000 100 100')
    #     r = Range(150, 250)
    #     spl = rm.split_values_range(r)
    #     self.assertEqual(len(spl), 2)
    #     self.assertEqual(spl[0], Range(150, 199))
    #     self.assertEqual(spl[1], Range(200, 250))
        
    # def test_4(self):
    #     mf = MapFunction.from_map_str("1000 100 100\n2000 200 100")
    #     self.assertEqual(len(mf.ranges), 2)
    #     self.assertEqual(mf.ranges[1].source_start, 200)
    #     self.assertEqual(mf.ranges[1].dest_end, 2099)
    
    # def test_5(self):
    #     mf = MapFunction.from_map_str("1000 100 100")
    #     ranges = [Range(0, 50), Range(80, 150), Range(190, 220), Range(250, 350)]
    #     splitted_ranges = mf._splitted_ranges(ranges)
    #     self.assertEqual(len(splitted_ranges), 6)
    
    def test_6(self):
        mf = MapFunction.from_map_str("1000 100 100")
        ranges = [Range(0, 300)]
        splitted_ranges = mf(ranges)
        print('ok')
        self.assertEqual(len(splitted_ranges), 3)


if __name__ == '__main__':
    unittest.main()