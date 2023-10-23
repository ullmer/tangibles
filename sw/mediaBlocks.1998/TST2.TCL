## Quick pass at perspective wall example
## By Brygg Ullmer, MIT Media Lab
## Begun 08/12/1997

## Quick pass at generating slide sequence

package require pdf::client;# Load net server library
package require pdf::mimeMapper 1.0

package require tmg:mbSequencer::proxies:sequencer 1.0
package require tmg:mbSequencer::visuals:textLabel 1.0

package require pdf::digitals:mediaBlock 1.0

package require pdf::visuals:IvEngines 1.0
package require pdf::visuals:ivMgr 2.0

package require mbv::stackVis 1.0
package require mbv::clipRegistry 1.0
package require mbv::imagePane 1.0
package require mbv::ivButton 1.0

### Base setup code ###

pdfMimeMapper mimeMapper

mbvTextLabel textAnnouncer
proc blip {string {length 4}} {textAnnouncer showText $string $length}

tiAfter 2. {moveTo {35.2 26.4 84.4332}; rotTo {0 0 -90.}}
tiAfter 2. {textAnnouncer showText "Ready"}

wm withdraw . ;# minimize root window

## Set up interpolator engines

ivMgr animgr 

tiIdle {animgr update}

puts urg1
## Load our classes
puts urg2

#the latest location for something to fall to; this is hacky
set g_fallto [list 15.0 35.0 0.0]

stackVis stack0 -click_handler "global clickHandler; clickHandler stack0 0" \
  -x_dim 4 -y_dim 2

for {set i 0} {$i <= 10} {incr i} {
    stack0 addImage "/extra/data/movemoov.data/brazil$i.rgb"
}

stackVis stack1 -click_handler "clickHandler stack1 1" \
  -x_dim 4 -y_dim 2

for {set i 11} {$i <= 20} {incr i} {
    stack1 addImage "/extra/data/movemoov.data/brazil$i.rgb"
}

stack0 sset position_ {5  65 0}
stack1 sset position_ {10 65 0}

#put a button on top of each stackvis to simulate mediablock events
ivButton flow1btn -position_ {5 65 0} -x_dim 4 -y_dim 3 -click_handler "btnClick stack0" -text_ "stack0"
flow1btn assertIv

ivButton flow2btn -position_ {10 65 0} -x_dim 4 -y_dim 3 -click_handler "btnClick stack1" -text_ "stack1"
flow2btn assertIv

#put the camera in a decent place


#the handler for click events in the stack vis's.
proc clickHandler {stackname stacknum} {
    #make a copy and throw the copy down.
#    puts "handling click for $stackname $stacknum"
    set i [$stackname getCurFrame]
    set pane [$stackname getPaneName $i]

    set fallStartPos [$pane get position_]
    global g_fallto
    set fallEndPos $g_fallto

    #account for the relative position of $stackname
    set pos [$stackname get position_]
    set npos [list [expr -[lindex $pos 0]] [expr -[lindex $pos 1]] [expr -[lindex $pos 2]]]
    set fallEndPos [add3D $fallEndPos $npos]
#    puts "falling from $fallStartPos to $fallEndPos"

    #make a copy to fall
    set copy [$pane makeCopy]
    $copy assertIv
    $copy enableTexture
    $copy fall $fallStartPos $fallEndPos

    #...make the next falling thing fall to the right of this one, for now.
    set offset [list 0.0 -[$pane get y_dim].0 0.0]; 
    set g_fallto [add3D $g_fallto $offset]
}

proc btnClick {stackname} {
#    puts "clicked $which"

    global $stackname;

    #it'll do nothing if it's already asserted
    $stackname assertIv

    puts "asserted"
    if {[$stackname isLaidOut]} {
	puts "flowing up"
	$stackname flowUp;
    } else {
	puts "flowing down"
	$stackname flowDown;
    }
}


#puts "Scene graph under stack:"
#puts [getNObj stack]

#puts [getNObj root]



