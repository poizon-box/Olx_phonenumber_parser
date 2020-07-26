# Olx_phonenumber_parser
REQUIREMENTS:
beautifulsoup4 == 4.7.1
requests >= 2.21.0


USAGE:
$python3 OLXphone.py <link>

returns 9 digit phone number of advertiser

The script is proof-of-concept. It bypassess the obfuscator preventing phone number picking from OLX.pl.
It basically parses one variable from page content and makes a callback to ajax api to retrieve phone number normally hidden from bots.
