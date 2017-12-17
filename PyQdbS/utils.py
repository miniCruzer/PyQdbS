import re

HAS_COLOR = re.compile(r"[\x02\x03\x04\x1B\x1f\x16\x1d\x11\x06]")
MIRC_COLOR = re.compile(r"\x03(?:,\d{1,2}|\d{1,2}(?:,\d{1,2})?)?")
RGB_COLOR = re.compile(r"\x04[0-9a-fA-F]{0,6}")
ECMA48_COLOR = re.compile(r"\x1B\[.*?[\x00-\x1F\x40-\x7E]")
FMT_CODES = re.compile(r"[\x02\x1f\x16\x1d\x11\x06]")

def has_color(s: str) -> bool:

	## ported from IRC::Toolkit
	## https://metacpan.org/source/AVENJ/IRC-Toolkit-0.092002/lib/IRC/Toolkit/Colors.pm#L54

	if HAS_COLOR.match(s):
		return True
	return False

def strip_color(s: str) -> str:

	## ported from IRC::Toolkit
	## https://metacpan.org/source/AVENJ/IRC-Toolkit-0.092002/lib/IRC/Toolkit/Colors.pm#L58

	# mIRC
	s = MIRC_COLOR.sub("", s)

	# RGB
	s = RGB_COLOR.sub("", s)

	# ECMA-48
	s = ECMA48_COLOR.sub("", s)

	# Formatting codes
	s = FMT_CODES.sub("", s)

	# Cancellation code
	return s.replace("\x0f", "")

IRC_TIMESTAMP = re.compile(r"^\[?\d{2}:\d{2}(?::\d{2})?(?: AM| PM)?\]? <", re.M | re.I)

def remove_timestamps(s: str) -> str:
	return IRC_TIMESTAMP.sub("<", quote_str)
