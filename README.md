# pof

A tool that helps you fix common errors usually reported by `msgfmt` when compiling textual translation (po files) to binary messages (mo files).

The tool can take care of a few issues for now, like matching linebreak issues at the beginning and ending of source and translation strings, it can also fix improperly escaped characters in translation strings.

A report of other syntax errors that couldn't be fixed will be printed at the end, in a structure way a bit more readable than `msgfmt`.

```bash
% pof ~/django.po
Processing: /Users/beshr/django.po
[2016-03-24 14:43:53,658] - INFO - Fixing line 1170
[2016-03-24 14:43:53,658] - INFO - Fixing line 1214
...
[2016-03-24 14:43:53,908] - INFO - Fixing line 14525
[2016-03-24 14:43:54,768] - WARNING - The following errors couldn't be fixed automatically.
+--[ MSGFMT: FOUND 3 FATAL ERRORS ]-----------------------------------------------------------+------------------------------------------------------------------------------------+
| Line Number | Error                                                                         | Reason                                                                             |
+-------------+-------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
| 3           | warning: header field 'Last-Translator' still has the initial default value   |                                                                                    |
| 8774        | a format specification for argument 'company_name' doesn't exist in 'msgstr'  |                                                                                    |
| 20385       | a format specification for argument 'interest_rate' doesn't exist in 'msgstr' |                                                                                    |
| 20624       | 'msgstr' is not a valid Python format string, unlike 'msgid'.                 |  In the directive number 7, the character 'y' is not a valid conversion specifier. |
+-------------+-------------------------------------------------------------------------------+------------------------------------------------------------------------------------+
```

# Usecases

There are many ways to end up with po files with broken syntax, mainly I'd say is working with translators who aren't fimilar with `gettext` and the possible errors that could be reported by `msgfmt` when it's compiling textual translations messages to binary ones.

# Installation

The tool is still a work in progress, make a copy of your po file before attempting to to fix it.

If you're using [pipsi](https://github.com/mitsuhiko/pipsi#readme), simply run:

    $ pipsi install .

Otherwise:

    $ pip install .

# Usage

To use it:

    $ pof --help


# License

[MIT License](http://beshr.mit-license.org)