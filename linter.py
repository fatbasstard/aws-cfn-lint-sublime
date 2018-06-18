#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Markus Liljedahl
# Copyright (c) 2017 Markus Liljedahl
#
# License: MIT
#

from SublimeLinter.lint import Linter, util

import re

class CfnLint(Linter):
    """Provides an interface to cfn-lint."""

    cmd = ('cfn-lint', '--template', '${file}', '--format', 'parseable')
    executable = None
    version_args = '--version'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 3.0.1'
    regex = r'^.+?:(?P<line>\d+):(?P<col>\d+):\d+:\d+:((?P<warning>W)|(?P<error>E))(?P<code>.{4}):(?P<message>.+)'
    multiline = True
    line_col_base = (1, 1)
    tempfile_suffix = '-'
    error_stream = util.STREAM_STDOUT
    word_re = None
    comment_re = r'\s*#'

    defaults = {
        'selector': 'source.yaml, source.json',
        'strict': True
    }

    def communicate(self, cmd, code=None):
        """Run an external executable using stdin to pass code and return its output."""
        relfilename = self.filename

        is_cfn = False;

        # Check if we're processing a CloudFormation file
        with open(relfilename, 'r', encoding='utf8') as file:
            content = file.read()
            regex = re.compile(r'"?AWSTemplateFormatVersion"?\s*')

            if regex.search(content):
                is_cfn = True;

        if is_cfn:
            return super().communicate(cmd, code)
