"""Tests for code extraction and classification."""

include:jac utils.patterns;
include:jac pipeline.extractor;

import:py re;

test "classify_code detects node definitions" {
    code = '''
node Person {
    has name: str;
    has age: int;
}
''';
    types = classify_code(code);
    assert "node" in types;
}

test "classify_code detects walker definitions" {
    code = '''
walker greeter {
    can greet with `root entry {
        print("Hello!");
    }
}
''';
    types = classify_code(code);
    assert "walker" in types;
    assert "can" in types;
    assert "with_entry" in types;
}

test "classify_code detects edge definitions" {
    code = '''
edge Connects {
    has weight: float = 1.0;
}
''';
    types = classify_code(code);
    assert "edge" in types;
}

test "classify_code detects obj definitions" {
    code = '''
obj Config {
    has debug: bool = False;
    has timeout: int = 30;
}
''';
    types = classify_code(code);
    assert "obj" in types;
}

test "classify_code detects enum definitions" {
    code = '''
enum Status {
    PENDING = "pending",
    ACTIVE = "active",
    DONE = "done"
}
''';
    types = classify_code(code);
    assert "enum" in types;
}

test "classify_code detects by_llm usage" {
    code = '''
can summarize(text: str) -> str
by llm(model=llm, temperature=0.5);
''';
    types = classify_code(code);
    assert "by_llm" in types;
    assert "can" in types;
}

test "classify_code detects spawn keyword" {
    code = '''
with entry {
    result = spawn walker_name();
}
''';
    types = classify_code(code);
    assert "spawn" in types;
    assert "with_entry" in types;
}

test "classify_code detects connect operators" {
    code = '''
node1 ++> node2;
parent <++> child;
a +> b;
''';
    types = classify_code(code);
    assert "connect" in types;
}

test "classify_code detects traverse operators" {
    code = '''
nodes = [-->];
back_nodes = [<--];
''';
    types = classify_code(code);
    assert "traverse" in types;
}

test "classify_code detects __specs__ endpoint" {
    code = '''
walker list_items {
    has __specs__: dict = {"path": "/api/items", "methods": ["GET"]};
}
''';
    types = classify_code(code);
    assert "__specs__" in types;
    assert "walker" in types;
}

test "classify_code detects async definitions" {
    code = '''
async walker fetcher {
    can run with `root entry {
        await do_fetch();
    }
}
''';
    types = classify_code(code);
    assert "async" in types;
    assert "walker" in types;
}

test "classify_code handles multiple constructs" {
    code = '''
node Person {
    has name: str;
}

walker greeter {
    can visit_person with Person entry {
        report here.name;
    }
}

with entry {
    p = spawn Person(name="Alice");
    spawn greeter() on p;
}
''';
    types = classify_code(code);
    assert "node" in types;
    assert "walker" in types;
    assert "can" in types;
    assert "spawn" in types;
    assert "with_entry" in types;
    assert "report" in types;
}

test "find_keywords detects edge operators" {
    code = "node1 ++> node2; parent <++> child;";
    keywords = find_keywords(code);
    assert "++>" in keywords;
    assert "<++>" in keywords;
}

test "find_keywords detects spawn and visit" {
    code = "result = spawn greeter(); visit [-->];";
    keywords = find_keywords(code);
    assert "spawn" in keywords;
    assert "visit" in keywords;
}

test "find_keywords detects here and self" {
    code = '''
can process with Node entry {
    print(here.name);
    self.count += 1;
}
''';
    keywords = find_keywords(code);
    assert "here" in keywords;
    assert "self" in keywords;
}

test "find_keywords detects by llm" {
    code = "can generate() -> str by llm(model=gpt4);";
    keywords = find_keywords(code);
    assert "by llm" in keywords;
}

test "find_keywords detects with entry/exit" {
    code = '''
can enter with Node entry { }
can leave with Node exit { }
''';
    keywords = find_keywords(code);
    assert "with entry" in keywords;
    assert "with exit" in keywords;
}

test "find_keywords detects root entry" {
    code = "can main with `root entry { }";
    keywords = find_keywords(code);
    assert "`root" in keywords;
}

test "find_keywords detects report and disengage" {
    code = '''
report data;
disengage;
''';
    keywords = find_keywords(code);
    assert "report" in keywords;
    assert "disengage" in keywords;
}

test "find_patterns detects critical syntax" {
    text = '''
node Person { has name: str; }
walker greeter {
    can greet with entry { spawn helper(); }
}
by llm()
import:py json;
''';
    patterns = find_patterns(text);
    assert "node definition" in patterns;
    assert "walker definition" in patterns;
    assert "has x: type" in patterns;
    assert "with entry" in patterns;
    assert "spawn" in patterns;
    assert "by llm()" in patterns;
    assert "import:py" in patterns;
    assert "ability definition" in patterns;
}

test "validate_code_blocks with balanced fences" {
    text = '''
Some text
```jac
code here
```
More text
```python
more code
```
''';
    (valid, issue) = validate_code_blocks(text);
    assert valid == True;
    assert issue is None;
}

test "validate_code_blocks with unbalanced fences" {
    text = '''
```jac
code here

Missing closing fence
''';
    (valid, issue) = validate_code_blocks(text);
    assert valid == False;
    assert issue == "Unbalanced code fences";
}

test "validate_code_blocks with no fences" {
    text = "Just plain text without any code blocks.";
    (valid, issue) = validate_code_blocks(text);
    assert valid == True;
    assert issue is None;
}

test "should_exclude for excluded directories" {
    import:py from pathlib import Path;

    path1 = Path("docs/internals/memory.md");
    path2 = Path("docs/playground/test.jac");
    path3 = Path("docs/contributing/guide.md");

    assert should_exclude(path1) == True;
    assert should_exclude(path2) == True;
    assert should_exclude(path3) == True;
}

test "should_exclude for included paths" {
    import:py from pathlib import Path;

    path1 = Path("docs/language/nodes.md");
    path2 = Path("docs/tutorials/intro.md");
    path3 = Path("examples/hello.jac");

    assert should_exclude(path1) == False;
    assert should_exclude(path2) == False;
    assert should_exclude(path3) == False;
}

test "CodeExample line count calculation" {
    example = CodeExample(
        code="line1\nline2\nline3\nline4\nline5",
        source_file="test.md",
        construct_type="node"
    );
    assert example.line_count == 5;
}

test "CodeExample single line" {
    example = CodeExample(
        code="node Simple {}",
        source_file="test.md",
        construct_type="node"
    );
    assert example.line_count == 1;
}

test "ExtractedContent initialization" {
    content = ExtractedContent();
    assert content.total_examples == 0;
    assert content.total_signatures == 0;
}
