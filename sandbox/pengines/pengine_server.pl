#!/usr/bin/env swipl

:- use_module(library(pengines)).
:- use_module(library(http/thread_httpd)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(http/http_cors)).

% Configure CORS for cross-origin requests
:- set_setting(http:cors, [*]).

% Define the server port
server_port(3030).

% Start the pengines server
start_server :-
    server_port(Port),
    pengine_server([
        port(Port),
        allow(127.0.0.1),  % Allow local connections
        allow('*')         % Allow all connections (use with caution)
    ]),
    format('Pengines server started on http://localhost:~w~n', [Port]).

% Stop the server
stop_server :-
    server_port(Port),
    http_stop_server(Port, []).

% Application entry point
main :-
    start_server,
    % Keep the server running
    repeat,
    sleep(1),
    fail.

% If running from command line
:- initialization(main, main).
