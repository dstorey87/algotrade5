"""
IHyperStrategy interface, hyperoptable Parameter class.
This module defines a base class for auto-hyperoptable strategies.
"""

import logging
# REMOVED_UNUSED_CODE: from abc import ABC, abstractmethod
from collections.abc import Sequence
from contextlib import suppress
from typing import Any, Union

from freqtrade.enums import HyperoptState
from freqtrade.optimize.hyperopt_tools import HyperoptStateContainer


with suppress(ImportError):
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     from skopt.space import Categorical, Integer, Real

# REMOVED_UNUSED_CODE:     from freqtrade.optimize.space import SKDecimal

from freqtrade.exceptions import OperationalException


# REMOVED_UNUSED_CODE: logger = logging.getLogger(__name__)


class BaseParameter(ABC):
    """
    Defines a parameter that can be optimized by hyperopt.
    """

# REMOVED_UNUSED_CODE:     category: str | None
    default: Any
    value: Any
    in_space: bool = False
# REMOVED_UNUSED_CODE:     name: str

    def __init__(
        self,
        *,
        default: Any,
        space: str | None = None,
        optimize: bool = True,
        load: bool = True,
        **kwargs,
    ):
        """
        Initialize hyperopt-optimizable parameter.
        :param space: A parameter category. Can be 'buy' or 'sell'. This parameter is optional if
         parameter field
         name is prefixed with 'buy_' or 'sell_'.
        :param optimize: Include parameter in hyperopt optimizations.
        :param load: Load parameter value from {space}_params.
        :param kwargs: Extra parameters to skopt.space.(Integer|Real|Categorical).
        """
        if "name" in kwargs:
            raise OperationalException(
                "Name is determined by parameter field name and can not be specified manually."
            )
# REMOVED_UNUSED_CODE:         self.category = space
# REMOVED_UNUSED_CODE:         self._space_params = kwargs
        self.value = default
        self.optimize = optimize
        self.load = load

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

# REMOVED_UNUSED_CODE:     @abstractmethod
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_space(self, name: str) -> Union["Integer", "Real", "SKDecimal", "Categorical"]:
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Get-space - will be used by Hyperopt to get the hyperopt Space
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """

    def can_optimize(self):
        return (
            self.in_space
            and self.optimize
            and HyperoptStateContainer.state != HyperoptState.OPTIMIZE
        )


# REMOVED_UNUSED_CODE: class NumericParameter(BaseParameter):
# REMOVED_UNUSED_CODE:     """Internal parameter used for Numeric purposes"""
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     float_or_int = int | float
# REMOVED_UNUSED_CODE:     default: float_or_int
# REMOVED_UNUSED_CODE:     value: float_or_int
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         low: float_or_int | Sequence[float_or_int],
# REMOVED_UNUSED_CODE:         high: float_or_int | None = None,
# REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE:         default: float_or_int,
# REMOVED_UNUSED_CODE:         space: str | None = None,
# REMOVED_UNUSED_CODE:         optimize: bool = True,
# REMOVED_UNUSED_CODE:         load: bool = True,
# REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Initialize hyperopt-optimizable numeric parameter.
# REMOVED_UNUSED_CODE:         Cannot be instantiated, but provides the validation for other numeric parameters
# REMOVED_UNUSED_CODE:         :param low: Lower end (inclusive) of optimization space or [low, high].
# REMOVED_UNUSED_CODE:         :param high: Upper end (inclusive) of optimization space.
# REMOVED_UNUSED_CODE:                      Must be none of entire range is passed first parameter.
# REMOVED_UNUSED_CODE:         :param default: A default value.
# REMOVED_UNUSED_CODE:         :param space: A parameter category. Can be 'buy' or 'sell'. This parameter is optional if
# REMOVED_UNUSED_CODE:                       parameter fieldname is prefixed with 'buy_' or 'sell_'.
# REMOVED_UNUSED_CODE:         :param optimize: Include parameter in hyperopt optimizations.
# REMOVED_UNUSED_CODE:         :param load: Load parameter value from {space}_params.
# REMOVED_UNUSED_CODE:         :param kwargs: Extra parameters to skopt.space.*.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if high is not None and isinstance(low, Sequence):
# REMOVED_UNUSED_CODE:             raise OperationalException(f"{self.__class__.__name__} space invalid.")
# REMOVED_UNUSED_CODE:         if high is None or isinstance(low, Sequence):
# REMOVED_UNUSED_CODE:             if not isinstance(low, Sequence) or len(low) != 2:
# REMOVED_UNUSED_CODE:                 raise OperationalException(f"{self.__class__.__name__} space must be [low, high]")
# REMOVED_UNUSED_CODE:             self.low, self.high = low
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             self.low = low
# REMOVED_UNUSED_CODE:             self.high = high
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         super().__init__(default=default, space=space, optimize=optimize, load=load, **kwargs)


# REMOVED_UNUSED_CODE: class IntParameter(NumericParameter):
# REMOVED_UNUSED_CODE:     default: int
# REMOVED_UNUSED_CODE:     value: int
# REMOVED_UNUSED_CODE:     low: int
# REMOVED_UNUSED_CODE:     high: int
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         low: int | Sequence[int],
# REMOVED_UNUSED_CODE:         high: int | None = None,
# REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE:         default: int,
# REMOVED_UNUSED_CODE:         space: str | None = None,
# REMOVED_UNUSED_CODE:         optimize: bool = True,
# REMOVED_UNUSED_CODE:         load: bool = True,
# REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Initialize hyperopt-optimizable integer parameter.
# REMOVED_UNUSED_CODE:         :param low: Lower end (inclusive) of optimization space or [low, high].
# REMOVED_UNUSED_CODE:         :param high: Upper end (inclusive) of optimization space.
# REMOVED_UNUSED_CODE:                      Must be none of entire range is passed first parameter.
# REMOVED_UNUSED_CODE:         :param default: A default value.
# REMOVED_UNUSED_CODE:         :param space: A parameter category. Can be 'buy' or 'sell'. This parameter is optional if
# REMOVED_UNUSED_CODE:                       parameter fieldname is prefixed with 'buy_' or 'sell_'.
# REMOVED_UNUSED_CODE:         :param optimize: Include parameter in hyperopt optimizations.
# REMOVED_UNUSED_CODE:         :param load: Load parameter value from {space}_params.
# REMOVED_UNUSED_CODE:         :param kwargs: Extra parameters to skopt.space.Integer.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         super().__init__(
# REMOVED_UNUSED_CODE:             low=low, high=high, default=default, space=space, optimize=optimize, load=load, **kwargs
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_space(self, name: str) -> "Integer":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Create skopt optimization space.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param name: A name of parameter field.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return Integer(low=self.low, high=self.high, name=name, **self._space_params)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def range(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get each value in this space as list.
# REMOVED_UNUSED_CODE:         Returns a List from low to high (inclusive) in Hyperopt mode.
# REMOVED_UNUSED_CODE:         Returns a List with 1 item (`value`) in "non-hyperopt" mode, to avoid
# REMOVED_UNUSED_CODE:         calculating 100ds of indicators.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self.can_optimize():
# REMOVED_UNUSED_CODE:             # Scikit-optimize ranges are "inclusive", while python's "range" is exclusive
# REMOVED_UNUSED_CODE:             return range(self.low, self.high + 1)
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return range(self.value, self.value + 1)


# REMOVED_UNUSED_CODE: class RealParameter(NumericParameter):
# REMOVED_UNUSED_CODE:     default: float
# REMOVED_UNUSED_CODE:     value: float
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         low: float | Sequence[float],
# REMOVED_UNUSED_CODE:         high: float | None = None,
# REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE:         default: float,
# REMOVED_UNUSED_CODE:         space: str | None = None,
# REMOVED_UNUSED_CODE:         optimize: bool = True,
# REMOVED_UNUSED_CODE:         load: bool = True,
# REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Initialize hyperopt-optimizable floating point parameter with unlimited precision.
# REMOVED_UNUSED_CODE:         :param low: Lower end (inclusive) of optimization space or [low, high].
# REMOVED_UNUSED_CODE:         :param high: Upper end (inclusive) of optimization space.
# REMOVED_UNUSED_CODE:                      Must be none if entire range is passed first parameter.
# REMOVED_UNUSED_CODE:         :param default: A default value.
# REMOVED_UNUSED_CODE:         :param space: A parameter category. Can be 'buy' or 'sell'. This parameter is optional if
# REMOVED_UNUSED_CODE:                       parameter fieldname is prefixed with 'buy_' or 'sell_'.
# REMOVED_UNUSED_CODE:         :param optimize: Include parameter in hyperopt optimizations.
# REMOVED_UNUSED_CODE:         :param load: Load parameter value from {space}_params.
# REMOVED_UNUSED_CODE:         :param kwargs: Extra parameters to skopt.space.Real.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         super().__init__(
# REMOVED_UNUSED_CODE:             low=low, high=high, default=default, space=space, optimize=optimize, load=load, **kwargs
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_space(self, name: str) -> "Real":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Create skopt optimization space.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param name: A name of parameter field.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return Real(low=self.low, high=self.high, name=name, **self._space_params)


# REMOVED_UNUSED_CODE: class DecimalParameter(NumericParameter):
# REMOVED_UNUSED_CODE:     default: float
# REMOVED_UNUSED_CODE:     value: float
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         low: float | Sequence[float],
# REMOVED_UNUSED_CODE:         high: float | None = None,
# REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE:         default: float,
# REMOVED_UNUSED_CODE:         decimals: int = 3,
# REMOVED_UNUSED_CODE:         space: str | None = None,
# REMOVED_UNUSED_CODE:         optimize: bool = True,
# REMOVED_UNUSED_CODE:         load: bool = True,
# REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Initialize hyperopt-optimizable decimal parameter with a limited precision.
# REMOVED_UNUSED_CODE:         :param low: Lower end (inclusive) of optimization space or [low, high].
# REMOVED_UNUSED_CODE:         :param high: Upper end (inclusive) of optimization space.
# REMOVED_UNUSED_CODE:                      Must be none if entire range is passed first parameter.
# REMOVED_UNUSED_CODE:         :param default: A default value.
# REMOVED_UNUSED_CODE:         :param decimals: A number of decimals after floating point to be included in testing.
# REMOVED_UNUSED_CODE:         :param space: A parameter category. Can be 'buy' or 'sell'. This parameter is optional if
# REMOVED_UNUSED_CODE:                       parameter fieldname is prefixed with 'buy_' or 'sell_'.
# REMOVED_UNUSED_CODE:         :param optimize: Include parameter in hyperopt optimizations.
# REMOVED_UNUSED_CODE:         :param load: Load parameter value from {space}_params.
# REMOVED_UNUSED_CODE:         :param kwargs: Extra parameters to skopt.space.Integer.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         self._decimals = decimals
# REMOVED_UNUSED_CODE:         default = round(default, self._decimals)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         super().__init__(
# REMOVED_UNUSED_CODE:             low=low, high=high, default=default, space=space, optimize=optimize, load=load, **kwargs
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_space(self, name: str) -> "SKDecimal":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Create skopt optimization space.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param name: A name of parameter field.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return SKDecimal(
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:             low=self.low, high=self.high, decimals=self._decimals, name=name, **self._space_params
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def range(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get each value in this space as list.
# REMOVED_UNUSED_CODE:         Returns a List from low to high (inclusive) in Hyperopt mode.
# REMOVED_UNUSED_CODE:         Returns a List with 1 item (`value`) in "non-hyperopt" mode, to avoid
# REMOVED_UNUSED_CODE:         calculating 100ds of indicators.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self.can_optimize():
# REMOVED_UNUSED_CODE:             low = int(self.low * pow(10, self._decimals))
# REMOVED_UNUSED_CODE:             high = int(self.high * pow(10, self._decimals)) + 1
# REMOVED_UNUSED_CODE:             return [round(n * pow(0.1, self._decimals), self._decimals) for n in range(low, high)]
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return [self.value]


# REMOVED_UNUSED_CODE: class CategoricalParameter(BaseParameter):
# REMOVED_UNUSED_CODE:     default: Any
# REMOVED_UNUSED_CODE:     value: Any
# REMOVED_UNUSED_CODE:     opt_range: Sequence[Any]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         categories: Sequence[Any],
# REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE:         default: Any | None = None,
# REMOVED_UNUSED_CODE:         space: str | None = None,
# REMOVED_UNUSED_CODE:         optimize: bool = True,
# REMOVED_UNUSED_CODE:         load: bool = True,
# REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Initialize hyperopt-optimizable parameter.
# REMOVED_UNUSED_CODE:         :param categories: Optimization space, [a, b, ...].
# REMOVED_UNUSED_CODE:         :param default: A default value. If not specified, first item from specified space will be
# REMOVED_UNUSED_CODE:          used.
# REMOVED_UNUSED_CODE:         :param space: A parameter category. Can be 'buy' or 'sell'. This parameter is optional if
# REMOVED_UNUSED_CODE:          parameter field
# REMOVED_UNUSED_CODE:          name is prefixed with 'buy_' or 'sell_'.
# REMOVED_UNUSED_CODE:         :param optimize: Include parameter in hyperopt optimizations.
# REMOVED_UNUSED_CODE:         :param load: Load parameter value from {space}_params.
# REMOVED_UNUSED_CODE:         :param kwargs: Extra parameters to skopt.space.Categorical.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if len(categories) < 2:
# REMOVED_UNUSED_CODE:             raise OperationalException(
# REMOVED_UNUSED_CODE:                 "CategoricalParameter space must be [a, b, ...] (at least two parameters)"
# REMOVED_UNUSED_CODE:             )
# REMOVED_UNUSED_CODE:         self.opt_range = categories
# REMOVED_UNUSED_CODE:         super().__init__(default=default, space=space, optimize=optimize, load=load, **kwargs)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     def get_space(self, name: str) -> "Categorical":
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         Create skopt optimization space.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         :param name: A name of parameter field.
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:         return Categorical(self.opt_range, name=name, **self._space_params)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE: # REMOVED_UNUSED_CODE:     @property
# REMOVED_UNUSED_CODE:     def range(self):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Get each value in this space as list.
# REMOVED_UNUSED_CODE:         Returns a List of categories in Hyperopt mode.
# REMOVED_UNUSED_CODE:         Returns a List with 1 item (`value`) in "non-hyperopt" mode, to avoid
# REMOVED_UNUSED_CODE:         calculating 100ds of indicators.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         if self.can_optimize():
# REMOVED_UNUSED_CODE:             return self.opt_range
# REMOVED_UNUSED_CODE:         else:
# REMOVED_UNUSED_CODE:             return [self.value]


# REMOVED_UNUSED_CODE: class BooleanParameter(CategoricalParameter):
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         *,
# REMOVED_UNUSED_CODE:         default: Any | None = None,
# REMOVED_UNUSED_CODE:         space: str | None = None,
# REMOVED_UNUSED_CODE:         optimize: bool = True,
# REMOVED_UNUSED_CODE:         load: bool = True,
# REMOVED_UNUSED_CODE:         **kwargs,
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE:         Initialize hyperopt-optimizable Boolean Parameter.
# REMOVED_UNUSED_CODE:         It's a shortcut to `CategoricalParameter([True, False])`.
# REMOVED_UNUSED_CODE:         :param default: A default value. If not specified, first item from specified space will be
# REMOVED_UNUSED_CODE:          used.
# REMOVED_UNUSED_CODE:         :param space: A parameter category. Can be 'buy' or 'sell'. This parameter is optional if
# REMOVED_UNUSED_CODE:          parameter field
# REMOVED_UNUSED_CODE:          name is prefixed with 'buy_' or 'sell_'.
# REMOVED_UNUSED_CODE:         :param optimize: Include parameter in hyperopt optimizations.
# REMOVED_UNUSED_CODE:         :param load: Load parameter value from {space}_params.
# REMOVED_UNUSED_CODE:         :param kwargs: Extra parameters to skopt.space.Categorical.
# REMOVED_UNUSED_CODE:         """
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         categories = [True, False]
# REMOVED_UNUSED_CODE:         super().__init__(
# REMOVED_UNUSED_CODE:             categories=categories,
# REMOVED_UNUSED_CODE:             default=default,
# REMOVED_UNUSED_CODE:             space=space,
# REMOVED_UNUSED_CODE:             optimize=optimize,
# REMOVED_UNUSED_CODE:             load=load,
# REMOVED_UNUSED_CODE:             **kwargs,
# REMOVED_UNUSED_CODE:         )
