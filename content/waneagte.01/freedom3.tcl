#Freedom's first (proxied) program in Wish3
#12/1/95, proxy Brygg

proc readfile {file} {
  set f [open $file r]
  set result ""

  while {![eof $f]} {
    append result [gets $f] "\n"
  }

  return $result
}    
    
puts [readfile "hello"]
puts "(and then, for something *really* different)"

puts "Reading file..."
set fbvar [readfile "place11-2.iv"]
puts "file read"

addNObj arch $fbvar

bindNObj arch {shiftNObj arch {0 0 0} {-2 100 0} 2 30}

puts "assertions complete"

#exec playaiff soundfilename.aiff
#getCameraPosition
#dist3D 
#set radius [dist3D [getCameraPosition] $archPosition]
#if {$radius < 10} {puts "Whee!"}
