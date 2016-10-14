python_library (
  name="servertraklib",
  sources= [
    "servertraker.py",
  ],
)

python_binary (
  name="servertrak",
  source = "servertrak.py",
  dependencies = [
    ":servertraklib",
    "common",
    "host_discovery",
    "format",
    "proxies",
    "3rdparty:exrex",
    "3rdparty:PyYAML",
    "3rdparty:click",
  ],
)
