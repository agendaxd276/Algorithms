import unittest

from tools.tracers import (BINARY_EXAMPLE, LINEAR_EXAMPLE, SORT_EXAMPLE, TRACERS)


class TracerTests(unittest.TestCase):
    def test_sorts_end_sorted(self):
        for name, tracer in TRACERS.items():
            if name.endswith("_sort"):
                frames, final = tracer()
                self.assertEqual(final, sorted(SORT_EXAMPLE), name)
                self.assertEqual(frames[-1]["arr"], sorted(SORT_EXAMPLE), name)
                self.assertTrue(any(f["milestone"] for f in frames), name)

    def test_searches_find_the_key(self):
        frames, idx = TRACERS["linear_search"]()
        self.assertEqual(LINEAR_EXAMPLE[0][idx], LINEAR_EXAMPLE[1])
        frames, idx = TRACERS["binary_search"]()
        self.assertEqual(BINARY_EXAMPLE[0][idx], BINARY_EXAMPLE[1])

    def test_every_frame_is_a_permutation(self):
        for name, tracer in TRACERS.items():
            if name.endswith("_sort"):
                for f in tracer()[0]:
                    self.assertEqual(sorted(f["arr"]), sorted(SORT_EXAMPLE), f"{name}: {f['caption']}")


if __name__ == "__main__":
    unittest.main()
