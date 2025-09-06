#!/usr/bin/env swipl

:- use_module(library(pengines)).
:- use_module(library(http/thread_httpd)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(http/http_files)).
:- use_module(library(http/http_cors)).

% Load the genealogist application
:- pengine_application(genealogist).
:- use_module(genealogist:'genealogist.pl').

% Configure CORS
:- set_setting(http:cors, [*]).

% HTTP route handlers
:- http_handler('/', home_page, []).
:- http_handler('/pengines', pengine_server, []).

% Serve static files from current directory
:- http_handler('/static/', 
               http_reply_from_files('.', []), 
               [prefix]).

% Home page with a simple interface
home_page(_Request) :-
    reply_html_page(
        title('Pengines Server'),
        [ h1('Pengines Server Running'),
          p('The pengines server is running on this host.'),
          h2('Available Applications:'),
          ul([
              li('genealogist - Family relationship queries')
          ]),
          h2('Example Queries:'),
          ul([
              li('ancestor_descendant(mike, X) - Find descendants of mike'),
              li('siblings(X, Y) - Find all sibling pairs'),
              li('parent_child(X, Y) - Find all parent-child relationships')
          ]),
          h2('Test Interface:'),
          p('You can test queries using a web interface or HTTP requests to /pengines'),
          script(src('https://unpkg.com/pengines@1.5.0/web/js/pengines.js'), []),
          script('
            var pengine = new Pengine({
                server: "http://localhost:3030/pengines",
                application: "genealogist",
                oncreate: function() {
                    console.log("Pengine created:", this.id);
                },
                onsuccess: function(result) {
                    console.log("Success:", result);
                },
                onfailure: function() {
                    console.log("Query failed");
                }
            });
          ')
        ]).

% Start the HTTP server
start_server :-
    Port = 3030,
    http_server(http_dispatch, [port(Port)]),
    format('~n=================================~n'),
    format('Pengines HTTP Server Started~n'),
    format('URL: http://localhost:~w~n', [Port]),
    format('Applications: genealogist~n'),
    format('=================================~n~n').

% Stop the server
stop_server :-
    http_stop_server(3030, []).

% Keep server running
run_server :-
    start_server,
    repeat,
    sleep(1),
    fail.

% Main entry point
main :-
    catch(run_server, Error, (
        format('Error: ~w~n', [Error]),
        halt(1)
    )).

% Command line initialization
:- initialization(main, main).
