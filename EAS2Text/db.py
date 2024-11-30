# Standard Library
from typing import Any, Iterable

# Local Folder
from .errors import *


class db(object):

    def __init__(self) -> None:
        """Create the EAS Database."""
        self.countries: list[str] = ["US", "CA"]


    def get_locs_from_fips(
        self, fips_codes: Iterable[str], country: str = "US"
    ) -> dict[str, dict]:
        ## Define some pre-processing values:
        ## seen_fips used for keeping track of duplicates
        ## process_fips used for tracking regional and area mappings
        ## locs used for returned storage area
        seen_fips = []
        process_fips = {}
        locs = {
            "country": {"name": "", "abbrev": ""},
            "regions": {},
        }

        ## Use canadian FIPS codes if defined. Define output country.
        if country == "CA":
            locs["country"]["name"] = self.same_fips_ca["name"]
            locs["country"]["abbrev"] = self.same_fips_ca["abbrev"]
            samelist = self.same_fips_ca
        else:
            locs["country"]["name"] = self.same_fips_us["name"]
            locs["country"]["abbrev"] = self.same_fips_us["abbrev"]
            samelist = self.same_fips_us

        ## Process input into valid fips codes
        for fips_code in fips_codes:
            ## Skip if already processed
            if fips_code in seen_fips:
                continue
            else:
                seen_fips.append(fips_code)
                try:
                    ## Make sure the code is numeric
                    assert fips_code.isnumeric()
                    ## Make sure the code is 5 or 6 chars long
                    assert len(fips_code) >= 5 and len(fips_code) <= 6
                    ## Zfill to make sure in range
                    _valid_fips = fips_code.zfill(6)
                    ## Get Sub, Reg, Code from SAME FIPS
                    _subdiv = _valid_fips[0]
                    _region = _valid_fips[1:3]
                    _area = _valid_fips[3:6]
                    ## Check if region already defined, if not define it.
                    if _region in process_fips.keys():
                        process_fips[_region] += [
                            {"sub": _subdiv, "area": _area}
                        ]
                    else:
                        process_fips[_region] = [
                            {"sub": _subdiv, "area": _area}
                        ]
                except AssertionError:
                    raise InvalidSAME(fips_code, "Invalid SAME FIPS code.")

        ## Process fips codes
        for _region in process_fips.keys():
            ## Process region data:
            try:
                ## Define Region format
                reg = {"abbrev": "", "type": "", "locs": []}
                ## Check if region is valid in our FIPS list
                if _region in list(samelist.keys()):
                    reg_name = samelist[_region]["name"]
                    reg["abbrev"] = samelist[_region]["abbrev"]
                    reg["type"] = samelist[_region]["type"]
                ## Create an unknown loc if not defined
                else:
                    reg_name = f"Unknown"
                    reg["abbrev"] = ""
                    reg["type"] = ""

                ## Check if region is defined in our final output, if not define it.
                if reg_name not in locs["regions"].keys():
                    locs["regions"][reg_name] = reg
            except Exception as E:
                raise InvalidSAME(_region, f"Error ({E}) on processing region.")

            ## Process area codes:
            ## All Loc codes (000) get special processing based off of subdivision.
            ## Otherwise use "<subdiv> <area>"
            try:
                for codes in process_fips[_region]:
                    subdiv = self.same_fips_subdivisions[codes["sub"]]
                    code = codes["area"]
                    if code != "000":
                        if "Unknown" not in reg_name:
                            if code in samelist[_region]["codes"].keys():
                                area = samelist[_region]["codes"][code]
                            else:
                                area = f"Unknown FIPS ({_region}{code})"
                        else:
                            area = f"Unknown FIPS ({_region}{code})"
                        locs["regions"][reg_name]["locs"] += [
                            f"{subdiv} {area}".strip()
                        ]
                    else:
                        if subdiv == "":
                            area = samelist["00"]["codes"][code]
                            locs["regions"][reg_name]["locs"] += [
                                f"{area} {reg_name}".strip()
                            ]
                        else:
                            locs["regions"][reg_name]["locs"] += [
                                f"{subdiv} {reg_name}".strip()
                            ]
            except Exception as E:
                raise InvalidSAME(
                    _region, f"Error ({E}) on processing area code."
                )
        return locs

    def get_event(
        self, event_code: str, use_alt_names: bool = False
    ) -> dict[str, str]:
        try:
            ## Make sure the event is alphanumeric
            assert event_code.isalnum()
            ## Make sure the event is 3 chars long
            assert len(event_code) == 3
            ## Check if the event is valid
            if event_code in self.same_event_codes.keys():
                code = self.same_event_codes[event_code]
                name = code["name"]
                article = code["article"]
                ## swap to alternate names if requested
                if use_alt_names:
                    if "name_alt" in code.keys():
                        name = code["name_alt"]
                    if "article_alt" in code.keys():
                        article = code["article_alt"]
                return {
                    "name": name,
                    "sentance": f"{article} {name}".strip(),
                    "severity": code["severity"],
                }
            ## check if valid unknown event
            elif f"**{event_code[2]}" in self.same_event_codes:
                code = self.same_event_codes[f"**{event_code[2]}"]
                name = f"{code["name"]} ({event_code})".strip()
                article = code["article"]
                return {
                    "name": name,
                    "sentance": f"{article} {name}".strip(),
                    "severity": code["severity"],
                }
            ## return unknown event if invalid
            else:
                name = f"Unknown Event ({event_code})".strip()
                article = f"An"
                severity = "Statement"
                return {
                    "name": name,
                    "sentance": f"{article} {name}".strip(),
                    "severity": severity,
                }
        except AssertionError:
            raise InvalidSAME(event_code, "Invalid SAME event code.")

    def get_originator(
        self, originator_code: str, use_alt_names: bool = False
    ) -> dict[str, str]:
        try:
            ## Make sure the originator is alphanumeric
            assert originator_code.isalnum()
            ## Make sure the originator is 3 chars long
            assert len(originator_code) == 3
            ## Check if the originator is valid
            if originator_code in self.same_originator_codes.keys():
                code = self.same_originator_codes[originator_code]
                name = code["name"]
                article = code["article"]
                end = code["end"]
                ## swap to alternate names if requested
                if use_alt_names:
                    if "name_alt" in code.keys():
                        name = code["name_alt"]
                    if "article_alt" in code.keys():
                        article = code["article_alt"]
                    if "end_alt" in code.keys():
                        end = code["end_alt"]
                return {
                    "name": name,
                    "sentance": f"{article} {name} {end}".strip(),
                }
            ## return unknown originator if invalid
            else:
                name = f"Unknown Originator ({originator_code})".strip()
                article = f"An"
                end = "has"
                return {
                    "name": name,
                    "sentance": f"{article} {name} {end}".strip(),
                }
        except AssertionError:
            raise InvalidSAME(originator_code, "Invalid SAME originator code.")
