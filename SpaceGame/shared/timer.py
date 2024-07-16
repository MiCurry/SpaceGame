from dataclasses import dataclass


@dataclass
class Timer:
    name: str
    duration: int
    time: int
    pause: bool
    elapsed: bool


class TimerManager:
    def __init__(self):
        self._timers = {}
        self.elapsed_timers = {}

    def clear_elapsed_timer(self, timer_name):
        self.elapsed_timers.pop(timer_name)

    def get_elapsed_timers(self):
        return self.elapsed_timers

    def on_update(self, delta_time):
        for _ in self._timers:
            self.update_timer(delta_time)

    def update_timers(self, delta_time):
        for timer_name in self._timers:

            timer = self._timers[timer_name]
            if not timer.pause and not timer.elapsed:
                timer.time -= delta_time

            if timer.time <= 0:
                self.elapsed_timers[timer.name] = timer
                timer.elapsed = True

    def get_time(self, timer_name) -> int:
        if timer_name not in self._timers:
            return -1

        return self._timers[timer_name].time

    def add_timer(self, timer_name, duration, pause=False) -> bool:
        if timer_name in self._timers:
            return False

        self._timers[timer_name] = Timer(name=timer_name, duration=duration, time=duration, pause=pause, elapsed=False)
        return True

    def pause_timer(self, timer_name) -> bool:
        if timer_name not in self._timers:
            return False

        self._timers[timer_name].pause = not self._timers[timer_name].pause
        return True

    def unpause_timer(self, timer_name) -> bool:
        self.pause_timer(timer_name)

    def remove_timer(self, timer_name) -> bool:
        if timer_name not in self._timers:
            return False

        self._timers.pop(timer_name)
        return True
