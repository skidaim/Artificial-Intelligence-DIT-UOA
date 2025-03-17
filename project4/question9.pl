man(john).
man(peter).
man(timos).

woman(helen).
woman(katerina).

beautiful(helen).
beautiful(john).
muscular(peter).
muscular(timos).
rich(peter).
rich(john).
kind(timos).

happy(M) :- man(M), rich(M).
happy(M) :- man(M), likes(M, W), likes(W, M).
happy(W) :- woman(W), likes(W, M), likes(M, W).
likes(M, W) :- man(M), woman(W), beautiful(W).
likes(katerina, M) :- man(M), likes(M, katerina).
likes(helen, M) :- man(M), (kind(M), rich(M) ; muscular(M), beautiful(M)).
