#!/usr/bin/env swipl

% Simple and robust pengines server
% Usage: swipl -s simple_server.pl

:- use_module(library(pengines)).

% Load your genealogist application
:- pengine_application(genealogist).
:- use_module(genealogist:'genealogist.pl').

% Start the pengines server
start_server :-
    Port = 3030,
    pengine_server([
        port(Port),
        allow(127.0.0.1),  % Allow local connections only
        allow('*')         % Allow all IPs (comment this line for localhost only)
    ]),
    format('~n╔══════════════════════════════════════╗~n'),
    format('║        Pengines Server Started       ║~n'),
    format('║                                      ║~n'),
    format('║  Port: ~w                       ║~n', [Port]),
    format('║  Applications: genealogist           ║~n'),
    format('║                                      ║~n'),
    format('║  Test with:                          ║~n'),
    format('║  swipl -s test_client.pl -g main    ║~n'),
    format('║                                      ║~n'),
    format('║  Press Ctrl+C to stop                ║~n'),
    format('╚══════════════════════════════════════╝~n~n').

% Initialize and start server
:- initialization(start_server, main).
