import argparse
import sys


class Command:

    def __init__(self, description, usage=None, parent=None, subcommands=None):
        if usage:
            self.parser = argparse.ArgumentParser(description=description, usage=usage)
        else:
            self.parser = argparse.ArgumentParser(description=description)
        self.add_arguments()

        self.parent = parent

        next_parent = parent

        arg_start = 1

        while next_parent is not None:
            arg_start += 1
            next_parent = next_parent.parent

        if subcommands is None:
            arg = sys.argv[arg_start:]
        else:
            arg = sys.argv[arg_start:arg_start+1]
            self.parser.add_argument('subcommand', help='Subcommand to run')

        self.args = self.parser.parse_args(arg)
        if subcommands is not None:
            for command in subcommands:
                if self.args.subcommand == command[0]:
                    self.subcommand = command[1](parent=self)
                    break
            else:
                print('Unrecognized subcommand')
                self.parser.print_help()
                exit(1)

    def add_arguments(self):
        pass

    def execute(self):
        pass
