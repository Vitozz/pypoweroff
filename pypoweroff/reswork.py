#!/usr/bin/env python
#-*- coding: utf-8 -*-
#reswork.py
#

import os

class loadResFile:
    def __init__(self):
        pass

    def get(self, project, fname):
        cwd = str(os.getcwd())
        plist = (cwd,cwd[:-len(project)],"/usr/share", "/usr/local/share", str(os.environ['HOME']) + "/.local/share")
        for path in plist:
            if path:
                try:
                    tmp_path=""
                    if cwd in path:
                        tmp_path = os.path.join(path, fname)
                    else:
                        tmp_path = os.path.join(path, project, fname)
                    if os.path.exists(tmp_path):
                        return str(tmp_path)
                except Exception as error:
                    os.sys.stderr.write("Error when getting path %s" %error)
        return ""

