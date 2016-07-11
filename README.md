# nodenator

*The project is under development. This is just a prove of concept*

A simple tool to generate, visualize and check dependencies in graphs with directed edges. The representation is similar to Petri nets except there are no transitions and arcs with condition directly end in places.

## The Idea

A system is made of two primitives:
  * nodes
  * directed edges
  
A node can produce or accept a message. Each node is uniquely identified by its name which has to be unique in defined system. You can define input and output conditions for each node. These conditions are made of predicates that specify how should a message look like - e.g. if it should be a dictionary/list/string/..., what values should be present in case of dictionary etc.

An edge is directed edge and connects two nodes. Each edge has its name and predicate which defines whether a message will be sent to destination node (predicate is True) or not (predicate is False). If the predicate is True, the destination node should accept the message and process it.

## Installation

*Currently not available, see Quick Examples section*

You can use pip in order to install this tool:

```
$ pip install nodenator
```

## Usage

Currently there are supported following actions:

  * generate a graph representation of the whole system (see ```--graph```)
  * generate Python source code based on definitions (see ```--dump```)
  * for a given message validate if the message corresponds to a node input restrictions (see ```--check-input```)
  * for a given message validate if the message corresponds to a node output restrictions (see ```--check-output```)
  * for a given message check which nodes will accept the message based on edge condition (see ```--evaluate```)
  * basic system checks; more advanced checks - e.g. SMT solver are not supported now (see ```--check```)

See ```nodenator-cli --help``` for more info.

## Representation

The system is represented in a single YAML file which is divided into two sections - "nodes" and "edges". An example of a ```defs.yaml``` can be found in ```nodenator/examples/```.

### Predicates

The implementation of nodenator comes with predefined predicates, which are available under ```nodenator/predicates/``` directory. You can define your own predicates in a config file (see Configuration File section).

Each predicate tends to avoid exception rising - if anything goes wrong (e.g. accessing non-existing key in a dict), there is returned False instead.

There are available two predicate types:
  * build in predicates
  * leaf predicates
  
A build in predicate now corresponds to logical operators - ```and```, ```or```, ```not```.
  * ```and``` - n-ary logical operator - you can define a list of predicates. In order to return True, all child predicates has to return True. Short circuit evaluation is applied.
  * ```or``` - n-ary logical operator - you can define a list of predicates. In order to return True, at least one of child predicates has to return True. Short circuit evaluation is applied.
  * ```not``` - unary logical operator - you can define one child predicate. In order to return True, the child predicate has to return False.

Predicates can be arbitrarily nested and compounded with respect to arity, naming and passed arguments.
  
An example of building conditions can be seen in the following listing. More examples can be found in ````nodenator/examples/```` directory.

```yaml
and:
  - name: "fieldEqual"
    args:
      key:
        - "key1"
        - "key2"
        - "key3"
      value: "foo"
  - name: "fieldNotEqual"
    args:
      key: "bar"
      value: "baz"
  - or:
    - not:
        name: "fieldExist"
        args:
          key: "test"
    - name: "fieldExist"
      args:
        key: "test"
```

For a given message, the example corresponds to the following generated Python code. Note nested keys representation in YAML file - a list of keys.

```python
fieldEqual(message, key=['key1', 'key2', 'key3'], value='foo') and fieldNotEqual(message, key='bar', value='baz') and ((not fieldExist(message, key='test')) or fieldExist(message, key='test2'))
```

Which in fact corresponds to (checks removed intentionally):
```python
message['key1']['key2']['key3'] == 'foo' and message['bar'] != 'baz' and (('test' not in message) or 'test2' in message)
```

### Nodes

The following example demonstrates a node representation:

```yaml
  nodes:
    - name: "Task1"
      desc: "This is a simple description of node named Task1"
      srcpath: "foo/bar/baz/task1.py"
      dump-node-comparison:
        type: 'instance'
        import: 'modules.tasks.task1'
      input:
          name: "alwaysTrue"
      output:
          name: "alwaysTrue"
          
    - name: "Task2"
      desc: "Yet another node definition"
      srcpath: "foo/bar/baz/task2.py"
      dump-node-comparison:
        type: 'name'
      input:
          name: "alwaysTrue"
      output:
          name: "alwaysTrue"
```

Each node definition has to define following values:
  * name - a task name, has to be unique in the defined system (no two nodes share the same name in the definition file)
  * input - input restrictions - defined as a predicate tree - see Predicates section for more info
  * output - output restrictions - defined as a predicate tree - see Predicates section for more info

The following values are optional:
  * desc - node description
  * srcpath - defines path to sources when performing ```--dump``` (where dump will be stored for task)
  * dump-node-comparison - defines how should be node recognized when a message is sent (if omitted, name is used), possible values:
    * instance - a node is recognized by instance - calling ```isinstance()```, there has to be specified import where node is defined
      ```python
      from modules.tasks.task1 import Task1
      # ...
      if isinstance(node_from, Task1):
         # ...
      # ...
      ```
    * name - a node is recognized by a name - a simple string comparison with node name (```node_from == "Task2"```)
 
See ```nodenator/examples/``` directory for more examples.

### Edges

The following example demonstrates definition of edges:

```yaml
edges:
  - name: "Edge1"
    desc: "Edge1 description"
    from: "Task1"
    to: "Task2"
    condition:
      and:
      - name: "fieldEqual"
        args:
          key: "type"
          value: "foo"
      - name: "fieldNotEqual"
        args:
          key: "bar"
          value: "baz"
          
  - name: "Edge2"
    desc: "The second edge in our system"
    from: "Task2"
    to: "Task1"
    condition:
      not:
        name: "fieldNotEqual"
        args:
          key: "type"
          value: "foobar"
```

Each edge definition has to provide following values:
  * name - edge name
  * from - name of the node where the edge starts (definition of such node has to exist in ```nodes``` section)
  * to - name of the node where the edge ends (definition of such node has to exist in ```nodes``` section)
  * condition - definition of a predicate tree - see Predicate section for more info

The following values are optional:
  * desc - edge description

## Configuration File

You can adjust graph colors, style, fonts and much more in a config file in section ```style```. See ```nodenator/examples/``` file for more examples.

You can also define your own predicates made in your own module. The only thing you need to adopt is ```predicate-dir``` in the config file which should hold path to your predicate module (don't forget to place ```__init__.py``` to module dir). Each predicate has to be defined in a single file which name should be same as predicate name. Each predicate has to define the very first argument - a message. Based on predicate semantics, predicate can define its arguments, which will be passed to predicate as kwargs.

## Checks

Currently, there are supported only very easy checks. Since the system and its definition corresponds to satisfiability modulo theories, there can be implemented SMT solver in order to make more precise checks.

Keep in mind that all checks (```--check-input```, ```--check-output```, ```--check```) are simulating short circuit evaluation so checks correspond to generated Python code.

## Quick Examples

Clone the repo:
```
$ git clone https://github.com/fridex/nodenator && cd nodenator
```

Install requirements:
```
$ pip install -r requirements.txt
```

Or use virtualenv:
```
$ make venv && source venv/bin/activate
```

Some examples to demonstrate nodenator:

```
$ ./nodenator-cli --definition nodenator/examples/defs/defs.1.yaml --config nodenator/examples/config/config.1.yaml --graph graph.1.config.svg
$ xdg-open graph.1.config.svg
```

```
$ ./nodenator-cli --definition nodenator/examples/defs/defs.1.yaml --graph graph.1.no-config.svg
$ xdg-open graph.1.no-config.svg
```

```
$ mkdir tmp && ./nodenator-cli --definition nodenator/examples/defs/defs.1.yaml --check
```

```
$ mkdir tmp && ./nodenator-cli --definition nodenator/examples/defs/defs.1.yaml --dump
```

```
$ mkdir tmp && ./nodenator-cli --definition nodenator/examples/defs/defs.1.yaml --evaluate nodenator/examples/message/message.1.json
```

```
$ mkdir tmp && ./nodenator-cli --definition nodenator/examples/defs/defs.1.yaml --check-input nodenator/examples/message/message.1.json
```

```
$ mkdir tmp && ./nodenator-cli --definition nodenator/examples/defs/defs.1.yaml --check-output nodenator/examples/message/message.1.json
```

## Notes

Use on your own risk!
