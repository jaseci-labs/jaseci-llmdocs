"""Tests for pipeline stages and validation."""

include:jac models.stage;
include:jac pipeline.validator;

import:py from time import time, sleep;

test "StageStatus enum values" {
    assert StageStatus.PENDING.value == "pending";
    assert StageStatus.RUNNING.value == "running";
    assert StageStatus.COMPLETE.value == "complete";
    assert StageStatus.ERROR.value == "error";
}

test "StageMetrics default state" {
    stage = StageMetrics(name="test_stage");

    assert stage.name == "test_stage";
    assert stage.status == StageStatus.PENDING;
    assert stage.start_time is None;
    assert stage.end_time is None;
    assert stage.input_size == 0;
    assert stage.output_size == 0;
    assert stage.file_count == 0;
    assert len(stage.files) == 0;
    assert stage.progress == 0;
    assert stage.progress_total == 0;
    assert stage.error_message is None;
}

test "StageMetrics start method" {
    stage = StageMetrics(name="fetch");
    stage.start();

    assert stage.status == StageStatus.RUNNING;
    assert stage.start_time is not None;
    assert stage.end_time is None;
    assert stage.error_message is None;
}

test "StageMetrics complete method" {
    stage = StageMetrics(name="fetch");
    stage.progress_total = 10;
    stage.start();
    stage.complete();

    assert stage.status == StageStatus.COMPLETE;
    assert stage.end_time is not None;
    assert stage.progress == 10;
}

test "StageMetrics fail method" {
    stage = StageMetrics(name="fetch");
    stage.start();
    stage.fail("Connection timeout");

    assert stage.status == StageStatus.ERROR;
    assert stage.end_time is not None;
    assert stage.error_message == "Connection timeout";
}

test "StageMetrics update_progress" {
    stage = StageMetrics(name="extract");
    stage.start();
    stage.update_progress(5, 10, "Processing file 5 of 10");

    assert stage.progress == 5;
    assert stage.progress_total == 10;
    assert stage.progress_message == "Processing file 5 of 10";
}

test "StageMetrics reset method" {
    stage = StageMetrics(name="assemble");
    stage.start();
    stage.input_size = 1000;
    stage.output_size = 100;
    stage.file_count = 5;
    stage.progress = 50;
    stage.complete();

    stage.reset();

    assert stage.status == StageStatus.PENDING;
    assert stage.start_time is None;
    assert stage.end_time is None;
    assert stage.input_size == 0;
    assert stage.output_size == 0;
    assert stage.file_count == 0;
    assert stage.progress == 0;
}

test "StageMetrics get_duration" {
    stage = StageMetrics(name="fetch");
    stage.start();
    sleep(0.1);
    stage.complete();

    duration = stage.get_duration();
    assert duration is not None;
    assert duration >= 0.1;
}

test "StageMetrics get_duration when not complete" {
    stage = StageMetrics(name="fetch");
    assert stage.get_duration() is None;

    stage.start();
    assert stage.get_duration() is None;
}

test "StageMetrics get_compression_ratio" {
    stage = StageMetrics(name="fetch");
    stage.input_size = 1000;
    stage.output_size = 100;

    ratio = stage.get_compression_ratio();
    assert ratio == 0.1;
}

test "StageMetrics get_compression_ratio with zero input" {
    stage = StageMetrics(name="fetch");
    stage.output_size = 100;

    ratio = stage.get_compression_ratio();
    assert ratio is None;
}

test "StageMetrics to_dict" {
    stage = StageMetrics(name="fetch");
    stage.input_size = 1000;
    stage.output_size = 100;
    stage.file_count = 5;
    stage.start();
    stage.complete();

    d = stage.to_dict();

    assert d["name"] == "fetch";
    assert d["status"] == "complete";
    assert d["input_size"] == 1000;
    assert d["output_size"] == 100;
    assert d["file_count"] == 5;
    assert d["compression_ratio"] == 0.1;
    assert d["duration"] is not None;
    assert d["error"] is None;
}

test "Validator find_patterns detects edge operators" {
    validator = Validator();
    text = "node1 ++> node2; parent <++> child; a --> b;";

    patterns = validator.find_patterns(text);

    assert "edge: ++>" in patterns;
    assert "edge: <++>" in patterns;
    assert "edge: -->" in patterns;
}

test "Validator find_patterns detects definitions" {
    validator = Validator();
    text = '''
node Person { has name: str; }
walker Greeter { can greet with entry {} }
edge Knows {}
obj Config {}
''';

    patterns = validator.find_patterns(text);

    assert "node definition" in patterns;
    assert "walker definition" in patterns;
    assert "edge definition" in patterns;
    assert "obj definition" in patterns;
    assert "ability definition" in patterns;
    assert "has x: type" in patterns;
}

test "Validator find_patterns detects Jac-specific syntax" {
    validator = Validator();
    text = '''
import:py json;
can main with `root entry {
    result = spawn greeter();
    visit [-->];
    report here.name;
}
can generate() -> str by llm(model=gpt);
async walker fetcher {}
''';

    patterns = validator.find_patterns(text);

    assert "import:py" in patterns;
    assert "root entry" in patterns;
    assert "spawn" in patterns;
    assert "by llm()" in patterns;
    assert "with entry" in patterns;
    assert "report" in patterns;
    assert "visit" in patterns;
    assert "here keyword" in patterns;
    assert "async" in patterns;
}

test "Validator validate with valid output" {
    validator = Validator();

    input_text = '''
node Person { has name: str; }
walker Greeter {
    can greet with `root entry {
        person ++> other;
        spawn helper();
        report data;
    }
}
import:py json;
can generate() by llm();
''';

    output_text = input_text;

    result = validator.validate(input_text, output_text);

    assert result["is_valid"] == True;
    assert len(result["issues"]) == 0;
}

test "Validator validate with empty output" {
    validator = Validator();

    input_text = "node Person { has name: str; }";
    output_text = "";

    result = validator.validate(input_text, output_text);

    assert result["is_valid"] == False;
    assert "Output is empty" in result["issues"];
}

test "Validator validate with too small output" {
    validator = Validator();
    validator.min_size_ratio = 0.5;

    input_text = "node Person { has name: str; has age: int; has email: str; }" * 10;
    output_text = "node P {}";

    result = validator.validate(input_text, output_text);

    assert result["is_valid"] == False;
    assert any("too small" in issue.lower() for issue in result["issues"]);
}

test "Validator validate with missing patterns" {
    validator = Validator();
    validator.required_pattern_ratio = 0.8;

    input_text = '''
node Person { has name: str; }
walker Greeter { can greet with entry { spawn x(); } }
by llm()
import:py json;
person ++> other;
''';

    output_text = "node Person { has name: str; }";

    result = validator.validate(input_text, output_text);

    assert len(result["missing_patterns"]) > 0;
}

test "Validator validate with unbalanced code blocks" {
    validator = Validator();

    input_text = "node Person {}";
    output_text = '''
```jac
node Person {}
Missing closing fence
''';

    result = validator.validate(input_text, output_text);

    assert result["is_valid"] == False;
    assert any("unbalanced" in issue.lower() for issue in result["issues"]);
}

test "Validator validate_final with all required patterns" {
    validator = Validator();

    text = '''
node Person { has name: str; }
walker Greeter {
    can greet with `root entry {
        person ++> other;
        spawn helper();
    }
}
can generate() by llm();
''';

    result = validator.validate_final(text);

    assert result["is_valid"] == True;
    assert len(result["missing_patterns"]) == 0;
}

test "Validator validate_final with missing required patterns" {
    validator = Validator();

    text = "node Person { has name: str; }";

    result = validator.validate_final(text);

    assert result["is_valid"] == False;
    assert len(result["missing_patterns"]) > 0;
}

test "Validator validate_final with custom required patterns" {
    validator = Validator();

    text = "node Person { has name: str; } walker Greeter {}";
    required = ["node definition", "walker definition"];

    result = validator.validate_final(text, required);

    assert result["is_valid"] == True;
    assert len(result["missing_patterns"]) == 0;
}

test "ValidationResult structure" {
    result = ValidationResult(
        is_valid=True,
        issues=[],
        missing_patterns=[],
        size_ratio=0.95
    );

    assert result.is_valid == True;
    assert len(result.issues) == 0;
    assert len(result.missing_patterns) == 0;
    assert result.size_ratio == 0.95;
}

test "Stage lifecycle pending to running to complete" {
    stage = StageMetrics(name="fetch");

    assert stage.status == StageStatus.PENDING;

    stage.start();
    assert stage.status == StageStatus.RUNNING;

    stage.complete();
    assert stage.status == StageStatus.COMPLETE;
}

test "Stage lifecycle pending to running to error" {
    stage = StageMetrics(name="fetch");

    assert stage.status == StageStatus.PENDING;

    stage.start();
    assert stage.status == StageStatus.RUNNING;

    stage.fail("Network error");
    assert stage.status == StageStatus.ERROR;
    assert stage.error_message == "Network error";
}

test "Stage extra metadata" {
    stage = StageMetrics(name="extract");
    stage.extra = {
        "signatures": 150,
        "examples": 45,
        "keywords": 25
    };

    d = stage.to_dict();

    assert d["extra"]["signatures"] == 150;
    assert d["extra"]["examples"] == 45;
    assert d["extra"]["keywords"] == 25;
}
