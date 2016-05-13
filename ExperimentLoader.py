# Find here all that is needed to interpret the text files with the description of experiments.
# I do not want to create a full domain language (with loops, conditionals...).
# I don't want to create a new text format just for this.
# Therefore I let the user list the events' constructors in a text file, so I can eval() it line by line.
# Some python syntax may be added "on the fly" to the lines, but it is more conveniente from the point
# of view of the user (otherwise, if we force the user to write some python, execfile() could replace
# this "home-brew" mechanism).

from Events import *  # Pull everything in so that it is in the "scope" of eval().


class ExperimentLoader:
    def load(self, filename, gui):  # Gui must be a local so that eval finds it when it runs the code...
        events = []
        with open(filename, "r") as input_file:
            for line in input_file:
                filtered_line = self._remove_comments(line)
                if filtered_line != "":
                    events.append( eval(filtered_line) )  # TODO: filter code, or an attack becomes possible! Warn the user!
                # TODO: find a a way to kick the GUI out of the constructors!
        return events

    def _remove_comments(self, line):
        comment_start = line.find("#")  # TODO: not perfect: the user can't use # in strings in the file.
        if comment_start == -1:
            return line  # not a comment

        return line[:comment_start]
