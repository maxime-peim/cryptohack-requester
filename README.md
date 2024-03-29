# CryptoHack Requester Package

This is a simple python package to ease interaction with CryptoHack's challenges over Netcat and Web API.

## Installing / Getting started

The project has been tested with python >= 3.6.9. It may works with previous version, but nothing sure.

To install the package simply use `pip`:
```shell
python3 -m pip install CHRequester
```

## Features

CryptoHack has some challenges working with a Web API ([Block Cipher Mode challenges](https://cryptohack.org/challenges/aes/)), and some through server comunication. They generaly need automation so it is recommanded in the [FAQ](https://cryptohack.org/faq/) to use the [Requets](https://requests.readthedocs.io/en/master/) package for web challenges and [Pwntools](http://docs.pwntools.com/en/stable/) to communicate to a challenge on a server.
This package offer a more user-firendly and less time-consuming way to communicate with these challenges.

### Example of usage with the Web API:
```python
from ch_requester import URLRequester

if __name__ == "__main__":
    BASE_URL = "http://aes.cryptohack.org/oh_snap/"

    R = URLRequester(BASE_URL)
    # adding actions to the requester
    # first give the name of the action
    # then specify a tuple of inputs that are needed for this action
    # then specify a tuple of outputs that can given in return

    # 'error' can be specified as an output if the challenge returns
    # useful information through an error message
    # else, an Exception will be raised if an error is returned
    # and the user does not specify it as a desired output.
    # inputs must be in the order of the url, e.g.
    # http://aes.cryptohack.org/oh_snap/ciphertext/nonce/
    R.add_action('send_cmd', ('ciphertext', 'nonce'), ('msg', 'error'))

    # we can then execute an action, by giving its name as first parameters.
    # The following ordered arguments are the wanted outputs from this action.
    # Even if we specified multiple possible outputs for this actions ('error')
    # and 'msg', it is possible to retrieve a subset. If only one output is 
    # asked, then its value is returned by the function. Else a dictionnary
    # is returned.
    # Then inputs are specified through unordered arguments. There must always
    # be given as bytes, the requester is in charge to send it as hex to the web 
    # server. If some day the Web API changes, and some arguments are not expected
    # to be in hexadecimal, changes will be needed.
    error_message = R.do_action('send_cmd', 'error', ciphertext=b'\xff', nonce=b'\xff')

    # do awesome things to find the flag
```

### Example of usage with server communication using 'option' parameters:
```python
from ch_requester import NCRequester

if __name__ == "__main__":

    R = NCRequester(13397)
    # adding actions to the requester
    # first give the name of the action, and must match the option
    # paramete of the server-side.
    # then specify a tuple of inputs that are needed for this action
    # then specify a tuple of outputs that can given in return.
    # No particular ordering is needed here.
    R.add_action("insert_key", ("key",), ("msg"))
    R.add_action("unlock", (), ("msg",))

    # we then open the connection (using pwntools)
    R.open()
    # some challenges print a line to welcome the challenger
    # we can skip it
    R.flush_line()

    # As for the Web API, we can execute action, except this time
    # the user is responsible to put input data into the correct
    # format used by the server-side.
    msg = R.do_action("insert_key", "msg", key=(b"\x00" * 16).hex())

    print(msg)

    flag = R.do_action("unlock", "msg")

    # do awesome things to find the flag

    R.close()
```

### Example of usage with server communication without 'option' parameters:
```python
from ch_requester import NCRequester
from base64 import b64decode

if __name__ == "__main__":

    R = NCRequester(13370)
    # some challenges don't use the 'option' parameters
    # so you can send your own dictionnary payload to the server

    # we then open the connection (using pwntools)
    R.open()
    # some challenges print a line to welcome the challenger
    # we can skip it
    R.flush_line()

    PAYLOAD = {'msg': 'request'}
    ciphertext = b64decode(R.send_recv_raw_payload(PAYLOAD, 'ciphertext'))

    # do awesome things to find the flag

    R.close()
```

## Contributing

If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome.

## Licensing

The code in this project is licensed under MIT license.
