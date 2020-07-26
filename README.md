# Olx_phonenumber_parser
Retrieves hidden phone numbers.

REQUIREMENTS:
beautifulsoup4 == 4.7.1
requests >= 2.21.0


USAGE:
$python3 OLXphone.py link

returns 9 digit phone number of advertiser

This simple script is proof-of-concept. It bypassess the obfuscator preventing phone number picking from OLX.pl.
It basically parses one variable from page content and makes a callback to ajax api to retrieve phone number normally hidden from bots.


-----------------------------------------------------------------------------

Prosty skrypt pokazujacy jak latwo mozna obejsc zabezpieczenia anty-botowe w celu zbierania prywatnych numerow telefonow z ogłoszeń.
Skrypt pobiera zmienną ze strony i na jej podstawie wysyła żądanie do ajaxa aby wydobyc ukryty numer telefonu.
