# First explorations of book proxy-code
# In conjunction with Ishii/Ullmer Active Desk prototype
# Brygg Ullmer, ullmer@media.mit.edu
# Begun 01/11/95

global __BOOK__
if {[info exists __BOOK__]} {return}
set __BOOK__ 1

#The following should be net_source or equiv
source "~ullmer/pb/code/desk.1/base.tcl"

############################ Texture class #############################

itcl_class texture { #operates on RGB textures
  inherit base

  constructor {config} {
    set members [concat $members $local_members]
  }
  
  method getTextureSize {} {
    #find "size" file
    regsub {\.rgb$} $texture_name {.size} texture_size

    if {![file exists $texture_size]} {
      set texture_size {0 0}
      return $texture_size
    }

    set f [open $texture_size r]
    set size [gets $f]; close $f

    regsub {^.*[^0-9]([0-9]+) by ([0-9]+).*} $size {\1} x
    regsub {^.*[^0-9]([0-9]+) by ([0-9]+).*} $size {\2} y

    set texture_size [list $x $y]

    return $texture_size
  }

  public local_members {texture_name texture_size}

  public texture_name {}
  public texture_size {0 0}
}

############################ Book class #############################

itcl_class book {
  inherit base

  constructor {config} {
    set members [concat $members $local_members]
  }

  method init {lname} {
    set name $lname
    set cover [format {data/books/%s-cover.dsk.rgb} $name]
    set spine [format {data/books/%s-spine.dsk.rgb} $name]
    set back  [format {data/books/%s-back.dsk.rgb} $name]

    set texture_cover [format {%s_cover_texture} $name]
    set texture_spine [format {%s_spine_texture} $name]
    set texture_back  [format {%s_back_texture} $name]

    texture $texture_cover -texture_name $cover
    texture $texture_spine -texture_name $spine
    texture $texture_back  -texture_name $back

    inferSize
  }
  
  method inferSize {} {
    #Grab texture sizes from 42dpi images

    set spine_size [$texture_spine getTextureSize]
    set cover_size [$texture_cover getTextureSize]

    set xdim [expr [lindex $spine_size 0] * $size_multiplier]
    set ydim [expr [lindex $spine_size 1] * $size_multiplier]
    set zdim [expr [lindex $cover_size 0] * $size_multiplier]

    return [list $xdim $ydim $zdim]
  }

  method genSimplePlane {pt1 pt2 pt3 pt4 normal {texture NULL} {dir 1}} {
# dir: 1 = forwards, 0 = backwards

   if {[string match $texture NULL]} {set ivtexture {}} else {
     if {$dir == 1} {set tcoord {0 1, 1 1, 1 0, 0 0}} else {
		     set tcoord {1 1, 0 1, 0 0, 1 0}}

     set ivtexture [format {
	TextureCoordinate2 { point [%s] }
        Texture2 {
	 filename "%s"
	 model DECAL
        }} $tcoord [$texture get texture_name]]
   }

    set result [format {
      Separator {
	NormalBinding {value   PER_FACE}
	Normal        {vector  [%s, %s]}
	Coordinate3 { point [ %s, %s, %s, %s ] }

	%s

	FaceSet { numVertices 4 }
      }
      } $normal $normal $pt1 $pt2 $pt3 $pt4 $ivtexture]

    return $result
  }

  method genSimpleIv {} {

    set hx [expr $xdim/2.]
    set hy [expr $ydim/2.]
    set hz [expr $zdim/2.]

    set a [list  $hx -$hy -$hz]
    set b [list  $hx -$hy  $hz]
    set c [list -$hx -$hy  $hz]
    set d [list -$hx -$hy -$hz]

    set e [list  $hx  $hy -$hz]
    set f [list  $hx  $hy  $hz]
    set g [list -$hx  $hy  $hz]
    set h [list -$hx  $hy -$hz]

    set result ""

    append result [genSimplePlane $d $a $e $h {0 0 -1} $texture_spine]
    append result [genSimplePlane $a $b $f $e {1 0 0 } $texture_cover]
    append result [genSimplePlane $d $c $g $h {-1 0 0} $texture_back 0] 

    append result [genSimplePlane $e $f $g $h {0 1 0}]
    append result [genSimplePlane $a $b $c $d {0 -1 0}]
    append result [genSimplePlane $b $c $g $f {0 0 1}] 

    return $result
  }

  public local_members {
    name 
    texture_cover texture_spine dpi
    texture_cover_hires texture_spine_hires
    xdim ydim zdim
  }

  public name

  public texture_cover {}
  public texture_back {}
  public texture_spine {}
  public dpi {42}
  public size_multiplier {0.06047} ;#changes to cm units

  public texture_cover_hires {}
  public texture_back_hires {}
  public texture_spine_hires {}

  public xdim {0} ;#width of spine
  public ydim {0} ;#height of spine
  public zdim {0} ;#depth of cover
}


