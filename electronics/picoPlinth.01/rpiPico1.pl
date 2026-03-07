% rpi_pico1.pl — minimal, YAML-aligned pin/function map
% Source: official Pico pinout, cross-checked with Pinout.xyz.
% (SPI/I2C/UART alternates only; no CTS/RTS/PWM/PIO in this minimal set.)
% Prolog expansions of YAML file by CoPilot
% Brygg Ullmer and CoPilot, Clemson University
% Begun 2026-03-07 

pin(rpiPico1, 1,  [gp(0),  spi(0,rx),  i2c(0,sda), uart(0,tx)]).
pin(rpiPico1, 2,  [gp(1),  spi(0,csn), i2c(0,scl), uart(0,rx)]).
pin(rpiPico1, 3,  [gnd]).
pin(rpiPico1, 4,  [gp(2),  spi(0,sck), i2c(1,sda)]).
pin(rpiPico1, 5,  [gp(3),  spi(0,tx),  i2c(1,scl)]).
pin(rpiPico1, 6,  [gp(4),  spi(0,rx),  i2c(0,sda), uart(1,tx)]).
pin(rpiPico1, 7,  [gp(5),  spi(0,csn), i2c(0,scl), uart(1,rx)]).
pin(rpiPico1, 8,  [gnd]).
pin(rpiPico1, 9,  [gp(6),  spi(0,sck), i2c(1,sda)]).
pin(rpiPico1, 10, [gp(7),  spi(0,tx),  i2c(1,scl)]).
pin(rpiPico1, 11, [gp(8),  spi(1,rx),  i2c(0,sda), uart(1,tx)]).
pin(rpiPico1, 12, [gp(9),  spi(1,csn), i2c(0,scl), uart(1,rx)]).
pin(rpiPico1, 13, [gnd]).
pin(rpiPico1, 14, [gp(10), spi(1,sck), i2c(1,sda)]).
pin(rpiPico1, 15, [gp(11), spi(1,tx),  i2c(1,scl)]).
pin(rpiPico1, 16, [gp(12), spi(1,rx),  i2c(0,sda), uart(0,tx)]).
pin(rpiPico1, 17, [gp(13), spi(1,csn), i2c(0,scl), uart(0,rx)]).
pin(rpiPico1, 18, [gnd]).
pin(rpiPico1, 19, [gp(14), spi(1,sck), i2c(1,sda)]).
pin(rpiPico1, 20, [gp(15), spi(1,tx),  i2c(1,scl)]).
pin(rpiPico1, 21, [gp(16), spi(0,rx),  i2c(0,sda), uart(0,tx)]).
pin(rpiPico1, 22, [gp(17), spi(0,csn), i2c(0,scl), uart(0,rx)]).
pin(rpiPico1, 23, [gnd]).
pin(rpiPico1, 24, [gp(18), spi(0,sck), i2c(1,sda)]).
pin(rpiPico1, 25, [gp(19), spi(0,tx),  i2c(1,scl)]).
pin(rpiPico1, 26, [gp(20), spi(0,rx),  i2c(0,sda), uart(1,tx)]).
pin(rpiPico1, 27, [gp(21), spi(0,csn), i2c(0,scl), uart(1,rx)]).
pin(rpiPico1, 28, [gnd]).
pin(rpiPico1, 29, [gp(22), spi(0,sck), i2c(1,sda)]).
pin(rpiPico1, 30, [run]).
pin(rpiPico1, 31, [gp(26), adc(0)]).
pin(rpiPico1, 32, [gp(27), adc(1)]).
pin(rpiPico1, 33, [gnd, agnd]).
pin(rpiPico1, 34, [gp(28), adc(2)]).
pin(rpiPico1, 35, [adc_vref]).
pin(rpiPico1, 36, [v3v3_out]).
pin(rpiPico1, 37, [v3v3_en]).
pin(rpiPico1, 38, [gnd]).
pin(rpiPico1, 39, [vsys]).
pin(rpiPico1, 40, [vbus]).

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
power_pins(rpiPico1, [35,36,37,39,40]).

% Enumerates on backtracking (use this as your main is_power/2)
is_power(Component, Pin) :-
    power_pins(Component, L),
    member(Pin, L).

% Deterministic yes/no test when Pin is (usually) ground
is_power_chk(Component, Pin) :-
    power_pins(Component, L),
    memberchk(Pin, L).

%%% end %%%
