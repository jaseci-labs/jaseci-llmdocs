# walkers


## From: jac_in_a_flash.md

A `walker` visits a chain of `turn` nodes created with `++>` edges. The walker moves with `visit [-->]` and stops via `disengage` when the guess is correct. The game is launched by `spawn`ing the walker at `root`.


## From: jac_playground.md

The Graph Visualizer makes Jac's spatial programming concepts tangible, allowing you to see exactly how your objects, walkers, and edges interact during program execution.


## From: jac-lens.md

If you're using Jac Cloud version prior to 0.2.5, you need to manually add the required walkers to your application.

### Required Walkers

Create a file named `jaclens.jac` with the following content:

```jac
walker get_attached_nodes {
    has node_id: str = "";
    can get_attach_nodes with `root entry {
        if(self.node_id == "") {
            report jid(here);
        } else {
            selected_node = &self.node_id;
            attached_nodes = [selected_node-->];
            report attached_nodes;
        }
    }
}

walker update_node_data {
    has node_id: str = "";
    has node_data: dict = {};
    can update_node_data with `root entry {
        selected_node = &self.node_id;
        selected_node.__dict__.update(self.node_data);
        report selected_node;
    }
}
```

### Integration Steps

1. **Create the file** `jaclens.jac` in your project
2. **Copy the walker code** above into the file
3. **Include in your main file** by adding `include jaclens;` at the top of your application entry JAC file

??? info "Why These Walkers?"
    These walkers provide the necessary functionality for Jac Lens to:
    - Retrieve node information and relationships
    - Update node properties in real-time
    - Navigate through your graph structure

??? failure "Graph Not Loading"
    - Confirm you have the required walkers installed
    - Check your server logs for errors
    - Verify your graph has data to display

??? failure "Changes Not Saving"
    - Ensure you have write permissions
    - Check your network connection
    - Verify the update_node_data walker is working


## From: keywords.md

**Core Archetype Keywords**

| Keyword | Description |
| --- | --- |
| [`walker`](https://www.jac-lang.org/learn/jac_ref/#archetype-types) | A mobile computational agent that traverses the graph of nodes and edges to process data. |


## From: tour.md

Jac introduces a new programming model that lets developers articulate relationships between objects in a graph-like structure and express computation as walkers that traverse this graph.


## From: library_mode.md

**In Jac:**
```jac
walker FriendFinder {
    has started: bool = False;
}
```

**In Library Mode:**
```python
from jaclang.lib import Walker


class FriendFinder(Walker):
    started: bool = False
```

Walkers are graph traversal agents implemented by inheriting from the `Walker` base class. Walkers navigate through the graph structure and execute logic at each visited node or edge.

| Class | Description | Usage |
|-------|-------------|-------|
| `Walker` | Graph traversal agent | `class MyWalker(Walker):` |


## From: example.md

- walker classes (`walker`), which encapsulate object interactions and specify how computation moves through the graph,
By modeling relationships directly as graph edges and expressing computation through walkers, OSP removes much of the boilerplate needed to manage graphs, traversals, search and state. This makes complex logic simpler, clearer, and more scalable.
```jac
walker Greeter {
    has greeting_count: int = 0;

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
}
```
```jac
walker create_post {
    has content: str, author: str;

    can func_name with `root entry {
        new_post = Post(content=self.content, author=self.author);
        here ++> new_post;
        report {"id": new_post.id, "status": "posted"};
    }
}
```


## From: syntax_quick_reference.md

```jac
	# Walkers are objects that "walk" across nodes doing operations
	# Walkers contain automatic methods that trigger on events
	# These methods are called abilities
	walker Visitor {
        has name: str;

        # abilities follow can <name> with <type> <operation> syntax
		# runs when walker spawns at root
		can start with `root entry {
			print(f"Starting!");
			# visit moves to an adjacent node
			visit [-->]; # [-->] corresponds to outgoing connections
			# visit [<--]; incoming connections
			# visit [<-->]; all connections
		}

		# runs


## From: chapter_2.md

A **literal** is a fixed value you write directly in your code, like "Alice" or 95. Jac uses common literals like *string*, *integer*, *float*, and *boolean*. It also introduces a special kind of literal called an **architype** (node, edge, and walker), which was briefly discussed in the prvious chapter.We will explore architypes in more detail later in chapter 9.


## From: chapter_10.md

Walkers introduce a fundamental shift from traditional programming. This is the core philosophy of Object-Spatial Programming.
- In Jac, you create a walker and send your code to your data.
This model of "mobile computation" is incredibly effective for working with the complex, interconnected data found in AI and other modern systems.
Walkers are special objects that can move through your graph, carrying state and executing abilities when they encounter different types of nodes and edges.

### Basic Walker Declaration

A walker is defined with the walker archetype. Like an obj, it can have has attributes to store data and def methods for internal logic. At this stage, a walker is just an object; it doesn't move or interact with the graph until it is "spawned."

```jac
        # Simple walker for visiting nodes
        walker MessageDelivery {
            has message: str;
            has delivery_count: int = 0;
            has visited_locations: list[str] = [];

            # Regular methods work like normal
            def get_status() -> str {
                return f"Delivered {self.delivery_count} messages to {len(self.visited_locations)} locations";
            }
        }

        with entry {
            # Create walker instance (but don't activate it yet)
            messenger = MessageDelivery(message="Hello from the principal!");

            # Check initial state
            print(f"Initial status: {messenger.get_status()}");
        }
```
```jac
        walker MessageDelivery {
            has message: str;
            has delivery_count: int = 0;
            has visited_locations: list[str] = [];

            # Entry ability - triggered when entering any Student
            can deliver_to_student with Student entry {
                print(f"Delivering message to student {here.name}");
                here.messages.append(self.message);
                self.delivery_count += 1;
                self.visited_locations.append(here.name);
            }

            # Entry ability - triggered when entering any Teacher
            can deliver_to_teacher with Teacher entry {
                print(f"Delivering message to teacher {here.name} ({here.subject})");
                # Teachers just acknowledge the message
                print(f"  {here.name} says: 'Message received!'");
                self.delivery_count += 1;
                self.visited_locations.append(here.name);
            }

            # Exit ability - triggered when leaving any node
            can log_visit with entry {
                node_type = type(here).__name__;
                print(f"  Visited {node_type}");
            }
        }

        with entry {
            # Create simple classroom
            alice = root ++> Student(name="Alice");
            bob = root ++> Student(name="Bob");
            ms_smith = root ++> Teacher(name="Ms. Smith", subject="Math");

            # Create and activate messenger
            messenger = MessageDelivery(message="School assembly at 2 PM");

            # Spawn walker on Alice - this activates it
            alice[0] spawn messenger;

            # Check Alice's messages
            print(f"Alice's messages: {alice[0].messages}");
        }
```
Walkers move through graphs using `spawn` (to start) and `visit` (to continue to connected nodes). This enables complex traversal patterns with simple syntax.
```jac
        walker MessageDelivery {
            has message: str;
            has delivery_count: int = 0;
            has visited_locations: list[str] = [];

            # Entry ability - triggered when entering any Student
            can deliver_to_student with Student entry {
                print(f"Delivering message to student {here.name}");
                here.messages.append(self.message);
                self.delivery_count += 1;
                self.visited_locations.append(here.name);
            }

            # Entry ability - triggered when entering any Teacher
            can deliver_to_teacher with Teacher entry {
                print(f"Delivering message to teacher {here.name} ({here.subject})");
                # Teachers just acknowledge the message
                print(f"  {here.name} says: 'Message received!'");
                self.delivery_count += 1;
                self.visited_locations.append(here.name);
            }

            # Exit ability - triggered when leaving any node
            can log_visit with entry {
                node_type = type(here).__name__;
                print(f"  Visited {node_type}");
            }
        }

        edge InClass {
            has room: str;
        }

        walker ClassroomMessenger {
            has announcement: str;
            has rooms_visited: set[str] = {};
            has people_reached: int = 0;

            can deliver_student with Student entry {
                print(f" Student {here.name}: {self.announcement}");
                self.people_reached += 1;

                # Continue to connected nodes
                visit [-->];
            }

            can deliver_teacher with Teacher entry {
                print(f" Teacher {here.name}: {self.announcement}");
                self.people_reached += 1;

                # Continue to connected nodes
                visit [-->];
            }

            can track_room with InClass entry {
                room = here.room;
                if room not in self.rooms_visited {
                    self.rooms_visited.add(room);
                    print(f" Now in {room}");
                }
            }

            can summarize with Student exit {
                # Only report once at the end
                if len([-->]) == 0 {  # At a node with no outgoing connections
                    print(f" Delivery complete!");
                    print(f"   People reached: {self.people_reached}");
                    print(f"   Rooms visited: {list(self.rooms_visited)}");
                }
            }
        }

        with entry {
            # Create classroom structure
            alice = root ++> Student(name="Alice");
            bob = root ++> Student(name="Bob");
            charlie = root ++> Student(name="Charlie");
            ms_jones = root ++> Teacher(name="Ms. Jones", subject="Science");

            # Connect them in the same classroom
            alice +>:InClass(room="Room 101"):+> bob;
            bob +>:InClass(room="Room 101"):+> charlie;
            charlie +>:InClass(room="Room 101"):+> ms_jones;

            # Send a message through the classroom
            messenger = ClassroomMessenger(announcement="Fire drill in 5 minutes");
            alice[0] spawn messenger;
        }
```
```jac
        walker AttendanceChecker {
            has present_students: list[str] = [];
            has absent_students: list[str] = [];
            has max_checks: int = 5;
            has checks_done: int = 0;

            can check_attendance with Student entry {
                self.checks_done += 1;

                # Simulate checking if student is present (random for demo)
                is_present = random.choice([True, False]);

                if is_present {
                    print(f"{here.name} is present");
                    self.present_students.append(here.name);
                } else {
                    print(f"{here.name} is absent");
                    self.absent_students.append(here.name);
                }

                # Control flow based on conditions
                if self.checks_done >= self.max_checks {
                    print(f"Reached maximum checks ({self.max_checks})");
                    self.report_final();
                    disengage;  # Stop the walker
                }

                # Skip if no more connections
                connections = [-->];
                if not connections {
                    print("No more students to check");
                    self.report_final();
                    disengage;
                }

                # Continue to next student
                visit [-->];
            }

            def report_final() -> None {
                print(f" Attendance Report:");
                print(f"   Present: {self.present_students}");
                print(f"   Absent: {self.absent_students}");
                print(f"   Total checked: {self.checks_done}");
            }
        }

        with entry {
            # Create a chain of students
            alice = root ++> Student(name="Alice", grade_level=9);
            bob = alice ++> Student(name="Bob", grade_level=9);
            charlie = bob ++> Student(name="Charlie", grade_level=9);
            diana = charlie ++> Student(name="Diana", grade_level=9);
            eve = diana ++> Student(name="Eve", grade_level=9);

            # Start attendance check
            checker = AttendanceChecker(max_checks=3);
            alice[0] spawn checker;
        }
```
Walkers can control their movement through the graph using special statements like `visit` and `disengage`.
```jac
        walker AttendanceChecker {
            has present_students: list[str] = [];
            has absent_students: list[str] = [];
            has max_checks: int = 5;
            has checks_done: int = 0;

            can check_attendance with Student entry {
                self.checks_done += 1;

                # Simulate checking if student is present (random for demo)
                import random;
                is_present = random.choice([True, False]);

                if is_present {
                    print(f"{here.name} is present");
                    self.present_students.append(here.name);
                } else {
                    print(f"{here.name} is absent");
                    self.absent_students.append(here.name);
                }

                # Control flow based on conditions
                if self.checks_done >= self.max_checks {
                    print(f"Reached maximum checks ({self.max_checks})");
                    self.report_final();
                    disengage;  # Stop the walker
                }

                # Skip if no more connections
                connections = [-->];
                if not connections {
                    print("No more students to check");
                    self.report_final();
                    disengage;
                }

                # Continue to next student
                visit [-->];
            }

            def report_final() -> None {
                print(f" Attendance Report:");
                print(f"   Present: {self.present_students}");
                print(f"   Absent: {self.absent_students}");
                print(f"   Total checked: {self.checks_done}");
            }
        }

        with entry {
            # Create a chain of students
            alice = root ++> Student(name="Alice", grade_level=9);
            bob = alice ++> Student(name="Bob", grade_level=9);
            charlie = bob ++> Student(name="Charlie", grade_level=9);
            diana = charlie ++> Student(name="Diana", grade_level=9);
            eve = diana ++> Student(name="Eve", grade_level=9);

            # Start attendance check
            checker = AttendanceChecker(max_checks=3);
            alice[0] spawn checker;
        }
```
- **Walkers** are mobile computational entities that traverse graphs
- **Keep abilities focused**: Each ability should have a single, clear purpose
- **Use descriptive names**: Make it clear what each walker and ability does
- **Control traversal flow**: Use conditions to avoid infinite loops
- **Report results**: Use exit abilities to summarize walker activities
- **Manage state**: Use walker properties to track progress and results
- **Mobile computation**: Walkers bring processing directly to data locations
- **State management**: Walkers carry their own state as they traverse
- **Traversal control**: Fine-grained control over movement patterns


## From: chapter_12.md

In this chapter, we'll explore how Jac automatically transforms walkers into RESTful API endpoints with our **Jac Cloud** Plugin. Jac Cloud, is a revolutionary cloud platform that transforms your Jac programs into scalable web services without code changes. This means you can focus on building your application logic while Jac handles the HTTP details for you.

- Converting walkers into API endpoints automatically

Your walker is now automatically available as a REST API endpoint!

In this example the endpoint is defined as `/walker/get_weather`, however, the endpoint also expects a JSON request body with a `city` field.

Now that we have a basic understanding of Jac Cloud and how it automatically generates APIs from walkers, let's build a more complex application: a shared notebook system.

First lets develop a walker that allows users to create and retrieve notes in a notebook. This will demonstrate how Jac handles request/response mapping, parameter validation, and persistence automatically.

```jac
        # weather.jac - No manual API setup needed
        walker get_weather {
            has city: str;

            obj __specs__ {
                static has auth: bool = False;
            }

            can get_weather_data with `root entry {
                # Your weather logic here
                weather_info = f"Weather in {self.city}: Sunny, 25°C";
                report {"city": self.city, "weather": weather_info};
            }
        }
```

```jac
        walker create_note {
            has title: str;
            has content: str;
            has author: str;

            obj __specs__ {
                static has auth: bool = False;
            }

            can create_new_note with `root entry {
                new_note = Note(
                    title=self.title,
                    content=self.content,
                    author=self.author
                );

                here ++> new_note;
                report {"message": "Note created", "id": new_note.id};
            }
        }

        walker get_notes {
            obj __specs__ {
                static has auth: bool = False;
            }

            can fetch_all_notes with `root entry {
                all_notes = [-->(`?Note)];
                notes_data = [
                    {"id": n.id, "title": n.title, "author": n.author}
                    for n in all_notes
                ];
                report {"notes": notes_data, "total": len(notes_data)};
            }
        }
```

The `create_note` walker will accept a JSON request body with `title`, `content`, and `author` fields, and return a response indicating the note was created.

To retrieve all notes, we can use the `get_notes` walker:

To convert the `get_notes` walker to a GET request, we can simply change the walker `___specs__` to indicate that it can be accessed via a GET request. This is done by setting the `methods` attribute in the `__specs__` object.

```jac
walker get_notes {
    obj __specs__ {
        static has auth: bool = False;
        static has methods: list = ["get"];
    }

    can fetch_all_notes with `root entry {
        all_notes = [-->(`?Note)];
        notes_data = [
            {"id": n.id, "title": n.title, "author": n.author}
            for n in all_notes
        ];
        report {"notes": notes_data, "total": len(notes_data)};
    }
}
```

The `get_notes` walker can now be accessed via a GET request at the endpoint `/walker/get_notes`.

Jac automatically validates request parameters based on walker attribute types. This eliminates manual validation code and ensures type safety.

```jac
    walker create_note {
        has title: str;
        has content: str;
        has author: str;
        has priority: int = 1;
        has tags: list[str] = [];

        obj __specs__ {
            static has auth: bool = False;
        }

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
    }
```

Walkers naturally map to REST operations, creating intuitive API patterns for common CRUD operations.

```jac
    # CREATE - Add new note
    walker create_note {
        has title: str;
        has content: str;
        has author: str;
        has priority: int = 1;

        can add_note with `root entry {
            new_note = Note(
                title=self.title, content=self.content,
                author=self.author, priority=self.priority,
                id="note_" + str(uuid4())
            );
            here ++> new_note;
            report {"message": "Note created", "id": new_note.id};
        }
    }

    # READ - Get all notes
    walker list_notes {
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
    }

    # READ - Get specific note
    walker get_note {
        has note_id: str;

        can fetch_note with `root entry {
            target_note = [-->(`?Note)](?id == self.note_id);

            if target_note {
                note = target_note[0];
                report {
                    "note": {
                        "id": note.id,
                        "title": note.title,
                        "content": note.content,
                        "author": note.author,
                        "priority": note.priority
                    }
                };
            } else {
                report {"error": "Note not found"};
            }
        }
    }

    # UPDATE - Modify note
    walker update_note {
        has note_id: str;
        has title: str = "";
        has content: str = "";
        has priority: int = 0;

        can modify_note with `root entry {
            target_note = [-->(`?Note)](?id == self.note_id);

            if target_note {
                note = target_note[0];

                # Update only provided fields
                if self.title {
                    note.title = self.title;
                }
                if self.content {
                    note.content = self.content;
                }
                if self.priority > 0 {
                    note.priority = self.priority;
                }

                report {"message": "Note updated", "id": note.id};
            } else {
                report {"error": "Note not found"};
            }
        }
    }

    # DELETE - Remove note
    walker delete_note {
        has note_id: str;

        can remove_note with `root entry {
            target_note = [-->(`?Note)](?id == self.note_id);

            if target_note {
                note = target_note[0];
                # Delete the node and its connections
                del note;
                report {"message": "Note deleted", "id": self.note_id};
            } else {
                report {"error": "Note not found"};
            }
        }
    }
```

```jac
    walker create_shared_note {
        has title: str;
        has content: str;
        has author: str;
        has shared_with: list[str] = [];
        has is_public: bool = false;

        can create_note with `root entry {
            new_note = Note(
                title=self.title,
                content=self.content,
                author=self.author,
                shared_with=self.shared_with,
                is_public=self.is_public,
                id="note_" + str(uuid4())
            );
            here ++> new_note;

            report {
                "message": "Shared note created",
                "id": new_note.id,
                "shared_with": len(self.shared_with),
                "is_public": self.is_public
            };
        }
    }

    walker get_user_notes {
        has user: str;

        can fetch_accessible_notes with `root entry {
            all_notes = [-->(`?Note)];
            accessible_notes = [];

            for note in all_notes {
                # User can access if they're the author, note is public,
                # or they're in the shared_with list
                if (note.author == self.user or
                    note.is_public or
                    self.user in note.shared_with) {
                    accessible_notes.append({
                        "id": note.id,
                        "title": note.title,
                        "author": note.author,
                        "is_mine": note.author == self.user
                    });
                }
            }

            report {
                "user": self.user,
                "notes": accessible_notes,
                "count": len(accessible_notes)
            };
        }
    }

    walker share_note {
        has note_id: str;
        has user: str;
        has share_with: str;

        can add_share_permission with `root entry {
            target_note = [-->(`?Note)](?id == self.note_id);

            if target_note {
                note = target_note[0];

                # Only author can share
                if note.author == self.user {
                    if self.share_with not in note.shared_with {
                        note.shared_with.append(self.share_with);
                    }

                    report {
                        "message": f"Note shared with {self.share_with}",
                        "shared_with": note.shared_with
                    };
                } else {
                    report {"error": "Only author can share notes"};
                }
            } else {
                report {"error": "Note not found"};
            }
        }
    }
```

- **Use descriptive walker names**: Names become part of your API surface
- **Keep walkers focused**: Each walker should have a single responsibility
- **Zero configuration**: Walkers become REST endpoints without setup
- **Natural REST patterns**: CRUD operations map intuitively to walker semantics
- **JSON mapping**: Request bodies automatically map to walker attributes
- **Response formatting**: Walker reports become structured JSON responses
- Every walker you create automatically becomes an API endpoint when deployed!


## From: chapter_18.md

```jac
walker get_weather {
    has city: str;

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
}

walker health_check {
    can check_health with `root entry {
        weather_count = len([-->(`?WeatherData)]);
        report {
            "status": "healthy",
            "cached_cities": weather_count,
            "debug_mode": config["debug"]
        };
    }
}
```
```jac
walker get_weather {
    has city: str;

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
}

walker health_check {
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
}

walker metrics_endpoint {
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
}

walker detailed_health_check {
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
}
```


## From: jac-scale.md

- Intelligent walker scheduling across multiple nodes


## From: jac-cloud.md

- **Dynamic Runtime Walker Endpoint**: Fixes auto-generated endpoints for walkers created at runtime.
- **Jac Clouds Traverse API**: Introduced the ability to traverse graph. This API support control of the following:
  - source - Starting node/edge. Defaults to root
  - detailed - If response includes archetype context. Defaults to False
  - depth - how deep the traversal from source. Count includes edges. Defaults to 1
  - node_types - Node filter by name. Defaults to no filter
  - edge_types - Edge filter by name. Defaults to no filter
- **Support Spawning a Walker with List of Nodes and Edges**: Introduced the ability to spawn a walker on a list of nodes and edges. This feature enables initiating traversal across multiple graph elements simultaneously, providing greater flexibility and efficiency in handling complex graph structures.
- **Async Walker Support**: Introduced comprehensive async walker functionality that brings Python's async/await paradigm to object-spatial programming. Async walkers enable non-blocking spawns during graph traversal, allowing for concurrent execution of multiple walkers and efficient handling of I/O-bound operations.


## From: chapter_19.md

```jac
walker find_mutual_friends {
    has person1_name: str;
    has person2_name: str;

    can find_efficiently with `root entry {
        # Direct graph traversal - no nested loops
        person1 = [-->(`?Person)](?name == self.person1_name);
        person2 = [-->(`?Person)](?name == self.person2_name);

        if not person1 or not person2 {
            report {"error": "Person not found"};
            return;
        }

        # Get friends using graph navigation
        person1_friends = [person1[0] --> Friend --> Person];
        person2_friends = [person2[0] --> Friend --> Person];

        # Efficient set intersection
        mutual_names = {f.name for f in person1_friends} & {f.name for f in person2_friends};

        report {
            "mutual_friends": list(mutual_names),
            "count": len(mutual_names)
        };
    }
}
```
```jac
# basic_friend_finder.jac
walker find_friends_of_friends {
    has person_name: str;
    has max_depth: int = 2;
    has visited: set[str] = set();
    has results: set[str] = set();

    can traverse_network with `root entry {
        start_person = [-->(`?Person)](?name == self.person_name);

        if not start_person {
            report {"error": "Person not found"};
            return;
        }

        # Start traversal from the person
        self.traverse_from_person(start_person[0], self.max_depth);

        # Remove the starting person from results
        self.results.discard(self.person_name);

        report {
            "person": self.person_name,
            "friends_of_friends": list(self.results),
            "total_found": len(self.results)
        };
    }

    def traverse_from_person(person: Person, remaining_depth: int) {
        if remaining_depth <= 0 or person.name in self.visited {
            return;
        }

        self.visited.add(person.name);
        self.results.add(person.name);

        # Navigate to friends and continue traversal
        friends = [person --> Friend --> Person];
        for friend in friends {
            self.traverse_from_person(friend, remaining_depth - 1);
        }
    }
}
```
```jac
# optimized_friend_finder.jac
import from collections { deque }

walker find_friends_optimized {
    has person_name: str;
    has max_depth: int = 2;

    can breadth_first_search with `root entry {
        start_person = [-->(`?Person)](?name == self.person_name);

        if not start_person {
            report {"error": "Person not found"};
            return;
        }

        # Use BFS for more predictable performance
        queue = deque([(start_person[0], 0)]);  # (person, depth)
        visited = {self.person_name};
        results = set();

        while queue {
            current_person, depth = queue.popleft();

            if depth >= self.max_depth {
                continue;
            }

            # Get friends efficiently
            friends = [current_person --> Friend --> Person];

            for friend in friends {
                if friend.name not in visited {
                    visited.add(friend.name);
                    results.add(friend.name);
                    queue.append((friend, depth + 1));
                }
            }
        }

        report {
            "person": self.person_name,
            "friends_of_friends": list(results),
            "total_found": len(results),
            "algorithm": "breadth_first"
        };
    }
}

# Cached version for repeated queries
walker find_friends_cached {
    has person_name: str;
    has max_depth: int = 2;

    can cached_search with `root entry {
        start_person = [-->(`?Person)](?name == self.person_name);

        if not start_person {
            report {"error": "Person not found"};
            return;
        }

        person = start_person[0];

        # Check if we have cached results
        cache_nodes = [person --> CacheEntry](?depth == self.max_depth);

        if cache_nodes {
            cache = cache_nodes[0];
            report {
                "person": self.person_name,
                "friends_of_friends": cache.friend_names,
                "total_found": len(cache.friend_names),
                "cached": true
            };
            return;
        }

        # Compute and cache results
        queue = deque([(person, 0)]);
        visited = {self.person_name};
        results = set();

        while queue {
            current_person, depth = queue.popleft();

            if depth >= self.max_depth {
                continue;
            }

            friends = [current_person --> Friend --> Person];
            for friend in friends {
                if friend.name not in visited {
                    visited.add(friend.name);
                    results.add(friend.name);
                    queue.append((friend, depth + 1));
                }
            }
        }

        # Cache the results
        cache = CacheEntry(
            depth=self.max_depth,
            friend_names=list(results),
            computed_at="2024-01-15"
        );
        person ++> cache;

        report {
            "person": self.person_name,
            "friends_of_friends": list(results),
            "total_found": len(results),
            "cached": false
        };
    }
}
```
```jac
# memory_optimized.jac
# Use lightweight nodes for large-scale networks
node LightPerson {
    has name: str;
    has age: int;
    # Remove unnecessary cached data to save memory

    def get_friend_count() -> int {
        # Calculate on-demand instead of caching
        return len([self --> (`?Friend) --> (`?LightPerson)]);
    }

    def get_connections_summary() -> dict {
        friends = [self --> (`?Friend) --> (`?LightPerson)];

        return {
            "friend_count": len(friends),
            "avg_age": sum(f.age for f in friends) / len(friends) if friends else 0,
            "friend_names": [f.name for f in friends[:5]]  # Limit for memory
        };
    }
}

# Memory-conscious walker with cleanup
walker find_friends_memory_efficient {
    has person_name: str;
    has max_depth: int = 2;
    has batch_size: int = 100;  # Process in batches

    can memory_conscious_search with `root entry {
        start_person = [-->](`?LightPerson)(?name == self.person_name);

        if not start_person {
            report {"error": "Person not found"};
            return;
        }

        results = [];
        processed = 0;
        queue = deque([(start_person[0], 0)]);
        visited = {self.person_name};

        while queue and processed < self.batch_size {
            current_person, depth = queue.popleft();
            processed += 1;

            if depth >= self.max_depth {
                continue;
            }

            # Get only essential friend data
            friends = [current_person --> Friend --> LightPerson];

            for friend in friends[:10] {  # Limit friends per iteration
                if friend.name not in visited {
                    visited.add(friend.name);
                    results.append({
                        "name": friend.name,
                        "age": friend.age,
                        "depth": depth + 1
                    });

                    if depth + 1 < self.max_depth {
                        queue.append


## From: chapter_15.md

```jac
        walker create_chat_room {
            has room_name: str;

            can setup_room with `root entry {
                new_room = ChatRoom(
                    name=self.room_name,
                    created_at="2024-01-15"
                );
                here ++> new_room;

                report {
                    "room_id": new_room.id,
                    "name": new_room.name,
                    "max_users": chat_config["max_users"]
                };
            }
        }
```

```jac
        walker join_room {
            has room_name: str;
            has username: str;

            can join_chat with `root entry {
                # Find or create room
                room = [-->(`?ChatRoom)](?name == self.room_name);

                if not room {
                    # Check room limit
                    total_rooms = len([-->(`?ChatRoom)]);
                    if total_rooms >= config["max_rooms"] {
                        report {"error": "Maximum rooms reached"};
                        return;
                    }

                    room = ChatRoom(name=self.room_name);
                    here ++> room;
                } else {
                    room = room[0];
                }

                # Check user limit
                if len(room.users) >= config["max_users_per_room"] {
                    report {"error": "Room is full"};
                    return;
                }

                # Add user if not already in room
                if self.username not in room.users {
                    room.users.append(self.username);
                }

                report {
                    "room": room.name,
                    "users": room.users,
                    "user_count": len(room.users)
                };
            }
        }
```

```jac
        walker join_room {
            has room_name: str;
            has username: str;

            obj __specs__ {
                static has auth: bool = False;
            }

            can join_chat with `root entry {
                # Find or create room
                room = [-->(`?ChatRoom)](?name == self.room_name);

                if not room {
                    # Check room limit
                    total_rooms = len([-->(`?ChatRoom)]);
                    if total_rooms >= int(getenv("MAX_ROOMS", "100")) {
                        report {"error": "Maximum rooms reached"};
                        return;
                    }

                    room = ChatRoom(name=self.room_name);
                    here ++> room;
                } else {
                    room = room[0];
                }

                # Check user limit
                if len(room.users) >= int(getenv("MAX_USERS_PER_ROOM", "100")) {
                    report {"error": "Room is full"};
                    return;
                }

                # Add user if not already in room
                if self.username not in room.users {
                    room.users.append(self.username);
                }

                report {
                    "room": room.name,
                    "users": room.users,
                    "user_count": len(room.users)
                };
                # return room;
            }
        }


        walker send_message {
            has room_name: str;
            has username: str;
            has message: str;

            obj __specs__ {
                static has auth: bool = False;
            }

            can process_message with `root entry {
                # Find the room
                room = [-->(`?ChatRoom)](?name == self.room_name);

                if not room {
                    report {"error": "Room not found"};
                    return;
                }

                room = room[0];

                # Check if user is in room
                if self.username not in room.users {
                    report {"error": "User not in room"};
                    return;
                }

                # Add message
                new_message = room.add_message(self.username, self.message);

                report {
                    "status": "message_sent",
                    "message_id": new_message.id,
                    "timestamp": new_message.timestamp
                };
            }
        }

        walker get_chat_history {
            has room_name: str;
            has limit: int = 20;

            obj __specs__ {
                static has auth: bool = False;
            }

            can fetch_history with `root entry {
                room = [-->(`?ChatRoom)](?name == self.room_name);

                if room {
                    messages = room[0].get_recent_messages(self.limit);
                    report {"room": self.room_name, "messages": messages};
                } else {
                    report {"error": "Room not found"};
                }
            }
        }
```

```jac
    # Webhook receiver walker
    walker receive_webhook {
        has source: str = "unknown";
        has event_type: str;
        has data: dict;

        can process_webhook with `root entry {
            # Log the webhook
            webhook_log = WebhookLog(
                source=self.source,
                event_type=self.event_type,
                data=self.data,
                received_at=datetime.now().isoformat()
            );
            here ++> webhook_log;

            # Process different webhook types
            if self.source == "github" and self.event_type == "push" {
                self.handle_github_push();
            } elif self.source == "slack" and self.event_type == "message" {
                self.handle_slack_message();
            } else {
                print(f"Unknown webhook: {self.source}/{self.event_type}");
            }

            report {"status": "webhook_processed", "log_id": webhook_log.id};
        }

        can handle_github_push() {
            # Extract commit information
            commits = self.data.get("commits", []);
            repo_name = self.data.get("repository", {}).get("name", "unknown");

            # Send notification to chat
            for commit in commits {
                message = f"🔨 New commit in {repo_name}: {commit.get('message', 'No message')}";
                self.send_to_chat("dev-updates", "GitBot", message);
            }
        }

        can handle_slack_message() {
            # Forward Slack messages to our chat
            user = self.data.get("user_name", "SlackUser");
            text = self.data.get("text", "");
            channel = self.data.get("channel_name", "general");

            message = f"[Slack] {text}";
            self.send_to_chat(channel, user, message);
        }

        can send_to_chat(room_name: str, sender: str, message: str) {
            # Find or create room
            room = [-->(`?ChatRoom)](?name == room_name);
            if not room {
                room = ChatRoom(name=room_name);
                here ++> room;
            } else {
                room = room[0];
            }

            # Add message
            room.add_message(sender, message);
        }
    }

    walker get_webhook_logs {
        has source: str = "";
        has limit: int = 50;

        can fetch_logs with `root entry {
            all_logs = [-->(`?WebhookLog)];

            # Filter by source if specified
            if self.source {
                filtered_logs = [log for log in all_logs if log.source == self.source];
            } else {
                filtered_logs = all_logs;
            }

            # Get recent logs
            recent_logs = filtered_logs[-self.limit:];

            report {
                "logs": [
                    {
                        "source": log.source,
                        "event_type": log.event_type,
                        "received_at": log.received_at
                    }
                    for log in recent_logs
                ],
                "total": len(filtered_logs)
            };
        }
    }
```

```jac
    walker log_activity {
        has level: str = "info";
        has message: str;
        has context: dict = {};

        can record_log with `root entry {
            # Create log entry
            log_entry = LogEntry(
                level=self.level,
                message=self.message,
                timestamp=datetime.now().isoformat(),
                context=self.context
            );
            here ++> log_entry;

            # Also log to system logger
            if self.level == "error" {
                logger.error(f"{self.message} | Context: {self.context}");
            } elif self.level == "warning" {
                logger.warning(f"{self.message} | Context: {self.context}");
            } else {
                logger.info(f"{self.message} | Context: {self.context}");
            }

            report {"log_id": log_entry.id, "logged_at": log_entry.timestamp};
        }
    }

    # Enhanced chat with logging
    walker send_logged_message {
        has room_name: str;
        has username: str;
        has message: str;

        can send_with_logging with `root entry {
            # Log the attempt
            log_activity(
                level="info",
                message="Message send attempt",
                context={
                    "room": self.room_name,
                    "user": self.username,
                    "message_length": len(self.message)
                }
            ) spawn here;

            # Find room
            room = [-->(`?ChatRoom)](?name == self.room_name);

            if not room {
                log_activity(
                    level="warning",
                    message="Message failed - room not found",
                    context={"room": self.room_name, "user": self.username}
                ) spawn here;

                report {"error": "Room not found"};
                return;
            }

            room = room[0];

            # Check if user can send
            if self.username not in room.users {
                log_activity(
                    level="warning",
                    message="Message failed - user not in room",
                    context={"room": self.room_name, "user": self.username}


## From: env_vars.md

```jac
walker check_config {
    can enter with `root entry {
        if not env("DATABASE_HOST") {
            print("Warning: DATABASE_HOST not set, using default");
        }
    }
}
```


## From: logging.md

```json
{
  "timestamp": "2024-04-10T14:25:36.789Z",
  "level": "INFO",
  "message": "Request processed successfully",
  "request": {
    "method": "POST",
    "path": "/walker/create_user",
    "headers": {"authorization": "Bearer ***", "content-type": "application/json"},
    "body": {"username": "example_user", "email": "user@example.com"}
  },
  "response": {
    "status_code": 200,
    "body": {"status": 200, "reports": ["User created successfully"]}
  },
  "duration": 125,
  "client_ip": "192.168.1.1"
}
```

### Monitoring User Activity

```bash
grep '/walker/login' /tmp/jac_cloud_logs/jac-cloud.log |
  jq '.request.body.username'
```


## From: websocket.md

You can declare a walker to handle WebSocket connections by setting the `methods` property to include `"websocket"` in the `__specs__` configuration:

```jac
walker your_event_name {
    has val: int;

    can enter with `root entry {
        report "Do something!";
    }

    class __specs__ {
        has methods: list = ["websocket"];
    }
}
```

**Note**: WebSocket walkers can still work with other HTTP methods; however, they currently don't support file uploads.

### 1. Walker Event

Triggers a walker just like a REST API call:

```python
{
    # event type
	"type": "walker",

    # walker's name
	"walker": "your_event_name",

    # if you want to receive a notification for response
	"response": true,

    # walker's request context
	"context": {
        "val": 1
    }
}
```

### Server-Side (Jac)

```jac
"""Websocket scenarios."""
import from jac_cloud.plugin {WEBSOCKET_MANAGER as socket}

###########################################################
#                   WEBSOCKET ENDPOINTS                   #
###########################################################

walker send_chat_to_user {
    has root_id: str;

    can enter1 with `root entry {
        _root = &(self.root_id);

        socket.notify_users([_root], {"type": "chat", "data": {"message": "string"}});
    }

    class __specs__ {
        has methods: list = ["websocket", "post"];
    }
}


walker send_chat_to_group {
    has channel_id: str;

    can enter1 with `root entry {
        socket.notify_channels([self.channel_id], {"type": "chat", "data": {"message": "string"}});
    }

    class __specs__ {
        has methods: list = ["websocket", "post"];
    }
}

walker send_chat_to_client {
    has client_id: str;

    can enter1 with `root entry {
        socket.notify_clients([self.client_id], {"type": "chat", "data": {"message": "string"}});
    }

    class __specs__ {
        has methods: list = ["websocket", "post"];
    }
}
```

```js
// TRIGGER WALKER EVENT
client.send(JSON.stringify({
	"type": "walker",
	"walker": "your_walker_name",
	"response": true,
	"context": {}
}));
```


## From: webhook.md

## What are Webhooks?

Webhooks are a way for external services to securely call your Jac Cloud application when certain events occur. Unlike regular authenticated walkers (which are associated with a specific user), webhook walkers are directly linked to the root node and are secured with API keys rather than user tokens.

## Key Features

- **Customizable**: You can specify allowed walkers, nodes, and expiration dates for each API key

## Creating a Webhook Walker

To declare a walker as a webhook endpoint, add a `webhook` configuration to the `__specs__` class:

```jac
walker webhook {
    can enter1 with `root entry {
        report here;
    }

    class __specs__ {
        has webhook: dict = {
            "type": "header | query | path | body",  # optional: defaults to header
            "name": "any string"                     # optional: defaults to X-API-KEY
        };
    }
}
```

| Parameter | Description |
|---|---|
| walkers | A list of specific walker names that are permitted to use this key. If this list is empty, all walkers are allowed. |

```python
{
  "name": "webhook1",
  "walkers": ["webhook"],
  "nodes": ["root"],
  "expiration": {
    "count": 60,
    "interval": "days"
  }
}
```

```python
{
  "id": "672203ee093fd3d208a4b6d4",
  "name": "test",
  "root_id": "6721f000ee301e1d54c3de3d",
  "walkers": ["webhook"],
  "nodes": ["root"],
  "expiration": "2025-12-24T10:01:18.206000",
  "key": "6721f000ee301e1d54c3de3d:1730282478:P4Nrs3DOLIkaw5aYsbIWNzWZZAwEyb20"
}
```

## Webhook Implementation Examples

Here are examples of different webhook implementations:

### 1. Using Header for API Key (Default)

```jac
walker webhook_by_header {
    can enter1 with `root entry {
        report here;
    }

    class __specs__ {
        has webhook: dict = {
            "type": "header",
            "name": "test-key"
        };
    }
}
```

**Example Request:**

```bash
curl -X 'POST' 'http://localhost:8001/webhook/walker/webhook_by_header' \
  -H 'test-key: YOUR-GENERATED-KEY'
```

### 2. Using Query Parameter for API Key

```jac
walker webhook_by_query {
    can enter1 with `root entry {
        report here;
    }

    class __specs__ {
        has webhook: dict = {
            "type": "query",
            "name": "test_key"
        };
    }
}
```

**Example Request:**

```bash
curl -X 'POST' 'http://localhost:8001/webhook/walker/webhook_by_query?test_key=YOUR-GENERATED-KEY'
```

### 3. Using Path Parameter for API Key

```jac
walker webhook_by_path {
    can enter1 with `root entry {
        report here;
    }

    class __specs__ {
        has webhook: dict = {
            "type": "path",
            "name": "test_key"  # name and the path var should be the same
        }, path: str = "/{test_key}";
    }
}
```

**Example Request:**

```bash
curl -X 'POST' 'http://localhost:8001/webhook/walker/webhook_by_path/YOUR-GENERATED-KEY'
```

### 4. Using Request Body for API Key

```jac
walker webhook_by_body {
    can enter1 with `root entry {
        report here;
    }

    class __specs__ {
        has webhook: dict = {
            "type": "body",
            "name": "test_key"
        };
    }
}
```

**Example Request:**

```bash
curl -X 'POST' 'http://localhost:8001/webhook/walker/webhook_by_body' -d '{"test_key": "YOUR-GENERATED-KEY"}'
```
2. **Limit Walker Access**: Specify only the walkers that should be accessible for each key.
4. Confirm the walker and node are allowed for the API key
- Explore [Task Scheduling](scheduler.md) for running walkers on a schedule


## From: scheduler.md

To configure a scheduled walker, add a `schedule` dictionary to the walker's `__specs__` configuration. The schedule supports three trigger types:

1. **Cron** - Schedule using cron expressions
2. **Interval** - Schedule at regular time intervals
3. **Date** - Schedule at a specific date and time

### Cron Example

```jac
walker walker_cron {
    has arg1: int;
    has arg2: str;
    has kwarg1: int = 3;
    has kwarg2: str = "4";

    can enter with `root entry {
        print("I am a scheduled walker!")
    }

    class __specs__ {
        has private: bool = True;
        has schedule: dict = {
            "trigger": "cron",
            "args": [1, "2"],
            "kwargs": {
                "kwarg1": 30,
                "kwarg2": "40"
            },
            # Run every day at midnight
            "hour": "0",
            "minute": "0",
            "save": True
        };
    }
}
```

### Interval Example

```jac
walker walker_interval {
    has arg1: int;
    has arg2: str;
    has kwarg1: int = 3;
    has kwarg2: str = "4";

    can enter with `root entry {
        print("I am a scheduled walker running every 5 seconds!");
    }

    class __specs__ {
        has private: bool = True;
        has schedule: dict = {
            "trigger": "interval",
            "args": [1, "2"],
            "kwargs": {
                "kwarg1": 30,
                "kwarg2": "40"
            },
            "seconds": 5,
            "save": True
        };
    }
}
```

### Date Example

```jac
walker walker_date {
    has arg1: int;
    has arg2: str;
    has kwarg1: int = 3;
    has kwarg2: str = "4";

    can enter with `root entry {
        print("I am a scheduled walker running once at a specific time!");
    }

    class __specs__ {
        has private: bool = True;
        has schedule: dict = {
            "trigger": "date",
            "args": [1, "2"],
            "kwargs": {
                "kwarg1": 30,
                "kwarg2": "40"
            },
            "run_date": "2025-04-30T11:12:00+00:00",
            "save": True
        };
    }
}
```
```jac
walker get_or_create_counter {
    can enter1 with `root entry {
        tc = TaskCounter();
        here ++> tc;

        report tc;
    }

    can enter2 with TaskCounter entry {
        report here;
    }
}

walker increment_counter {
    has val: int;

    can enter with TaskCounter entry {
        here.val += self.val;
    }

    class __specs__ {
        has private: bool = True;
    }
}

walker trigger_counter_task {
    can enter with `root entry {
        tcs = [-->(`?TaskCounter)];
        if tcs {
            report create_task(increment_counter(val=1), tcs[0]);
        }
    }
}
```


## From: introduction.md

- Automatically converts Jac walkers into REST endpoints
- **Walker Endpoints**: Automatic REST API generation from walker declarations
- [Walker Endpoints](quickstart.md#walker-endpoints) - Learn how to configure API endpoints


## From: chapter_14.md

```jac
        walker create_note {
            has title: str;
            has content: str;
            has owner: str;

            can create_user_note with `root entry {
                # Create note with specified owner
                new_note = Note(
                    title=self.title,
                    content=self.content,
                    owner=self.owner
                );
                here ++> new_note;

                report {
                    "message": "Note created successfully",
                    "id": new_note.id,
                    "owner": new_note.owner
                };
            }
        }

        walker get_my_notes {
            has user_id: str;

            can fetch_user_notes with `root entry {
                # Filter by specified user
                my_notes = [-->(`?Note)](?owner == self.user_id);

                notes_data = [
                    {"id": n.id, "title": n.title, "created_at": n.created_at}
                    for n in my_notes
                ];

                report {"notes": notes_data, "total": len(notes_data)};
            }
        }
```
```jac
        walker create_note {
            has title: str;
            has content: str;
            has owner: str;
            has is_private: bool = True;

            obj __specs__ {
                static has auth: bool = False;
            }

            can add_note with `root entry {
                new_note = Note(
                    title=self.title,
                    content=self.content,
                    owner=self.owner,
                    is_private=self.is_private
                );
                here ++> new_note;

                report {
                    "status": "created",
                    "note_id": new_note.id,
                    "private": new_note.is_private
                };
            }
        }

        walker list_my_notes {
            has user_id: str;

            obj __specs__ {
                static has auth: bool = False;
            }

            can get_user_notes with `root entry {
                # Only get notes owned by specified user
                user_notes = [-->(`?Note)](?owner == self.user_id);

                report {
                    "user": self.user_id,
                    "notes": [
                        {
                            "id": n.id,
                            "title": n.title,
                            "private": n.is_private
                        }
                        for n in user_notes
                    ],
                    "count": len(user_notes)
                };
            }
        }
```
```jac
    walker create_note {
        has title: str;
        has content: str;
        has owner: str;
        has is_public: bool = False;

        obj __specs__ {
            static has auth: bool = False;
        }

        can add_note with `root entry {
            new_note = Note(
                title=self.title,
                content=self.content,
                owner=self.owner,
                is_public=self.is_public
            );
            here ++> new_note;

            report {
                "status": "created",
                "note_id": new_note.id,
                "public": new_note.is_public
            };
        }
    }

    walker share_note {
        has note_id: str;
        has current_user: str;
        has target_user: str;
        has permission_level: str = "read";  # "read" or "write"

        obj __specs__ {
            static has auth: bool = False;
        }

        can add_sharing_permission with `root entry {
            target_note = [-->(`?Note)](?id == self.note_id);

            if not target_note {
                report {"error": "Note not found"};
                return;
            }

            note = target_note[0];

            # Only owner can share notes
            if note.owner != self.current_user {
                report {"error": "Only note owner can share"};
                return;
            }

            # Add user to shared list if not already there
            if self.target_user not in note.shared_with {
                note.shared_with.append(self.target_user);
            }

            report {
                "message": f"Note shared with {self.target_user}",
                "permission": self.permission_level,
                "shared_count": len(note.shared_with)
            };
        }


## From: permission.md

```jac
# Allow User2 to read a post
walker grant_access {
    has target_root_id: str;  # ID of User2's root
    has access_level: str;    # ReadPerm, ConnectPerm, or WritePerm

    can grant_access with post entry {
        # Grant access to the current post
        _.allow_root(here, NodeAnchor.ref(self.target_root_id), self.access_level);
        report "Access granted!";
    }
}
```
```jac
# Remove User2's access to a post
walker revoke_access {
    has target_root_id: str;  # ID of User2's root

    can revoke_access with post entry {
        # Revoke access to the current post
        _.disallow_root(here, NodeAnchor.ref(self.target_root_id));
        report "Access revoked!";
    }
}
```
```jac
# Make a post readable by everyone
walker make_public {
    can make_public with post entry {
        # Grant READ access to all users
        grant(here, ReadPerm);
        report "Post is now public!";
    }
}
```
```jac
# Make a post private (owner-only)
walker make_private {
    can make_private with post entry {
        # Remove all access
        revoke(here);
        report "Post is now private!";
    }
}
```
```jac
# Create a public post
walker create_public_post {
    has content: str;

    can enter with `root entry {
        # Create the post
        post = Post({content: self.content});
        here ++> post;

        # Make it readable by everyone, but only writable by owner
        grant(post, ReadPerm);

        report "Public post created!";
    }
}
```
```jac
# Grant access to a team
walker grant_team_access {
    has team_members: list[str];  # List of root IDs
    has access_level: str;        # ReadPerm, ConnectPerm, or WritePerm

    can grant_access with document entry {
        # Grant access to each team member
        for member_id in self.team_members {
            _.allow_root(here, NodeAnchor.ref(member_id), self.access_level);
        }

        report "Team access granted!";
    }
}
```
```jac
# Only friends can see posts
walker check_access {
    has viewer_id: str;

    can check with post entry {
        owner = [post<--][0];

        # Check if viewer is friends with owner
        is_friend = False;
        for friend in [owner -->] {
            if friend.id == self.viewer_id {
                is_friend = True;
                break;
            }
        }

        if is_friend {
            # Grant access if they're friends
            _.allow_root(here, NodeAnchor.ref(self.viewer_id), "READ");
            report "Access granted to friend!";
        } else {
            report "Access denied - not a friend!";
        }
    }
}
```


## From: quickstart.md

Jac Cloud automatically converts your walker declarations into REST API endpoints. By default, each walker creates two endpoint groups:

| Endpoint Type | URL Pattern | Description |
|--------------|-------------|-------------|
| **Root Entry** | `/walker/{walker_name}` | Executes on the root |
| **Node Entry** | `/walker/{walker_name}/{node_id}` | Executes on a specific node |

To disable automatic endpoint generation, set the environment variable:
```bash
export DISABLE_AUTO_ENDPOINT=True
```
Control endpoint behavior using the `__specs__` object within your walker:

```jac
walker my_walker {
    has data: str;

    # This is where you configure your endpoint behavior
    obj __specs__ {
        static has methods: list = ["get", "post"];   # Supports both GET and POST
        static has auth: bool = False;                # No authentication required
        static has as_query: list = ["data"];         # "data" will be a query parameter
        static has private: bool = True;              # Skip auto endpoint generation from walker
    }
}
```
| **Setting** | **Type** | **Description** | **Default** |
|-------------|----------|-----------------|-------------|
| `methods` | `list[str]` | Allowed HTTP methods: `"get"`, `"post"`, `"put"`, `"delete"`, etc. | `["post"]` |
| `as_query` | `str \| list[str]` | Fields to treat as query parameters. Use `"*"` for all fields | `[]` |
| `auth` | `bool` | Whether endpoint requires authentication | `true` |
| `path` | `str` | If it starts with `/`, it will be the complete path. Otherwise, it will be prefixed with `/walker` (for walkers) or /`webhook/walker` (for webhooks). If not specified, it defaults to the walker's name with its respective prefix. | N/A |
| `private` | `bool` | Skip walker in auto-generation | `false` |
| `entry_type` | `str` | `"NODE"`, `"ROOT"`, or `"BOTH"` | `"BOTH"` |
Let's create a simple endpoint that returns the current time. For this example, we create a walker named `public_info` which provides one rest method `get` at the url `http://localhost:8000/walker/public_info`. The ability `get_current_time` will return the current timestamp in ISO format via the use of the `report` statement.

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
This example demonstrates how to create an endpoint from a walker that accepts query parameters for searching users. The walker `search_users` will allow users to search for a user by their username.

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
In this example, we will create a walker that allows users to upload a file. The walker `single_file_upload` will accept a single file and return the filename in the response. This shows how the walker can handle post requests with file uploads.

Since jac is a superset of Python, we can use the `UploadFile` type from FastAPI to handle file uploads.

First, we create the upload_file.jac file with the following content:
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
All walker endpoints return a standardized JSON response:

```json
{
    "status": 200,
    "reports": [
        "Any reports generated during walker execution"
    ],
    "returns": [
        "Walker return values (optional - requires SHOW_ENDPOINT_RETURNS=true)"
    ]
}
```
Jac Cloud automatically serializes walker, edge, and node archetypes:

```json
{
    "id": "unique_anchor_reference_id",
    "context": {
        "attribute1": "value1",
        "attribute2": "value2"
    }
}
```
To save a walker or object to memory (queued for later database commit):

```jac
# Save a walker instance
save(my_walker_instance)

# Save an object instance
save(my_object_instance)
```
- `DISABLE_AUTO_ENDPOINT=True` - Disable automatic endpoint generation
- `SHOW_ENDPOINT_RETURNS=True` - Include walker return values in responses
While not recommended, as you typically shouldn't change your API specifications in this manner, Jac Cloud does support manually creating walker endpoints.
This allows for advanced customization if absolutely necessary, but generally, you should rely on the automatic generation and configuration via **specs**.

Example Code snippet:

```
type("NameOfYourWalker", (_.Walker,), {
    "__specs__": your_specs_class,
    ... annotations / additional fields ...
})
```


## From: async_walker.md

Async walkers in Jac Cloud allow you to execute walkers asynchronously in separate threads. This is particularly useful for long-running operations that shouldn't block the main execution flow, such as intensive computations or external API calls.

To create an async walker, simply add the `async` keyword before the walker declaration:

```jac
async walker sample {
    has value: int = 0;

    can enter with `root entry {
        print("test");
        self.value = 1;
    }
}
```

Key characteristics:

- Executes in a separate thread without blocking the main application
- Returns immediately with a reference ID while continuing execution in the background
- Similar to task scheduling but with a simpler syntax
- Results can be retrieved later using the walker ID

How It Works
1. When an async walker is triggered, it's scheduled as a background task
2. The API call returns immediately with a walker ID reference
3. The walker executes asynchronously in its own thread
4. Results are stored in the database and can be retrieved later

Response Format
When you call an async walker, you receive a response containing the walker's unique ID:

```json
{
  "status": 200,
  "walker_id": "w:sample:550e8400-e29b-41d4-a716-446655440000"
}
```

Retrieving Results
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

Available Status Information
The `__jac__.schedule` object contains all execution metadata:

| **Field**       | **Description**                                                |
| --------------- | -------------------------------------------------------------- |
| `status`        | Current execution status (pending, running, completed, failed) |
| `node_id`       | ID of the node where the walker was executed                   |
| `root_id`       | ID of the root node of the user who triggered the walker       |
| `execute_date`  | When the walker was scheduled to execute                       |
| `executed_date` | When the walker actually executed                              |
| `http_status`   | HTTP status code for the execution result                      |
| `reports`       | Any values reported during walker execution                    |
| `custom`        | Custom metadata associated with the walker                     |
| `error`         | Error message if execution failed                              |
Even though those fields are available, we still recommend using a walker's attribute as your status checker for more customizable and direct status updates.

Example: Long-Running Process

```jac
async walker process_large_dataset {
    has dataset_id: str;
    has results: list = [];

    can enter with `root entry {
        # Simulate long-running process
        dataset = get_dataset(self.dataset_id);

        for item in dataset{
            # Do intensive processing
            processed = complex_computation(item);
            self.results.append(processed);
        }

        # Final result is stored in the walker
        print("Processing complete!");
    }
}

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

Common Use Cases
1. Processing Large Datasets

```jac
async walker analyze_data {
    has dataset_id: str;
    has summary: dict = {};

    can enter with `root entry {
        # Fetch data (could take minutes)
        data = fetch_dataset(self.dataset_id);

        # Process each item (CPU intensive)
        for item in data{
            process_item(item);
        }

        # Generate final summary
        self.summary = create_summary(data);
    }
}
```

2. Generating Reports

```jac
async walker generate_report {
    has user_id: str;
    has report_type: str;
    has report_url: str;

    can enter with `root entry {
        # Collect user data
        user_data = fetch_user_data(self.user_id);

        # Generate PDF (slow operation)
        report_file = create_pdf_report(user_data, self.report_type);

        # Upload to storage
        self.report_url = upload_file(report_file);

        # Optional: Notify user
        send_email(self.user_id, "Your report is ready!", self.report_url);
    }
}
```

3. External API Integration

```jac
async walker sync_with_external_system {
    has account_id: str;
    has sync_status: str = "pending";
    has sync_results: list = [];

    can enter with `root entry {
        # Connect to external API
        self.sync_status = "connecting";
        api_client = connect_to_api();

        # Fetch data (network-bound, can be slow)
        self.sync_status = "fetching";
        external_data = api_client.fetch_account_data(self.account_id);

        # Process and save data
        self.sync_status = "processing";
        for item in external_data{
            result = process_and_save(item);
            self.sync_results.append(result);
        }

        self.sync_status = "complete";
    }
}
```

Advanced Techniques
Combining with WebSockets for Real-time Updates

```jac
import from jac_cloud.plugin {WEBSOCKET_MANAGER as socket}

async walker process_with_updates {
    has client_id: str;
    has progress: int = 0;

    can enter with `root entry {
        # Send initial notification
        socket.notify_clients([self.client_id], {
            "type": "progress",
            "data": {"progress": 0}
        });

        # Process in chunks and send updates
        for i in range(10){
            process_chunk(i);
            self.progress = (i+1) * 10;

            # Send progress update via WebSocket
            socket.notify_clients([self.client_id], {
                "type": "progress",
                "data": {"progress": self.progress}
            });
        }

        # Send completion notification
        socket.notify_clients([self.client_id], {
            "type": "complete",
            "data": {"message": "Processing complete!"}
        });
    }
}
```

Error Handling

```jac
async walker safe_process {
    has input_id: str;
    has success: bool = False;
    has error_message: str = "";
    has results: dict = {};

    can enter with `root entry {
        try {
            # Attempt processing
            data = fetch_data(self.input_id);
            if not data{
                self.error_message = "No data found";
                return;
            }

            self.results = process_data(data);
            self.success = True;
        } except e {
            # Capture error details
            self.error_message = str(e);
            log_error(self.input_id, str(e));
        }
    }
}
```


## From: sequence.md

```jac
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


## From: jaclang.md

- **Node Spawn Walker supported**: Spawning walker on a node with `jac serve` is supported.
- **Optional Ability Names**: Ability declarations now support optional names, enabling anonymous abilities with event clauses (e.g., `can with entry { ... }`). When a name is not provided, the compiler automatically generates a unique internal name based on the event type and source location. This feature simplifies walker definitions by reducing boilerplate for simple entry/exit abilities.
- **Typed Context Blocks (OSP)**: Fully implemented typed context blocks (`-> NodeType { }` and `-> WalkerType { }`) for Object-Spatial Programming, enabling conditional code execution based on runtime types.
- **Support Spawning a Walker with List of Nodes and Edges**: Introduced the ability to spawn a walker on a list of nodes and edges. This feature enables initiating traversal across multiple graph elements simultaneously, providing greater flexibility and efficiency in handling complex graph structures.
- **Queue Insertion Index for Visit Statements**: Visit statements


## From: llmdocs.md

### Mini (Recommended)
- Objects, nodes, edges, walkers


## From: nodes_and_edges.md

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


## From: filtering.md

## Node-Based Filtering

Node-based filtering restricts traversal to specific nodes that satisfy predefined conditions. This is useful when you need to:

- Limit traversal to nodes with certain attributes or properties.
- Filter nodes dynamically based on walker state or external context.


## From: walkers.md

Walkers are "worker bots" that move (walk) along the graph while performing tasks on the nodes they visit.

They play a crucial role in executing visit-dependent abilities as discussed in nodes and facilitating interactions between graph nodes and themselves.

## Spawning a Walker
A walker can be spawned at any point on the graph with the ```spawn``` keyword.

=== "Jac"
    <div class="code-block">
    ```jac
    --8<-- "jac/examples/data_spatial/define_walker.jac"
    ```
    </div>
??? example "Graph"
    ```mermaid
    flowchart LR
    0 -->|"a()"| 1
    1 -->|"a()"| 2
    2 -->|"a()"| 3
    1 -->|"a()"| 4
    4 -->|"a()"| 5
    0["Root()"]
    1["A(val=5)"]
    2["A(val=10)"]
    3["A(val=15)"]
    4["A(val=20)"]
    5["A(val=25)"]
    ```

## Graph Traversal Using Visit
Walkers navigate the graph using the ```visit``` keyword.
=== "visiting_node.jac"
    ```jac linenums="1"
    visit [node_name]; # Visits a particular node
    ```
=== "visiting_sucessor.jac"
    ```jac linenums="1"
    visit [node_name-->]; # Visits successive nodes of a node
    ```
=== "visiting_predecessor.jac"
    ```jac linenums="1"
    visit [<--node_name]; # Visits predecessor nodes of a node
    ```
## Attributes & Abilities
- Similar to nodes, walkers can have their own attributes and abilities including both callable and visit-dependent abilities.

- **Visit-dependent Abilities:**
    - Ensures the ability is executed only when the walker visits a node.
    - Can be defined within:
        - **Nodes:** Triggered upon a walker's arrival.
        - **Walkers:** Specific to the walker’s operation during its visit.
## Reference Keywords:
- ```self``` : Refers to the walker object itself.
- ```here```: References the current node visited by the walker, enabling access to its attributes and callable abilities.
    This allows seamless interaction between walker and node attributes.

- Control Movement:
    - Use ```visit``` to:
        - Direct the walker to a specific node.
        - Walk along an edge connecting nodes.

- Remove Walkers:
    - Use ```disengage``` to remove a walker from the graph.

## Walkers in Action:
- Walkers prioritize their visit-dependent abilities first before executing the abilities of the visited node.
- This enables flexible task delegation:
    - Define visit-dependent tasks either within the walker or in the node.

By using these principles, walkers can efficiently traverse and interact with graphs, enabling dynamic workflows.

### Example:
=== "Jac"
    <div class="code-block">
    ```jac
    --8<-- "jac/examples/data_spatial/ds_entry_exit.jac"
    ```
    </div>

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

- A walker is an archetype that performs actions within the graph. It can traverse nodes through edges, performing operations at each step.
```jac
walker walker_name {
  can walker_ability with `specific_node entry;
}
```
- You can spawn a walker from a specific node or root:
```jac
    with entry {
      root spawn walker_name();
    }
```
- Walkers can inherit from other walkers and override their abilities:
```jac
    walker walker_1{
    }
    walker walker_2 : walker_1:{
    }
```
- To override a walker’s ability:
```jac
    walker walker_1{
      can ability_1 with `root entry{
          print("write");
      }
    }
    walker walker_2 : walker_1:{
      override can ability_1 with `root entry{
          print("override");
      }
    }
```


## From: Overview.md

## Object Spatial Programming

Your application uses Jac's Object Spatial Programming to create a clean, modular design:

**Walkers** move through your node network, carrying information and executing logic. They represent the actions your system can perform.

The combination of Object Spatial Programming, Mean Typed Programming, and modular tool architecture gives you a solid base for creating intelligent, scalable applications.

Your application exposes these main endpoints:

- `POST /walker/upload_file` — Upload files (requires authentication)
- `POST /walker/interact` — Chat with the AI (requires authentication)


## From: friendzone-lite.md

- **Update Walker**: Handles user interactions and memory updates


## From: agentic_ai.md

**Walkers**: Entities spawned on the graph that traverse it, triggering node abilities and serving as the execution engine. In agentic systems, walkers are the orchestrators that coordinate task flow and decision-making across agents.

The `walker task_manager` is the orchestrator—the "brain" of the agentic system. Unlike agents (nodes) which are passive and reactive, the orchestrator is **active** and **proactive**. It:

1. Receives the user's high-level goal (utterance)
2. Plans decomposition into subtasks using the LLM
3. Routes each subtask to the appropriate agent
4. Manages execution flow across agents

The orchestrator demonstrates how **walkers coordinate multi-agent systems**. Because walkers can traverse the graph and visit nodes, they provide the perfect mechanism for implementing orchestration logic.

**Walker Execution**

The walker executes in three steps:

1. **Plan**: Call the LLM to decompose the user's request into a list of subtasks
2. **Map**: For each subtask, map the `agent_type` to its corresponding node class (TaskHandling → TaskHandling, EmailHandling → EmailHandling, etc.)
3. **Execute**: Ensure a node instance exists on the graph, set the current task on the walker, and `visit` the node to trigger its `can execute` ability

This pattern is powerful because it separates **strategy** (what needs to be done) from **execution** (how it's done). The walker handles strategy via the LLM, while agents handle execution through their entry abilities.

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

    # Step 3: Execute - route and visit each agent
    for subtask in subtasks {
      node_type = node_map[subtask.agent_type];
      routed_node = [-->(`?node_type)];  # Check if agent exists
      if not routed_node {
        routed_node = here ++> node_type();  # Create if doesn't exist
      }
      self.cur_task = subtask;  # Pass subtask to agent
      visit routed_node;  # Trigger agent's can execute ability
    }
  }
}
```


## From: tutorial.md

### 3. Walkers: Make Things Happen

**Walkers** move through your graph and perform actions. They make your app interactive.

**Simple Example:**
```jac
walker create_tweet(visit_profile) {
    has content: str;
    can tweet with Profile entry;
}
```

This walker creates new tweets when users post messages.
### Step 3: Create User Profiles

When someone signs up, we create their profile:

```jac
walker visit_profile {
    can visit_profile with `root entry;
}

impl visit_profile.visit_profile {
    visit [-->(`?Profile)] else {
        new_profile = here ++> Profile();
        grant(new_profile[0], level=ConnectPerm);
        visit new_profile;
    }
}
```

**What this does:** Creates a new profile if one doesn't exist, or visits the existing profile.

### Step 4: Post Messages

Users can create and share posts:

```jac
walker create_tweet(visit_profile) {
    has content: str;
    can tweet with Profile entry;
}

impl create_tweet.tweet {
        embedding = vectorizer.fit_transform([self.content]).toarray().tolist();
        tweet_node = here +>:Post():+> Tweet(content=self.content, embedding=embedding);
        grant(tweet_node[0], level=ConnectPerm);
        report tweet_node;
}
```

**What this does:** Creates a new tweet with the user's message and connects it to their profile.

### Step 5: Follow Other Users

Build your network by following others:

```jac
walker follow_request {}

impl Profile.follow {
    current_profile = [root-->(`?Profile)];
    current_profile[0] +>:Follow():+> self;
    report self;
}
```

**What this does:** Creates a follow relationship between the current user and another user.

### Step 6: View Your Feed

See posts from people you follow:

```jac
walker load_feed(visit_profile) {
    has search_query: str = "";
    has results: list = [];
    can load with Profile entry;
}

impl load_feed.load {
    visit [-->(`?Tweet)];
    for user_node in [->:Follow:->(`?Profile)] {
        visit [user_node-->(`?Tweet)];
    }
    report self.results;
}
```

**What this does:** Collects tweets from the current user and everyone they follow.
- **Walkers** for creating functionality


## From: streamlit.md

```jac
            result = make_api_call(
                st.session_state.token,
                "walker/interact",
                {"message": user_input}
            );
```


## From: task-manager-lite.md

### Walker
- **task_manager**: Main walker that routes requests and coordinates responses


## From: jac_serve.md

3. Converts all walkers into REST APIs where:
   - Walker fields (has variables) become the API interface
   - An additional `target_node` field specifies where to spawn the walker

#### GET /walkers
List all available walkers in the module.

**Example:**
```bash
curl http://localhost:8000/walkers \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "walkers": ["CreateTask", "ListTasks", "CompleteTask"]
}
```

#### GET /walker/<name>
Get the field information for a specific walker.

**Example:**
```bash
curl http://localhost:8000/walker/CreateTask \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "name": "CreateTask",
  "info": {
    "fields": {
      "title": {
        "type": "str",
        "required": true,
        "default": null
      },
      "priority": {
        "type": "int",
        "required": false,
        "default": "1"
      },
      "target_node": {
        "type": "str (node ID, optional)",
        "required": false,
        "default": "root"
      }
    }
  }
}
```

#### POST /walker/<name>
Spawn a walker with the provided fields.

**Request Body:**
```json
{
  "fields": {
    "title": "Buy groceries",
    "priority": 2,
    "target_node": "optional-node-id"
  }
}
```

**Response:**
```json
{
  "result": "Walker executed successfully",
  "reports": []
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/walker/CreateTask \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"title": "Buy groceries", "priority": 2}}'
```

### 4. Create tasks using walkers
```bash
# Create first task
curl -X POST http://localhost:8000/walker/CreateTask \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"title": "Buy groceries", "priority": 2}}'

# Create second task
curl -X POST http://localhost:8000/walker/CreateTask \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"title": "Write documentation", "priority": 1}}'
```

### 5. List all tasks
```bash
curl -X POST http://localhost:8000/walker/ListTasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fields": {}}'
```

### 6. Complete a task
```bash
curl -X POST http://localhost:8000/walker/CompleteTask \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"title": "Buy groceries"}}'
```

1. **Automatic API Generation**: Functions and walkers automatically become REST endpoints

- The `target_node` field for walkers is optional and defaults to the user's root node
- If `target_node` is specified, it should be a valid node ID (hex string)
- All walker execution happens in the context of the authenticated user

