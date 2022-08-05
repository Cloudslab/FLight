# Federated Learning as tasks

## List of Contents

- APIs and Usage
- Router
- Data warehouse
- Define new federated learning relationship
- Add a new underlying machine learning model
- Define new federated strategy
- Federation triggers, asynchronous, synchronous
- Add authorization
- Walk through Example

## APIs and Usage
All machine learning models used by federated framework are expected to implement functions defined in [base_model](./federaed_learning_model/base_model.py). This part will describe expected usage of each function.
```python
from federated_learning_model.base_model import base_model

class my_model(base_model):
    #class definition ...
    pass
```

### 1 `my_model.step(train_data)`
- Step will train the model locally for one iteration.
- **train_data**: can be x, y pair ,data_loader or any format that suit `my_model::step` implementation
- each time `step` trained successfully, version of model should be incremented by 1. (`my_model.version += 1`)

### 2 `my_model.federate(fl_algo)`
- Federate will federate(aggregate) model weights it holds from other party (clients, server, peer).
- Whatever federation algorithm (aggregation algorithm) should be extended from this function.
- **fl_algo**: can be a callable object (average, median...) or any information suit `my_model::step` implementation
- A simple federated average algorithm can be implemented as: `my_model.federate(lambda li : sum(li) / len(li))`

### 3 `my_model.fetch_server(ptr)`
- **ptr**: (server_ip_address, server_model_id)
- fetch_server will request model weights from server side model identified by ptr: `(server_ip_address, server_model_id)`
- Whatever is returned from server is based on server's implementation. If remote model on server side agrees to send back the model, `server_model.push_client(ptr)` should be called.
- This function is not expected to be overridden, but incase more information needs to be added to ptr (so needs to override fetch_server) here are few tips:
  - use `fetch______c_s_` for router communication within function (explained at next section: Router)
  - redefine `fetch_____` -> `_c_s_` message handler (explained at next section: Router) on server side

### 4 `my_model.fetch_client(ptr)`
- **ptr**: (server_ip_address, server_model_id)
- fetch_client will request model weights from client side model identified by ptr: `(client_ip_address, client_model_id)`
- Whatever is returned from client is based on client's implementation. If remote model on client side agrees to send back the model, `client_model.push_server(ptr)` should be called.
- This function is not expected to be overridden, but incase more information needs to be added to ptr (so needs to override fetch_client) here are few tips:
  - use `fetch______s_c_` for router communication within function (explained at next section: Router)
  - redefine `fetch_____` -> `_s_c_` message handler (explained at next section: Router) on server side

### 5 `my_model.fetch_peer(ptr)`
- **ptr**: (peer_ip_address, peer_model_id)
- fetch_peer will request model weights from peer side model identified by ptr: `(peer_ip_address, peer_model_id)`
- Whatever is returned from peer is based on peer's implementation. If remote model on peer side agrees to send back the model, `peer_model.push_peer(ptr)` should be called.
- This function is not expected to be overridden, but incase more information needs to be added to ptr (so needs to override fetch_peer) here are few tips:
  - use `fetch______p_p_` for router communication within function (explained at next section: Router)
  - redefine `fetch_____` -> `_p_p_` message handler (explained at next section: Router) on peer side

### 6 `my_model.export()`
- export will port model to a serializable data structure, which can be loaded by model of same class
- For example for [linear_regression](federaed_learning_model/linear_regression.py). A model with weights, bias, learning rate, version, id can be exported as: `(w, b, lr, v, uuid)`
- For more complex, heavy model, it is better to export model as a file and return file path so other model can start a FTP transmission.

### 7 `my_model.load(data)`
- load will load parameter **data** into current model and update weights of current model
- **data**: can be any format as long as it suits `my_model::load` implementation
- Ideally, `my_model.load(my_model.export())` should return the same model
- For more complex, heavy model, if `my_model::export` return necessary information to start FTP connection, load should start a FTP connection, then fetch weights as file, and import the file.

### 8 `my_model.can_fetch(role, ptr)`
- can_fetch check whether a remote model with role: `role` and identified by `ptr`:`(fetch_model_ip_address, fetch_model_model_id)` is authorized to fetch the weights of this model.
- **role**: one of `client`, `server`, `peer` or any other that suit `my_model::can_fetch` implementation
- **ptr**: (fetch_model_ip_address, fetch_model_model_id) or any other that suit `my_model::can_fetch` implementation
- This is where access control can be extended from. For example:
  - Encrypt `ptr` with fetch side private key can allow public/private key check.
  - Basic implementation can check if `ptr` is with in model's collection of clients/servers/peers base on role.

### 9 `my_model.can_load(role, ptr, version)`
- can_load check whether weights from a remote model with role: `role` and identified by `ptr`: `(push_model_ip_address, push_model_model_id)` is authorized to override local model weights by weights they provide.
- **role**: one of `client`, `server`, `peer` or any other that suit `my_model::can_load` implementation
- **ptr**: (push_model_ip_address, push_model_model_id) or any other that suit `my_model::can_load` implementation
- This is where access control can be extended from. For example:
  - Encrypt `ptr` with push side private key can allow public/private key check.
  - Basic implementation can check if `ptr` is with in model's collection of servers/peers base on role. (It is not common that clients overrides server model weights)

### 10 `my_model.add_server(ptr)`
- **ptr**: (server_ip_address, server_model_id)
- add_server will request connection with a model from server side identified by ptr: `(server_ip_address, server_model_id)`.
  - If `server_model_id` is None, it means request server to create a model and allow that model to be server model of this model.
  - If `server_model_id` is not None, it means request server model identified by `(server_ip_address, server_model_id)` to be the server model of this model.
- Whatever is returned from server is based on server's implementation. If server agrees to give back a model to be the server model of this one, id of the server model will be returned.
- This function is not expected to be overridden, but incase more information needs to be added to ptr (so needs to override add_server) here are few tips:
  - use `add_server?????` for router communication within function, five char code `?????` should be replaced with model unique code (explained at next section: Router)
  - redefine `add_server` -> `?????` message handler (explained at next section: Router) on server side

### 11 `my_model.add_client(ptr)`
- **ptr**: (client_ip_address, client_model_id)
- add_client will request connection with a model from client side identified by ptr: `(client_ip_address, client_model_id)`.
  - If `client_model_id` is None, it means request client to create a model and allow that model to be client model of this model.
  - If `client_model_id` is not None, it means request client model identified by `(client_ip_address, client_model_id)` to be the client model of this model.
- Whatever is returned from client is based on client's implementation. If client agrees to give back a model to be the client model of this one, id of the client model will be returned.
- This function is not expected to be overridden, but incase more information needs to be added to ptr (so needs to override add_client) here are few tips:
  - use `add_client?????` for router communication within function, five char code `?????` should be replaced with model unique code (explained at next section: Router)
  - redefine `add_client` -> `?????` message handler (explained at next section: Router) on client side

### 12 `my_model.add_peer(ptr)`
- **ptr**: (peer_ip_address, peer_model_id)
- add_peer will request connection with a model from peer side identified by ptr: `(peer_ip_address, peer_model_id)`.
  - If `peer_model_id` is None, it means request peer to create a model and allow that model to be peer model of this model.
  - If `peer_model_id` is not None, it means request peer model identified by `(peer_ip_address, peer_model_id)` to be the peer model of this model.
- Whatever is returned from peer is based on peer's implementation. If peer agrees to give back a model to be the peer model of this one, id of the peer model will be returned.
- This function is not expected to be overridden, but incase more information needs to be added to ptr (so needs to override add_peer) here are few tips:
  - use `add_peer__?????` for router communication within function, five char code `?????` should be replaced with model unique code (explained at next section: Router)
  - redefine `add_peer__` -> `?????` message handler (explained at next section: Router) on peer side

### 13 `my_model.can_federate()`
- can_federate check whether the model is ready for next round aggregation i.e. `my_model.federate()`.
- This is where different federated logic can be extended (both synchronous and asynchronous)
- Whenever model weights from a client/peer is pushed to this model, `my_model::can_federate` should be called to see if another round of federation should start.
- For ideas about different can_federate() implementation check section: Federation triggers, asynchronous, synchronous

### 14 `my_model.ack_ready(role, ptr, flg)`
- ack_ready informs remote models that have a client-server/server-client/peer-peer relationship with this one that this model get updated (finish local train/ finish aggregation ...) So remote side can decide to fetch the updated version or not and avoid unnecessary information (model weights) transmission.
- **role**: one of `client`, `server`, `peer` or any other that suit `my_model::ack_ready` implementation. Role indicate this model's role in the relationship with model identified by `ptr`.
- **ptr**: `(ack_ready_destination_ip, ack_ready_destination_model_id)` or any other that suit `my_model::ack_ready` implementation
- **flg**: flag indicate what the model is ready for:
  - `_fl_r`: ready to take a train signal from server side
  - `_fl_t`: local train finished, weights ready to be fetched
  - `_fl_f`: local federation finished, weights ready to be fetched

### 15 `my_model.ask_next(itr_nums)`
- **itr_nums** iteration that remote model should train. This is just an indicative number, actual training iterations depend on remote model implementation.
- ask_next should request all remote model (clients or clients+peers depend on implementation).
- This function is expected to be overridden, if wish to only ask part of remote model to perform local training
  - use `ask_next__?????` for router communication within function, five char code `?????` should be replaced with model unique code (explained at next section: Router)
  - redefine `ask_next__` -> `?????` message handler (explained at next section: Router) on peer side

### 16 `my_model.can_next(ptr)`
- can_next check whether the remote_model identified by `ptr`: `(ask_next_model_ip_address, ask_next_model_id)` is authorized to ask this model to perform training.
- Basic implementation would be checking whether `ptr` within trusted server list of this model or not.

### 17 `my_model.push_server(ptr)`
- **ptr**: (server_ip_address, server_model_id)
- push_server will push local model weights to server side model identified by ptr: `(server_ip_address, server_model_id)`
- Although the API is exposed and clients can push data to server whenever they wish, it is recommended to push weights only after `fetch______s_c_` tag received from a server.
- Overriding this function needs to configure few things:
  - use `push_______c_s_` for router communication within function (explained at next section: Router)
  - redefine `push______` -> `_c_s_` message handler (explained at next section: Router) on server side
  - append `my_model.export()` to data to be transmitted.

### 18 `my_model.push_client(ptr)`
- **ptr**: (client_ip_address, client_model_id)
- push_client will push local model weights to client side model identified by ptr: `(client_ip_address, client_model_id)`
- Although the API is exposed and servers can push data to clients whenever they wish, it is recommended to push weights only after `fetch______c_s_` tag received from a client.
- Overriding this function needs to configure few things:
  - use `push_______s_c_` for router communication within function (explained at next section: Router)
  - redefine `push______` -> `_s_c_` message handler (explained at next section: Router) on client side
  - append `my_model.export()` to data to be transmitted.

### 18 `my_model.push_peer(ptr)`
- **ptr**: (peer_ip_address, peer_model_id)
- push_peer will push local model weights to peer side model identified by ptr: `(peer_ip_address, peer_model_id)`
- Although the API is exposed and peers can push data to clients whenever they wish, it is recommended to push weights only after `fetch______p_p_` tag received from a peer.
- Overriding this function needs to configure few things:
  - use `push_______p_p_` for router communication within function (explained at next section: Router)
  - redefine `push______` -> `_p_p_` message handler (explained at next section: Router) on peer side
  - append `my_model.export()` to data to be transmitted.

----

## Router
When models needs to interact with remote models, messages should be sent via socket which is encapsulated by [router](communicate/router.py). \
Use `router.send(addr, flg, data)`
- **addr**: destination ip and port
- **flg**: consist of 15 character. 
  - First 10 character indicate behavior, and receiver will find handler based on that 10 character. 
  - Last 5 character provides supplementary information for the corresponding message handler to digest
  - Each `flg` should have corresponding message handler defined
- `add_client`: add client flag
  - `_lr__`: linear regression model
- `ack_ready_`: acknowledge model finish some task flag
  - `_fl_r`: ready to participate in next round train, waiting remote model to ask to start train
  - `_fl_t`: train finished and can be fetched by remote model (sever and peer especially), waiting for fetch call
  - `_fl_f`: federation(aggregation) finished and can be fetched by remote model (peer and client especially), waiting for fetch call
- `ask_next__`: ask remote model to perform a local training
  - `_fl__`: linear regression model
- `fetch_____`: fetch the weights of a remote model
  - `_s_c_`: server fetch client
  - `_c_s_`: client fetch server
  - `_p_p_`: peer fetch peer
- `push______`: push model weights to a remote model
  - `_c_s_`: client push server
  - `_s_c_`: server push client
- Note that handler is not automatically bounded to flag mentioned above, use `router::add_handler(flag, handler)` to match key(10 character) to a handler (callable object that can digest message) E.g.:
```python
from handler.add_client_handler import add_client_handler
from handler.ack_ready_handler import ack_ready_handler
from handler.ask_next_handler import ack_next_handler
from handler.fetch_handler import fetch_handler
from handler.push_handler import push_handler
from .federated_learning.communicate.router import router_factory
# router_factory can initiate a router based on address (start listening on port) and return router based on addr
... addr: (ip, port) ...
router_factory.get_router(addr)
router_factory.get_router(addr).add_handler("add_client", add_client_handler())
router_factory.get_router(addr).add_handler("ack_ready_", ack_ready_handler())
router_factory.get_router(addr).add_handler("ask_next__", ack_next_handler())
router_factory.get_router(addr).add_handler("fetch_____", fetch_handler())
router_factory.get_router(addr).add_handler("push______", push_handler())
```
- Additional handler/flag pair can be added and defined just as example above

----

## [Data warehouse](federaed_learning_model/datawarehouse.py)

Since when model interact with each other, they will need to refer to remote model. It is done by\
`ptr`: `(remote_mode_addr, model_id)` and remote_model_addr is `(remote_model_ip, port)` which have router listening there.
If there is a router listening at that point and flag is recognized which means a handler will be responsible to handle, 
handler will try to retrieve the model based on `model_id` from data warehouse which is an uuid.

**1. data warehouse is a singleton class**\
**2. data warehouse store models/data like a dictionary, identified by an id (uuid)**


### APIs
```python
from federaed_learning_model.datawarehouse import data_warehouse 
dw = data_warehouse()
```
- `dw.get(uuid)`: get a model based on uuid
- `dw.set(model, uuid=None)`: set a model with uuid, uuid will be a new generated one if uuid not given
- `dw.update(model, uuid)`: update a model based on uuid and new data
- `dw.set_default_data(scalar, length)`: set default x,y pair (for experiment purpose) to `range(length), range(length)*scalar`
- `dw.get_default_data()`: get the default data

----

## Define new federated learning relationship

In order to start a relationship with a remote model, we need to:
  - send a message with `add` flag
  - provide the model id (5 character code and `?????` is placeholder used)
  - provide uuid if refer to an existing model, or leave uud as None if wish remote create a model and return that one for requested relationship
```python
from .communicate.router import router_factory
router = router_factory.get_default_router()
```
- add client:`router.send(addr, "add_client?????", (model_data_to_initialize_model_remotely, uuid=None))`
- add server:`router.send(addr, "add_server?????", (model_data_to_initialize_model_remotely, uuid=None))`
- add peer:  `router.send(addr, "add_peer__?????", (model_data_to_initialize_model_remotely, uuid=None))`

`addr` refers to the address and make sure there is a router listening on that address and the router hold handler that can handle `add_client`, `add_server`, `add_peer__`

It is expected to encapsulate router sending message into functions `add_client`, `add_server`, `add_peer` from [base_model](federaed_learning_model/base_model.py).

----

## Add a new underlying machine learning model

Define new model within [federated learning model directory](federaed_learning_model) and inherit from [base model](federaed_learning_model/base_model.py). All abstract functions are explained in section API above. Current supported model includes:
- [simple linear regression](federaed_learning_model/linear_regression.py)
- more comming soon...

---
## Define new federated strategy
`federate(fl_algo)` is the function that should be overridden to achieve whatever federated algorithm. Some examples include:

- pure federated average:
```python
new_model::federate(fl_algo)
def federate(self, fl_algo):
    W, B = [], []
    for w_, b_, _, _, _ in self.models.values():
        W.append(w_)
        B.append(b_)
        self.ready_to_train_client -= 1

    self.w = fl_algo(W)
    self.b = fl_algo(B)
    self.version += 1
    self.models.clear()

new_model.federate(lambda li : sum(li) / len(li))
```

- federated average weighted by number of training data
```python
new_model::federate(fl_algo)
def federate(self, fl_algo):
    W, B, C = [], [], []
    count = 0
    for w_, b_, c_, _, _, _ in self.models.values():
        count += c_
        W.append(w_)
        B.append(b_)
        C.append(c_)
        self.ready_to_train_client -= 1
    W_weighted = [w * c/count for w,c in zip(W,C)]
    B_weighted = [b * c/count for b,c in zip(B,C)]
    self.w = fl_algo(W_weighted)
    self.b = fl_algo(B_weighted)
    self.version += 1
    self.models.clear()

new_model.federate(lambda li : sum(li))
```

- more coming soon...
----

## Federation triggers, asynchronous, synchronous
As described above `my_model.can_federate()` described above checks whether the model retained necessary information to start next round iteration. Different triggers can achieve different federated behavior:

- return true only when number of model weights equals to number of clients **(fully synchronous)**
- return true only when number of model achieve a proportion of clients **(asynchronous)**
- always return true **(asynchronous)**
- return true if current time stamp - last time a federation finish less than a threshold **(time based asynchronous)**
- more coming soon...
----


## Add authorization
Add check/key comparison/ version check etc. within:
- `can_fetch` to control if other can access (fetch) model weights of this model
- `can_load` to control if other can override current model with weights from them \
Pass any information required for authorization check by parameters

----
## Walk through Example
