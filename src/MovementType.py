from enum import Enum
import os
import sys

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
sys.path.insert(0, __location__)

class MovementType(Enum):
    urm = 'urm'
    uarm = 'uarm'
    trap = 'trap'
