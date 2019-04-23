grandchild(C,A) :- child(C,B), child(B,A).
greatgrandparent(A,D) :- child(D,C), child(C,B), child(B,A).
    ancestor(X,Z) :- greatgrandparent(Z,X).
    ancestor(X,Z) :- grandchild(X,Z).
brother(X,Y) :- male(X), sibling(X,Y).
sister(X,Y) :- female(X), sibling(X,Y).
daughter(D,P) :- female(D), child(D,P).
son(S,P) :- male(S), child(S,P).
firstcousin(X,Y) :- auntoruncle(Z,X), parent(Z,Y).
brotherinlaw(X,Y) :- spouse(Y,Z), brother(X,Z).
    sisterinlaw(X,Y) :- spouse(Y,Z), sister(X,Z).
    aunt(A,C) :- female(a), auntoruncle(A,C).
    uncle(A,C) :- male(a), auntoruncle(A,C).
   
    child(william, diana).
    child(william, charles).
    child(harry, diana).
    child(harry, charles).
    child(peter, anne).
    child(peter, mark).
    child(zara, anne).
    child(zara, mark).
    child(beatrice, andrew).
    child(beatrice, sarah).
    child(eugenie, andrew).
    child(eugenie, sarah).
    child(louise, edward).
    child(louise, sophie).
    child(james, edward).
    child(james, sophie).
    child(diana, spencer).
    child(diana, kydd).
    child(charles, elizabeth).
    child(charles, philip).
    child(anne, elizabeth).
    child(anne, philip).
    child(andrew, elizabeth).
    child(andrew, philip).
    child(edward, elizabeth).
    child(edward, philip).
    child(elizabeth, george).
    child(elizabeth, mum).
    child(margaret, george).
    child(margaret, mum).

    male(william).
    male(harry).
    male(peter).
    male(james).
    male(charles).
    male(mark).
    male(andrew).
    male(edward).
    male(spencer).
    male(philip).
    male(george).
    
    female(zara).
    female(beatrice).
    female(eugenie).
    female(louise).
    female(diana).
    female(anne).
    female(sarah).
    female(sophie).
    female(kydd).
    female(elizabeth).
    female(margaret).
    female(mum).

    spouse(diana, charles).
    spouse(anne, mark).
    spouse(andrew, sarah).
    spouse(edward, sophie).
    spouse(spencer, kydd).
    spouse(elizabeth, philip).
    spouse(george,mum).
   
    sibling(william, harry).
    sibling(harry, william).
    sibling(peter, zara).
    sibling(zara, peter).
    sibling(beatrice, eugenie).
    sibling(eugenie, beatrice).
    sibling(louise, james).
    sibling(james, louise).
    sibling(charles,anne).
    sibling(anne,charles).
    sibling(charles,andrew).
    sibling(andrew,charles).
    sibling(charles, edward).
    sibling(edward,charles).
    sibling(anne, andrew).
    sibling(andrew,anne).
    sibling(anne, edward).
    sibling(edward, anne).
    sibling(andrew, edward).
    sibling(edward, andrew).
    sibling(elizabeth, margaret).
    sibling(margaret, elizabeth).
 
