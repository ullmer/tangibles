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

package require pdf::visuals:ivMgr 2.0

package require mbv::stackVis 1.0
package require mbv::imagePane 1.0
package require mbv::ivButton 1.0

#for making unique stack names
set stacknum 0

set cache ::textureCache
#    set cache ""

set lowerStackNames {a a a a a}

proc handleBird {msg} {
regsub "bird1 " $msg "" parsed
#puts "$parsed"
moveNObj [birdbtn getPosNode] $parsed
}

proc handleMBEvent {msg} {
    set which [lindex $msg 0]
    global lowerStackNames
    if {$which == "exit"} {
	set port [lindex $msg 2]
	set pos [expr $port - 1]
	set name [lindex $lowerStackNames $pos]
	if {$name != "a"} {
	    puts "exiting pos $pos, retracting $name"
	    $name interruptFlow;
#	    set exitName [$name flowUp]
#	    $exitName appendExitEvent "$name retractIv; $name delete;"
	    $name retractIv; $name delete;
	    puts "done"
	}
    } elseif {$which == "entrance"} {
	set id [lindex $msg 4]
	set port [lindex $msg 2]
	set pos [expr $port - 1]
	puts "$id entered pos $pos"

	#make a stackvis
	set name [makeStack $pos $id]
	rotNObj [$name getRotNode] {0 70 0}
	$name sset rotation_ {0 70 0}
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

    global cache

    stackVis $stackname -click_handler "global clickHandler; clickHandler $stackname 0" \
	    -texture_cache $cache -x_dim 3.0 -y_dim 2.25 -y_dir -1 \
	    -animMgr [animgr getThis]
    placeStack $stackname $pos

    puts "querying mb server for mb contents..."
    set texlist [mbclient getMbLocalFiles $id]
    puts "done."

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
#top rack places
    set portpos {17 14 11 8}

#for bottom rack
#    set portpos {15.5 11.25 6.75 2.5}
    set stacky 14

    set position "[lindex $portpos $port] $stacky -10."
    $stackname sset position_ $position
}

### Base setup code ###

pdfMimeMapper mimeMapper
textureCacheMgr textureCache

#talk to the mediablocks
mbdMbClient mbclient \
  -mimeMapper [mimeMapper getThis] -textureCacheMgr [textureCache getThis]


ivButton birdbtn -position_ {0 0 0} -x_dim 3.0 -y_dim 2.0 -click_handler "btnClick destStack" -text_ "b"
birdbtn assertIv

#pdfClientBase bclient -host chinook -port 7075 -manualCB handleBird
#bclient connect; bclient startAutohandler

#talk to the sequencer; will be replaced eventually
pdfClientBase client -host the-brain -port 7700 -manualCB handleMBEvent
client connect; client startAutohandler

#mbvTextLabel textAnnouncer
#proc blip {string {length 4}} {textAnnouncer showText $string $length}

tiAfter 2. {moveTo {35.2 26.4 84.4332}; rotTo {0 0 -90.}}
#tiAfter 2. {textAnnouncer showText "Ready"}

wm withdraw . ;# minimize root window

## Set up interpolator engines

ivMgr animgr 

tiIdle {animgr update}

global cache;
stackVis destStack -texture_cache $cache -x_dim 5 -y_dim 3.5 -y_dir 1 -animMgr [animgr getThis]

#old unrotated pos
#destStack sset position_ {22 5.5 0}
destStack sset position_ {17 12.5 -10}
destStack sset rotation_ {-30 -50 0}

destStack assertIv; #it's gotta exist to be able to receive panes
destStack flowDown;


#put a button on top of each stackvis to simulate mediablock events
ivButton flow0btn -position_ {3 2 0} -x_dim 4 -y_dim 3 -click_handler "btnClick stack0" -text_ "stack0"
flow0btn assertIv

#simulate an MB event
handleMBEvent "entrance port 01 id 0000026925C101"
#handleMBEvent "entrance port 02 id 0000026925C101"
#handleMBEvent "entrance port 03 id 0000026925C101"
#handleMBEvent "entrance port 04 id 0000026925C101"



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
#    puts "sending stack is at pos $pos, pane is at $paneRelPos"
    set paneAbsPos [add3D $paneRelPos $pos]

#i'm assuming the panes aren't rotated with respect to their stackvis; only the stackvis
#is rotated, foo'.
    set paneRot [$stackname get rotation_]

#    puts "[getNObj [$stackname getIvName]]"
    destStack receivePane $pane $paneAbsPos $paneRot
}

proc btnClick {stackname} {
#    puts "clicked $which"

    global $stackname;

    #it'll do nothing if it's already asserted
    $stackname assertIv

#    puts "asserted"
    if {[$stackname isFlowing]} {
	puts "interrupting!"
	$stackname interruptFlow
    } elseif {[$stackname numLaidOut] > 0} {
	puts "flowing up"
	set exitEvent [$stackname fade]
	
	#when we finish fading, flow up (rapidly)
	set exitaction "$stackname flowUp 0.001"
	$exitEvent appendExitEvent $exitaction
    } else {
	puts "flowing down"
#.1 for one after the other
#.5 for group scale & show up
	[$stackname unfade 0.001] appendExitEvent "$stackname flowDown 0 .1";
    }
}


#puts "Scene graph under stack:"
#puts [getNObj stack]

#puts [getNObj root]


