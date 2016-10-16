python_library (
  name="servertraklib",
  sources= [
    "servertraker.py",
  ],
  dependencies = [
    "src/python/common",
    "src/python/host_discovery",
    "src/python/format",
    "src/python/proxies",
  ]
)

python_binary (
  name="servertrak",
  source = "servertrak.py",
  dependencies = [
    ":servertraklib",
    "3rdparty/python:exrex",
    "3rdparty/python:PyYAML",
    "3rdparty/python:click",
  ],
  resources = [
    "servers.yaml",
  ],
)
