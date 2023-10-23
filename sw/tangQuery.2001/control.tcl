## Send control signals to remote program
## Brygg Ullmer
## Begun April 11, 2002


set server {tsunami}
#set server {1cc-dhcp-107}

set port   5000

set s [socket $server $port]

button .start -text start -command {puts $s start; flush $s}
button .stop  -text stop  -command {puts $s stop; flush $s}
button .exit  -text exit  -command {catch {puts $s exit; flush $s}; exit}

pack .start .stop .exit -side top -expand 1 -fill both
wm geometry . +10+10
#wm geometry . +900+10



