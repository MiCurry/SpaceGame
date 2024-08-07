from dataclasses import dataclass

@dataclass
class PidInput:
    kp: float
    kp: float
    ki: float
    kd: float
    tau: float
    lim_min: float
    lim_max: float
    lim_min_init: float
    lim_max_init: float

@dataclass
class PidData:
    integrator: float
    errorAccum: float
    prevError: float
    differentiator: float
    prevMeasurement: float


class Pid:
    def __init__(self,
                 pid_input,
                 anti_integral_windup=True,
                 debug=False,
                 # Probably want the below to be zero
                 integrator=0.0,
                 errorAccum=0.0,
                 prevError=0.0,
                 differentiator=0.0,
                 prevMeasurment=0.0):

        self.anti_integral_windup = anti_integral_windup
        self.input = pid_input
        self.data = PidData(integrator=integrator,
                            errorAccum=errorAccum,
                            prevError=prevError,
                            differentiator=differentiator,
                            prevMeasurement=prevMeasurment)
        self.debug = debug

    def update(self, setpoint: float, measurement: float, dt):
        error = setpoint - measurement

        proportion = self.input.kp * error
        self.data.integrator = self.data.errorAccum + self.input.ki * error * dt
        self.data.differentiator = self.input.kd * (error - self.data.prevError) / dt

        output = proportion + self.data.integrator + self.data.differentiator

        if output > self.input.lim_max:
            output = self.input.lim_max
        elif output < self.input.lim_min:
            output = self.input.lim_min

        if self.debug:
            print(f"E:{error} "
                f"DE:{error - self.data.prevError} "
                  f"P:{proportion} "
                  f"I:{self.data.integrator} "
                  f"D:{self.data.differentiator} "
                  f"O: {output} ")

        self.data.prevError = error
        self.data.errorAccum = self.data.integrator

        return output