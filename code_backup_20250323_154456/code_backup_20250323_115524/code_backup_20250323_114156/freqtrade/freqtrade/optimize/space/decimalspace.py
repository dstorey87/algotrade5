import numpy as np
from skopt.space import Integer


# REMOVED_UNUSED_CODE: class SKDecimal(Integer):
# REMOVED_UNUSED_CODE:     def __init__(
# REMOVED_UNUSED_CODE:         self,
# REMOVED_UNUSED_CODE:         low,
# REMOVED_UNUSED_CODE:         high,
# REMOVED_UNUSED_CODE:         decimals=3,
# REMOVED_UNUSED_CODE:         prior="uniform",
# REMOVED_UNUSED_CODE:         base=10,
# REMOVED_UNUSED_CODE:         transform=None,
# REMOVED_UNUSED_CODE:         name=None,
# REMOVED_UNUSED_CODE:         dtype=np.int64,
# REMOVED_UNUSED_CODE:     ):
# REMOVED_UNUSED_CODE:         self.decimals = decimals
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         self.pow_dot_one = pow(0.1, self.decimals)
# REMOVED_UNUSED_CODE:         self.pow_ten = pow(10, self.decimals)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         _low = int(low * self.pow_ten)
# REMOVED_UNUSED_CODE:         _high = int(high * self.pow_ten)
# REMOVED_UNUSED_CODE:         # trunc to precision to avoid points out of space
# REMOVED_UNUSED_CODE:         self.low_orig = round(_low * self.pow_dot_one, self.decimals)
# REMOVED_UNUSED_CODE:         self.high_orig = round(_high * self.pow_dot_one, self.decimals)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         super().__init__(_low, _high, prior, base, transform, name, dtype)
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __repr__(self):
# REMOVED_UNUSED_CODE:         return (
# REMOVED_UNUSED_CODE:             f"Decimal(low={self.low_orig}, high={self.high_orig}, decimals={self.decimals}, "
# REMOVED_UNUSED_CODE:             f"prior='{self.prior}', transform='{self.transform_}')"
# REMOVED_UNUSED_CODE:         )
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def __contains__(self, point):
# REMOVED_UNUSED_CODE:         if isinstance(point, list):
# REMOVED_UNUSED_CODE:             point = np.array(point)
# REMOVED_UNUSED_CODE:         return self.low_orig <= point <= self.high_orig
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def transform(self, Xt):
# REMOVED_UNUSED_CODE:         return super().transform([int(v * self.pow_ten) for v in Xt])
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     def inverse_transform(self, Xt):
# REMOVED_UNUSED_CODE:         res = super().inverse_transform(Xt)
# REMOVED_UNUSED_CODE:         # equivalent to [round(x * pow(0.1, self.decimals), self.decimals) for x in res]
# REMOVED_UNUSED_CODE:         return [int(v) / self.pow_ten for v in res]
