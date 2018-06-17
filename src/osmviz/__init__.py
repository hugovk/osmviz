# osmviz module #
# Copyright (c) 2010 Colin Bick, Robert Damphousse

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import sys

if sys.version_info < (3,):
    raise ImportError(
        """You are running OSMViz 3.0 on Python 2.

OSMViz 3.0 and above are no longer compatible with Python 2, and you still
ended up with this version installed. That's unfortunate; sorry about that.
It should not have happened. Make sure you have pip >= 9.0 to avoid this kind
of issue, as well as setuptools >= 24.2:

 $ pip install pip setuptools --upgrade

Your choices:

- Upgrade to Python 3.

- Install an older version of OSMViz:

 $ pip install 'osmviz<3.0'

It would be great if you can figure out how this version ended up being
installed, and try to check how to prevent it for future users.

See the following for more up-to-date information:

https://github.com/hugovk/osmviz/issues/18
""")
