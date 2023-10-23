#new code for original sequencer hardware
#by John Alex, MIT media Lab
#begun 3/31/98

## Quick pass at generating slide sequence

package require pdf::digitals:mediaSeq 2.0
package require pdf::client;# Load net server library
package require pdf::mimeMapper 1.0

#these want mediaSeq 1.0
#package require tmg:mbSequencer::proxies:sequencer 2.0
#package require tmg:mbSequencer::visuals:textLabel 1.0

package require pdf::digitals:mediaBlock 2.0
package require pdf::digitals:mediaBlockClient 2.0
package require pdf::digitals:textureCache 2.0

#package require pdf::visuals:IvEngines 1.0
package require pdf::visuals:IvEngines 2.0
package require pdf::visuals:ivMgr 2.0

package require mbv::stackVis 1.0
#package require mbv::clipRegistry 1.0
package require mbv::imagePane 1.0
package require mbv::ivButton 1.0

puts "uh"

set stacknum 0

set lowerStackNames {a a a a}

proc handleMBEvent {msg} {
    set which [lindex $msg 0]
    global lowerStackNames
    if {$which == "exit"} {
	set port [lindex $msg 2]
	set pos [expr $port - 1]
	set name [lindex $lowerStackNames $pos]
	if {$name != "a"} {
	    puts "exiting pos $pos, retracting $name"
	    set exitName [$name flowUp]
	    $exitName appendExitEvent "$name retractIv; $name delete;"
	}
    } elseif {$which == "entrance"} {
	set id [lindex $msg 4]
	set port [lindex $msg 2]
	set pos [expr $port - 1]
	puts "$id entered pos $pos"

	#make a stackvis
	set name [makeStack $pos $id]
	$name flowDown
	set lowerStackNames [lreplace $lowerStackNames $pos $pos $name]
#	puts "lowerstacknames is now $lowerStackNames"
    } else {
	puts "unknown msg: $msg"
    }
}

proc makeStack {pos id} {
    global stacknum
    set stackname "::stack$stacknum"
    incr stacknum

    global lowerRackStackNames

#-texture_cache ::textureCache
    stackVis $stackname -click_handler "global clickHandler; clickHandler $stackname 0" \
	    -texture_cache ::textureCache -x_dim 4 -y_dim 3 -y_dir 1
    placeStack $stackname $pos

    set texlist [mbclient getMbLocalFiles $id]

    foreach tex $texlist {
#	puts "adding image $tex"
	$stackname addImage $tex
    }

    $stackname assertIv

    return $stackname
}

proc swap {port1 port2} {
    set stack1 [lindex $lowerRackStackNames $port1]
    set stack2 [lindex $lowerRackStackNames $port2]

    #need to swap $stack1 and $stack2 in $lowerRackStackNames XXX

    #swap their actual positions
    placeStack $stack1 $port2
    placeStack $stack2 $port1
}

proc placeStack {stackname port} {
    set portpos {15.5 11.25 6.75 2.5}
    set stacky 2

    set position "[lindex $portpos $port] $stacky 0."
    $stackname sset position_ $position
}

### Base setup code ###

pdfMimeMapper mimeMapper
textureCacheMgr textureCache

#talk to the mediablocks
mbdMbClient mbclient \
  -mimeMapper [mimeMapper getThis] -textureCacheMgr [textureCache getThis]

#talk to the sequencer; will be replaced eventually
pdfClientBase client -host the-brain -port 7700 -manualCB handleMBEvent
client connect; client startAutohandler

#mbvTextLabel textAnnouncer
#proc blip {string {length 4}} {textAnnouncer showText $string $length}

tiAfter 2. {moveTo {12.5 10.0 22.8811}; rotTo {0 0 180.}}
#tiAfter 2. {textAnnouncer showText "Ready"}

wm withdraw . ;# minimize root window

## Set up interpolator engines

ivMgr animgr 

tiIdle {animgr update}
stackVis destStack -x_dim 4 -y_dim 3 -y_dir 1
destStack sset position_ {22 5.5 0}

destStack assertIv; #it's gotta exist to be able to receive panes
destStack flowDown;

#put a button on top of each stackvis to simulate mediablock events
#ivButton flow0btn -position_ {3 2 0} -x_dim 4 -y_dim 3 -click_handler "btnClick stack0" -text_ "stack0"
#flow0btn assertIv
#simulate an MB event
#handleMBEvent "entrance port 01 id 0000026925CB01"

#ivButton flow1btn -position_ {8 2 0} -x_dim 4 -y_dim 3 -click_handler "btnClick stack1" -text_ "stack1"
#flow1btn assertIv

ivButton destbtn -position_ {22 2 0} -x_dim 4 -y_dim 3 -click_handler "btnClick destStack" -text_ "dest"
destbtn assertIv

#put the camera in a decent place


#the handler for click events in the stack vis's.
proc clickHandler {stackname stacknum} {
    #make a copy and throw the copy down.
#    puts "handling click for $stackname $stacknum"
    set i [$stackname getCurFrame]
    set pane [$stackname getPaneName $i]

    set paneRelPos [$pane get position_]
    #account for the relative position of $stackname
    set pos [$stackname get position_]
    set paneAbsPos [add3D $paneRelPos $pos]

    destStack receivePane $pane $paneAbsPos
}

proc btnClick {stackname} {
#    puts "clicked $which"

    global $stackname;

    #it'll do nothing if it's already asserted
    $stackname assertIv

#    puts "asserted"
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


