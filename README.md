# cs262_marina_noah
Marina Elmore + Noah Zweben for CS 262

Some observations from Ex.1:
* In implementing our wireprotcol, it was amazing and disappointing to see how little control over the underlying bytes python afforded. C for the win!
* When we shifted from our own wire protocol -> gRPC, we realized the way we had been managing client login state on the server was less than ideal. We then improved our design to use a stateless server (similar to HTTP) where the gRPC server sets a login "cookie" for the client, which the client uses in subsequent requests. This was much cleaner.
* Implemeting helper functions as a reusable module was helpful for reducing code.