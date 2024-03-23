# Code for building picture structures supporting IDW P4
# By Brygg Ullmer, MIT Media Lab
# 05/09/1998: Begun

package require pdf::base

##################################################################
#################### building Picture class ######################
##################################################################

itcl_class bldgPicStruct {
  inherit pdfBase

  constructor {config} {set structFileName $imageFileName}

  method saveStruct {} {}
  method loadStruct {} {}
  method structExists {} {} 

 ## local members
  
  public whichFloor {floor4}
  public whichYear  {1996}
  public floorCoord {.5 .5} ;# 2D, 0..1
  public imageAspect {portrait}
  public paneAngle   {0}
  public paneHeight  {6.}
  public paneWidth   {8.}
  public baseElev    {}

  public paneElev    {5}

  public floorOptions  {basement floor1 floor2 floor3 floor4}
  public yearOptions   {1990 1992 1994 1996 1998 2000}
  public aspectOptions {portrait landscape}

  public imageFilePrefix {ml-images}
  public imageFileName   {}

  public structFilePrefix {pic-structs}
  public structFileName  {}

  public saveFields {
    whichFloor whichYear floorCoord imageAspect
    paneAngle paneHeight paneWidth
    imageFilePrefix imageFileName
    structFilePrefix structFileName baseElev
  }
}

#################################################################
#################### building Picture body ######################
#################################################################
  
# file format:
# ignore lines beginning with # or without content
# expect other lines to be of form "-arg val"
# run {catch {eval $this configure $inline}} on these

#################### load struct ######################

body bldgPicStruct::loadStruct {} {

  set structPath [format {%s/%s} $structFilePrefix $structFileName]
  if {$structFileName == {} || ![file exists $structPath]} {
    puts "$this loadStruct error: bogus structPath $structPath"
    return {}
  }

  set f [open $structPath {r}]

  if {$f == {}} {
    puts "$this loadStruct error: problem opening $structPath"
    return {}
  }

  while {![eof $f]} {
    set inline [gets $f]
    if {[regexp {^#} $inline] || [regexp {^[^a-zA-Z0-9]*$} $inline]} {
      continue ;#comment or empty line
    }

    #assume we read some valid args
    set errCode [catch {eval $this configure $inline} res]
    if {$errCode} {
      puts "$this loadStruct error: ignoring $structPath bogus line <$inline>"
      continue
    }
  }

  close $f
}

#################### save struct ######################

body bldgPicStruct::saveStruct {} {

  set structPath [format {%s/%s} $structFilePrefix $structFileName]
  if {$structFileName == {}} {
    puts "$this saveStruct error: bogus structPath $structPath"
    return {}
  }

  set f [open $structPath {w}]

  if {$f == {}} {
    puts "$this saveStruct error: problem opening $structPath"
    return {}
  }

  ## write the file

  set date [clock format [clock seconds]]
  puts $f "# building picture structure auto-written $date\n"

  foreach field $saveFields {
    puts $f [format {-%s {%s}} $field [$this get $field]]
  }

  close $f
}

#################### save struct ######################

body bldgPicStruct::structExists {} {

  set structPath [format {%s/%s} $structFilePrefix $structFileName]
  set result [file exists $structPath]
  return $result
}

## END ##

