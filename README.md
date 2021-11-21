# TTIC
Disease spread simulation with cellular automaton.

## How to use?
Run application without preventions:
```sh
python3 -m simulaton
```

To run with preventions just run the same command with `--isolation`, `--mask` and/or `--vaccine` params.
```sh
python3 -m simulaton --isolation --mask --vaccine
```

In short:
```sh
python3 -m simulaton -i -m -v
```


## How to configure?
In simulation.config file, there are some variables that refers to disease/prevention probabilities.

Some examples: `PROB_INFECTION` indicates the disease infection probability.

## Outputs
### GIF with disease spread simulation
<p float="left">
  <img src="./documentations/simulation/wp/movie.gif" width="50%"/><img src="./documentations/simulation/ap/movie.gif" width="50%"/>
</p>

### Graphs
<p float="left">
  <img src="./documentations/simulation/wp/infected.png" width="50%"/><img src="./documentations/simulation/ap/infected.png" width="50%"/>
  <img src="./documentations/simulation/wp/infected_per_day.png" width="50%"/><img src="./documentations/simulation/ap/infected_per_day.png" width="50%"/>
  <img src="./documentations/simulation/wp/dead.png" width="50%"/><img src="./documentations/simulation/ap/dead.png" width="50%"/>
  <img src="./documentations/simulation/wp/dead_per_day.png" width="50%"/><img src="./documentations/simulation/ap/dead_per_day.png" width="50%"/>
  <img src="./documentations/simulation/ap/dead_by_age.png" width="50%"/><img src="./documentations/simulation/wp/dead_by_age.png" width="50%"/>
</p>

## Other works
This project is an evolution of Roger Vieira's solution in his article ["Modelo de propagação de doenças epidêmicas baseado em autômatos celular"](http://repositorio.unesc.net/handle/1/8862)
