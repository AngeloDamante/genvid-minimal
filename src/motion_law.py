from typing import Tuple


def urm(x_0: float, v_m: float, t: float) -> float:
    """Compute Uniform Rectilinear Motion (U.R.M) law.

    Args:
        x_0(float): initial point
        v_m(float): constant velocity
        t(float): time

    Returns:
        x(float): $$ x_0 + v_m * t $$
    """
    return x_0 + v_m * t


def uarm(x_0: float, v_0: float, a_m: float, t: float) -> float:
    """Compute Uniformly Accelerated Rectilinear Motion (U.A.R.M) law.

    Args:
        x_0(float): initial point
        v_0(float): initial velocity
        a_m(float): constant acceleration
        t(float): time

    Returns:
        x(float): $$ x_0 + v_0 * t + 0.5 * a_m * (t ** 2) $$
    """
    return x_0 + v_0 * t + 0.5 * a_m * (t ** 2)


def trapezoidal_profile(x_i: float, x_f: float, t_f: float, v_c: float, t: float) -> Tuple[bool, float]:
    """Compute motion law with trapezoidal profile for velocity.

    v_c --- /----------\
           / |        | \
          /  |        |  \
           tc_1     tc_2  t_f

    cruise velocity condition:
        \[
            \frac{\vert x_f - x_i \vert}{t_f} < \vert v_c \vert \leq 2 \frac{\vert x_f - x_i \vert}{v_c}
        \]

    Args:
        x_i(float): initial position
        x_f(float): final position
        t_f(float): final time (duration)
        v_c(float): cruise velocity
        t(float): time

    Returns:
        flag(bool): cruise velocity condition check
        x(float): motion law
    """
    if abs(v_c) <= abs(x_f - x_i) / t_f or abs(v_c) > 2 * abs(x_f - x_i) / t_f:
        return False, x_i

    t_c = (x_i - x_f + v_c * t_f) / v_c
    acc = (v_c ** 2) / (x_i - x_f + v_c * t_f)

    tc_1 = t_c
    tc_2 = t_f - t_c

    if t <= tc_1:
        return True, x_i + 0.5 * acc * t ** 2
    elif tc_1 < t <= tc_2:
        return True, x_i + acc * tc_1 * t - 0.5 * acc * tc_1 ** 2
    elif t > tc_2:
        return True, x_f - 0.5 * acc * (t_f - t) ** 2
