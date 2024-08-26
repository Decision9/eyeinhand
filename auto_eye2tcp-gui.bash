#!/bin/bash
source /home/yofo/gitlab/aiws_alpha_version_2024/version/env.sh

{
    gnome-terminal -t "gui" -x bash -c -i "conda activate aiws && cd ~/gitlab/aiws_alpha_version_2024/version/weld_calib_sdk && python auto_eye2tcp_gui_1.1.py; exec bash"
}