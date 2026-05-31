#!/usr/local/bin/python

import os
import subprocess

def jail():
    print("Run anything you want! With... some modifications, anyways")

    for _ in range(5):
        cmd = input("$ ")
        cmd = cmd.replace(" ", '')
        cmd = cmd.replace("sh", '')
        if cmd == "exit":
            break
        elif cmd.startswith("cat "):
            print("Nope, can't do that")
        elif cmd.startswith("ls "):
            print("Nope, can't do that")
        else:
            res = subprocess.run("bash -c '" + cmd + "'", shell=True, capture_output=True, env={'PATH': '/tmp:.'})
            print("Input:\n" + cmd)
            if res.returncode != 0:
                print("Error:\n" + res.stderr.decode().strip())
                continue
            print("Output: \n" + res.stdout.decode().strip())


if __name__ == "__main__":
    jail()