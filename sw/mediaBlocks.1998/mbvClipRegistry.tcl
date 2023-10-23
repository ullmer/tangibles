# MoveMoov code
# By Phillip Tiongson and Brygg Ullmer, MIT Media Lab
# Begun 02/12/1998

package require pdf::base 1.0
package require pdf::visuals:TextureCache 1.0

package provide mbv::clipRegistry 1.0

#################### arrayWall #########################

itcl_class clipRegistry {
  inherit pdfBase

  constructor {config} {}

## methods

  method registerFrames {beginFrame endFrame} {}
  method getFrame      {framenum} {}
  method getFrameRange {beginFrame endFrame} {}

  method setLabelRange {labelName beginFrame endFrame} {}
  method getLabelRange {labelName} {}

  method cacheFrameRange   {beginFrame endFrame} {}
  method uncacheFrameRange {beginFrame endFrame} {}
  method getTextureCache   {} {return [$textureCache getThis]}

  method buildName {num} {return [format {%s/%s%i.%s} $fprefix $fbase $num $fpostfix]}

## members

  public frameList    {}
  public frameNum2Name   ;# assoc array for frame num -> frame name
  public label2range     ;# assoc array for label ranges

  public fprefix  {/extra/data/movemoov.data}
  public fbase    {brazil}
  public fpostfix {rgb}

  public textureCache {tcache}
  public cacheByDefault {1}
}

########################################################
#################### clipRegistry ######################
########################################################

#################### constructor #########################

body clipRegistry::constructor {config} {
  if {[info objects $textureCache] == {}} {
    textureCacheMgr $textureCache 
    ;# allows us to share a global texture cache pool
  }
}

#################### registerFrames #########################
  
body clipRegistry::registerFrames {beginFrame endFrame} {
  if {$verbose} {puts "$this registerFrames $beginFrame $endFrame called"}

  for {set i $beginFrame} {$i <= $endFrame} {incr i} {
    set fname [buildName $i]
    if {![file exists $fname]} {
      puts "$this registerFrames error: \"$fname\" doesn't exist.  Ignoring..."
      continue
    }

    set frameNum2Name($i) $fname
    lappend frameList $fname
    if {$cacheByDefault} {$textureCache cacheFilename $fname}
  }
}

#################### getFrame #########################
  
body clipRegistry::getFrame      {framenum} {

  if {![info exists frameNum2Name($framenum)]} {
    puts "$this getFrame -- element $i doesn't exist."
    return {}
  }
  set result $frameNum2Name($framenum)
  return $result
}

#################### getFrameRange #########################
  
body clipRegistry::getFrameRange {beginFrame endFrame} {
  if {$verbose} {puts "$this getFrameRange $beginFrame $endFrame called"}

  set result {}

  for {set i $beginFrame} {$i <= $endFrame} {incr i} {
    if {![info exists frameNum2Name($i)]} {
      puts "$this getFrameRange -- element $i doesn't exist.  Ignoring"
      continue
    }

    lappend result $frameNum2Name($i)
  }

  return $result
}
  
#################### setLabelRange #########################

body clipRegistry::setLabelRange {labelName beginFrame endFrame} {

  #something stupid for the moment
  set label2range($labelName) [list $beginFrame $endFrame]
}

## END ##

