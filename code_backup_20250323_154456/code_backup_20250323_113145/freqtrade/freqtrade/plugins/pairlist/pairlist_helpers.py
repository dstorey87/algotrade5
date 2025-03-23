import re

# REMOVED_UNUSED_CODE: from freqtrade.constants import Config


# REMOVED_UNUSED_CODE: def expand_pairlist(
# REMOVED_UNUSED_CODE:     wildcardpl: list[str], available_pairs: list[str], keep_invalid: bool = False
# REMOVED_UNUSED_CODE: ) -> list[str]:
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     Expand pairlist potentially containing wildcards based on available markets.
# REMOVED_UNUSED_CODE:     This will implicitly filter all pairs in the wildcard-list which are not in available_pairs.
# REMOVED_UNUSED_CODE:     :param wildcardpl: List of Pairlists, which may contain regex
# REMOVED_UNUSED_CODE:     :param available_pairs: List of all available pairs (`exchange.get_markets().keys()`)
# REMOVED_UNUSED_CODE:     :param keep_invalid: If sets to True, drops invalid pairs silently while expanding regexes
# REMOVED_UNUSED_CODE:     :return: expanded pairlist, with Regexes from wildcardpl applied to match all available pairs.
# REMOVED_UNUSED_CODE:     :raises: ValueError if a wildcard is invalid (like '*/BTC' - which should be `.*/BTC`)
# REMOVED_UNUSED_CODE:     """
# REMOVED_UNUSED_CODE:     result = []
# REMOVED_UNUSED_CODE:     if keep_invalid:
# REMOVED_UNUSED_CODE:         for pair_wc in wildcardpl:
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 comp = re.compile(pair_wc, re.IGNORECASE)
# REMOVED_UNUSED_CODE:                 result_partial = [pair for pair in available_pairs if re.fullmatch(comp, pair)]
# REMOVED_UNUSED_CODE:                 # Add all matching pairs.
# REMOVED_UNUSED_CODE:                 # If there are no matching pairs (Pair not on exchange) keep it.
# REMOVED_UNUSED_CODE:                 result += result_partial or [pair_wc]
# REMOVED_UNUSED_CODE:             except re.error as err:
# REMOVED_UNUSED_CODE:                 raise ValueError(f"Wildcard error in {pair_wc}, {err}")
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:         # Remove wildcard pairs that didn't have a match.
# REMOVED_UNUSED_CODE:         result = [element for element in result if re.fullmatch(r"^[A-Za-z0-9:/-]+$", element)]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     else:
# REMOVED_UNUSED_CODE:         for pair_wc in wildcardpl:
# REMOVED_UNUSED_CODE:             try:
# REMOVED_UNUSED_CODE:                 comp = re.compile(pair_wc, re.IGNORECASE)
# REMOVED_UNUSED_CODE:                 result += [pair for pair in available_pairs if re.fullmatch(comp, pair)]
# REMOVED_UNUSED_CODE:             except re.error as err:
# REMOVED_UNUSED_CODE:                 raise ValueError(f"Wildcard error in {pair_wc}, {err}")
# REMOVED_UNUSED_CODE:     return result


# REMOVED_UNUSED_CODE: def dynamic_expand_pairlist(config: Config, markets: list[str]) -> list[str]:
# REMOVED_UNUSED_CODE:     expanded_pairs = expand_pairlist(config["pairs"], markets)
# REMOVED_UNUSED_CODE:     if config.get("freqai", {}).get("enabled", False):
# REMOVED_UNUSED_CODE:         corr_pairlist = config["freqai"]["feature_parameters"]["include_corr_pairlist"]
# REMOVED_UNUSED_CODE:         expanded_pairs += [pair for pair in corr_pairlist if pair not in config["pairs"]]
# REMOVED_UNUSED_CODE: 
# REMOVED_UNUSED_CODE:     return expanded_pairs
