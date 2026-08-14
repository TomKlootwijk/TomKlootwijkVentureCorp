"""UGTS-0: a bounded reference implementation of the unified geometric-topological substrate."""

from .math2d import Vec2
from .state import Entity, EntityState, EventRecord
from .trajectory import LinearTrajectory, QuadraticTrajectory
from .events import EventRule, EventSolver, LineSurface, CircleSurface, GenericFieldSurface
from .support import RadialAngularSupport
from .compatibility import CompatibilityRule, CompatibilityResult
from .transition import TransitionRule
from .world import World
from .topology import MobiusBand, KleinBottleQuotient, PortalMap, HourglassRouter
from .logpolar import LogPolarLUT, LogPolarPoint, to_log_polar, from_log_polar
from .bce import BCEController, BCEMeasurement, BCEDecision, BCEStage
from .grammar import FiniteGrammar, Production, ShapeGrammarCompiler
from .io import load_world, world_from_dict, write_event_log

__all__ = [
    'Vec2', 'Entity', 'EntityState', 'EventRecord',
    'LinearTrajectory', 'QuadraticTrajectory',
    'EventRule', 'EventSolver', 'LineSurface', 'CircleSurface', 'GenericFieldSurface',
    'RadialAngularSupport', 'CompatibilityRule', 'CompatibilityResult',
    'TransitionRule', 'World',
    'MobiusBand', 'KleinBottleQuotient', 'PortalMap', 'HourglassRouter',
    'LogPolarLUT', 'LogPolarPoint', 'to_log_polar', 'from_log_polar',
    'BCEController', 'BCEMeasurement', 'BCEDecision', 'BCEStage',
    'FiniteGrammar', 'Production', 'ShapeGrammarCompiler',
    'load_world', 'world_from_dict', 'write_event_log',
]

__version__ = '1.0.0'
