import unittest

from SpaceGame.shared.timer import TimerManager


class TestTimer(unittest.TestCase):
    def test_add_timer(self):
        timers = TimerManager()
        self.assertTrue(timers.add_timer("test_timer", 60, False))

    def test_add_two_timers(self):
        timers = TimerManager()
        self.assertTrue(timers.add_timer("test_timer_1", 60, False))
        self.assertTrue(timers.add_timer("test_timer_2", 60, False))

    def test_lotta_timers(self):
        timers = TimerManager()
        for i in range(0, 10):
            self.assertTrue(timers.add_timer(f"test_timer_{i}", i, False))

    def test_get_timer(self):
        time = 60
        timers = TimerManager()
        timers.add_timer("test_timer", time, False)
        test_timer = timers.get_time("test_timer")
        self.assertEqual(time, test_timer)

    def test_get_lotta_timers(self):
        timers = TimerManager()
        for i in range(0, 10):
            timers.add_timer(f"test_timer_{i}", i, False)
            t = timers.get_time(f"test_timer_{i}")
            self.assertEqual(t, i)

    def test_update_timer(self):
        time = 10
        timers = TimerManager()
        timers.add_timer("test_timer", time, False)
        timers.update_timers(1)
        update_time = timers.get_time("test_timer")
        self.assertEqual(update_time, time - 1)

    def test_update_timer_alot(self):
        time = 10
        timers = TimerManager()
        timers.add_timer("test_timer", time, False)

        for i in range(0, 5):
            timers.update_timers(1)

        update_timer = timers.get_time("test_timer")
        self.assertEqual(update_timer, time - 5)

    def test_update_two_timers(self):
        timers = TimerManager()
        timers.add_timer("test_timer_1", 15, False)
        timers.add_timer("test_timer_2", 10, False)

        for i in range(0, 5):
            timers.update_timers(1)

        self.assertEqual(timers.get_time("test_timer_1"), 10)
        self.assertEqual(timers.get_time("test_timer_2"), 5)

    def test_udpate_lotta_timers(self):
        timers = TimerManager()

        for i in range(0, 10):
            timers.add_timer(f"test_timer_{i}", 20, False)

        for i in range(0, 5):
            timers.update_timers(1)

        for i in range(0, 5):
            t = timers.get_time(f"test_timer_{i}")
            self.assertEqual(t, 15)

    def test_timer_pause(self):
        timers = TimerManager()
        timers.add_timer("test_timer_1", 60, False)

        timers.pause_timer("test_timer_1")
        timers.update_timers(1)

        self.assertEqual(timers.get_time("test_timer_1"), 60)

    def test_timer_pause_start(self):
        timers = TimerManager()
        timers.add_timer("test_timer_1", 60, True)

        timers.update_timers(1)

        self.assertEqual(timers.get_time("test_timer_1"), 60)

    def test_timer_pause_unpause(self):
        timers = TimerManager()
        timers.add_timer("test_timer", 60, False)

        timers.update_timers(1)
        self.assertEqual(timers.get_time("test_timer"), 59)

        timers.pause_timer("test_timer")
        timers.update_timers(1)
        self.assertEqual(timers.get_time("test_timer"), 59)

        timers.unpause_timer("test_timer")
        timers.update_timers(1)
        self.assertEqual(timers.get_time("test_timer"), 58)

    def test_elapsed_timers(self):
        timers = TimerManager()
        timers.add_timer("elapse_timer_1", 5, False)
        timers.add_timer("elapse_timer_2", 10, False)
        timers.add_timer("elapse_timer_3", 15, False)
        timers.add_timer("not_elapsed_timer", 50, False)

        timers.update_timers(10)
        elapsed_timers = timers.get_elapsed_timers()

        self.assertTrue("elapse_timer_1" in elapsed_timers)
        self.assertTrue("elapse_timer_2" in elapsed_timers)
        self.assertTrue("elapse_timer_3" not in elapsed_timers)

