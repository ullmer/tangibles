% rpi_pico1.pl — minimal, YAML-aligned pin/function map
% Source: official Pico pinout, cross-checked with Pinout.xyz.
% (SPI/I2C/UART alternates only; no CTS/RTS/PWM/PIO in this minimal set.)
% Prolog expansions of YAML file by CoPilot
% Brygg Ullmer and CoPilot, Clemson University
% Begun 2026-03-07 

pin(1,  [gp(0),  spi(0,rx),  i2c(0,sda), uart(0,tx)]).
pin(2,  [gp(1),  spi(0,csn), i2c(0,scl), uart(0,rx)]).
pin(3,  [gnd]).
pin(4,  [gp(2),  spi(0,sck), i2c(1,sda)]).
pin(5,  [gp(3),  spi(0,tx),  i2c(1,scl)]).
pin(6,  [gp(4),  spi(0,rx),  i2c(0,sda), uart(1,tx)]).
pin(7,  [gp(5),  spi(0,csn), i2c(0,scl), uart(1,rx)]).
pin(8,  [gnd]).
pin(9,  [gp(6),  spi(0,sck), i2c(1,sda)]).
pin(10, [gp(7),  spi(0,tx),  i2c(1,scl)]).
pin(11, [gp(8),  spi(1,rx),  i2c(0,sda), uart(1,tx)]).
pin(12, [gp(9),  spi(1,csn), i2c(0,scl), uart(1,rx)]).
pin(13, [gnd]).
pin(14, [gp(10), spi(1,sck), i2c(1,sda)]).
pin(15, [gp(11), spi(1,tx),  i2c(1,scl)]).
pin(16, [gp(12), spi(1,rx),  i2c(0,sda), uart(0,tx)]).
pin(17, [gp(13), spi(1,csn), i2c(0,scl), uart(0,rx)]).
pin(18, [gnd]).
pin(19, [gp(14), spi(1,sck), i2c(1,sda)]).
pin(20, [gp(15), spi(1,tx),  i2c(1,scl)]).
pin(21, [gp(16), spi(0,rx),  i2c(0,sda), uart(0,tx)]).
pin(22, [gp(17), spi(0,csn), i2c(0,scl), uart(0,rx)]).
pin(23, [gnd]).
pin(24, [gp(18), spi(0,sck), i2c(1,sda)]).
pin(25, [gp(19), spi(0,tx),  i2c(1,scl)]).
pin(26, [gp(20), spi(0,rx),  i2c(0,sda), uart(1,tx)]).
pin(27, [gp(21), spi(0,csn), i2c(0,scl), uart(1,rx)]).
pin(28, [gnd]).
pin(29, [gp(22), spi(0,sck), i2c(1,sda)]).
pin(30, [run]).
pin(31, [gp(26), adc(0)]).
pin(32, [gp(27), adc(1)]).
pin(33, [gnd, agnd]).
pin(34, [gp(28), adc(2)]).
pin(35, [adc_vref]).
pin(36, [v3v3_out]).
pin(37, [v3v3_en]).
pin(38, [gnd]).
pin(39, [vsys]).
pin(40, [vbus]).

% -------- Convenience predicates --------

% true if Pin supplies Capability (exact term match).
pin_supports(Pin, Capability) :-
    pin(Pin, Caps),
    member(Capability, Caps).

% list all physical pins that match a Capability, e.g., pins_with(i2c(1,sda), Pins).
pins_with(Capability, Pins) :-
    findall(P, pin_supports(P, Capability), PList),
    sort(PList, Pins).

% collect pins that offer any role on a given SPI or I2C controller
% (e.g., pins_for_spi(0, Pins).)
pins_for_spi(Ctrl, Pins) :-
    findall(P, (pin(P, Caps), member(spi(Ctrl, _), Caps)), PList),
    sort(PList, Pins).

pins_for_i2c(Ctrl, Pins) :-
    findall(P, (pin(P, Caps), member(i2c(Ctrl, _), Caps)), PList),
    sort(PList, Pins).

% lightweight name lookup helpers
is_ground(Pin)   :- pin(Pin, Caps), member(gnd, Caps).
is_power(Pin)    :- memberchk(Pin, [35,36,37,39,40]).
is_analog(Pin)   :- pin(Pin, Caps), (member(adc(_), Caps); member(adc_vref, Caps); member(agnd, Caps)).

%%% end %%%
