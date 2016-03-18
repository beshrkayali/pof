from terminaltables import AsciiTable
import subprocess
import polib
import logging

formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')

logger = logging.getLogger('pof')
logger.setLevel(logging.DEBUG)

sh = logging.StreamHandler()
sh.setFormatter(formatter)

logger.addHandler(sh)


class POFixer(object):

    def __init__(self, input_file, output_file=None):
        self.input_file = input_file
        self.output_file = output_file if output_file else input_file
        self.pofile = polib.pofile(input_file)

    def check_errors(self, report=False):
        p = subprocess.Popen(
            ['msgfmt', '-c', self.input_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        out, errs = p.communicate()

        if errs:
            errs = errs.split('\n')

            if len(errs) > 2:
                if len(errs) > 2:
                    msgfmt_errors = errs[len(errs) - 2]

                    if report:
                        logger.warning(
                            "The following errors couldn't be fixed automatically.")

                        table_data = [
                            ['Line Number', 'Error', 'Reason'],
                        ]

                        for e in errs[:len(errs) - 2]:
                            line_num = e[
                                e.index(self.input_file) + len(self.input_file) + 1:
                                e.index(self.input_file) + len(self.input_file) + 1 + e[
                                    e.index(self.input_file) + len(self.input_file) + 1:].find(':')
                            ]
                            message = e[
                                e.index(
                                    self.input_file
                                ) + len(self.input_file) + 1 + e[e.index(self.input_file) +
                                                                 len(self.input_file) + 1:].find(':') + 2:
                            ]

                            reason = ""

                            if 'Reason' in message:
                                reason = message[message.find(
                                    'Reason:'):].replace('Reason:', '')
                                message = message[:message.find('Reason:')]

                            table_data.append(
                                [line_num, message, reason]
                            )

                        table = AsciiTable(
                            table_data, title="--[ {} ]".format(msgfmt_errors.upper()))

                        print table.table

                    return True

        if report:
            logger.info("All complete!")
        return False

    def print_errors(self):
        self.check_errors(report=True)

    def get_fixed(self, i, o, linenum):
        if "\r" in o and "\r" not in i:
            logger.info("Fixing line {}".format(linenum))
            o = o.replace("\r", '')
        if "\n" == i[0] and "\n" != o[0]:
            logger.info("Fixing line {}".format(linenum))
            o = "\n" + o
        elif "\n" != i[0] and "\n" == o[0]:
            logger.info("Fixing line {}".format(linenum))
            o = o.lstrip()
        if "\n" == i[-1] and "\n" != o[-1]:
            logger.info("Fixing line {}".format(linenum))
            o = o + "\n"
        elif "\n" != i[-1] and "\n" == o[-1]:
            logger.info("Fixing line {}".format(linenum))
            o = o.rstrip()

        if '%%' in i and '%%' not in o:
            logger.info("Fixing line {}".format(linenum))
            o = o.replace('%', '%%')

        return o

    def fix_all(self):
        for entry in self.pofile:
            if entry.msgstr != "":
                entry.msgstr = self.get_fixed(
                    i=entry.msgid, o=entry.msgstr, linenum=entry.linenum)
            else:
                for k, v in entry.msgstr_plural.items():
                    entry.msgstr_plural[k] = self.get_fixed(
                        i=entry.msgid, o=v, linenum=entry.linenum)

    def save(self):
        self.pofile.save(self.output_file)
