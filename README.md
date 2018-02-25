PictoRoom
=========

A revival of the PictoChat DS program.

## Usage

Users may easily set up their own servers by executing the `srv.py` program.

Users may also use the `client.py` program to connect to a server of their
choosing. These servers will be instances of the `srv.py` mentioned above.

Once you run client.py, you'll be prompted for the ip address and port number
of the server you'd like to use. The client will be automatically
connected to the first server you connected to on, and to connect to a different
server, you should delete the config.json file.

The primary communication method is through drawing black and white pictures.
Users may draw pictures on the drawing panel, then click "send" to broadcast it
to the entire network. These pictures are shown in a real time feed above the
drawing space.

## PictoChat Protocol

To facilitate the communication between users, we came up with the PictoChat
protocol.

Data is allowed to be split into different packets. This means that a large
image can be efficiently transfered from client to client. In order to
accomodate this, we added a footer that would denote the end of a stream.

Thus, a message should be structured in the following way:

    message:          | unknown | base64 encoded png
    magic terminator: | 4 bytes | 0xdeadbeef

We have a dedicated AWS server for you to try!
IP Address: `18.219.82.126` and Port: `8000`.
