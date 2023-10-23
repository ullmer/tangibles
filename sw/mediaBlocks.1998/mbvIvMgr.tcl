# Minimally-reasonable interpolation/animation engine
# By Brygg Ullmer, MIT Media Lab
# Begun 09/06/1997

package require pdf::base 1.0
package require pdf::digitals 1.0

package require pdf::visuals:InterpEngine 1.0
package require pdf::visuals:IvEngines 2.0

package provide pdf::visuals:ivMgr 2.0

#################### interp Manager ####################

itcl_class ivMgr {
  inherit interpMgr 

  constructor {config} {}

  method shiftCam {beginPos endPos duration} {}
  method spinCam  {beginPos endPos duration} {}

  method shiftObj {transname beginPos endPos duration} {}
  method spinObj    {rotname beginRot endRot duration} {}
  method fadeObj  {materialname beginVal endVal duration} {}
  method scaleObj  {scalename beginVal endVal duration} {}

  method shiftTexture {transname beginPos endPos duration} {}
  method cshiftTexture {transname beginPos diffRate} {}

  method shiftCamTo {camname endPos duration} {}
  method shiftObjTo {transname endPos duration} {}
  method spinObjTo  {rotname endRot duration} {}

  method genName {} {incr lastID; return [format {::IVMGR_transf%i} $lastID]}

  method nodeChanging {nodeName} {return 0} ;#placeholder 
  method setNodeChanging {nodeName val engine} {}

 ## Local members
  public lastID {0}
  public nodeBeingModified ;#assoc array
}

###################################################
#################### ivMgr ########################
###################################################

############## shiftObj ###################

body ivMgr::shiftObj {transName beginPos endPos duration} {
  set eventName [genName]
  if {$verbose} {puts "creating shift engine $eventName"}

  genInterpEngine $eventName -field_text "translation" -field_name $transName \
    -beginVal $beginPos -endVal $endPos \
    -autoDelete 1 -fullDuration $duration

  setNodeChanging $transName 1 $eventName
  $eventName appendExitEvent "$this setNodeChanging $transName 0 $eventName"

  $this addEvent $eventName
  return $eventName;
}

############## shiftObj ###################

body ivMgr::scaleObj {scaleName beginScale endScale duration} {
  set eventName [genName]
  if {$verbose} {puts "creating scale engine $eventName"}

  genInterpEngine $eventName -field_text "scaleFactor" -field_name $scaleName \
    -beginVal $beginScale -endVal $endScale \
    -autoDelete 1 -fullDuration $duration

  setNodeChanging $scaleName 1 $eventName
  $eventName appendExitEvent "$this setNodeChanging $scaleName 0 $eventName"

  $this addEvent $eventName
  return $eventName;
}

############## fadeObj ###################

body ivMgr::fadeObj  {materialname beginVal endVal duration} {
  set eventName [genName]
  if {$verbose} {puts "creating fade engine $eventName"}

  genInterpEngine $eventName -field_text "transparency" -field_name $materialname \
    -beginVal $beginVal -endVal $endVal \
    -autoDelete 1 -fullDuration $duration

  setNodeChanging $materialname 1 $eventName
  $eventName appendExitEvent "$this setNodeChanging $materialname 0 $eventName"

  $this addEvent $eventName
  return $eventName
}

############## spinObj ###################

body ivMgr::spinObj {transName beginPos endPos duration} {
  set eventName [genName]
  if {$verbose} {puts "creating spin engine $eventName"}

  spinEngine $eventName -transName $transName \
    -beginVal $beginPos -endVal $endPos \
    -autoDelete 1 -fullDuration $duration

  setNodeChanging $transName 1 $eventName
  $eventName appendExitEvent "$this setNodeChanging $transName 0 $eventName"

  $this addEvent $eventName
  return $eventName;
}

############## shiftCam ###################

#body ivMgr::shiftCam {camname beginPos endPos duration} {

body ivMgr::shiftCam {beginPos endPos duration} {
  set eventName [genName]
  if {$verbose} {puts "creating shiftCam engine $eventName"}

  shiftCamEngine $eventName \
    -beginVal $beginPos -endVal $endPos \
    -autoDelete 1 -fullDuration $duration

  $this addEvent $eventName
  return $eventName;
}

############## spinCam ###################

body ivMgr::spinCam {beginPos endPos duration} {
  set eventName [genName]
  if {$verbose} {puts "creating shiftCam engine $eventName"}

  spinCamEngine $eventName \
    -beginVal $beginPos -endVal $endPos \
    -autoDelete 1 -fullDuration $duration

  $this addEvent $eventName
  return $eventName;
}

############## shiftTexture ###################

body ivMgr::shiftTexture {transname beginPos endPos duration} {
  set eventName [genName]
  if {$verbose} {puts "creating shiftTexture engine $eventName"}
  puts "creating shiftTexture engine $eventName"

  shiftTextureEngine $eventName -transName $transname \
    -beginVal $beginPos -endVal $endPos \
    -autoDelete 1 -fullDuration $duration

  $this addEvent $eventName
  return $eventName;
}

############## cshiftTexture ###################

body ivMgr::cshiftTexture {transname beginPos diffRate} {
  set eventName [genName]
  if {$verbose} {puts "creating shiftTexture engine $eventName"}
  puts "creating shiftTexture engine $eventName"

  cshiftTextureEngine $eventName -transName $transname \
    -beginVal $beginPos -diffRate $diffRate -autoDelete 1 

  $this addEvent $eventName
  return $eventName
}

############## shiftObj ###################

body ivMgr::setNodeChanging {nodeName val engine} {
}

## END ##

