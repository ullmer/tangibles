# Algorithm to close polygons of MIT campus model vertices, grouping into buildings
#  in the process
# Brygg Ullmer, MIT Media Lab
# Begun 01/06/1997 as chainverts
# Revised for geometry closure beginning 01/19/1997

# Aiming for simplicity, not efficiency.

# Algorithm:  take face lists like
#410, 412, 152, -1,
#153, 152, 412, -1,
#153, 412, 410, -1,
#...

# Sort lists; remove duplicate faces.
# Build big assoc array mapping all vertices to all connecting
#  vertices, including list of faces involved

# Take some starting vertex; e.g., the first vertex

#####################

package require Itcl
package require Tclx ;# for lrmdups, among others
package require tmg::base

#################### Chain Vertices ##############################

itcl_class chainpolys {

 inherit base

 constructor {config} {
    set members [concat $members $local_members]
 }


### Read SparseIvFile

 method readSparseIvFile {filename} {

   # Sucks in first coordinate3 list, followed by first indexed face set list.
   # Stores these in rough_facelist and coordlist

   # Longer than I'd like... I could abstract, but I think it would be more time
   # than it's worth

   set f [open $filename r]

   ##### Scan for beginning of coordinates 

   set coordsFound 0
   while {![eof $f] && !($coordsFound)} {
     set inline [gets $f]

     if {[regexp {Coordinate3} $inline]} {set coordsFound 1} ;# break out of loop
   }

   if {[eof $f]} {
     puts "$this readSparseIvFile $filename error: eof encountered before complete (1)"
     return -1
   }

   set entranceFound 0
   while {![eof $f] && !($entranceFound)} {
     set inline [gets $f]
     if {[regexp {point[ ]*\[} $inline]} {set entranceFound 1}
   }

   if {[eof $f]} {
     puts "$this readSparseIvFile $filename error: eof encountered before complete (2)"
     return -1
   }

   ##### Scan in coordinates 
   
   set coordsLeft 1
   set coordnum 0
   set coordlist {}

   while {![eof $f] && $coordsLeft} {
     set inline [gets $f]
     if {[regexp {\]} $inline]}  {set coordsLeft 0; continue}

     set inline [string trim $inline]
     regsub {,$} $inline { } inline
     set inline [string trim $inline]

     lappend coordlist $inline
     set coordnum2val($coordnum) $inline
     incr coordnum
   }
   
   if {[eof $f]} {
     puts "$this readSparseIvFile $filename error: eof encountered before complete (3)"
     return -1
   }

     
   ##### Scan for beginning of faces

   set facesFound 0
   while {![eof $f] && !($facesFound)} {
     set inline [gets $f]

     if {[regexp {IndexedFaceSet} $inline]} {set facesFound 1} ;# break out of loop
   }

   if {[eof $f]} {
     puts "$this readSparseIvFile $filename error: eof encountered before complete (4)"
     return -1
   }

   set entranceFound 0
   while {![eof $f] && !($entranceFound)} {
     set inline [gets $f]
     if {[regexp {coordIndex[ ]*\[} $inline]} {set entranceFound 1}
   }

   if {[eof $f]} {
     puts "$this readSparseIvFile $filename error: eof encountered before complete (5)"
     return -1
   }

   ##### Scan in faces
   
   set facesLeft 1
   set facelist {}

   while {![eof $f] && $facesLeft} {
     set inline [gets $f]
     if {[regexp {\]} $inline]}  {set facesLeft 0; continue}

     set inline [string trim $inline]
     regsub -- {-1,$} $inline { } inline
     regsub -all {,} $inline { } inline
     set inline [string trim $inline]

     lappend facelist $inline
   }
   
   if {[eof $f]} {
     puts "$this readSparseIvFile $filename error: eof encountered before complete (6)"
     return -1
   }

   ### return
   return
}


### Process Facelist

 method processFacelist {} {

   puts "Processing facelist..."

   set facelist [lrmdups $facelist]

   #Build list of neighbors
   set facenum 0

   puts "Roughly thrashing facelist..."
   foreach face $facelist { ;# REALLY rough
     foreach vert $face {
       lappend vert2faces($vert) $facenum 
       append vert2adjvert($vert) " " $face " "
     }
     set face2verts($facenum) $face
     incr facenum
   }

   set vertlist [array names vert2faces] 

   # Clean up vert2faces

   puts "Cleaning up vert2faces"
   foreach vert $vertlist {
     set faces $vert2faces($vert)
     set nfaces [lrmdups $faces]
     set vert2faces($vert) $nfaces
   }

   # Clean up vert2adjvert

   puts "Cleaning up vert2adjvert"

   foreach vert $vertlist {
     set adjverts $vert2adjvert($vert)

     set nadjverts [lrmdups $adjverts]
     set vert2adjvert($vert) $nadjverts
   }
  }

### Chain vertex

 method chainVert {vert {ignoremarks 0}} {

   if {[isVertexMarked $vert] && !($ignoremarks)} {
     puts "$this chainVert $vert error: vertex already marked.  ignoring."
     return
   }

   markVertex $vert

  ## Here are the slots I'll work through:
   #visited prospects nextprospects goodprospects faces

   set faces $vert2faces($vert)
   set prospects $vert2adjvert($vert)
   lappend visited $vert

   set stillwork 1
  
   while {$stillwork} {
     set nextprospects {}
     puts -nonewline "."; flush stdout ;# show working...

     foreach prospect $prospects {
       puts -nonewline "*"   ;#show working...
       if {[lsearch $visited $prospect] != -1} {continue}
       lappend visited $prospect
       append faces " " $vert2faces($prospect) " "
       append nextprospects " " $vert2adjvert($prospect) " "
     }

     set nextprospects [lrmdups $nextprospects]
     set goodprospects {}

     foreach prospect $nextprospects {
       if {[lsearch $visited $prospect] == -1} {
	 lappend goodprospects $prospect
	 markVertex $prospect
       }
     }

     if {$goodprospects == {}} {set stillwork 0} else {set stillwork 1}
     set prospects $goodprospects
   }

   set faces [lrmdups $faces]
   return $faces
 }

### Show faces

  method showFaces {nfacelist} {

    set result {}
    foreach face $nfacelist  {
      #set verts [lindex $facelist $face]

      if {![info exists face2verts($face)]} {
	puts "$this showFaces error: can't find face $face; handling"
        continue
      }

      set verts $face2verts($face) 
      set str {}
      if {$verts == {}} {continue}

      foreach vert $verts {
	append str $vert ", "
      }

      append str "-1, "
      append result $str "\n "
    }

    return $result
  }

#### Mark/check vertices
  
  method markVertex {vertex} {
    set markedVerts($vertex) 1
  }

  method isVertexMarked {vertex} {
    if {![info exists markedVerts($vertex)]} { return 0 }
    return $markedVerts($vertex)
  }

##### Synthesize geometry

 method findMinFaceZList {faces} {
   set minZ  {} 
   set minVerts {}

   foreach face $faces { 
      if {![info exists face2verts($face)]} {
	puts "$this showFaces error: can't find face $face; handling"
        continue
      }

      set verts $face2verts($face) 
      foreach vert $verts {

	if {![info exists coordnum2val($vert)]} {continue}
        set coord $coordnum2val($vert)
	set z [lindex $coord 1]

	if {$minZ == {} || $z <= $minZ} {
	  if {$z == $minZ} {lappend minVerts $vert ;# adding to minVert list
	  } else { set minZ $z; set minVerts $vert} 
        }
      }
   }

   set result [lrmdups $minVerts]

   return $result
 }
     

 method findMaxFaceZList {faces} {
   set maxZ  {} 
   set maxVerts {}

   foreach face $faces { 
      if {![info exists face2verts($face)]} {
	puts "$this showFaces error: can't find face $face; handling"
        continue
      }

      set verts $face2verts($face) 
      foreach vert $verts {

	if {![info exists coordnum2val($vert)]} {continue}
        set coord $coordnum2val($vert)
	set z [lindex $coord 1]

	if {$maxZ == {} || $z >= $maxZ} {
	  if {$z == $maxZ} {lappend maxVerts $vert ;# adding to maxVert list
	  } else { set maxZ $z; set maxVerts $vert} 
        }
      }
   }

   set result [lrmdups $maxVerts]

   return $result
 }

 #### Order Face Vertices ####

 method orderFaceVerts {lfacelist} {
   # doing by seat of pants; Not Intended To Be Graceful or Efficient.  :-) BAU

   if {[llength $lfacelist] < 3} {
     puts "$this orderFaceVerts $lfacelist; too few verts"; return {}
   }

   ## Ok, get us to a starting config

   set head [lindex $lfacelist 0]
   set tail [lrange $lfacelist 1 end]

   set headadj $vert2adjvert($head)

   if {[llength $headadj] > 2} {
     puts "$this orderFaceVerts:  adjacencies ($headadj) loosely imply face may already be capped"
     return {}
   }

   set neighbors [intersect $headadj $lfacelist] ;# find people who are both adjacent and on
						;# said lfacelist
   set neighborOfChoice [lindex $neighbors 0] ;# arbitrarily select 1.

   set result [list $head $neighborOfChoice]
   set index  [lsearch $tail $neighborOfChoice]

   if {$index == -1} {
     puts "$this orderFaceVerts $lfacelist; something odd (1:: $headadj // $neighbors)"; return
   }

   ## OK, wind up for the repetition

   set vertsleft [lreplace $tail $index $index]

   set lastptr $head
   set ptr $neighborOfChoice

   while {[llength $vertsleft] > 0} { 

     set ptradj $vert2adjvert($ptr)
     set neighbors [intersect $ptradj $lfacelist]
     set index     [lsearch $neighbors $lastptr]
     if {$index == -1 || ([llength $neighbors] != 2)} {
       puts "$this orderFaceVerts $lfacelist; something odd (2)"; return
     }

     set nextptr [lreplace $neighbors $index $index]

     set index [lindex $vertsleft $nextptr]
     if {$index == -1} {
      puts "$this orderFaceVerts $lfacelist; something odd (3)"; return
     }
   
     lappend $result $nextptr

     set vertsleft [lreplace $vertsleft $index $index]
     set lastptr $ptr
     set ptr $nextptr
   }

   return $result
 }

 ############## Synth Geom ################

 method synthGeom {outfile} {

   set f [open $outfile {w}]

   ## Add header

   set str {#Inventor V2.0 ascii

    Separator {
        DEF SceneInfo Info {
                string "Converted by wcvt2pov v2.7"
        }
        ShapeHints {
                vertexOrdering CLOCKWISE
                shapeType SOLID
                faceType CONVEX
                creaseAngle 0.0
        }
    }}
    regsub {\}$} $str {} str
    puts $f $str

    ### Print coordinates

    puts $f "Coordinate3 \{\n  point \["
    foreach coord $coordlist {
      puts $f "$coord,"
    }
    puts $f "\]\n\}"

    ### Print faces

    set geomnum 0

    set colorgeoms 1
    #set colorgeoms 0

    set facesets [lrmdups $facesets]
    puts "$this:: facesets [llength $facesets] $facesets"

    foreach set $facesets {
       set output [showFaces $set] 

       if {$colorgeoms} {
	 set r [expr [random 10] * 1. / 10.]
	 set g [expr [random 10] * 1. / 10.]
	 set b [expr [random 10] * 1. / 10.]
	 puts $f "Material {diffuseColor $r $g $b}"
       } 	 

       puts $f [format "DEF GEOM_%s IndexedFaceSet \{\n  coordIndex \[" $geomnum]

       #puts $f "min verts [findMinFaceZList $set]"

       puts $f $output
       puts $f "\]\n\}\n"

       incr geomnum
    }

    puts $f "\}\n"

    close $f
 }	     

#### Process file

  method processFile {infile outfile} {

    puts "$this processFile: scanning $infile"

    readSparseIvFile $infile

    puts "$this processFile: execing chainverts"

    processFacelist 

    puts "$this processFile: chaining all vertices"

    foreach vert $vertlist { ;# scanning through 0, 1, 2, ... 

      if {[isVertexMarked $vert]} {continue}

      set newFaceSet [chainVert $vert]
      lappend facesets $newFaceSet
    }

    puts "MUST CLOSE GEOMS HERE"

    synthGeom $outfile

 }

## Local members

 public local_members {facelist vertlist coordlist facesets}

 public facelist {}
 public vertlist {}
 public coordlist {}
 public coordnum2val
 public vert2faces
 public vert2adjvert
 public face2verts 
 public markedVerts
 public facesets {}
}

