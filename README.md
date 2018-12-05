# grpc-pattern as microservice

Pattern is a great framework for Natural Language Processing for Python.

gRPC is the new efficient and effective transfer protocol powered by Google to create microservice.

grpc-pattern brings Pattern as microservice through Docker container.

# Run it

To use it, just execute:
```
docker run -p 50051:50051 digitalilusion/grpc-pattern
```

## Try out

You can use `grpcc` tool to try the microservice

```
grpcc -i -p api.proto -a localhost:50051
```
A REPL interface with node is launched. Let's try the parser. `language = 1` for English, `language = 2` for Spanish, ... (see `api.proto` for full language options)

```
client.parse({'language': 1, 'text': 'The cat is over the roof. And the dog?'}, pr)
```

And this is the result:
