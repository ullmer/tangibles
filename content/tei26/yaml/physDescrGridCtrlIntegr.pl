% Physical description of grid controllers
% Brygg Ullmer and CoPilot
% Begun 2025-07-17

% Load data and logic
:- consult('physDescrGridCtrlData.pl').
:- consult('physDescrGridCtrlTransf.pl').

% physDescrReeds.pl

% Optional: define a test or entry predicate
run_ex01 :-
    grid_pad_dist_between_pads(adafruit_neotrellis, mm, X, Y),
    format("Pad spacing (mm): ~w x ~w~n", [X, Y]),
    dims(adafruit_neotrellis, in, W, H, D),
    format("Dimensions (in): ~2f x ~2f x ~2f~n", [W, H, D]).

%%% end %%%
