# Base class for proxy code
# borrowed from dynamic GSSM dbase code
# Brygg Ullmer, ullmer@media.mit.edu
# Begun 1/1/1996 

package require Itcl
package provide tmg::base 1.0

################################ Atom ##############################

itcl_class base {

  constructor {config} {}
  method config {config} {}
  method get {var} {return [lindex [$this info public $var] 2]}

  method addOptions {optionlist} {
    set result ""

    # adding newline after each option here so RCS will work well on
    # results

    foreach option $optionlist {
      if {![string match [$this get $option] {}]} {
	append result [format {-%s {%s} } $option [$this get $option]] 
      }
    }
    return $result
  }

  method self {} {
    return [format {%s %s %s} [$this info class] $this [addOptions $members]]
  }

  method folded_self {} {
    #prefixes each "-" option with "\\\n" to help RCS work well

    set self [self]
    set result {}
    foreach el $self {
      if {[regexp {^-[a-zA-Z]} $el]} {
	lappend result [format {\%s%s} "\n" $el]
      } else {lappend result $el}
    }

    return $result
  }

  method expandVar {quoted} {
    ;# Definitely not the most efficient procedure in the world, but
    ;# it sure could help for more maintainable/cleaner code
  
    regsub -all {\{} $quoted {\\\{} quoted
    set quotedlist [split $quoted "\n"]

    set result {}

    foreach line $quotedlist {
      append result [uplevel 1 eval list $line] "\n"
    }

    regsub -all {\\\{} $result "\{" result
    regsub -all {\\\}} $result "\}" result

    return $result
  }

  public members {verbose}
  public verbose {0}
}

