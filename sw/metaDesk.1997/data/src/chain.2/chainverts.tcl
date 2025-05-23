# Algorithm to chain MIT campus model vertices into buildings
# Brygg Ullmer, MIT Media Lab
# Begun 01/06/1997

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

#################### Chain Vertices ##############################

itcl_class chainverts {

### Read SparseIvFile

### Read FaceFile

 method readFaceFile {filename} {
   set rough_facelist {}

   set f [open $filename r]
   while {![eof $f]} {
     set inline [gets $f]
     regsub -- {-1,} $inline {} inline ;#remove trailing -1
     regsub -all {,} $inline {} inline ;#remove commas

     lappend rough_facelist $inline
   }
   close $f

   return $rough_facelist
 }

### Process Facelist

 method processFacelist {rough_facelist} {

   puts "Processing facelist..."

   set facelist [lrmdups $rough_facelist]

   #Build list of neighbors
   set facenum 0

   puts "Roughly thrashing facelist..."
   foreach face $facelist { ;# REALLY rough
     foreach vert $face {
       lappend vert2faces($vert) $facenum 
       append vert2adjvert($vert) $face " "
     }
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

 method chainVert {vert} {

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
       append faces $vert2faces($prospect) " "
       append nextprospects $vert2adjvert($prospect) " "
     }

     set nextprospects [lrmdups $nextprospects]
     set goodprospects {}

     foreach prospect $nextprospects {
       if {[lsearch $visited $prospect] == -1} {
	 lappend goodprospects $prospect
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
      set verts [lindex $facelist $face]
      set str {}

      foreach vert $verts {
	append str $vert ", "
      }

      append str "-1,"
      lappend result $str
    }

    return $result
  }


## Local members

 public facelist {}
 public vert2faces
 public vert2adjvert
 public vertlist {}

}

