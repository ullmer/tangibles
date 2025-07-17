% Interactive compositional fabrication query
% Brygg Ullmer and CoPilot
% 2025-07-16

% Load data
:- consult('physDescrReeds.pl').
:- consult('physDescrGridCtrl01.pl').

%['physDescrReeds.pl'].
%['physDescrGridCtrl01.pl'].

% Compute run lengths for a controller
run_lengths(Controller, RowRun, ColRun) :-
    grid_controller(Controller, _, grid(Rows, Cols), pad_pitch_mm(XPitch, YPitch), _, _),
    RowRun is Cols * XPitch,
    ColRun is Rows * YPitch.

% Check if a reed width supports a given run length
reed_satisfies_constraints(RunLength, Width, Score) :-
    reed_cut_constraint_dec(range(Min, Max), min_cut(MinCut), preferred_cut(PrefCut)),
    Width >= Min, Width =< Max,
    Cuts is floor(RunLength / PrefCut),
    (Cuts >= 1 -> Score is Cuts ; Score is 0).

% Rank reed widths for a given run length
rank_reeds(RunLength, Ranked) :-
    findall(Score-Width,
        (reed_width(_, Width), reed_satisfies_constraints(RunLength, Width, Score), Score > 0),
        Scored),
    sort(0, @>=, Scored, Sorted),
    pairs_values(Sorted, Ranked).

% Top 3 reeds for a controller
top_reeds_for_controller(Controller, TopRow, TopCol) :-
    run_lengths(Controller, RowRun, ColRun),
    rank_reeds(RowRun, RowRanks),
    rank_reeds(ColRun, ColRanks),
    length(RowRanks, L1), L1 >= 3,
    length(ColRanks, L2), L2 >= 3,
    append(RowRanks, ColRanks, Combined),
    sort(Combined, Unique),
    length(Unique, L3), L3 >= 3,
    TopRow = RowRanks,
    TopCol = ColRanks.

%top_reeds_for_controller(akai_apc_mini_mk2, TopRow, TopCol).
%top_reeds_for_controller(novation_launchpad_x, TopRow, TopCol).


