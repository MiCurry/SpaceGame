from dataclasses import dataclass

import pyglet.clock


@dataclass
class Timer:
    name: str
    duration: int
    time: int
    pause: bool
    elapsed: bool
    restart: bool


class TimerManager:
    def __init__(self):
        self._timers = {}
        self.elapsed_timers = {}
        pyglet.clock.schedule(self.on_update)

    def clear_elapsed(self, name):
        self.elapsed_timers.pop(name)
        if self._timers[name].restart:
            self.restart(name)
        else:
            self._timers.pop(name)

    def get_elapsed(self):
        return self.elapsed_timers

    def is_elapsed(self, name, restart=None) -> bool:
        if name not in self.get_elapsed():
            return False

        self.clear_elapsed(name)
        self.restart(name)
        return True

    def restart(self, name):
        timer = self._timers[name]
        timer.time = timer.duration
        timer.elapsed = False

    def on_update(self, delta_time):
        for _ in self._timers:
            self.update_timers(delta_time)

    def update_timers(self, delta_time):
        for timer_name in self._timers:

            timer = self._timers[timer_name]
            if not timer.pause and not timer.elapsed:
                timer.time -= delta_time

            if timer.time <= 0:
                self.elapsed_timers[timer.name] = timer
                timer.elapsed = True

    def get(self, timer_name) -> int:
        if timer_name not in self._timers:
            return -1

        return self._timers[timer_name].time

    def add(self, name, duration, pause=False, restart=False) -> bool:
        if name in self._timers:
            return False

        self._timers[name] = Timer(name=name,
                                   duration=duration,
                                   time=duration,
                                   pause=pause,
                                   elapsed=False,
                                   restart=restart)
        return True


    def pause(self, timer_name) -> bool:
        if timer_name not in self._timers:
            return False

        self._timers[timer_name].pause = not self._timers[timer_name].pause
        return True

    def unpause(self, timer_name) -> bool:
        self.pause(timer_name)

    def remove(self, timer_name) -> bool:
        if timer_name not in self._timers:
            return False

        self._timers.pop(timer_name)
        return True
