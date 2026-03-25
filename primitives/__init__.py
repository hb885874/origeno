"""
primitives/__init__.py
========================
Imports all primitive modules so their @register() decorators fire
and they are added to the registry.

HOW TO ADD A NEW PRIMITIVE
---------------------------
1. Create primitives/<n>.py
2. Inherit from BasePrimitive, implement render()
3. Decorate the class with @register("<n>")
4. Add the import line below — that's all.

The import order here does not matter. The registry stores by name.

NOTE ON IMPORT STYLE
--------------------
These are relative imports (leading dot). This ensures they resolve
correctly regardless of how Python's sys.path is configured — on
Windows, Linux, and Mac. Do NOT change these to absolute imports
like `from primitives import stamp` — that style fails on Windows
when sys.path does not include the project root.
"""

from . import stamp
from . import counter
from . import chart
from . import character
from . import map
from . import prop
from . import flood
from . import electricity
from . import glitch

# Future primitives: add import here
# from . import timeline
# from . import race_track
# from . import network_graph
# from . import text_reveal
