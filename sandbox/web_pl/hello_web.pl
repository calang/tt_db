:- use_module(library(http/thread_httpd)).
:- use_module(library(http/http_dispatch)).
:- use_module(library(http/http_error)).
:- use_module(library(http/html_write)).


%  Add another abstract base location like root
%  this one is files, and we map it to /f,
%  so /f/limburger can be described as files(limburger)
:- multifile http:location/3.
:- dynamic   http:location/3.

http:location(files, '/f', []).

% Declare a handler, binding an HTTP path to a predicate.
% Here our path is / (the root) and the goal we'll query will be
% say_hi. The third argument is for options
:- http_handler('/hi', say_hi, []).
:- http_handler(root(ho), ho(ho), []).

%  accessed via http://localhost:8000/f/bunny
:- http_handler(files(bunny), say_bunny , []).

:- http_handler('/direct', say_direct, []).
:- http_handler('/phtml', say_phtml, []).
:- http_handler('/dcg', say_dcg, []).
:- http_handler('/realdcg', say_realdcg, []).
:- http_handler('/reply', say_reply, []).

/* The implementation of /. The single argument provides the request
details, which we ignore for now. Our task is to write a CGI-Document:
a number of name: value -pair lines, followed by two newlines, followed
by the document content, The only obligatory header line is the
Content-type: <mime-type> header.
Printing can be done using any Prolog printing predicate, but the
format-family is the most useful. See format/2.   */
say_hi(Request) :-
    format('Content-type: text/plain~n~n'),
    format('Request: ~w~n~n', [Request]),
    format('Hello_world !~n').

ho(Word, Request) :-
    format('Content-type: text/plain~n~n'),
    format('Request: ~w~n~n', [Request]),
    format('Hello_world, ~w !~n', [Word]).

say_bunny(_Request) :-
        format('Content-type: text/plain~n~n'),
        format('bunnies are cute!~n').

say_direct(_Request) :-
        format('Content-type: text/html~n~n'),
        format('<html><head><title>Howdy</title></head><body><h2>A Simple Web Page</h2><p>With some text.</p></body></html>~n').

% Don’t do this in your own code.
% print_html is a behind the scenes predicate that converts
% a list of HTML chunks into a string containing HTML.
% Besides just concatenating, it inserts some rough formatting.
say_phtml(_Request) :-
        format('Content-type: text/html~n~n'),
	    print_html([
            '<html>',
            '<head>',
            '<title>',
            'Howdy',
            '</title>',
            '</head>',
            '<body>',
            '<h2>',
            'A Simple Web Page',
            '</h2>',
            '<p>',
            'With some textooo.',
            '</p>',
            '</body>',
            '</html>'
        ]).

say_dcg(_Request) :-
	phrase(
	  html([
			head(title('Howdy')),
		 	body([
				h1('A Simple Web Page'),
				p('With some text, from dcg.')
			])
		]),
        TokenizedHtml,
        []
    ),
	format('Content-type: text/html~n~n'),
	print_html(TokenizedHtml).

say_realdcg(_Request) :-
    phrase(
        my_nonterm,
        TokenizedHtml,
        []
    ),
    format('Content-type: text/html~n~n'),
	print_html(TokenizedHtml).

my_nonterm -->
    html([
        head([
            title('Howdy')
        ]),
        body([
            h1('A Simple Web Page'),
            p('With some text, from realdcg')
        ])
    ]).

say_reply(_Request) :-
    reply_html_page(
       [title('Howdy')],
       [    h1('A Simple Web Page'),
            p('With some text, from reply')
       ]
    ).

% The predicate server(+Port) starts the server. It simply creates a
% number of Prolog threads and then returns to the toplevel, so you can
% (re-)load code, debug, etc.
server(Port) :-
    http_server(http_dispatch, [port(Port)]).

:- server(8000).
