# The Competition

This repository is our entry to the Python Discord Summer Code Jam 2023. In this competition, individuals are randomly allocated 4 other teammates and given just over a week to make something that fits a theme.

This year, the theme was "Secret codes". Submissions also had to incorporate image manipulation, using one of the [approved frameworks](https://www.pythondiscord.com/events/code-jams/10/frameworks/). We chose to use pillow as our primary framework for image manipulation.

Find out more about the competition [here](https://www.pythondiscord.com/events/code-jams/10/).

# Our Program

After our discussion, we decide to made a image manipulation tool which can encoding data or hiding secret codes into selected image, and obfuscate selected text inside the image, so that certain message will become a secret.

This is primarily intended as a command line tool to quickly get things done however we have also made a UI so that it's nice and easy to use for new users. Both interfaces have exactly the same functionality, and each have their strengths and weaknesses so use whichever you prefer.

Our tools include two modes: watermarking and obfuscator.

## 1. Watermarking

This mode uses steganography to hide a secret code in the image (like a hidden watermark) that can help identify the image later. You can then share this image around but it will always have your signature secretly attached to it. For example, you could send the same image with different signatures to different people, and then figure out who leaked it!

## 2. Obfuscator

The other tool is a way of automatically detecting text (or text matching a regex) in an image and automatically obfuscating it. This is useful if you have secret information that you want to remove, you can do it all automatically! For example, you could type "password: .*" to censor all passwords.

# Frameworks Used

Notable frameworks include:
- PySimpleGUI
- numpy
- Google Cloud Vision
- OpenCV

# Example Pictures

Here's some pictures of it working:

## Obfuscator

### Original Image
![Original image](https://cdn.discordapp.com/attachments/1145778261549404243/1151922040547319868/res.jpg)

### Obfuscated
![Obfuscated](https://cdn.discordapp.com/attachments/1145778261549404243/1151922113100398592/image.png)

### Obfuscated (with a regex)
![Obfuscated Regex](https://cdn.discordapp.com/attachments/1145778261549404243/1151922321834115202/image.png)

### Obfuscated (blur instead of black box)
![Obfuscated Blur](https://cdn.discordapp.com/attachments/1145778261549404243/1151922555549138974/image.png)

## Watermarking

![Watermarking](https://cdn.discordapp.com/attachments/1145778261549404243/1151925218227539980/Screenshot_2023-09-14_175629.png)

# Setup

#### Create a virtual environment (optional)
Create a virtual environment in the folder `.venv`.
```shell
$ python -m venv .venv
```

#### Enter the environment (optional)
It will change based on your operating system and shell.
```shell
# Linux, Bash
$ source .venv/bin/activate
# Linux, Fish
$ source .venv/bin/activate.fish
# Linux, Csh
$ source .venv/bin/activate.csh
# Linux, PowerShell Core
$ .venv/bin/Activate.ps1
# Windows, cmd.exe
> .venv\Scripts\activate.bat
# Windows, PowerShell
> .venv\Scripts\Activate.ps1
```

#### Install Dependencies
Use `$ pip install -r requirements.txt` to install the dependencies to run the application.
There are additional requirements to develop the program and run tests under  `$ pip install -r dev-requirements.txt`.
Note that the code base requires Python 3.11+

#### Run the Application
```shell
# run the UI
$ python3 -m app ui
# run the CLI
$ python3 -m app cli <options> <args>
```

#### Example CLI
```shell
# watermark
python3 -m app cli watermark encode "secret message" data/image.jpg data/encoded_image.png
python3 -m app cli watermark decode data/encoded_image.png
secret message

# obfuscate
python3 -m app cli obfuscate data/image.jpg data/output.jpg --regex "\d+" --mode blur
python3 -m app cli obfuscate data/image.jpg data/output.jpg "hide this text" "other text" --mode blur
python3 -m app cli obfuscate data/image.jpg data/output.jpg "hide this text" "other text" --mode colour --colour red
```

#### Running Tests
`$ pytest`

# Known Issues

Unfortunately, not everything always works properly. Here are the issues we're aware of and any potential workarounds:

- Watermarking does not work properly in the GUI. Please use the CLI instead.
- Some unusual images can cause it to malfunction.

# The Team

This was made by:

- smileyface12349
- _jx2
- CactusBrother
- HiPeople
- LokiGray
