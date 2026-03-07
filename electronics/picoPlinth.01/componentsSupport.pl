% rpi_pico1.pl — minimal, YAML-aligned pin/function map
% Source: official Pico pinout, cross-checked with Pinout.xyz.
% (SPI/I2C/UART alternates only; no CTS/RTS/PWM/PIO in this minimal set.)
% Prolog expansions of YAML file by CoPilot
% Brygg Ullmer and CoPilot, Clemson University
% Begun 2026-03-07 

% -------- Convenience predicates --------

% true if Pin supplies Capability (exact term match).
pin_supports(Component, Pin, Capability) :-
    pin(Component, Pin, Caps),
    member(Capability, Caps).

% list all physical pins that match a Capability, e.g., pins_with(i2c(1,sda), Pins).
pins_with(Component, Capability, Pins) :-
    findall(P, pin_supports(Component, P, Capability), PList),
    sort(PList, Pins).

% collect pins that offer any role on a given SPI or I2C controller
% (e.g., pins_for_spi(0, Pins).)
pins_for_spi(Component, Ctrl, Pins) :-
    findall(P, (pin(Component, P, Caps), member(spi(Ctrl, _), Caps)), PList),
    sort(PList, Pins).

pins_for_i2c(Component, Ctrl, Pins) :-
    findall(P, (pin(Component, P, Caps), member(i2c(Ctrl, _), Caps)), PList),
    sort(PList, Pins).

% lightweight name lookup helpers
is_ground(Component, Pin)   :- pin(Component, Pin, Caps), member(gnd, Caps).
is_analog(Component, Pin)   :- pin(Component, Pin, Caps), (member(adc(_), Caps); member(adc_vref, Caps); member(agnd, Caps)).

% Deterministic yes/no test when Pin is (usually) ground

% Enumerates on backtracking (use this as your main is_power/2)
is_power(Component, Pin) :-
    power_pins(Component, L),
    member(Pin, L).

% Deterministic yes/no test when Pin is (usually) ground
is_power_chk(Component, Pin) :-
    power_pins(Component, L),
    memberchk(Pin, L).

%%% end %%%
