# Sleep-Early

This is a real machine automation project to help you sleep early.


## Environment Setup
1. brew install pillow
2. brew tap homebrew/homebrew-science
3. brew install opencv

## For IOS
1. This can only run on **Mac**
1. Get Developer Apple ID
1. Get latest Xcode and commond line tools
1. git clone https://github.com/facebook/WebDriverAgent.git
1. Open WebDriverAgent in Xcode and change the sign configuration
1. Connect your devices by USB
1. You should have Homebrew
1. Type in terminal: brew install usbmuxd
1. Type in terminal: brew install ios-webkit-debug-proxy
1. run WebDriverAgent test in Xcode
1. Type in terminal: iproxy 8100 8100 $(idevice_id -l)
1. Set up atx.connect('http://localhost:8100')
1. Run automation script

## For Android
1. Install this [APK](https://o8oookdsx.qnssl.com/atx-assistant-1.0.4.apk) to your phone
1. Connect your devices by USB
1. Set up atx.connect()
1. Run automation script
