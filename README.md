# dcos-template

This project provides a convenient way to generate configuration files and signal the programs that utilize these files based off the current state of your DCOS cluster.

`dcos-template` has three methods for gathering data:

- Polling Mesos' state.json on a regular interval
- Polling Marathon(s) for the current state of your applications
- Listening for events from Marathon(s)'s event bus

When a change in either of these data sources results in a change to the configuration files on disk, `dcos-template` can signal the configured daemon.

# Installation

# Usage

## Options

|   Option   | Description |
| ---------- | ----------- |
| `marathon` | The name of a marathon you'd like to gather data from.
| `template`* | The input template, output path and command to signal the owner process, separated by a colon (`:`). This option is additive and may be specified multiple times for multiple templates.
| `debug`    | Output the data that is being used to populate the templates.

## Command Line

1. Query `leader.mesos` every 30s for state.json
2. Query marathon (via. framework name) every 30s for app definitions.
3. Register to consume marathon events in real time.
4. Render the template on disk at `/tmp/tmpl.jinja` every time new data is received.
5. Update the data at `/tmp/result` every time the rendered template differs.
6. Every time the template is updated, run `signal`.

```shell
$ dcos-template \
    --template "/tmp/tmpl.jinja:/tmp/result:signal"
    --template "/tmp/other.jinja:/tmp/other:signal-other"
```

## Docker

```shell
$ cat env
DCOS_TEMPLATE="/tmp/tmpl.jinja:/tmp/result:signal"
DCOS_TEMPLATE="/tmp/other.jinja:/tmp/other:signal-other"
$ docker run -d --env-file=env -v /tmp:/tmp mesosphere/dcos-template
```
