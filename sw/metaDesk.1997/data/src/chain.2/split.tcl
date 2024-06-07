## Quick program to split campus model into n submodels, one for
## each DEFined subsection

## By Brygg Ullmer, MIT Media Lab TMG
## Begun 01/24/1997

set target {campus.iv}
set outputdir {data}

set f [open $target r]

set inline {}

# Scan file 'til first inline
while {![eof $f] && ![regexp {DEF} $inline]} {set inline [gets $f]} 

# Use DEF as filename, keep scanning to next def
while {![eof $f]} {
  regsub {^.*DEF ([^ ]*).*$} $inline {\1} name

  if {[info exists g]} {close $g}
  set g [open "$outputdir/$name.iv" w]

  puts "Scanning $name..."

  puts $g $inline
  set inline {}

  while {![eof $f] && ![regexp {DEF} $inline]} {
     set inline [gets $f]
     puts $g $inline
  } 
}

close $f
close $g



