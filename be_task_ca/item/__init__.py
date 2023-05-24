"""
NOTE:

The user and item modules are heavily dependent on each other, and there's no clear separation between them. 
For example, the add_item_to_cart function in the user module directly imports and uses the item module. 
This makes it difficult to separate the system into different microservices, 
as both modules would need to be significantly refactored to operate independently

In general, to make the dependencies between modules more explicit, 
we should clearly define interfaces between different layers 
For example, between services and repositories. 
The Dependency Inversion Principle should be followed, meaning that both high-level modules and low-level modules should depend on abstractions.
"""
