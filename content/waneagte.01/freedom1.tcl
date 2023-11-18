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
puts [readfile "freedom1.tcl"]
