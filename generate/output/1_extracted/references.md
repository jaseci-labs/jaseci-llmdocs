# references


## From: jac_playground.md

#### Object Spatial Programming
- **Reference** - Understanding object references and relationships


## From: jac_import_patterns.md

This document provides a comprehensive reference of all JavaScript/ECMAScript import patterns and their Jac equivalents, showing which patterns are currently supported.

## Import Pattern Support Matrix

| Category | JavaScript Pattern | Jac Pattern | Status | Generated JavaScript | Notes |
|----------|-------------------|---------------------|---------------------|-------|
| **Category 1: Named Imports** |
| Single named | `import { useState } from 'react'` | `cl import from react { useState }` | ✅ Working | `import { useState } from "react";` | |
| Multiple named | `import { map, filter } from 'lodash'` | `cl import from lodash { map, filter }` | ✅ Working | `import { map, filter } from "lodash";` | |
| Named with alias | `import { get as httpGet } from 'axios'` | `cl import from axios { get as httpGet }` | ✅ Working | `import { get as httpGet } from "axios";` | |
| Mixed named + aliases | `import { createApp, ref as reactive } from 'vue'` | `cl import from vue { createApp, ref as reactive }` | ✅ Working | `import { createApp, ref as reactive } from "vue";` | |
| **Category 1: Relative Paths** |
| Single dot (current) | `import { helper } from './utils'` | `cl import from .utils { helper }` | ✅ Working | `import { helper } from "./utils";` | |
| Double dot (parent) | `import { format } from '../lib'` | `cl import from ..lib { format }` | ✅ Working | `import { format } from "../lib";` | |
| Triple dot (grandparent) | `import { settings } from '../../config'` | `cl import from ...config { settings }` | ✅ Working | `import { settings } from "../../config";` | Supports any number of dots |
| **Category 1: Module Prefix** |
| With jac: prefix | `import { renderJsxTree } from 'jac:client_runtime'` | `cl import from jac:client_runtime { renderJsxTree }` | ✅ Working | `import { renderJsxTree } from "client_runtime";` | Prefix stripped for resolution |
| **Category 1: String Literal Imports** |
| Hyphenated packages | `import { render } from 'react-dom'` | `cl import from "react-dom" { render }` | ✅ Working | `import { render } from "react-dom";` | Use string literals for package names with hyphens |
| Multiple hyphens | `import { BrowserRouter } from 'react-router-dom'` | `cl import from "react-router-dom" { BrowserRouter }` | ✅ Working | `import { BrowserRouter } from "react-router-dom";` | Works with any special characters |
| **Category 2: Default Imports** |
| Default import | `import React from 'react'` | `cl import from react { default as React }` | ✅ Working | `import React from "react";` | Must use `cl` prefix |
| Default with relative | `import Component from './Button'` | `cl import from .Button { default as Component }` | ✅ Working | `import Component from "./Button";` | |
| **Category 4: Namespace Imports** |
| Namespace import | `import * as React from 'react'` | `cl import from react { * as React }` | ✅ Working | `import * as React from "react";` | Must use `cl` prefix |
| Namespace with relative | `import * as utils from './utils'` | `cl import from .utils { * as utils }` | ✅ Working | `import * as utils from "./utils";` | |
| **Category 3: Mixed Imports** |
| Default + Named | `import React, { useState } from 'react'` | `cl import from react { default as React, useState }` | ✅ Working | `import React, { useState } from "react";` | Order matters: default first |
| Default + Namespace | `import React, * as All from 'react'` | `cl import from react { default as React, * as All }` | ✅ Working | `import React, * as All from "react";` | Valid JS (rarely used) |
| Named + Namespace | `import * as _, { map } from 'lodash'` | `cl import from lodash { * as _, map }` | ⚠️ Generates | `import * as _, { map } from "lodash";` | **Invalid JavaScript** - not recommended |

## Examples

### Full Feature Demo
```jac
cl {
    # Named imports
    import from react { useState, useEffect, useRef }
    import from lodash { map as mapArray, filter }

    # Default imports
    import from react { default as React }
    import from axios { default as axios }

    # Namespace imports
    import from "date-fns" { * as DateFns }
    import from .utils { * as Utils }

    # String literal imports (for hyphenated packages)
    import from "react-dom" { render, hydrate }
    import from "styled-components" { default as styled }
    import from "react-router-dom" { BrowserRouter, Route }

    # Mixed imports
    import from react { default as React, useState, useEffect }

    # Relative paths
    import from .components.Button { default as Button }
    import from ..lib.helpers { formatDate }
    import from ...config.constants { API_URL }

    def MyComponent() {
        let [count, setCount] = useState(0);
        let now = DateFns.format(new Date());
        axios.get(API_URL);

        return count;
    }
}
```

### Generated JavaScript Output
```javascript
import { useState, useEffect, useRef } from "react";
import { map as mapArray, filter } from "lodash";
import React from "react";
import axios from "axios";
import * as DateFns from "date-fns";
import * as Utils from "./utils";
import { render, hydrate } from "react-dom";
import styled from "styled-components";
import { BrowserRouter, Route } from "react-router-dom";
import React, { useState, useEffect } from "react";
import Button from "./components.Button";
import { formatDate } from "../lib.helpers";
import { API_URL } from "../../config.constants";

function MyComponent() {
  let [count, setCount] = useState(0);
  let now = DateFns.format(new Date());
  axios.get(API_URL);
  return count;
}
```

## Status Summary

- ✅ **Category 1 (Named Imports)**: Fully implemented and tested
- ✅ **Category 2 (Default Imports)**: Fully implemented and tested
- ✅ **Category 3 (Mixed Imports)**: Working for default+named and default+namespace
- ✅ **Category 4 (Namespace Imports)**: Fully implemented and tested
- ✅ **Relative Paths**: Full support with automatic conversion
- ✅ **String Literal Imports**: Full support for hyphenated package names (react-dom, styled-components, etc.)
- ⚠️ **Named + Namespace Mix**: Generates but produces invalid JavaScript


## From: example.md

Much like every object instance has a self referencial `this` or `self` reference. Every instance of a Jac program invocation has a `root` node reference that is unique to every user and for which any other node or edge objects connected to `root` will persist across code invocations. That's it. Using `root` to access persistent user state and data, Jac deployments can be scaled from local environments infinitely into to the cloud with no code changes.


## From: byllm.md

- **Custom Model Declaration**: Custom model interfaces can be defined by using the `BaseLLM` class that can be imported form `byllm.lib`. A guide for using this feature is added to [documentation](https://docs.jaseci.org/learn/jac-byllm/create_own_lm/).


## From: logging.md

For more detailed documentation:

- [Getting Started](https://www.elastic.co/guide/en/cloud/current/ec-getting-started-search-use-cases-python-logs.html)
- [Configure filebeat](https://www.elastic.co/guide/en/beats/filebeat/current/configuring-howto-filebeat.html)


## From: scheduler.md

- Learn about [WebSocket Communication](websocket.md) for real-time updates
- Explore [Webhook Integration](webhook.md) for external service integration
- Set up [Logging & Monitoring](logging.md) to track task execution
- Deploy your application using [Kubernetes](deployment.md) for scalable task processing


## From: litellm_proxy.md

Reference: [https://docs.litellm.ai/docs/proxy/deploy](https://docs.litellm.ai/docs/proxy/deploy)

You can find more information about how to obtain this key in the [LiteLLM documentation](https://docs.litellm.ai/docs/proxy/virtual_keys).


## From: quickstart.md

- [Authentication & Permissions](permission.md) - Secure your API
- [Real-time WebSocket Communication](websocket.md) - Add real-time features
- [Task Scheduling](scheduler.md) - Automate recurring tasks
- [Webhook Integration](webhook.md) - Create API integrations
- [Environment Variables](env_vars.md) - Configure your application
- [Logging & Monitoring](logging.md) - Track application performance


## From: async_walker.md

- Returns immediately with a reference ID while continuing execution in the background
The API call returns immediately with a walker ID reference
When you call an async walker, you receive a response containing the walker's unique ID:

```json
{
  "status": 200,
  "walker_id": "w:sample:550e8400-e29b-41d4-a716-446655440000"
}
```

You can retrieve the results of an async walker by using its ID:

```jac
walker view_sample_result {
    has walker_id: str;

    can enter with `root entry {
        # Get a reference to the walker instance
        wlk = &walker_id;

        # Access the walker's attributes
        print(wlk.value);  # Will be 1 after execution completes

        # Check execution status and metadata
        schedule_info = wlk.__jac__.schedule;

        # Print execution details
        print(f"Status: {schedule_info.status}");
        print(f"Executed at: {schedule_info.executed_date}");

        # Check for errors
        if schedule_info.error{
            print(f"Error: {schedule_info.error}");
        }
    }
}
```

```jac
# Retrieve results when needed
walker check_processing {
    has process_id: str;

    can enter with `root entry {
        process = &process_id;

        if process.__jac__.schedule.status == "COMPLETED"{
            print("Results:", process.results);
        }
        else{
            print("Still processing...");
        }
    }
}
```


## From: cli.md

- `automate_ref` tool automates the reference guide generation.
```bash
jac tool automate_ref
```


## From: walkers.md

## Reference Keywords:
- ```self``` : Refers to the walker object itself.
- ```here```: References the current node visited by the walker, enabling access to its attributes and callable abilities.
    This allows seamless interaction between walker and node attributes.


## From: streamlit.md

- Check out the [Jac Cloud documentation](../jac-cloud/introduction.md) for backend integration


## From: rpg_game.md

For more details access the [full documentation of MTP](/learn/jac-byllm/with_llm).

