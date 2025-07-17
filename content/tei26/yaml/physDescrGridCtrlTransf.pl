% MIDI Grid Controller Descriptions
% By Brygg Ullmer and CoPilot
% Begun 2025-07-17

% Distance between pads in X and Y directions
% Example: grid_pad_dist_between_pads(adafruit_neotrellis, mm, 3, 3).
grid_pad_dist_between_pads(Controller, Unit, GapX, GapY) :-
    pad_spacing(Controller, Unit, GapX, GapY).

% Optional offset from center
% Example: grid_pad_center_offset(adafruit_neotrellis, mm, 1.5, 1.5).
grid_pad_center_offset(Controller, Unit, OffsetX, OffsetY) :-
    pad_offset(Controller, Unit, OffsetX, OffsetY).

% Margins around the grid
% If offset exists, margins are asymmetric and centered is false
% If no offset, margins are symmetric and centered is true
grid_pad_dist_margins(Controller, Unit, margin(Left, Right, top_bottom(Top, Bottom)), false) :-
    grid_pad_center_offset(Controller, Unit, OffsetX, OffsetY),
    pad_spacing(Controller, Unit, GapX, GapY),
    Left is OffsetX,
    Right is GapX - OffsetX,
    Top is OffsetY,
    Bottom is GapY - OffsetY.

grid_pad_dist_margins(Controller, Unit, margin(Horiz, Vert, both), true) :-
    \+ grid_pad_center_offset(Controller, Unit, _, _),
    pad_spacing(Controller, Unit, GapX, GapY),
    Horiz is GapX / 2,
    Vert is GapY / 2.

% Conversion factor
mm_to_in(25.4).

% Extract pad spacing from grid_controller facts
pad_spacing(Controller, mm, GapX, GapY) :-
    grid_controller(Controller, _, _, _, pad_pitch_mm(GapX, GapY), _).

% Convert pad spacing to inches
pad_spacing(Controller, in, GapX_in, GapY_in) :-
    pad_spacing(Controller, mm, GapX_mm, GapY_mm),
    mm_to_in(Factor),
    GapX_in is GapX_mm / Factor,
    GapY_in is GapY_mm / Factor.

% Extract dimensions in mm
dims(Controller, mm, W, H, D) :-
    grid_controller(Controller, _, dims_mm(W, H, D), _, _, _).

% Convert dimensions to inches
dims(Controller, in, W_in, H_in, D_in) :-
    dims(Controller, mm, W_mm, H_mm, D_mm),
    mm_to_in(Factor),
    W_in is W_mm / Factor,
    H_in is H_mm / Factor,
    D_in is D_mm / Factor.

%%% end %%%

