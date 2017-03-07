import re

def has_color(s):

	## ported from IRC::Toolkit
	## https://metacpan.org/source/AVENJ/IRC-Toolkit-0.092002/lib/IRC/Toolkit/Colors.pm#L54

	if re.match("[\x02\x03\x04\x1B\x1f\x16\x1d\x11\x06]", s):
		return True
	return False

def strip_color(s):

	## ported from IRC::Toolkit
	## https://metacpan.org/source/AVENJ/IRC-Toolkit-0.092002/lib/IRC/Toolkit/Colors.pm#L58

	# mIRC
	s = re.sub("\x03(?:,\d{1,2}|\d{1,2}(?:,\d{1,2})?)?", "", s)

	# RGB
	s = re.sub("\x04[0-9a-fA-F]{0,6}", "", s)

	# ECMA-48
	s = re.sub("\x1B\[.*?[\x00-\x1F\x40-\x7E]", "", s)

	# Formatting codes
	s = re.sub("[\x02\x1f\x16\x1d\x11\x06]", "", s)

	# Cancellation code
	return re.sub("\x0f", "", s)


def remove_timestamps(s):

	return re.sub("^a-zA-Z\d\s:]", "", s)