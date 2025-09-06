:- use_module(library(pengines)).

% Test client for the pengines server
test_local_pengine :-
    % Create a pengine connected to local server
    pengine_create([
        server('http://localhost:3030'),
        application(genealogist),
        ask(ancestor_descendant(mike, X))
    ]),
    pengine_event_loop(handle_result, []).

% Handle pengine results
handle_result(create(ID, Features)) :-
    format('Pengine created: ~w~n', [ID]),
    format('Features: ~w~n', [Features]).

handle_result(success(ID, Bindings, More)) :-
    format('Success - ID: ~w, Bindings: ~w, More: ~w~n', [ID, Bindings, More]),
    (   More == true 
    ->  pengine_next(ID, [])
    ;   pengine_destroy(ID)
    ).

handle_result(failure(ID)) :-
    format('Query failed for pengine: ~w~n', [ID]),
    pengine_destroy(ID).

handle_result(error(ID, Error)) :-
    format('Error in pengine ~w: ~w~n', [ID, Error]),
    pengine_destroy(ID).

handle_result(destroy(ID)) :-
    format('Pengine destroyed: ~w~n', [ID]).

% Test specific queries
test_genealogist_queries :-
    pengine_create([
        server('http://localhost:3030'),
        application(genealogist)
    ], ID),
    
    % Test multiple queries
    test_query(ID, 'Find all ancestors of sally', ancestor_descendant(X, sally)),
    test_query(ID, 'Find all descendants of mike', ancestor_descendant(mike, X)),
    test_query(ID, 'Find all siblings', siblings(X, Y)),
    test_query(ID, 'Find all parent-child relationships', parent_child(X, Y)),
    
    pengine_destroy(ID).

test_query(ID, Description, Query) :-
    format('~n--- ~w ---~n', [Description]),
    pengine_ask(ID, Query, []),
    collect_all_solutions(ID).

collect_all_solutions(ID) :-
    pengine_event(ID, Event),
    (   Event = success(_, Bindings, More)
    ->  format('  Result: ~w~n', [Bindings]),
        (   More == true
        ->  pengine_next(ID, []),
            collect_all_solutions(ID)
        ;   true
        )
    ;   Event = failure(_)
    ->  format('  No more solutions.~n')
    ;   Event = error(_, Error)
    ->  format('  Error: ~w~n', [Error])
    ).

% Main test runner
main :-
    format('Testing pengines server...~n'),
    test_genealogist_queries,
    format('~nTest completed.~n').
