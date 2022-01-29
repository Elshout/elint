#!/usr/bin/env bash

NEWLINE=$'\n'
TAB=$'\t'
python -c "import os${NEWLINE}import py_compile${NEWLINE}import pathlib${NEWLINE}import zipapp${NEWLINE}${NEWLINE}modules = pathlib.Path(os.getcwd() + os.path.sep + 'modules')${NEWLINE}build = pathlib.Path(os.getcwd() + os.path.sep + 'build')${NEWLINE}out = pathlib.Path(os.getcwd() + os.path.sep + 'build' + os.path.sep + 'out')${NEWLINE}for mod in modules.glob('*.py'):${NEWLINE}${TAB}py_compile.compile(file = mod, cfile = out / mod.name.replace('.py', '.pyc'), optimize = 2, invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH)${NEWLINE}zipapp.create_archive(out, target=build / 'elint.pyz', interpreter='/usr/bin/env python3', main='main:main', compressed=True)"
