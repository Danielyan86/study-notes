# udpate ubuntu source
- use tsinghua https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/
# Configure copy&paste from host to virtual box
- 常规高级里共享粘贴板已经选中双向
- Device - insert geust CD image 

# install some tools
- sudo apt install curl vim git tmux -y

# set network config proxy
- https://shadowsocks.org/en/download/clients.html
- https://shadowsockshelp.github.io/Shadowsocks/linux.html

## set network proxy in terminal
- eg: export HTTP_PROXY=http://127.0.0.1:1801
- e.g: export HTTPS_PROXY=http://127.0.0.1:1801
 
# install software 
## install chrome
- wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
- sudo dpkg -i google-chrome-stable_current_amd64.deb

# install om-my-sh

## install zsh
- https://github.com/ohmyzsh/ohmyzsh/wiki/Installing-ZSH
- https://ohmyz.sh/
## install fonts
- https://github.com/powerline/fonts
## install theme bullet-train
- https://github.com/caiogondim/bullet-train.zsh

## config&install zsh plugin
### config the plugin in zsh file directly
- git 
### need to install first
- zsh-autosuggestions https://github.com/zsh-users/zsh-autosuggestions
    - git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
- zsh-completions 
    - git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
- zsh-syntax-highlighting
- autojump https://github.com/wting/autojump
## change defalut folder
- add cd ~ in .zshrc file

# install pycharm
- https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=linux&code=PCC
# install code
- sudo snap install --classic code  
# install anaconda
- https://www.anaconda.com/products/individual#linux

# install docker
check docker official site
- sudo apt-get remove docker docker-engine docker.io containerd runc
https://fcitx-im.org/wiki/Install_and_Configure

## update docker permisson 
Create a docker group (it doesn't matter if this already exists).

- sudo groupadd docker
Add your use to the docker group.

- sudo usermod -aG docker $USER
In order for that change to take effect you need to log out and back on again.

If you have completed these steps and find that you are still having problems with the permissions error then you'll need to allow more access to the docker.sock file. This can be done using the following command.

- sudo chmod 666 /var/run/docker.sock

# install pin yin
- Install the language 
sudo apt install language-pack-gnome-zh-hans
- install the input method fcixt
- config the language
- config the fcixt
## unintall the ibus
## install the fcitx
## config fcitx
- open ~/.pam_environment with your text editor and set the following environment variables to start fcitx
```
XMODIFIERS DEFAULT=@im=fcitx
GTK_IM_MODULE DEFAULT=fcitx
QT_IM_MODULE DEFAULT=fcitx
```
