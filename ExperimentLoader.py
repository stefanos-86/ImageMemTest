# Find here all that is needed to interpret the text files with the description of experiments.
# I do not want to create a full domain language (with loops, conditionals...).
# I don't want to create a new text format just for this.
# Therefore I let the user list the events' constructors in a text file, so I can eval() it line by line.
# Some python syntax may be added "on the fly" to the lines, but it is more conveniente from the point
# of view of the user (otherwise, if we force the user to write some python, execfile() could replace
# this "home-brew" mechanism).
#
# There is the risk of an attacker being able to pass a file with a malicious expression that would go
# trough the eval. The risk is mitigated because the users are not supposed to take files from 3rd parties
# (e.g. the internet) and if the attacker can compromise a file in the user PC... he could well change the Python code
# of the application directly!

from Events import *  # Pull everything in so that it is in the "scope" of eval().

import os

class ExperimentLoader:
    def load(self, filename, gui, image_collection):
        events = None
        with open(filename, "r") as input_file:
            events = self.parse_input_file(input_file, filename, gui, image_collection)
        return events

    def parse_input_file(self, input_file, filename, gui, image_collection):
        """ Public only for testability reasons. """
        events = []
        line_counter = 0
        for line in input_file:
            line_counter += 1
            filtered_line = self._remove_comments(line)
            filtered_line = self._remove_whitespace(filtered_line)
            if filtered_line != "":
                try:
                    # The construction has to be completed outside the constructor.
                    # This way the user can write "simplified" constructors in the experiment file.
                    # ...but I start to think this is not a good idea.
                    new_event = eval(filtered_line)
                    new_event.attach_images(image_collection)
                    new_event.attach_gui(gui)
                except Exception as problem:
                    self._friendly_error_message(filename, line, line_counter, problem)

                events.append(new_event)
        return events


    def _remove_comments(self, line):
        comment_start = line.find("#")
        if comment_start == -1:
            return line  # not a comment

        return line[:comment_start]

    def _remove_whitespace(self, line):
        return line.strip()

    def _friendly_error_message(self, filename, line, lineno, problem):
        """ Users are scientists, not programmers. Try to hide the stack trace
            from them, but still give useful error messages."""
        message = "Error in file " + os.path.abspath(filename) + " at line " + str(lineno) + ":\n"
        message += "\n" + line + "\n"
        message += str(problem)

        raise Exception(message)

