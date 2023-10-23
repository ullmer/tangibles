package require mbv::ivBase 1.0

package require pdf::visuals:ivMgr 2.0
package require mbv::imagePane 1.0
package require mbv::ivButton 1.0

package provide mbv::stackVis 1.0

#getFieldVal:
#given an object name and the field name,
#extracts out the field contents.
#assumes only one field in the object!
proc getFieldVal {ivname fieldname} {
    set fulltransp [getNObj $ivname]

#    puts "getting field val $fieldname from $fulltransp"

    #filter out the fieldname part of it
    regsub  "^.+$fieldname" $fulltransp "" trans
    regsub  "\}" $trans "" trans

#    puts "done: $trans"

    return $trans;
}

#manualFireEngine does nothing; you have to fire it when you like
itcl_class manualFireEngine {
  inherit interpEngine

  constructor {config} {}

  method fire {} {set eventComplete 1;}
  method update {} {}
}

###################################################################
######################### Stack Vis ###############################
###################################################################

itcl_class stackVis {
    inherit ivBase

    constructor {config} {}
    destructor {foreach image $image_list {$image delete}}

    method addImage {fname} {} ;#returns pane #
    method popImage {} {}

    method assertIv {} {}
    method retractIv {} {}

    method getTranspNode {} {return [format {%s:transp} $iv_name]}
    method getLightNode {} {return [format {%s:light} $iv_name]}
    method getNumFrames {} {return [llength $filename_list];} 

#getPaneName takes a frame # and returns the pane variable name
#used by click handler

    method getAllPaneNames {} {return $image_list}

    method getPaneName {framenum} {return [lindex $image_list $framenum]}
    method getCorrectPanePos {framenum} {return [list 0 [expr $y_dir * $y_dim * ([getNumFrames] - 1 - $framenum)] 0] };
    method getPaneNum {relpos} {}; #given a position in our coord space, returns the pane that encompasses it, or -1 if there's no such pane.
    method getCurFrame {} {return $cur_frame;}

    method getLightNodeContents {} {} ;#returns appropriate light node def, given our highlighted/unhighlighted state

    method highlight {} {}
    method unhighlight {} {}

    method flowDown {{duration .25}} {} ;# the frames come flyin' down
    method flowUp {{duration .15}} {} ;# the frames go back up to the start 
    method fade {{duration .5}} {} ;# the frames stay laid out as is; they just fade. returns the fade event
    method unfade {{duration .5}} {} ;# the frames stay laid out as is; they just fade. returns the fade event
    method getTransp {} {return [getFieldVal [getTranspNode] "transparency"]}; #gets current transparency val

#private methods, used by flowDown & flowUp
    method flowDownCB {panenum endevent duration} {}
    method flowUpCB {panenum endevent duration} {}

    method interruptFlow {} {set flow_irq 1;} ;#turn on the interrupt request
    method numLaidOut {} {return $num_laid_out;} ;#num panes laid out currently
    method isFlowing {} {return $is_flowing;} ;#are we busy?

#genFrameName takes an absolute frame # and makes a new var name - used
#when creating all the panes
    method genFrameName {framenum} {return "[getThis]image$framenum"}

#internal click handler; passes stuff on to click_handler
    method handleClick {frameNum} {}

#appends the pane to our list
    method receivePane {panename abspanepos abspanerot} {}

    method displayPane {panenum} {}

  ### local members
    #dimensions of each image; in floating point, please!
    public y_dim {40.0}
    public x_dim {80.0}

    public anim_mgr {}

    public y_dir {-1} ;#-1 to flow in the -y direction, +1 to flow in the +yu direction
    public mag_factor {2.} ;#magnification factor when zoomed; unused.

    public texture_cache {} ;#set this to something to use it
    public click_handler {} ;# what to call when someone clicks on our panes
    public filename_list {} ; #list of image filenames that the stackvis should contain

    public is_highlighted {0}
    public is_flowing {0} ;#1 if flowing down, -1 if flowing up, 0 if doing nothing
    public line_width {2}

    protected flow_irq {0} ;#did user request that the flow be interrupted?


    protected image_list {} ; #list of imagePanes that we created
    protected cur_frame  {-1} ; #which frame is currently selected
    protected num_laid_out  {0} ; # number of frames laid out

    public stack_slot_pos {0}
    public id {}
}

#################### stackVis addImage #########################
#if stackvis is already asserted, you'll have to assert the new pane yourself
#I do this so you can addImage, get the pane, and then animate the image into place
#as you like. rcvPane does this
body stackVis::addImage {fname} {

    set i [llength $filename_list]
    lappend filename_list $fname

#    puts "adding image $i to $filename_list"

    set panename [genFrameName $i]
#    puts "genframename $panename"

    set objPos [getCorrectPanePos $i]

    fallableImagePane $panename -parent_ [getIvName] \
	    -texture_cache $texture_cache -image_fname $fname \
	    -position_ [list 0 0 0] -x_dim $x_dim -y_dim $y_dim \
	    -animduration .5 -anim_mgr $anim_mgr -line_width $line_width
	
    lappend image_list [$panename getThis]


#XXX if we're already asserted, scroll 'em
    if {$iv_asserted != 0} {
	set numFrames [getNumFrames]
	for {set j [expr $numFrames - 2]} {$j >= 0}  {set j [expr $j - 1]} {
	    set name [getPaneName $j]
	    set newpanepos [getCorrectPanePos $j]
	    set curpanepos [getFieldVal [$name getPosNode] translation]
	    $anim_mgr shiftObj [$name getPosNode] "$curpanepos" "$newpanepos" .5
	}
    }
    return $i;
}

#################### stackVis popImage #########################
#removes highest-numbered image
body stackVis::popImage {} {
    set i [llength $filename_list]
    lappend filename_list $fname
    lappend image_list [$panename getThis]

#    puts "removing image $i from $filename_list"

    set panename [getPaneName $i]

#XXX if we're already asserted, scroll 'em
    if {$iv_asserted != 0} {
	#make it push 'em all down
#	set num_laid_out 0
	#maybe do a for loop and shift obj 'em all

	set numFrames [getNumFrames]
	for {set j [expr $numFrames - 2]} {$j >= 0}  {set j [expr $j - 1]} {
	    set name [getPaneName $j]
	    set newpanepos [getCorrectPanePos $j]
	    set curpanepos [getFieldVal [$name getPosNode] translation]
	    $anim_mgr shiftObj [$name getPosNode] "$curpanepos" "$newpanepos" .5
	}
    }
    return $i;
}

#################### stackVis assertIv #########################
body stackVis::assertIv {} {
    if {$iv_asserted != 0} {return;}

    #add separator that all the panes will go under in the inventor scene graph
    #(put in our transparency deal)
    set lightnode [getLightNodeContents]
    set ournode "DEF [getTranspNode] Material {transparency 0.} \
	    DEF [getLightNode]  DirectionalLight {$lightnode}"

    addNObj [getIvName] $ournode

#    puts "[getNObj [getIvName]]"
    #place all the frames that have been laid out
    set numFrames [getNumFrames]
    for {set i [expr $numFrames - 1]} {$i >= [expr $numFrames - $num_laid_out]} {set i [expr $i - 1]} {
	#show the image
	displayPane $i
    }
    #put it in the right place
    rotNObj [getRotNode] $rotation_
    moveNObj [getPosNode] $position_

    set iv_asserted 1; #we've added it to the scene graph

#    puts "$this done asserting frames."
}

#################### stackVis retractIv #########################
body stackVis::retractIv {} {
    if {$iv_asserted == 0} {return;}

#retract the individual panes
    set numFrames [getNumFrames]
    for {set i 0} {$i < $numFrames} {incr i} {
	set name [getPaneName $i]
#	puts "retracting $name, [$name getIvName]"

	#retract the image
	$name retractIv
    }

#now retract us
    delNObj [getIvName]
    set iv_asserted 0;
    set num_laid_out 0;
}

######################### handle click ###############################

#handleClick takes the frame # as an arg
#it demonstrates how to highlight/unhighlight a frame, and
#then calls the ClickCB.
body stackVis::handleClick {i} {

    #unhighlight the previous selection
    if {$cur_frame != -1} {
	[getPaneName $cur_frame] unhighlight;
    }
    
    set pane [getPaneName $i]

    #do a highlight while we're at it.
    $pane highlight;
    set cur_frame $i
    if {$click_handler != ""} {eval $click_handler}
}

######################### flow down ###############################

# the frames come flyin' down
body stackVis::flowDown {{duration .25}} {
 #were we already down?
    if {$iv_asserted == 0} {puts "can't flowdown w/o being asserted!"; return;}

#clear interrupts
    set flow_irq 0;

#    if {$verbose != 0} {puts "starting flowdown";}

 #make an end event that user can grab on to.
    set endevent [$anim_mgr genName]
    manualFireEngine $endevent -autoDelete 1;
    $anim_mgr addEvent $endevent;

 #start it goin
    set is_flowing 1;
    flowDownCB [expr [getNumFrames] - 1 - $num_laid_out] $endevent $duration

    return $endevent
} 

######################### flow up ###############################

# the frames retract back up to the start 
body stackVis::flowUp {{duration .15}} {
    if {$iv_asserted == 0} {puts "can't flowup w/o being asserted!"; return;}

#clear interrupts
    set flow_irq 0;

#    if {$verbose != 0} {puts "starting flowup";}

 #make an end event that user can grab on to.
    set endevent [$anim_mgr genName]
    manualFireEngine $endevent -autoDelete 1;
    $anim_mgr addEvent $endevent;

 #start it up
    set is_flowing -1;
    flowUpCB [expr [getNumFrames] - $num_laid_out] $endevent $duration

    return $endevent
}

#abspanepos = source pane pos + source stackvis pos
#abspanerot = source pane rot + source stackvis rot
body stackVis::receivePane {panename abspanepos abspanerot} {
    if {$iv_asserted == 0} {puts "$this receiving a pane although we're not asserted!?"}

    #get the source pane's position in relative coords
    set negpos [list [expr -[lindex $position_ 0]] [expr -[lindex $position_ 1]] [expr -[lindex $position_ 2]]]
    set relpanepos [add3D $abspanepos $negpos]

    #and its rotation
    set negrot [list [expr -[lindex $rotation_ 0]] [expr -[lindex $rotation_ 1]] [expr -[lindex $rotation_ 2]]]

    set negx [lindex $negrot 0]
    set negy [lindex $negrot 1]
    set negz [lindex $negrot 2]

    #if you want it to flip, add/subtract multiples of 360 as appropriate
#    if {$negx < 0} {set negx [expr $negx - 360]} else {set negx [expr $negx + 360]}
#    if {$negy < 0} {set negy [expr $negy - 360]} else {set negy [expr $negy + 360]}
#    if {$negz < 0} {set negz [expr $negz - 360]} else {set negz [expr $negz + 360]}
    set negrotx "$negx 0 0"
    set negroty "0 $negy 0"
    set negrotz "0 0 $negz"

    #add it to our list
    set newnum [addImage [$panename get image_fname]]

    set newpane [getPaneName $newnum]

    set xsizeratio [expr [$panename get x_dim] / $x_dim]
    set ysizeratio [expr [$panename get y_dim] / $y_dim]

    #start the pane out where the source pane was, at his size
    
    #the scene graph we'll set up at the start looks like so:

    #ourstackvis separator {
    #      translation $position_ 
    #      rotation    $rotation_ 
    #      newpane separator {
    #             rotation    $rotation_  = 0
    #             translation $position_  = 0
    #             rotation    extraRot1    = -ourstackvis's rotation z aka $negrotz
    #             rotation    extraRot2    = -ourstackvis's rotation y, aka $negroty
    #             rotation    extraRot3    = -ourstackvis's rotation x, aka $negrotx
    #             translation extraTrans = -ourstackvis's position ($negpos) + source stack $position_ + source pane $position_, aka $abspanepos
    #             rotation    extraRot4   = source pane rotation, aka $abspanerot
    #             scale       $scale_ = source pane size / our pane size
    #             the pane itself
    #      }
    #}

    #so if you read the transformations from top to bottom, the pane will
    #be placed at the source position, at the source size.
    #the reason we need three rot's to undo our stack's rotation is because
    #rotNobj rotates around x, then y, then z. so to undo, we need to rotate
    #in the order of z, y, x. to do *that*, we need three separate rotnobj's

    $newpane sset position_ [list 0 0 0]
    $newpane sset rotation_ [list 0 0 0]
    $newpane sset scale_ "$xsizeratio $ysizeratio 1"
    displayPane $newnum
    moveNObj [$newpane getExtraTransNode] [add3D $abspanepos $negpos]
    rotNObj [$newpane getExtraRotNode1] $negrotz
    rotNObj [$newpane getExtraRotNode2] $negroty
    rotNObj [$newpane getExtraRotNode3] $negrotx
    rotNObj [$newpane getExtraRotNode4] $abspanerot
    $newpane enableTexture
#    puts "[getNObj [getIvName]]"

    #and we want to transform to:
    #ourstackvis separator {
    #      translation $position_ 
    #      rotation    $rotation_ 
    #      newpane separator {
    #             rotation    $rotation_  = 0 0 0, aka $newrot
    #             translation $position_  = new pane position_, aka $newpos
    #             rotation    extraRot1    = 0
    #             rotation    extraRot2    = 0
    #             rotation    extraRot3    = 0
    #             translation extraTrans = 0 0 0
    #             rotation    extraRot4    = 0
    #             scale       $scale_ = 1 1 1
    #             the pane itself
    #      }
    #}
    set newpos [getCorrectPanePos $newnum]
    set newrot [list 0 0 0] ;#not rotated w/ respect to us!

    set dur [$newpane get animduration]

    #make it fall in a parabola to its new position
    set fallEvent [$newpane fall [list 0. 0. 0.] $newpos]
    $fallEvent appendExitEvent "$newpane sset position_ \{$newpos\};"

    #match rotations - 0 to 0, aka nothing
#    set spinEvent [$anim_mgr spinObj [$newpane getRotNode] $negrotz $newrot $dur]
#    $spinEvent appendExitEvent "$newpane sset rotation_ \{$newrot\};"

    #get the extra translation and rots cleared
    $anim_mgr shiftObj [$newpane getExtraTransNode] [add3D $abspanepos $negpos] "0 0 0" $dur
    $anim_mgr spinObj [$newpane getExtraRotNode1] $negrotz "0 0 0" $dur
    $anim_mgr spinObj [$newpane getExtraRotNode2] $negroty "0 0 0" $dur
    $anim_mgr spinObj [$newpane getExtraRotNode3] $negrotx "0 0 0" $dur
    $anim_mgr spinObj [$newpane getExtraRotNode4] $abspanerot "0 0 0" $dur

    #make it scale from source size to our pane size
    set scaleEvent [$anim_mgr scaleObj [$newpane getScaleNode] "$xsizeratio $ysizeratio 1" "1 1 1" $dur]
    $scaleEvent appendExitEvent "$newpane sset scale_ \{1 1 1\};"
}

######################### flow down CB ###############################

body stackVis::flowDownCB {panenum endevent duration} {
    #finish up the prev guy
    set prev [expr $panenum + 1]
    set startPanePos [getCorrectPanePos $prev]

    #if we're not the first pane to flow down...
    if {$panenum < [expr [getNumFrames] - 1]} {
	#finish up our predecessor
	set prevname [getPaneName $prev]
	if {[$prevname isAsserted]} {
	    $prevname enableTexture;
	}
	#last guy ends up where we start
	$prevname sset position_ $startPanePos
    } else {
#	set startPanePos [list 0 0 0]
    }

    set num_laid_out [expr [getNumFrames] - $panenum - 1]

    #are we done? or did somebody request an interrupt?
    if {$panenum == -1 || $flow_irq} {
#	puts "[getNObj [getIvName]]"
#	puts "[getNObj root]"
	set is_flowing 0
	set flow_irq 0;

	if {[getNumFrames] == 0} {
	    tiAfter .1 "$endevent fire"
	} else {
	    $endevent fire;
	}
	return;
    }

    #alright, make this one happen
    set name [getPaneName $panenum]

    set endPanePos [getCorrectPanePos $panenum]

    #	$name sset scale_ "1 .01 1"
    #	set scaleevent [$anim_mgr scaleObj [$name getScaleNode] "1 .01 1" "1 1 1" $duration]
    #	set fadeevent [$anim_mgr fadeObj [$name getTranspNode] 1 0 $duration]
    
    displayPane $panenum

    if {$duration > 0} {
	set shiftevent [$anim_mgr shiftObj [$name getPosNode] "$startPanePos" "$endPanePos" $duration];
	$shiftevent appendExitEvent "$this flowDownCB  [expr $panenum - 1] $endevent $duration"
    } else {
    	$name sset position_ $endPanePos
    	moveNObj [$name getPosNode] $endPanePos
	flowDownCB  [expr $panenum - 1] $endevent $duration 
    }


}

######################### flow up CB ###############################

body stackVis::flowUpCB {panenum endevent duration} {
    
    #we want them all to flow off-screen - get the -1th pane position
    #since the first pane is $numframes - 1, the one before that is $numframes
    set behindPanePos [getCorrectPanePos [getNumFrames]]

    #finish up the prev guy
    if {$panenum > 0} {
	set prev [expr $panenum - 1]
	set prevname [getPaneName $prev]
	$prevname sset position_ $behindPanePos
        $prevname retractIv
    } else {
	set startPanePos $behindPanePos
    }

    set num_laid_out [expr [getNumFrames] - $panenum]

    #are we done?
    #or did somebody request an interrupt?
    if {$num_laid_out == 0 || $flow_irq} {
	set is_flowing 0
	set flow_irq 0
	if {$panenum == 0} {
	    tiAfter .1 "$endevent fire"
	} else {
	    $endevent fire;
	}
	return;
    }

    #alright, make this one happen
    set name [getPaneName $panenum]

    $name disableTexture;
    set startPanePos [getFieldVal [$name getPosNode] translation]
    set endPanePos $behindPanePos
	
    #move it to endpanepos and make the next pane go.
    if {$duration > 0} {
	set shiftevent [$anim_mgr shiftObj [$name getPosNode] "$startPanePos" "$endPanePos" $duration];
	$shiftevent appendExitEvent "$this flowUpCB [expr $panenum + 1] $endevent $duration"
    } else {
	#do it instantaneously
	moveNObj [$name getPosNode] $endPanePos
    	$name sset position_ $endPanePos
	flowUpCB [expr $panenum + 1] $endevent $duration 
    }
}

body stackVis::fade {{duration .5}} {
#    puts "fading from transp [getTransp]"
    set fadeevent [$anim_mgr fadeObj [getTranspNode] [getTransp] 1 $duration]
    return $fadeevent
}

body stackVis::unfade {{duration .5}} {
    set fadeevent [$anim_mgr fadeObj [getTranspNode] [getTransp] 0 $duration]
    return $fadeevent
}

body stackVis::displayPane {panenum} {
    set panename [getPaneName $panenum]
#	puts "showing $panename, [$panename getIvName]"

    if {[$panename isAsserted]} {
    } else {
	$panename assertIv
	#when we click on a frame, do something!
	bindNObj [$panename getIvName] "$this handleClick $panenum"
    }
}

######################### get Pane Num ###############################

#given a position in our coord space, (should be x, y, 0), returns
#the pane num that encompasses it, or -1 if it's outside us.
body stackVis::getPaneNum {relpos} {
    set numFrames [getNumFrames]
    for {set j [expr $numFrames - 1]} {$j >= 0}  {set j [expr $j - 1]} {
	#get the position relative to the pane by subtracting out
	#the pane's pos from relpos
	
	set pane [getPaneName $j]
	set panepos [$pane get position_];
	set negpos [list [expr -[lindex $panepos 0]] [expr -[lindex $panepos 1]] [expr -[lindex $panepos 2]]]
	
	set reltopanepos [add3D $negpos $relpos]
#	puts "$reltopanepos"
	
	if {[$pane containsPt $reltopanepos]} {
#	    puts "$pane at $panepos has $relpos";
	    return $j;
	}
    }    
    return -1;
}

######################### highlight ###############################

body stackVis::highlight {} {
    if {$is_highlighted} {return;}

    set is_highlighted 1;

    set numFrames [getNumFrames]
    for {set i [expr $numFrames - 1]} {$i >= [expr $numFrames - $num_laid_out]} {set i [expr $i - 1]} {
	set name [getPaneName $i]
	$name specHighlight
    }
}

######################### unhighlight ###############################

body stackVis::unhighlight {} {
    if {!$is_highlighted} {return;}

    set numFrames [getNumFrames]
    for {set i [expr $numFrames - 1]} {$i >= [expr $numFrames - $num_laid_out]} {set i [expr $i - 1]} {
	set name [getPaneName $i]
	$name specUnHighlight
    }
}

###################### get light node contents ############################

#returns appropriate light node def, given our highlighted/unhighlighted state
body stackVis::getLightNodeContents {} {
    set contents "direction 0 0 1 \
            on $is_highlighted \
            color 1 1 1 \
            intensity 1"
    return $contents
} 
