% experiments using sqlite package

/*
to install the package:
?- pack_install(prosqlite).

to verify installation:
?- pack_list_installed.
*/

:- use_module(library(prosqlite)).

% create empty the sqlite DB file, if needed
:- shell('> uniprot.db.sqlite').

:- sqlite_connect('uniprot.db.sqlite', uniprot).

:- sqlite_query('CREATE TABLE movie(title, year, score)', Row).

:- sqlite_query('\c
    INSERT INTO movie VALUES \c
        ("Monty Python and the Holy Grail", 1975, 8.2), \c
        ("And Now for Something Completely Different", 1971, 7.5) \c
    ',
        Row
).

q(Row) :- sqlite_query('select * from movie', Row).

% end of the script
end :- sqlite_disconnect(uniprot).


