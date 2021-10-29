# Pynion

Pynion is a middleware framework for serverless functions. The usage and experience aims to be similar to middleware frameworks for common HTTP REST API libraries, such as Flask, Express, or ASP Web API. Pynion implements an onion model, where middleware functions will wrap around the main handler function which provides the unique application logic of the function. Each middleware will have the opportunity to inspect, enrich, and otherwise modify the inbound event in turn, beginning with the first middleware object applied. After the handler returns, the middleware will again have the opportunity to inspect and modify the outbound result. All middlewares also have the option to provide an error handling function, which can respond to and potentially resolve any exception raised during execution. And finally, the handler or any middleware can abort further execution and return immediately, if necessary.

## Usage

This package is very young, and I wouldn't recommend using it for production work loads. But, if you want to use it for fun, it's fairly straightforward.

Simply import `Pynion` along with any middlwares you want to use (currently none exist; you would have to implement your own). `Pynion()` will wrap your handler function in the provided middleware and return an AWS Lambda handler function.

```python
from Pynion import Pynion
from MagicMiddleware import MagicLogs, MagicAuth

def controller_fn(event: dict, context: dict, abort: Callable, raw_event: dict):
    # do processing on the event and context
    # raw_event is the original, unmodified event as provided by the serverless function invocation
    
    if(should_abort):
        return abort({"abort": "data"})
    return {"your": "data"}

handler = Pynion(controller_fn).use(MagicLogs).use(MagicAuth)
```

In the above example, `handler` is a function with event and context parameters. It will be invoked by AWS Lambda, and it will execute the middleware and `controller_fn`, like so:
```
Function Invocation
│
├ MagicLogs
│
├ MagicAuth
│
├ controller_fn
│
├ MagicAuth
│
└ MagicLogs
```

If a middleware has nothing to do at either the inbound pre-handler phase, or the outbound post-handler phase, then it can simply do nothing.

In the event an exception was raised, error handlers provided by first the logs then the auth middlewares would have an opportunity to react. If the exception is handled, normal execution will continue. Otherwise, the exception will be re-raised to the serverless function invocation.

## Future Enhancements

The big thing is to implement some basic middlewares. I also would like to provide some mechanism which would automatically adapt middlewares from common frameworks. Either Django, Flask, or both.

Test and support other clouds.

## Todo

More testing and real world use.
