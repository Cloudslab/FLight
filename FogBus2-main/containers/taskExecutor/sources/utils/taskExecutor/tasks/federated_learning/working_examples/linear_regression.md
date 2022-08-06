# Linear Regression Example

----
## Modification of FogBus2 Task Executor Handler
This example is running under FogBus2 environment.
- Remote Logger is running
- Master is running
- At least one Actor is running

Note that each task within task executor needs to be able to communicate with each other, so we need to pass in address 
of task executor as argument for child task executor. This can be done if we set attribute `tag` as `FederatedLearning` 
from user application, as shown in [line 52 of federated learning user implementation](../../../../../../../user/sources/utils/user/applications/federatedLearning.py). 
```python
...
    inputData = {
        ...
        "tag": "Federated Learning"
    }
...
```
And the [taskExecutor message handler](../../../messageHandler/handler.py) will pass the address of basic component to 
child task Executor. 

----
## Task Dependency
Tasks include:
- [federatedLearning0](../../federatedLearning0.py)
- [federatedLearning1](../../federatedLearning1.py)
- [federatedLearning2](../../federatedLearning2.py)
- [federatedServer](../../federatedServer.py)

With FogBus2 task dependency as: **Sensor -> federatedLearning0-2 -> actuator**.\
So address of taskExecutor of federatedLearning0-2 will be passed to federatedServer as parameters `inputData["child_addr"]`

----
## [`federatedLearning0`](../../federatedLearning0.py)
```python
... import ...
class federatedLearning0(BaseTask):
    def __init__(self):
        super().__init__(taskID=231, taskName='FederatedLearning0')

    def exec(self, inputData):
        router_factory.get_router((inputData["self_addr"][0], 54321))
        router_factory.get_router((inputData["self_addr"][0], 54321)).add_handler("add_client", add_client_handler())
        router_factory.get_router((inputData["self_addr"][0], 54321)).add_handler("ack_ready_", ack_ready_handler())
        router_factory.get_router((inputData["self_addr"][0], 54321)).add_handler("ask_next__", ack_next_handler())
        router_factory.get_router((inputData["self_addr"][0], 54321)).add_handler("fetch_____", fetch_handler())
        router_factory.get_router((inputData["self_addr"][0], 54321)).add_handler("push______", push_handler())
        data_warehouse.set_default_data(inputData["default_data_param"]["w1s"], inputData["default_data_param"]["w1l"])
```

- `router_factory.get_router((inputData["self_addr"][0], 54321))` will let a message handler start to listen on self address with port 54321
- `router_factory.get_router((inputData["self_addr"][0], 54321)).add_handler(<key>, handler_constructor())` will map <key> to the handler given, so whenever a socket message come in, if the first 10 char from socket match a key, rest message stream will be handled by corresponding message handler
- `data_warehouse.set_default_data(inputData["default_data_param"]["w1s"], inputData["default_data_param"]["w1l"])` will:
  - make default data X be: range(1, inputData["default_data_param"]["w1l"])
  - make default data Y be: range(1, inputData["default_data_param"]["w1l"]) * inputData["default_data_param"]["w1s"]
  - The X Y pair will be used for step function of model at this address.

After the code finish, message handler will start to listen for incoming message and handle what ever message with leading 10 character match any key for message handler.

Same logic works for federatedLearning1-2 (port of federatedLearning1-2 is 54322 and 54323)

----
## [`federatedServer`](../../federatedServer.py)
### 1 Full Code
```python
... import ...
class FederatedServer(BaseTask):
    def __init__(self):
        super().__init__(taskID=221, taskName='FederatedServer')
        self.worker_addr = []
        self.server_addr = None
    def exec(self, inputData):
        self.server_addr = inputData["self_addr"]
        self.worker_addr.append(inputData["child_addr"])

        if len(self.worker_addr) < 3:
            return

        router_factory.set_router((self.server_addr[0], 54324))
        router_factory.get_router((self.server_addr[0], 54324)).add_handler("add_client", add_client_handler())
        router_factory.get_router((self.server_addr[0], 54324)).add_handler("ack_ready_", ack_ready_handler())
        router_factory.get_router((self.server_addr[0], 54324)).add_handler("ask_next__", ack_next_handler())
        router_factory.get_router((self.server_addr[0], 54324)).add_handler("fetch_____", fetch_handler())
        router_factory.get_router((self.server_addr[0], 54324)).add_handler("push______", push_handler())

        lr = linear_regression(0, 0, 0.01)
        #for (addr, port) in self.worker_addr:
        lr.add_client((self.server_addr[0], 54321))
        lr.add_client((self.server_addr[0], 54322))
        lr.add_client((self.server_addr[0], 54323))


        while len(lr.client) < 3 and lr.ready_to_train_client < 3:
            time.sleep(1)

        for i in range(100):
            version = lr.version
            while len(lr.client) < 3 and lr.ready_to_train_client:
                time.sleep(0.01)
            lr.ask_next(10)
            while  lr.version == version:
                time.sleep(0.01)
        #
        inputData["Ress"] = {"final_model": lr.export(), "final_clients":lr.client, "twf": self.worker_addr}
        return inputData
```
### 2 Waiting for enough worker
Firstly, the code will check if it receives all address information of workers, and only proceed after that.
```python
        self.server_addr = inputData["self_addr"]
        self.worker_addr.append(inputData["child_addr"])
    
        if len(self.worker_addr) < 3:
            return
```
### 3 Set Up handler for incomming message
Then the server will set up message handler on its own address (so when clients send message to server, it will respond accordingly). This part is same as `federatedLearning0-2`
```python
        router_factory.set_router((self.server_addr[0], 54324))
        router_factory.get_router((self.server_addr[0], 54324)).add_handler("add_client", add_client_handler())
        router_factory.get_router((self.server_addr[0], 54324)).add_handler("ack_ready_", ack_ready_handler())
        router_factory.get_router((self.server_addr[0], 54324)).add_handler("ask_next__", ack_next_handler())
        router_factory.get_router((self.server_addr[0], 54324)).add_handler("fetch_____", fetch_handler())
        router_factory.get_router((self.server_addr[0], 54324)).add_handler("push______", push_handler())
```

### 4 Create Model Locally
After that: `lr = linear_regression(0, 0, 0.01)` create a linear regression model. In the constructor of 
[linear_regression](../federaed_learning_model/linear_regression.py), it will put itself into the data warehouse and 
generate a uuid for itself. So later remote model can refer to this `lr` by `(addr, the_uuid)`

### 5 Request Server Client Relationship
```python
        ...
        lr.add_client((self.server_addr[0], 54321))
        lr.add_client((self.server_addr[0], 54322))
        lr.add_client((self.server_addr[0], 54323))


        while len(lr.client) < 3 and lr.ready_to_train_client < 3:
            time.sleep(1)
        ...
```
`lr.add_client((addr, port))` will send a message with leading `add_client` tag to address (client_addr, 54321-54323). 
Since the model itself is linear_regression. `_lr__` will come strictly after.

The socket of server side will then send a message to address (client_addr, client_port) for each child. After message 
arrive at client side, say [`federatedLearning0`](../../federatedLearning0.py). [Message Router](../communicate/router.py) 
listening on that address will first handle the incoming message:
```python
    def _dispatch(self):
        self.socket.listen(5)
        while True:
            conn, _ = self.socket.accept()
            event = conn.recv(EVENT_STRING_LEN).decode("utf-8")
            model_type = conn.recv(MODEL_STRING_LEN).decode("utf-8")
            addr = ast.literal_eval(conn.recv(ADDRESS_STRING_LEN).decode("utf-8").rstrip())
            if hasattr(self, event) and callable(getattr(self, event)):
                Thread(target=getattr(self, event), args=(conn, addr, model_type, )).start()
```
Since `add_client` tag is added to each router of client (check section federatedLearning0) it will be recognized and 
following message will be handled by [add_client_handler()](../handler/add_client_handler.py) which will create a model 
(linear regession due to `_lr__`tag) and acknowledge client side is ready by `model.ack_ready("client", (addr, model.server[0][0]), "_fl_r")`

This will send a message with tag leading tag `ack_ready_` with following tag `_fl_r` which stands for client model is
ready for a train of federated learning. And when the message received at server side, the message will be handled by 
[Message Router](../communicate/router.py) on server side and since `ack_ready_` key is registered, 
[ack_ready_handler()](../handler/ack_ready_handler.py) will handle the rest of message.
```python
        ...  
        if (remote_id, addr) not in model.client:
              model.client.append((remote_id, addr))
        model.ready_to_train_client += 1
        ...
```
As shown above, it will add client model address and id to server model's client list and increment ready to train client of server model.

Same thing will happen between server and each client model. And the server model will wait until it have enough client (3 in this example) as shown in code below.
```python
        ...
        while len(lr.client) < 3 and lr.ready_to_train_client < 3:
            time.sleep(1)
        ...
```

----
### 6 Perform Training
```python
        ...
        for i in range(100):
            version = lr.version
            while len(lr.client) < 3 and lr.ready_to_train_client:
                time.sleep(0.01)
            lr.ask_next(10)
            while  lr.version == version:
                time.sleep(0.01)
        ...
```

The code above will perform 100 iteration of:
  - firstly client train
  - then server aggregate
#### 1) ask to train

The [`lr.ask_next(10)`](../federaed_learning_model/linear_regression.py):
```python
    def ask_next(self, itr_nums):
        router = router_factory.get_default_router()
        for (remote_id, addr) in self.client:
            router.send(addr, "ask_next___fl__", (self.uuid, remote_id, itr_nums))
```

will request all client model hold by `lr` to perform a train of 10 iterations locally by sending with tag
`ask_next__` followed by tag `_fl__`. However, at this point the server model `lr` will not send data to any client to 
avoid flooding client side.

#### 2) client do train
After [client router](../communicate/router.py) receive the message, `ask_next__` will forward the message to 
[ask_next_handler()](../handler/ask_next_handler.py)
```python
            if model and model.can_next((remote_id, addr)):
                for i in range(itr_nums):
                    model.step()
                model.ack_ready("client", (addr, remote_id), "_fl_t")
```
Which will validate if remote model is authorized to ask for train `model.can_next((remote_id, addr))` and if approved,
followed by `model.step()` to train the model. 

#### 3) client acknowledge server training down
After the client model finish training, it will send message back to 
server to indicate local train is done: `model.ack_ready("client", (addr, remote_id), "_fl_t")`. Do note that this ack_ready
use the flag `_fl_t` instead of `_fl_r` used for acknowledging ready to participate for next round training. 

#### 4) server fetch finished training clients' model weights
After the message arrive at server side, it will be forward to [ack_ready_handler()](../handler/ack_ready_handler.py) which will cause the 
server to fetch model weights from client if server recognize and wish to fetch weights from this client:
```python
            if role == "client" and (remote_id, addr) in model.client: # Can be more complex logic here
                model.fetch_client((addr, remote_id))
```

The `fetch_client((addr, remote_id))` will fetch weights of client model by sending message with tag `fetch_____` referring
to fetch behavior followed by `_s_c_` means server fetch client.

#### 5) client send back weights
After [client router](../communicate/router.py) receive the message, `fetch_____` will forward the message to 
[fetch_handler()](../handler/fetch_handler.py):
```python
            if model and model.can_fetch("server", (remote_id, addr)):
                model.push_server((addr, remote_id))
```
Which will validate if the server model is authorized to fetch data (`model.can_fetch("server", (remote_id, addr))`) and 
push back the data (`model.push_server((addr, remote_id))`) if server model is allowed to fetch client model. The 
`push_server` function will send message with tag `push______` followed by `_c_s_` indicating client push to server

#### 6) server save results from clients
After [server router](../communicate/router.py) receive the message, `push______` will forward the message to 
[push_handler()](../handler/push_handler.py) `_c_s_` client to server branch:
```python
      if model and model.can_load("client", (remote_id, addr), remote_model[-2]):
          model.versions[(remote_id, addr)] = remote_model[-2]
          model.models[(remote_id, addr)] = remote_model
          if model.can_federate():
              model.federate(lambda li : sum(li) / len(li))
```

Which will check against the version and see if the model is authorized to contribute to this server model: 
`model.can_load("client", (remote_id, addr), remote_model[-2])`. If agreed, model version and weights will be recorded and
server will check if it receive enough information to perform a federation `if model.can_federate()`. If federation 
criteria met (enough response, enough time, etc...). Then it will federate the model (aggregate results) followed by acknowledge
all clients that this model is ready (aggregation complete, model can fetch the new version):
```python
        for remote_id, addr in self.client:
            self.ack_ready("server", (addr, remote_id), "_fl_f")
```
Note for this time the flag is `_fl_f` indicating federation complete.

#### 7) client decide what to do next
After receiving the `ack_ready` flag with `_fl_f` from server. Client have few options.
1. do nothing (so server won't message this client's model anymore)
2. fetch data from server (`model.fetch_server((server_addr, server_remote_id))`)
3. tell server it is ready for next round training by sending `ack_ready` to server with flag `_fl_r` (see section 5 Request Server Client Relationship above)

Note point 2 and 3 do not contradict with each other.

In this example client will 
- fetch the data whenever server is ready, defined in [ack_ready_handler](../handler/ack_ready_handler.py) `model.fetch_server((addr, remote_id))`
- after server respond the server model weights, client will agree for next round iteration, defined in [push_handler](../handler/push_handler.py) `model.ack_ready("client", (addr, remote_id), "_fl_r")`

----
### 7 Server Start Next Round
Recall from code above, in this example server will wait for `ack_ready` from clients and continue next iteration of training.
```python
        while len(lr.client) < 3 and lr.ready_to_train_client < 3:
            time.sleep(1)

        for i in range(100):
            version = lr.version
            while len(lr.client) < 3 and lr.ready_to_train_client:
                time.sleep(0.01)
            lr.ask_next(10)
            while  lr.version == version:
                time.sleep(0.01)
```