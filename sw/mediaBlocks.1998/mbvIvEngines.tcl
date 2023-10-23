# Minimally-reasonable interpolation/animation engine
# By Brygg Ullmer, MIT Media Lab
# Begun 09/06/1997

if {[info exists IVENG]} {return} 
set IVENG 1 ;# simple conditional source flag

package require pdf::visuals:InterpEngine 1.0
package require pdf::visuals:CycleEngine 1.0

package provide pdf::visuals:IvEngines 2.0

#################### shiftcam engine #########################

itcl_class shiftCamEngine {
  inherit interpEngine

  constructor {config} {
    #set exitEvent "tweakNObj $transName \"position $endVal\""
    set exitEvent "moveTo \{$endVal\}"
  }

  #method update {} {updateVal; tweakNObj $transName "position $currentVal"}
  method update {} {updateVal; moveTo $currentVal}
}

#################### shift texture engine #########################

itcl_class shiftTextureEngine {
  inherit interpEngine

  constructor {config} {
    set exitEvent "tweakNObj $transName \"translation $endVal\""
  }

  method update {} {
    updateVal; 
    set command "tweakNObj $transName \"translation $currentVal\""
    if {$verbose} {puts $command}
    eval $command

    #puts "tweakNObj $transName \"translation $currentVal\""
    #updateVal; tweakNObj $transName \"translation $currentVal\""
  }

  public transName {}
}

#################### cshift texture engine #########################

itcl_class cshiftTextureEngine {
  inherit cycleEngine

  constructor {config} {}

  method update {} {
    updateVal; 
    set command "tweakNObj $transName \"translation $currentVal\""
    if {$verbose} {puts $command}
    eval $command

    #puts "tweakNObj $transName \"translation $currentVal\""
    #updateVal; tweakNObj $transName \"translation $currentVal\""
  }

  public transName {}
}

#################### rotation engine #########################

itcl_class spinEngine {
  inherit interpEngine

    constructor {config} {set exitEvent "rotNObj $transName \{$endVal\}"}

  method update {} {
    updateVal; 
#    puts "$this --> rotNObj $transName $currentVal"
    rotNObj $transName $currentVal
  }

  public rotName {}
  public transName {}
}

#################### spincam engine #########################

itcl_class spinCamEngine {
  inherit interpEngine

  constructor {config} {
    set exitEvent "rotTo \{$endVal\}"
  }

  method update {} {updateVal; rotTo $currentVal}
}

#################### shift engine #########################

itcl_class shiftEngine {
  inherit interpEngine

  constructor {config} {set exitEvent "moveNObj $transName \{$endVal\}"}

  method update {} {updateVal; moveNObj $transName $currentVal}

  public transName {}
}


#################### fadeEngine #########################

itcl_class fadeEngine {
  inherit interpEngine

  constructor {config} {}

  method update {} {updateVal; tweakNObj $fadeName "transparency $currentVal"}

  public fadeName {}
}

#################### shiftCurveEngine #########################

itcl_class shiftCurveEngine {
  inherit shiftEngine

  constructor {config} {set exitEvent "moveNObj $transName \[$this calcNewPos $endVal\]"}

  method calcNewPos {t} {eval $calc_pos_fxn}
  method update {} {updateVal; moveNObj $transName [calcNewPos $currentVal]}

  public calc_pos_fxn {}
}

#################### scaleEngine #########################

#itcl_class scaleEngine {
#  inherit interpEngine

#    constructor {config} {set exitEvent "tweakNObj $scale_name \"scaleFactor $endVal\""}

#  method update {} {updateVal; tweakNObj $scale_name "scaleFactor $currentVal"}

#  public scale_name {}
#}

#################### 1ValInterpEngine #########################

itcl_class genInterpEngine {
  inherit interpEngine
    
  constructor {config} {set exitEvent "tweakNObj $field_name \"$field_text $endVal\"";}

  method update {} {updateVal; tweakNObj $field_name "$field_text $currentVal"}

  public field_text {}
  public field_name {}
}

## END ##

