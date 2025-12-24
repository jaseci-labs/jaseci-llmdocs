# abilities


## From: example.md

- abilities (`abilities`), special methods that walkers automatically execute when they visit specific node types.
```jac
    can start with `root entry {
        print("Starting journey!");
        visit [-->];
    }

    # ability greet will only execute when Greeter enters a Person type node
    can greet with Person entry {
        print(f"Hello, {here.name}!");
        self.greeting_count += 1;

        # specify how this walker can traverse the graph
        # in this case, visit all outgoing edges from the current node
        visit [-->];
    }
```
```jac
    can func_name with `root entry {
        new_post = Post(content=self.content, author=self.author);
        here ++> new_post;
        report {"id": new_post.id, "status": "posted"};
    }
```


## From: chapter_12.md

```jac
            can get_weather_data with `root entry {
                # Your weather logic here
                weather_info = f"Weather in {self.city}: Sunny, 25°C";
                report {"city": self.city, "weather": weather_info};
            }
```

```jac
            can create_new_note with `root entry {
                new_note = Note(
                    title=self.title,
                    content=self.content,
                    author=self.author
                );

                here ++> new_note;
                report {"message": "Note created", "id": new_note.id};
            }
```

```jac
            can fetch_all_notes with `root entry {
                all_notes = [-->(`?Note)];
                notes_data = [
                    {"id": n.id, "title": n.title, "author": n.author}
                    for n in all_notes
                ];
                report {"notes": notes_data, "total": len(notes_data)};
            }
```

```jac
    can fetch_all_notes with `root entry {
        all_notes = [-->(`?Note)];
        notes_data = [
            {"id": n.id, "title": n.title, "author": n.author}
            for n in all_notes
        ];
        report {"notes": notes_data, "total": len(notes_data)};
    }
```

```jac
        can validate_and_create with `root entry {
            # Jac automatically validates types before this runs

            # Additional business logic validation
            if len(self.title) < 3 {
                report {"error": "Title must be at least 3 characters"};
                return;
            }

            if self.priority < 1 or self.priority > 5 {
                report {"error": "Priority must be between 1 and 5"};
                return;
            }

            # Create note with validated data
            new_note = Note(
                title=self.title,
                content=self.content,
                author=self.author,
                priority=self.priority,
                tags=self.tags
            );
            here ++> new_note;

            report {
                "message": "Note created successfully",
                "note_title": new_note.title,
                "priority": new_note.priority
            };
        }
```

```jac
        can add_note with `root entry {
            new_note = Note(
                title=self.title, content=self.content,
                author=self.author, priority=self.priority,
                id="note_" + str(uuid4())
            );
            here ++> new_note;
            report {"message": "Note created", "id": new_note.id};
        }
```

```jac
        can get_all_notes with `root entry {
            all_notes = [-->(`?Note)];
            report {
                "notes": [
                    {
                        "id": n.id,
                        "title": n.title,
                        "author": n.author,
                        "priority": n.priority
                    }
                    for n in all_notes
                ],
                "total": len(all_notes)
            };
        }
```

```jac
        can fetch_note with `root entry {
            target


## From: chapter_18.md

```jac
            can fetch_weather with `root entry {
                # Check cache first
                cached = [-->(`?WeatherData)](?city == self.city);

                if cached {
                    weather = cached[0];
                    report {
                        "city": weather.city,
                        "temperature": weather.temperature,
                        "description": weather.description,
                        "cached": True
                    };
                } else {
                    # Simulate API call
                    new_weather = WeatherData(
                        city=self.city,
                        temperature=22.5,
                        description="Sunny",
                        last_updated="2024-01-15T10:00:00Z"
                    );
                    here ++> new_weather;

                    report {
                        "city": self.city,
                        "temperature": 22.5,
                        "description": "Sunny",
                        "cached": False
                    };
                }
            }
```
```jac
            can check_health with `root entry {
                weather_count = len([-->(`?WeatherData)]);
                report {
                    "status": "healthy",
                    "cached_cities": weather_count,
                    "debug_mode": config["debug"]
                };
            }
```
```jac
        can fetch_weather with `root entry {
            # Update metrics
            metrics["requests_total"] += 1;
            metrics["requests_per_city"][self.city] = metrics["requests_per_city"].get(self.city, 0) + 1;

            # Check cache first
            cached = [-->(`?WeatherData)](?city == self.city);

            if cached {
                metrics["cache_hits"] += 1;
                weather = cached[0];
                report {
                    "city": weather.city,
                    "temperature": weather.temperature,
                    "description": weather.description,
                    "cached": True
                };
            } else {
                metrics["cache_misses"] += 1;
                # Simulate external API call
                new_weather = WeatherData(
                    city=self.city,
                    temperature=22.5,
                    description="Sunny",
                    last_updated=datetime.now().isoformat()
                );
                here ++> new_weather;

                report {
                    "city": self.city,
                    "temperature": 22.5,
                    "description": "Sunny",
                    "cached": False
                };
            }
        }
```
```jac
        can check_health with `root entry {
            uptime = time() - metrics["start_time"];
            cache_hit_rate = metrics["cache_hits"] / max(metrics["requests_total"], 1) * 100;

            report {
                "status": "healthy",
                "uptime_seconds": uptime,
                "total_requests": metrics["requests_total"],
                "cache_hit_rate_percent": round(cache_hit_rate, 2),
                "cached_cities": len([-->(`?WeatherData)]),
                "timestamp": datetime.now().isoformat()
            };
        }
```
```jac
        can get_metrics with `root entry {
            uptime = time() - metrics["start_time"];
            cache_hit_rate = metrics["cache_hits"] / max(metrics["requests_total"], 1) * 100;

            report {
                "uptime_seconds": uptime,
                "total_requests": metrics["requests_total"],
                "cache_hit_rate_percent": round(cache_hit_rate, 2),
                "requests_by_city": metrics["requests_per_city"],
                "timestamp": datetime.now().isoformat()
            };
        }
```
```jac
        can comprehensive_health with `root entry {
            cached_cities = len([-->(`?WeatherData)]);
            memory_usage = "healthy";  # Simplified for demo

            # Check if service is responding normally
            status = "healthy";
            if metrics["requests_total"] == 0 and time() - metrics["start_time"] > 300 {
                status = "warning";  # No requests in 5 minutes
            }

            report {
                "status": status,
                "cached_cities": cached_cities,
                "total_requests": metrics["requests_total"],
                "memory_status": memory_usage,
                "uptime_seconds": time() - metrics["start_time"],
                "version": "1.0.0"
            };
        }
```


## From: quickstart.md

The ability `get_current_time` will return the current timestamp in ISO format via the use of the `report` statement.

```jac
import from datetime {datetime}

# Public endpoint (no authentication)
walker public_info {
    obj __specs__ {
        static has methods: list = ["get"];
        static has auth: bool = False;
    }

    can get_current_time with `root entry{
        report {
            "timestamp": datetime.now().isoformat()
        };
    }
}
```
```jac
# GET endpoint with query parameters
walker search_users {
    has query: str;
    static has users: list = [
        {"username": "alice", "email": "alice@example.com"},
        {"username": "bob", "email": "bob@example.com"}
    ];

    obj __specs__ {
        static has methods: list = ["get"];
        static has as_query: list = ["query"];
        static has auth: bool = False;
    }

    can search_by_name with `root entry{
        for user in self.users {
            if user['username'] == self.query {
                report user;
                return;
            }
        }

        report {
            "error": f"User with username {self.query} not found"
        };
    }
}
```
```jac
# upload_file.jac
import from fastapi { UploadFile }

# Single file upload
walker single_file_upload {
    has file: UploadFile;

    obj __specs__ {
        static has methods: list = ["post"];
        static has auth: bool = False;
    }

    can enter with `root entry {
        report {
            "output": f"Received file: {self.file.filename}"
        };
    }
}

```


## From: sequence.md

```jac
node Node {
    has val: str;

    can entry1 with entry {
        print(f"{self.val}-2");
    }

    can entry2 with Walker entry {
        print(f"{self.val}-3");
    }

    can exit1 with Walker exit {
        print(f"{self.val}-4");
    }

    can exit2 with exit {
        print(f"{self.val}-5");
    }
}

walker Walker {
    can entry1 with entry {
        print("walker entry");
    }

    can entry2 with `root entry {
        print("walker enter to root");
        visit [-->];
    }

    can entry3 with Node entry {
        print(f"{here.val}-1");
    }

    can exit1 with Node exit {
        print(f"{here.val}-6");
    }

    can exit2 with exit {
        print("walker exit");
    }
}
```


## From: nodes_and_edges.md

### Abilities in Nodes
- Callable Abilities: They are similar to standard methods in OOP. Inside any ability, the node can refer to itself using the `self` keyword, much like in OOP.

- Visit-dependent Abilities: These abilities are only triggered when a specific type of "walker" (discussed later) interacts with the node. This ensures that certain actions are performed only in response to a walker's visit. In these abilities, a special keyword `here` is used to reference the visiting walker. This allows you to access the walker's attributes and abilities directly during its interaction with the node.

- This is an example of defining a node.
```jac linenums="1"
node test_node {
    has value: int;

    can log_entry with entry {
        print(f">>> Some Walker entered the node: ", self);
    }
    can log_test_walker_entry with test_walker entry {
        print(f">>> {here} entered the node {self}");
        here.callable();
    }
    can log_test_walker_exit with test_walker exit {
        print(f"<<< {here} exited the node {self}");
    }
    can log_exit with exit {
        print(f"<<< Some Walker exited the node {self}");
    }
    def callable {
        print(f"===== Callable on {self}");
    }
}
```


## From: walkers.md

Walkers play a crucial role in executing visit-dependent abilities as discussed in nodes and facilitating interactions between graph nodes and themselves.

## Attributes & Abilities
- Similar to nodes, walkers can have their own attributes and abilities including both callable and visit-dependent abilities.

- **Visit-dependent Abilities:**
    - Ensures the ability is executed only when the walker visits a node.
    - Can be defined within:
        - **Nodes:** Triggered upon a walker's arrival.
        - **Walkers:** Specific to the walker’s operation during its visit.
- ```here```: References the current node visited by the walker, enabling access to its attributes and callable abilities.
    This allows seamless interaction between walker and node attributes.

## Walkers in Action:
- Walkers prioritize their visit-dependent abilities first before executing the abilities of the visited node.
- This enables flexible task delegation:
    - Define visit-dependent tasks either within the walker or in the node.

!!! Abstract "can log_entry with entry"
    - This ability is triggered once when the walker is spawned. It is essentially the "entry point" of the walker’s operation.
    In the example, it logs the entry at the beginning, increments entry_count by 1, and prints the node where the walker starts (in this case, the root node).
    !!! Info ""
        - This DS function is called once at the beginning of the walker’s traversal before visiting any nodes.

!!! Abstract "can log_visit with test_node exit"
    - This ability is executed each time the walker visits a node of type test_node during its traversal.
    In the example, whenever the walker visits a test_node, it prints the node and appends the node to visited_nodes.
    !!! Info ""
        - This DS function operates during traversal and is called on each node of type test_node the walker visits.

!!! Abstract "can log_exit with exit"
    - This ability is triggered once when the walker finishes its traversal, marking the end of its operation.
    In the example, it logs the exit point, increments exit_count by 1, and prints the final node visited.
    !!! Info ""
        - This DS function is executed at the end of the walker's execution, after all nodes have been visited.


## From: FAQ.md

- You can set up special abilities for root or specific node entries in walkers:
```jac
    # Entry through root
    walker  walker_name {
      can walker_ability with `root entry;
    }
    # Entry through a given node
    walker  walker_name {
      can walker_ability with specific_node entry;
    }
    # Entry through root or a given node
    walker  walker_name {
      can walker_ability with `root | specific_node entry;
    }
```
- Walkers can have special DS abilities triggered through the `root` or a specific node. You can define such abilities based on where the walker starts its traversal:
```jac
    # Ability entry through the root
    walker walker_name {
      can walker_ability with `root entry;
    }

    # Ability entry through a specific node
    walker walker_name {
      can walker_ability with specific_node entry;
    }

    # Ability entry through either root or a specific node
    walker walker_name {
      can walker_ability with `root | specific_node entry;
    }
```
- This allows you to specify different behavior depending on whether the walker enters the DS ability from the root or a particular node, or both.
- The ability_name ability is called once at the start of the walker’s lifecycle. It is triggered when the walker is first spawned and acts as the initial entry point.
- Key Point: This is executed only once at the beginning of the walker’s execution.
- You can setup special ability of a node for a certain walker using:
```jac
    node  node_name {
      can node_ability with walker_name entry;
    }
```
- Current walker instance can be accessed using the `here` keyword within Object-Spatial abilities of the node.
```jac
walker walker_name {

    can log_visit with test_node entry{
        print("Visiting node : ", here);
    }
}
```
- You can access the current walker instance inside Object-Spatial abilities of a node using the `self` keyword.
```jac
node node_name {
    can node_ability with walker_name entry{
        print("Current walker : ", here);
    }
}
```
- You can access the current walker instance inside Object-Spatial abilities of the current walker using the `self` keyword.
```jac
walker walker_name {
    can walker_ability with node_name entry{
        print("Current walker : ", self);
    }
}
```


## From: agentic_ai.md

Nodes have attributes (data) and special abilities that trigger on preset events rather than being directly called. In an agentic system, nodes are agents that maintain local state and respond to visitor events.

The agent's entry point is the `can execute with task_manager entry` ability. This = ability triggers **automatically** when the `task_manager` walker visits this node, making it easy to define agent behavior without explicit callbacks.

```jac linenums="1"
node TaskHandling {
  def get_current_time() -> str {
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime());
  }

  def add_task(task: str, date: str, time: str) -> str {
    task_created = Task(task=task, date=date, time=time);
    self ++> task_created;
    return "Task added successfully";
  }

  def summarize_tasks -> str {
    scheduled_tasks = [self-->(`?Task)];
    return str(scheduled_tasks);
  }

  def route_and_run(utterance: str) -> str by llm(
    method="ReAct",
    tools=([self.add_task, self.get_current_time, self.summarize_tasks])
  );

  can execute with task_manager entry {
    print("[TaskHandling Node Activated]");
    response = self.route_and_run(visitor.cur_task.task);
    print("→", response);
    report {
      "utterance": visitor.cur_task.task,
      "response": response,
      "node_type": self.__class__.__name__
    };
  }
}
```

```jac linenums="1"
node EmailHandling {
  def write_email_content(utterance: str) -> str by llm();
  def route_and_run(utterance: str) -> str by llm(
    method="ReAct",
    tools=([self.write_email_content])
  );
  can execute with task_manager entry {
    print("[EmailHandling Node Activated]");
    response = self.route_and_run(visitor.cur_task.task);
    print("→", response);
    report {
      "utterance": visitor.cur_task.task,
      "response": response,
      "node_type": self.__class__.__name__
    };
  }
}
```

```jac linenums="1"
node GeneralChat {
  def chat(utterance: str) -> str by llm();
  can execute with task_manager entry {
    print("[GeneralChat Node Activated]");
    response = self.chat(visitor.cur_task.task);
    print("→", response);
    report {
      "utterance": visitor.cur_task.task,
      "response": response,
      "node_type": self.__class__.__name__
    };
  }
}
```

```jac linenums="1"
walker task_manager {
  has utterance: str = "";
  has cur_task: TaskPartition = None;

  def route_to_node(utterance: str) -> RoutingNodes by llm();
  def plan_tasks(main_task: str) -> list[TaskPartition] by llm();

  can execute with `root entry {
    # Step 1: Plan - decompose the user's request
    subtasks = self.plan_tasks(self.utterance);
    print("[Planned Subtasks]:", subtasks);

    # Step 2: Map agent types to node classes
    node_map = {
      RoutingNodes.TASK_HANDLING: TaskHandling,
      RoutingNodes.EMAIL_HANDLING: EmailHandling,
      RoutingNodes.GENERAL_CHAT: GeneralChat
    };

    # Step 3: Execute - route


## From: tutorial.md

#### littleX.jac - What Your App Has
```jac
# Define what exists
node Profile {
    has username: str;
    can update with update_profile entry;
}
```
```jac
walker create_tweet(visit_profile) {
    has content: str;
    can tweet with Profile entry;
}
```
```jac
walker visit_profile {
    can visit_profile with `root entry;
}
```
```jac
walker create_tweet(visit_profile) {
    has content: str;
    can tweet with Profile entry;
}
```
```jac
walker load_feed(visit_profile) {
    has search_query: str = "";
    has results: list = [];
    can load with Profile entry;
}
```
### Profile Node
```jac
node Profile {
    has username: str = "";

    can update with update_profile entry;
    can get with get_profile entry;
    can follow with follow_request entry;
    can un_follow with un_follow_request entry;
}
```
### Tweet Node
```jac
node Tweet {
    has content: str;
    has embedding: list;
    has created_at: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S");

    can update with update_tweet exit;
    can delete with remove_tweet exit;
    can like_tweet with like_tweet entry;
    can remove_like with remove_like entry;
    can comment with comment_tweet entry;

    def get_info() -> TweetInfo;
    can get with load_feed entry;
}
```

