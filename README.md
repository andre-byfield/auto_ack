# auto_ack

Quick python script that uses selenium and sqlite to complete Enlyte's online Covid-19
acknowledgment form (https://leavexpert.com/?ReturnUrl=%2fSelfService) when I log into
my work desktop.

If the job hasn't successfully completed on the day it's run, it will log into the site 
and confirm I'm not suffering from Covid-19 symptoms (if I am, then I STAY HOME!).

To use:

1) Create a copy of auto_ack_credentials.yaml.example, name it auto_ack_credentials.yaml, and provide your email/password.
2) Call auto_ack.py from a scheduler (I'm using Windows Task Scheduler to call it when I log into my machine).

Windows Task Scheduler:
https://www.jcchouinard.com/python-automation-using-task-scheduler/

I'm checking in a .gitignore file to help prevent someone from committing his or her credentials to the branch.