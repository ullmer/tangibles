%https://www.swi-prolog.org/pack/list?p=yaml
%
:- module(ex, []).

:- use_module(library(yaml/parser)).
:- use_module(library(yaml/util)).
:- use_module(library(yaml/serializer)).

ex1 :-
 read_yaml('posters-iui24.yaml', YAML),
 parse(YAML, PL),
 print_term(PL, []),
 serialize(PL, YAML1),
 write(YAML1),
 write_yaml('ex1_gen.yaml', YAML1).
