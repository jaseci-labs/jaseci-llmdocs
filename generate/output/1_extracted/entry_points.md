# entry_points


## From: sequence.md

```jac
with entry{
    root ++> Node(val = "a");
    root ++> Node(val = "b");
    root ++> Node(val = "c");

    Walker() spawn root;
}
```

