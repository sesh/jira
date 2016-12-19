#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys
import webbrowser


ticket_re = re.compile('\w{2,5}\-\d{1,9}')


def jira():
    # get the branch name
    try:
        cmd = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE, check=True)
        branch = cmd.stdout.strip().decode()
    except subprocess.CalledProcessError:
        sys.exit("Failed to get git branch")

    # find the ticket number
    match = ticket_re.search(branch)
    if not match:
        sys.exit("Could not detect JIRA ticket number")

    jira_ticket = match.group(0)

    # find the .jira file / base URL
    cwd = os.getcwd()
    cwd_parts = cwd.split('/')

    base_url = ''

    for x in range(len(cwd_parts), 1, -1):
        fn = '/'.join(cwd_parts[:x]) + '/.jira'

        try:
            base_url = [x.strip() for x in open(fn).readlines() if not x.strip().startswith('#')][0]

            # do some cleaning up
            if base_url.endswith('/'):
                base_url = base_url[:-1]

            break
        except FileNotFoundError:
            pass
        except IndexError:
            sys.exit("{} found but not formatted correctly".format(fn))

    if not base_url:
        sys.exit("Could not find .jira file")

    # open the URL
    url = base_url + '/browse/' + jira_ticket
    webbrowser.open(url)


if __name__ == '__main__':
    jira()
