# Software & utils to monitor 3D stem cell culture

This project consists of a software application and utilities needed to complement
the thesis topic **Investigation of machine learning methods to monitor 3D stem cell culture
in a bioreactor** and it is just a prototype to illustrate how the trained models work.

It ONLY supports:

```
PRETTY_NAME="Debian GNU/Linux 11 (bullseye)"
NAME="Debian GNU/Linux"
VERSION_ID="11"
VERSION="11 (bullseye)"
VERSION_CODENAME=bullseye
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
```

Could run on a Raspberry Pi 3, but preferred on a Raspberry Pi 4

## Installation & run

1. You can install the dependencies by typing:

```
bash  install_pkgs.sh
```

2. It is necessary to download and use some modules from [YOLOv5](https://github.com/ultralytics/yolov5).
   the following command clones the repository and locates the relevant code in the correct path

```
bash  prework.sh
```

3. The application is executed by:

```
bash  run.sh
```
