# KuberCoins
Kubercoins is a training material based on [dockercoins](https://github.com/jpetazzo/container.training/tree/main/dockercoins).

# Dockercoins
Dockercoins is a simple application that emulate a bitcoin miner.<br>
Worker ask a random bit string to rng. Then worker ask to hasher to hash this string. Finaly, worker register in redis that a string have been hashed.<br>
Webui provide a web graphical interface that show the rate of processed strings.

![Architecture](docs/architecture.pdf)

# How to use
Skaffold is used to build/run.

The application can be run with:
```
skaffold run
```

A debug version with proforward directly opened is available with:
```
skaffold debug
```
