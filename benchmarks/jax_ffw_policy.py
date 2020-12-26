import jax
import jax.numpy as jnp
from jax import jit, vmap


def init_ffw_policy(rng_input, sizes, population_size=1, scale=1e-2):
    """ Initialize the weights of all layers of a relu + linear layer """
    # Initialize a single layer with Gaussian weights - helper function
    def initialize_layer(population_size, m, n, key, scale):
        w_key, b_key = jax.random.split(key)
        return (scale * jax.random.normal(w_key, (population_size, n, m)),
                scale * jax.random.normal(b_key, (population_size, n,)))

    keys = jax.random.split(rng_input, len(sizes)+1)
    W1, b1 = initialize_layer(population_size, sizes[0], sizes[1],
                              keys[0], scale)
    W2, b2 = initialize_layer(population_size, sizes[1], sizes[2],
                              keys[1], scale)
    if population_size == 1:
        params = {"W1": W1.squeeze(), "b1": b1.squeeze(),
                  "W2": W2[0], "b2": b2[0]}
    else:
        params = {"W1": W1, "b1": b1, "W2": W2, "b2": b2}
    return params


def ffw_policy(params, obs):
    """ Compute forward pass and return action from deterministic policy. """
    def relu_layer(W, b, x):
        """ Simple ReLu layer for single sample. """
        return jnp.maximum(0, (jnp.dot(W, x) + b))
    # Simple single hidden layer MLP: Obs -> Hidden -> Action
    activations = relu_layer(params["W1"], params["b1"], obs)
    mean_policy = jnp.dot(params["W2"], activations) + params["b2"]
    return mean_policy
