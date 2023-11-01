#new code for original sequencer hardware
#by John Alex, MIT media Lab
#begun 3/31/98

# Tweaks by Brygg
# First made on 6/26/98 to reactivate target pad
# Next  made on 7/6/98  to activate target pad flow from seq rack

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

package require pdf::visuals:perspVis 2.0

package require tmg:mbSequencer::physicals:targetPad 2.0


#for making unique stack names
set stacknum 0
set stacklist {}

textureCacheMgr textureMgr
#set cache ::textureMgr
    set cache ""

set lowerStackNames {a a a a a}

proc handleBird {msg} {
regsub "bird1 " $msg "" parsed
#puts "$parsed"
moveNObj [birdbtn getPosNode] $parsed
}

#this should all go into a proxy destpad class...
proc destEvent {msg} {
    set which [lindex $msg 0]

    global cache;

    if {$which == 0} {
	global wallup
	global wallpos
	if {$wallup} {
	    global destStack
	    set panename [wall getPaneEl [wall get currentFocus]]
	    destStack receivePane $panename $wallpos "0 0 0"
	    puts "should be putting destStack contents into hardcoded MB now!"
	} else {
	    puts "concatting MB's..."
	    #should concat all known mb's?!

	    copySeqRackToTarget
	}
    } elseif {$which == 1} {
#	if {$destup} {destStack retractIv; destStack delete; set destup 0;}
    } else {
	puts "dest pad got unknown msg $msg"
    }
}

proc stacksorter_stub {stack_a stack_b} {
  set a [$stack_a get stack_slot_pos]
  set b [$stack_b get stack_slot_pos]

  if {$a < $b} {return -1}
  if {$a > $b} {return  1}
  return 0
}

proc copySeqRackToTarget {} {

  global stacklist

  set sortedlist [lsort -command stacksorter_stub $stacklist]

  set cumdelay 0
  foreach stack $sortedlist {
    regsub {^::} $stack {} stack

    puts "stack <$stack>"
    set info      [itcl_info objects $stack]
    if {$info == {}} {
      puts "stack <$stack> has gone away; ignoring"; return
    }
  
    set paneNames [$stack getAllPaneNames]
    puts "sending <$paneNames> to stack $stack"

    set smalldelay 400
    #set smalldelay 20

    set stackpos [$stack get position_]
    set stackrot [$stack get rotation_]
    set i 0
	    
    foreach pane $paneNames {
      set framepos [$stack getCorrectPanePos $i]
      set abspos   [add3D $stackpos $framepos]

      after $cumdelay "destStack receivePane $pane \{$abspos\} \{$stackrot\}"
      incr cumdelay $smalldelay
      incr i
    }
  }
}

#this should all go into a proxy posrack class...
set wallpos "10 2.5 0"

set wallup 0 ; #if the wall's currently displayed or not
set numwall 0; #num frames in the wall

set numin 0 ;#number of blocks we think are on the lower rack

#called on a timer after an exit event on the lower rack; if 
#nobody's entered by then, we toast the rack
proc pexit {} {
    global numin
    global wallup
    if {$numin == 0} {
	if {$wallup} {wall retractIv; wall delete; set wallup 0;}
    }
}

#called for switch
proc pswitch {id} {
}

#handler of lower rack: expects 0-3: begin, left, right, end, or 4:exit
proc pwall {which id} {
    puts "pwall $which $id"

    global wallpos;
    global wallup;
    global numwall;
    global cache;
    global numin;

    if {$which == 4} {
	set numin [expr $numin - 1]
	puts "lost one: $numin"
	if {$numin < 0} {set numin 0}
	if {$numin == 0} {tiAfter .5 "pexit"}
	return;
    }

    set numin [expr $numin + 1]

    if {!$wallup} {
	perspWall wall -basePos $wallpos -baseRot "0 0 0" -textureCache $cache -animManager [animgr getThis] -paneXdim 6.0 -paneYdim 3.38 -xlen 6.1
	set wallup 1
	
	wall assertIv
	
	set texlist [mbclient getMbLocalFiles $id]
	
	foreach tex $texlist {
	    wall newappendPane $tex
	}

	set numwall [llength $texlist]
	wall focusPane 0
    }

    puts "in: $numin"
    if {$which == 0} { #begin
	wall focusPane 0
    } elseif {$which == 3} { #end
	if {$numwall > 0} {
	    wall focusPane [expr $numwall - 1]
	}
    } elseif {$which == 2} { #right
	set next [expr round([expr $numwall + 1].0 * 2.0 / 3.0)] 
	if {$next > 0} {set next [expr $next - 1]}
#	puts "next is $next"
	if {$next < $numwall} {wall focusPane $next}
    } elseif {$which == 1} { #left
	set prev [expr round([expr $numwall + 1].0 * 1.0 / 3.0)]
	if {$prev > 0} {set prev [expr $prev - 1]}
#	puts "prev is $prev"
	if {$prev >= 0} {wall focusPane $prev}
    }

}

proc handleMBEvent {msg} {
    set which [lindex $msg 0]

#    puts "$msg"

    set lower {2 3 4 0} 
    set upper {A B 8 1}
    global lowerStackNames

    set port [lindex $msg 2]
    set pos [lsearch $upper $port]
    if {$pos != -1} { #is it a port from the upper rack?
#	puts "upper"
	if {$which == "exit"} {
	    set name [lindex $lowerStackNames $pos]
	    if {$name != "a"} {
		puts "exiting pos $pos, retracting $name"
		$name interruptFlow;
		set exitName [$name fade .4]
#		set exitName [$name flowUp]
		$exitName appendExitEvent "$name retractIv; $name delete;"
#		$name retractIv; $name delete;

        # delete the fellow from the global stack list
        global stacklist
        set idx [lsearch $stacklist $name]
        if {$idx != -1} { set stacklist [lreplace $stacklist $idx $idx] }

		puts "done"
	    }
	} elseif {$which == "entrance"} {
	    set id [lindex $msg 4]
	    puts "$id entered pos $pos of upper"

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
    } else { #from the lower rack?
	set pos [lsearch $lower $port]
	if {$pos != -1} {
#	    puts "lower"
	    if {$which == "exit"} {
		puts "exited $pos of lower"
		pwall 4 $pos
	    } elseif {$which == "entrance"} {
		set id [lindex $msg 4]
		puts "$id entered pos $pos of lower"
		pwall $pos $id
	    } else {
		puts "msg $which unknown!"
	    }
	} else {
	    puts "port $port unknown!"
	}
    }
}

proc makeStack {pos id} {
    global stacknum stacklist
    set stackname "::stack$stacknum"
    incr stacknum

    global cache

    stackVis $stackname -click_handler "global clickHandler; clickHandler $stackname" \
	    -texture_cache $cache -x_dim 4.0 -y_dim 3.0 -y_dir -1 \
	    -anim_mgr [animgr getThis] -line_width 2 \
	    -stack_slot_pos $pos
    placeStack $stackname $pos

    puts "querying mb server for mb contents..."
    set texlist [mbclient getMbLocalFiles $id]
    puts "done."

    foreach tex $texlist {
#	puts "adding image $tex"
	$stackname addImage $tex
    }

    $stackname assertIv
    lappend stacklist $stackname

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
    set portpos {19 15 11 7}

#for bottom rack
#    set portpos {15.5 11.25 6.75 2.5}

#    set stacky 14
#    set position "[lindex $portpos $port] $stacky -10."
    set stacky 18.5
    set position "[lindex $portpos $port] $stacky 0."
    $stackname sset position_ $position
}

### Base setup code ###

pdfMimeMapper mimeMapper
textureCacheMgr textureCache

#talk to the mediablocks
mbdMbClient mbclient \
  -mimeMapper [mimeMapper getThis] -textureCacheMgr [textureCache getThis]

#ivButton birdbtn -position_ {0 0 0} -x_dim 3.0 -y_dim 2.0 -click_handler "btnClick destStack" -text_ "b"
#birdbtn assertIv

#pdfClientBase bclient -host chinook -port 7075 -manualCB handleBird
#bclient connect; bclient startAutohandler

#talk to the sequencer; will be replaced eventually
pdfClientBase client -host grasp -port 7700 -manualCB handleMBEvent
client connect; client startAutohandler

#talk to the target pad

mbpTargetPad tpad -pressCB "destEvent 0" -releaseCB "destEvent 1" \
  -host grasp -port 8000

#mbvTextLabel textAnnouncer
#proc blip {string {length 4}} {textAnnouncer showText $string $length}

#set up coords to correspond to small seq's dimensions in cm: 25x20
tiAfter 2. {moveTo {12.5 10.0 22.8811}; rotTo {0 0 180.}}

#tiAfter 2. {textAnnouncer showText "Ready"}

wm withdraw . ;# minimize root window

## Set up interpolator engines

puts blip

ivMgr animgr 

tiIdle {animgr update}

global cache;

#button to simulate persp wall events
#ivButton wall3 -position_ {16 2 0} -x_dim 4 -y_dim 3 -click_handler "pswitch UNKNOWN?" -text_ "p to d"
#wall3 assertIv

#put a button on top of each stackvis to simulate mediablock events
#ivButton flow0btn -position_ {3 2 0} -x_dim 4 -y_dim 3 -click_handler "btnClick stack0" -text_ "stack0"
#flow0btn assertIv

#simulate an MB event
#handleMBEvent "entrance port 01 id 0000026925C101"
#handleMBEvent "entrance port 02 id 0000026925C101"
#handleMBEvent "entrance port 03 id 0000026925C101"
#handleMBEvent "entrance port 04 id 0000026925C101"

stackVis destStack -texture_cache $cache -x_dim 4 -y_dim 3 -y_dir 1 -anim_mgr [animgr getThis] -position_ {21.5 2.2 0} -rotation_ {-30 -50 0}

destStack assertIv; #it's gotta exist to be able to receive panes
destStack flowDown;

puts blip

#ivButton flow1btn -position_ {8 2 0} -x_dim 4 -y_dim 3 -click_handler "btnClick stack1" -text_ "stack1"
#flow1btn assertIv

#ivButton destbtn -position_ {22 2 0} -x_dim 4 -y_dim 3 -click_handler "btnClick destStack" -text_ "dest"
#destbtn assertIv

#put the camera in a decent place


#the handler for click events in the stack vis's.
proc clickHandler {stackname} {
    #make a copy and throw the copy down.
#    puts "handling click for $stackname"

#what pane was clicked?
    set i [$stackname getCurFrame]

    set pane [$stackname getPaneName $i]

#get the pane's position in absolute coords: pane pos + stack pos
    set paneRelPos [$pane get position_]
    set pos [$stackname get position_]
    set paneAbsPos [add3D $paneRelPos $pos]

#i'm assuming the panes aren't rotated with respect to their stackvis;
#i think if they were, receivePane wouldn't be ready for it.
#so the absolute rotation of the pane is just the stack's rotation
    set paneAbsRot [$stackname get rotation_]

#    puts "[getNObj [$stackname getIvName]]"
    destStack receivePane $pane $paneAbsPos $paneAbsRot
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
#	$stackname highlight
    } elseif {[$stackname numLaidOut] > 0} {
	puts "flowing up"
	set exitEvent [$stackname fade]
	
	#when we finish fading, flow up (rapidly)
	set exitaction "$stackname flowUp 0"
	$exitEvent appendExitEvent $exitaction
    } else {
	puts "flowing down"
#.1 for one after the other
#.5 for group scale & show up
	[$stackname unfade 0.001] appendExitEvent "$stackname flowDown .1";
    }
}


#puts "Scene graph under stack:"
#puts [getNObj stack]

#puts [getNObj root]


