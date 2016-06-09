This is a small command line program for interacting with the 
[Micro Drone 3.0][md] camera.  The camera seems to be a [Reecam][],
for which [api documentation][api] is available online.

[reecam]: http://wiki.reecam.cn/

## Synopsis

    Usage: mdcam [OPTIONS] COMMAND [ARGS]...

    Options:
      -i, --ip, --ipaddr TEXT
      -p, --port INTEGER
      -v, --verbose
      -d, --debug
      -u, --user TEXT
      -p, --password TEXT
      --help                   Show this message and exit.

    Commands:
      backup
      download
      get_params
      get_properties
      get_status
      log
      ls
      restore
      rm
      set_params
      snapshot
      startrec
      stoprec
      streamurl

## Usage

Before you can use `mdcam` you will need to get connected to your
camera.  Typically, you do this by joining the wifi network
`MD3.0_795B` (or similar), at which point the camera will be at
address `192.168.1.1`.  You can use the `set_params` command to change
the ip address used by the camera.

### Taking a snapshot

Take a snapshot by running:

    mdcam snapshot

You can provide an explicit filename like this:

    mdcam snapshot -o mysnap.jpg

### Streaming video

You will need a tool such as [VLC][] to watch the streaming video.
Assuming that you have VLC available, the following will connect VLC
to the camera:

    vlc $(mdcam streamurl)

[vlc]: http://www.videolan.org/vlc/index.html

### Recording a video

To start recording a video:

    mdcam start_record

To stop recording the video:

    mdcam stop_record <taskid>

Where `<taskid>` is the task id value displayed when you ran the
`start_record` command.

### Downloading a video

Use the `ls` command to see the available videos (et al):

    mdcam ls

Use the `download` command to download a video:

    mdcam download /mnt/sd/VIDEO/MOVI0007.mov

The above would download the video to a file named `MOVI0007.mov` in
the current directory.

## License

mdcam -- micro drone 3.0 camera utility  
Copyright (C) 2016 Lars Kellogg-Stedman <lars@oddbit.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

[md]: http://microdrone.co.uk/
[api]: http://wiki.reecam.cn/CGI/Overview

