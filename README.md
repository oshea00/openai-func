# OpenAI function call example

How to setup a function call in OpenAI chat completion.

## Notes
In the "tools" collection, the parameters are described in natural language - note location can be a city, lat/lon, or zipcode.
```
...
    "properties": {
        "location": {
            "type": "string",
            "description": "The city and state, e.g. San Francisco, CA or a zip code, e.g. 94107, or a lat,lon pair, e.g. 37.7749,-122.4194",
        }
    },
...
```

If the model is unsure it can provide the required parameters, it is given a system prompt to clarify for more input.

In a "production-ized" version of this, more checks of the input values should be done along with other error handling.

## Example output
![output](https://raw.githubusercontent.com/oshea00/openai-func/main/WeatherCall.png)

