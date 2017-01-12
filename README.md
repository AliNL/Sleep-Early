# Sleep-Early
[中文版ReadMe](#中文版)

This is a real machine automation project to help you sleep early.


## Environment Setup
1. brew install pillow
   1. brew install homebrew/science/opencv
   1. pip install --pre --upgrade atx

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

# 中文版

## Common
1. brew install pillow
1. brew install homebrew/science/opencv
1. pip install --pre --upgrade atx

## IOS
1. 首先你要有个Mac
1. 然后要有苹果开发者账号，详情请看：https://developer.apple.com/
1. 安装最新Xcode，查看版本详情，保证这个版本可以cover你手机的IOS版本. 如果想用命令行跑的话，再安装对应版本的Command Line Tools：https://developer.apple.com/download/more/
1. git clone https://github.com/facebook/WebDriverAgent.git
1. 用Xcode打开刚才下载的项目，用你的开发者账号对项目重签名，步骤请参考[这篇文章](https://testerhome.com/topics/6172)中的配置WebDriverAgent部分。
1. 先在模拟器跑起来：Scheme设置为WebDriverAgentRunner，Simulator设置为iPhone 6，Product->Test。能看到SeverURL就表示成功了。
1. 然后连接真机，Device设置为真机，Product->Test
  * 或者用命令行：xcodebuild -project [项目完整地址]/WebDriverAgent/WebDriverAgent.xcodeproj -scheme WebDriverAgentRunner -destination "id=$(idevice_id -l)" test
1. 国行版iPhone需要安装iproxy：
  * brew install usbmuxd
  * brew install ios-webkit-debug-proxy
  * 运行iproxy：iproxy 8100 8100 $(idevice_id -l)
1. 在浏览器中打开：http://localhost:8100/inspector ，确保可以看到真机屏幕
1. 进入Sleep-Early目录，首先：python start_ios.py ，然后App不关，可以跑其他脚本。

## Android
1. 安装网易mumu模拟器
1. 直接运行：
  - python explore.py
  - python break.py
  - python group.py

## Tips
1. IOS问题可以在下班时间找我。Android真机问题请自行解决，我没有Android设备。
1. 有bug可以告诉我，心情好的时候会修。
