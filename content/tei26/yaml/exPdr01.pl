%pack_install('https://github.com/honnix/yaml.git').

use_module(library(yaml)).

yaml_read('physDescrReeds.yaml', Dict),
   get_dict(reed, Dict, Reed),
   get_dict(fab, Reed, Fab),
   get_dict(constraints, Fab, Constraints),
   get_dict(copilotEstimates, Constraints, Estimates),
   member(C, Estimates),
   writeln(C).

