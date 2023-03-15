from __future__ import print_function
import subprocess
from threading import Thread
from django.core.management.commands.runserver import Command as BaseCommand
from django.conf import settings
from termcolor import colored


BEEP_CHARACTER = '\a'


def call_then_log():
    try:
        output = subprocess.check_output('manage.py test --failfast',
                                         stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as ex:
        print(colored(ex.output, 'red', attrs=['bold']))
        print(BEEP_CHARACTER, end='')
        return

    print(output.decode("utf-8"))


def run_background_tests():
    print('Running tests...')
    thread = Thread(target=call_then_log, name='runserver-background-tests')
    thread.daemon = True
    thread.start()


class Command(BaseCommand):
    def inner_run(self, *args, **options):
        run_background_tests()
        super(Command, self).inner_run(*args, **options)