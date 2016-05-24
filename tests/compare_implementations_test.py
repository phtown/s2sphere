from __future__ import print_function, unicode_literals, division

import unittest

import s2  # SWIG wrapped original C++ implementation
import s2sphere


class TestCellId(unittest.TestCase):

    def test_cellid(self):
        lat, lng = (33, -122)
        py_cellid = s2sphere.CellId.from_lat_lng(
            s2sphere.LatLng.from_degrees(lat, lng)
        )
        cpp_cellid = s2.S2CellId.FromLatLng(
            s2.S2LatLng.FromDegrees(lat, lng)
        )
        self.assertEqual(py_cellid.id(), cpp_cellid.id())

    def cellid_parent_comparison(self, level=12):
        lat, lng = (33, -122)
        py_cellid = (s2sphere.CellId
                     .from_lat_lng(s2sphere.LatLng.from_degrees(lat, lng))
                     .parent(level))
        cpp_cellid = (s2.S2CellId
                      .FromLatLng(s2.S2LatLng.FromDegrees(lat, lng))
                      .parent(level))
        self.assertEqual(py_cellid.id(), cpp_cellid.id())

    def test_cellid_parents(self):
        for level in range(1, 31):
            self.cellid_parent_comparison(level)

    def test_cellid_from_truncated_token(self):
        py_cellid = s2sphere.CellId.from_token('89c259c4')
        cpp_cellid = s2.S2CellId.FromToken('89c259c4')
        self.assertEqual(py_cellid.id(), cpp_cellid.id())

    def test_cellid_to_token(self):
        py_cellid = s2sphere.CellId.from_token('89c259c4')
        cpp_cellid = s2.S2CellId.FromToken('89c259c4')
        self.assertEqual(py_cellid.to_token(), cpp_cellid.ToToken())

    def test_zeroprefix_token(self):
        py_cellid = s2sphere.CellId.from_token('03d23c0bdf')
        cpp_cellid = s2.S2CellId.FromToken('03d23c0bdf')
        self.assertEqual(py_cellid.to_token(), cpp_cellid.ToToken())

    def test_metric_level(self):
        # get level 10km scale
        radians = 10 / 6370
        py_level_min = s2sphere.kAvgEdge.get_min_level(radians)
        py_level_closest = s2sphere.kAvgEdge.get_closest_level(radians)
        py_level_max = s2sphere.kAvgEdge.get_max_level(radians)
        self.assertEqual(py_level_min, 10)
        self.assertEqual(py_level_closest, 10)
        self.assertEqual(py_level_max, 9)


if __name__ == '__main__':
    unittest.main()
