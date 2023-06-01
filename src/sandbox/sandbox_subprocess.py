import subprocess


def run_command(command):
    subprocess.run(command, check=True)


# Usage
command = ["echo", "Hello, World!"]
run_command(command)
print("Subprocess completed.")
