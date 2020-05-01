# Motion detection Telegram integrated for Raspberry Pi
If you have a Raspberry Pi with the camera module, with this script you can set up a security system with motion detection. I inspired the bot in *The Palantiri* of the Tolkien Legendarium.

The project is composed of 3 scripts:
- `Motion`: the software that monitors the webcam and takes pictures  when motion is detected.
- `motion.py`: the script triggered by the Motion’s parameter `on_motion_detected ` , that sends a message taken via Telegram to my self.
- `engine.py`: the core of the script. This is the Telegram bot engine which controls the whole project.

## How-to
1. Enable Raspberry Pi camera with `raspi-config`
2. Install required `apt` and `pip` packages:
```sh
sudo apt update
sudo apt install motion
python -m pip install python-telegram-bot
pìp install psutil telegram.ext
```
3. Add your user to `motion` group, in order to can manage `motion`: `sudo usermod -a -G motion <user>`
4. Clone this repository.
5. You'll need your Telegram chat id and a bot API key. After that, add these environment variables with these values: `TELEGRAM_ID`, `PALANTIR_KEY`.
6. Create a `pics/` directory in the working directory.
6. Run the script in daemon mode: `python engine.py`

The main script is running as daemon (you have to kill it manually when needed) and handles a Telegram bot with the following commands:

- `/snap` - *Take a shoot and send it*: uses `raspistill` to take a picture and immediately send it to the Telegram chat.
- `/see` - *Start motion surveillance*: start the Motion software with the personalised configuration file
- `/stop` - *Stop motion surveillance*: stop the Motion software with `proc.kill()`
- `/check`- *Check if motion surveillance is on*: check from `ps` if the Motion software is running
- `/lastphoto` - *Send last picture taken by motion surveillance*: pictures are taken during the motion detection, the last one saved in the /pics folder is sent via Telegram
- `/lastvideo` - *Send last video taken by motion surveillance*: videos are taken during the motion detection, the last one saved in the /pics folder is sent via Telegram
- `/clearphotos` - *Delete all photos taken by motion surveillance*: this delete all the `.jpg` files in the pics directory.
- `/clearvideos` - *Delete all videos taken by motion surveillance*: this delete all the `.avi` files in the pics directory.

_______________________________________________

Forked from and based in ![ttan/motion-detection-telegram](https://github.com/ttan/motion-detection-telegram)