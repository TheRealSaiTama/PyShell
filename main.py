#!/usr/bin/env python3

import os
import sys
import subprocess
from typing import Dict, List, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import readline
from pathlib import Path

class ShellCommand(ABC):
    @abstractmethod
    def execute(self, args: List[str]) -> None:
        pass

class ExitCommand(ShellCommand):
    def execute(self, args: List[str]) -> None:
        try:
            code = int(args[0]) if args else 0
            sys.exit(code)
        except ValueError:
            print("exit: Invalid exit code")

class EchoCommand(ShellCommand):
    def execute(self, args: List[str]) -> None:
        print(" ".join(args))

class TypeCommand(ShellCommand):
    def __init__(self, builtins: Dict[str, ShellCommand]):
        self.builtins = builtins

    def execute(self, args: List[str]) -> None:
        if not args:
            print("type: usage: type <command>")
            return

        cmd = args[0]
        print(cmd, end="")

        if cmd in self.builtins:
            print(" is a shell builtin")
        elif path := PathResolver.findinpath(cmd):
            print(f" is {path}")
        else:
            print(": not found")

class PwdCommand(ShellCommand):
    def execute(self, args: List[str]) -> None:
        print(os.getcwd())

class CdCommand(ShellCommand):
    def execute(self, args: List[str]) -> None:
        path = args[0] if args else os.path.expanduser("~")
        try:
            os.chdir(path)
        except FileNotFoundError:
            print(f"cd: {path}: No such file or directory")
        except NotADirectoryError:
            print(f"cd: {path}: Not a directory")
        except OSError as e:
            print(f"cd: {path}: {e}")

class PathResolver:
    @staticmethod
    def findinpath(cmd: str) -> Optional[str]:
        pathdirs = os.environ.get("PATH", "").split(os.pathsep)
        for directory in pathdirs:
            fullpath = os.path.join(directory, cmd)
            if os.path.exists(fullpath) and os.access(fullpath, os.X_OK):
                return fullpath
        return None

class Completer:
    def __init__(self, builtins: Dict[str, ShellCommand]):
        self.builtins = builtins

    def complete(self, text, state):
        if state == 0:
            parts = text.split()
            if not parts:
                self.matches = [cmd for cmd in self.builtins] + [p.name for p in Path('.').iterdir()]
                return self.matches[state] if state < len(self.matches) else None
            
            if len(parts) == 1:
                self.matches = [cmd for cmd in self.builtins if cmd.startswith(parts[0])] + [
                    p.name for p in Path('.').iterdir() if p.name.startswith(parts[0])
                ]
            elif len(parts) >= 2:
                current_path = Path('.')
                if parts[-2] == "cd":
                    target = parts[-1]
                    if target.startswith("/"):
                        current_path = Path("/")
                        target = target[1:]
                    
                    for component in target.split("/"):
                        if component == "..":
                            current_path = current_path.parent
                        elif component and component != ".":
                            current_path = current_path / component
                    
                    if not current_path.is_dir():
                        current_path = current_path.parent if current_path.parent.is_dir() else Path(".")

                    self.matches = [
                        (str(p) + "/") if p.is_dir() else str(p)
                        for p in current_path.iterdir()
                        if str(p.name).startswith(parts[-1])
                    ]
                else:
                    self.matches = [
                        (str(p) + "/") if p.is_dir() else str(p)
                        for p in current_path.iterdir()
                        if str(p.name).startswith(parts[-1])
                    ]
            else:
                self.matches = []
        try:
            return self.matches[state]
        except IndexError:
            return None

class Shell:
    def __init__(self):
        self.builtins: Dict[str, ShellCommand] = {}
        self.initializebuiltins()
        self.completer = Completer(self.builtins)
        readline.set_completer(self.completer.complete)
        readline.parse_and_bind("tab: complete")

    def initializebuiltins(self) -> None:
        self.builtins.update({
            "exit": ExitCommand(),
            "echo": EchoCommand(),
            "pwd": PwdCommand(),
            "cd": CdCommand(),
        })
        self.builtins["type"] = TypeCommand(self.builtins)

    def executeexternalcommand(self, tokens: List[str]) -> None:
        try:
            result = subprocess.run(tokens, capture_output=True, text=True, check=True)
            print(result.stdout, end="")
        except FileNotFoundError:
            print(f"{tokens[0]}: command not found")
        except subprocess.CalledProcessError as e:
            print(e.stderr, end="")
        except OSError as e:
            print(f"Error executing {tokens[0]}: {e}")

    def processinput(self, inputstr: str) -> None:
        tokens = inputstr.strip().split()
        if not tokens:
            return

        cmdname, cmdargs = tokens[0], tokens[1:]

        if cmdname in self.builtins:
            self.builtins[cmdname].execute(cmdargs)
        elif PathResolver.findinpath(cmdname):
            self.executeexternalcommand(tokens)
        else:
            print(f"{cmdname}: command not found")
    
    def run(self) -> None:
        while True:
            try:
                inputstr = input("$ ")
                self.processinput(inputstr)
            except KeyboardInterrupt:
                print()

def main():
    Shell().run()

if __name__ == "__main__":
    main()