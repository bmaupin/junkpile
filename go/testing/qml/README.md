# go-experiment
An experiment using Go

Building (Ubuntu 14.04)
---
1. Install go

        sudo apt-get -y install golang
        
2. Set up GOPATH

        mkdir $HOME/go
        export GOPATH=$HOME/go
        echo "export GOPATH=$HOME/go" >> ~/.bashrc

3. Install dependencies for go-qml

        sudo apt-get -y install libqt5opengl5-dev libqt5qml-quickcontrols qtbase5-private-dev qtdeclarative5-dev qtdeclarative5-private-dev qtdeclarative5-qtquick2-plugin

4. Download this project and dependencies

        go get -u github.com/bmaupin/go-experiment

5. Build it

        cd $GOPATH/src/github.com/bmaupin/go-experiment/
        go build
        
6. Run it

        ./go-experiment
