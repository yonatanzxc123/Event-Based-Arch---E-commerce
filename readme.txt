Name : Yehonatan Segev
ID : 322335878

*)Producer URL : http://localhost:8000/create-order  - Creates a new order (HTTP POST request) and publish it to RabbitMQ
also the user needs a body with order ID and item count
EX:
{
  "orderId": "Order-123",
  "itemCount": 5
}

*)Consumer URL: http://localhost:8001/order-details?orderId=Order-123   (you can replace the Order-123 with the relevant order ID)
this returns the stored order +computed shipping cost (GET HTTP request)



*)bash start commands :
docker compose -f producer.yml up
docker compose -f consumer.yml up


*)Exchange type and why I used it : 

the exchange type I chose is - fanout

why ?  the fanout exchange broadcasts every message to all bound queues without filterling (and we were asked to make sure that "The event must be broadcast to all consumers")
this method ensures that every consumer recevies every order event and it models broadcast-style event propagation exactly like the event-driven architecture pattern that we were taught.


*)Rergarding the binding key - there is none, becuase fanout exahcnge ignores routing keys entirely.
therefore, the consumer binds its queue to the exchange without a binding key



*)The service that delclated the exchange  - Producer 
why ? The producer is the source of all events and it guarntees that the exchange exists before any message is even published!
this makes sure that no meesage will fail due to some missing exchange.

but the Queues are declared by - Consumer

consumers will define his own queses becuase consumers own ther message storage,
each one of them can have its own queue name and consumers can decide how to bind to the exchange 







