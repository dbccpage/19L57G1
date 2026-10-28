# 01. Follow a walk

[Previous](00_points_and_connections.md) · [Path lab](README.md) · [Next](02_signed_endpoint_counts.md)

## Predict first

Using the five listed edges, compare A → B → C with A → B → D.
Does every proposed step have a connection?

## Check each consecutive pair

A **walk** is a sequence of listed vertices in which each consecutive
pair is joined by an edge. A → B → C is a walk because AB and BC exist.
A → B → D is not: BD is absent. The written arrow proposes a step;
it does not admit its missing connection.

These edges may be traversed either way in this teaching model. A → C
and C → A use the same undirected edge, with opposite traversal directions.

The **length** of a walk here is its number of steps. A → B → C has
length two. This counts edges traversed, not a distance in metres or
a duration. A single listed vertex, A, is a walk of length zero.

## Returning and repeating

A **closed walk** starts and ends at the same vertex. A → B → C → A
is closed. A → B → A is also closed: it goes out and directly back.
Returning does not require three different vertices.
Our definition also calls the zero-step walk at A closed.

We use **path** for a walk with no repeated vertices. Thus A → B → C
is a path; the closed examples above are called closed walks here.
Other texts may use these words differently, so keep this convention visible.

## Your turn

Remove AC. Is A → B → C still a walk? Is A → B → C → A still one?
State the missing consecutive pair in the failed example.

AuthorityEffect: None. These walks are supplied teaching records on the
edge list; they are not histories of passage events or physical trajectories.
