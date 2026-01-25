"""Tests for source management and graph operations."""

include:jac models.source;

import:py from uuid import uuid4;

test "Source node creation with defaults" {
    source = Source(git_url="https://github.com/test/repo.git");

    assert source.git_url == "https://github.com/test/repo.git";
    assert source.branch == "main";
    assert source.path == ".";
    assert source.source_type == SourceType.DOCS;
    assert source.enabled == True;
    assert source.file_patterns is None;
}

test "Source node with custom values" {
    source = Source(
        git_url="https://github.com/jaseci/jaclang.git",
        branch="develop",
        path="docs/",
        source_type=SourceType.JAC,
        enabled=False,
        file_patterns="*.jac,*.py"
    );

    assert source.branch == "develop";
    assert source.path == "docs/";
    assert source.source_type == SourceType.JAC;
    assert source.enabled == False;
    assert source.file_patterns == "*.jac,*.py";
}

test "Source patterns list for DOCS type" {
    source = Source(
        git_url="https://github.com/test/repo.git",
        source_type=SourceType.DOCS
    );

    patterns = source.get_patterns_list();
    assert patterns == ["*.md"];
}

test "Source patterns list for JAC type" {
    source = Source(
        git_url="https://github.com/test/repo.git",
        source_type=SourceType.JAC
    );

    patterns = source.get_patterns_list();
    assert patterns == ["*.jac"];
}

test "Source patterns list for BOTH type" {
    source = Source(
        git_url="https://github.com/test/repo.git",
        source_type=SourceType.BOTH
    );

    patterns = source.get_patterns_list();
    assert "*.md" in patterns;
    assert "*.jac" in patterns;
}

test "Source patterns list with custom patterns" {
    source = Source(
        git_url="https://github.com/test/repo.git",
        file_patterns="*.txt, *.rst, *.md"
    );

    patterns = source.get_patterns_list();
    assert len(patterns) == 3;
    assert "*.txt" in patterns;
    assert "*.rst" in patterns;
    assert "*.md" in patterns;
}

test "Source to_dict conversion" {
    source = Source(
        git_url="https://github.com/test/repo.git",
        branch="main",
        source_type=SourceType.DOCS
    );

    d = source.to_dict();

    assert d["git_url"] == "https://github.com/test/repo.git";
    assert d["branch"] == "main";
    assert d["source_type"] == "docs";
    assert d["enabled"] == True;
    assert "id" in d;
}

test "Source update_from with partial data" {
    source = Source(git_url="https://github.com/old/repo.git");

    source.update_from({
        "git_url": "https://github.com/new/repo.git",
        "branch": "feature-branch"
    });

    assert source.git_url == "https://github.com/new/repo.git";
    assert source.branch == "feature-branch";
    assert source.source_type == SourceType.DOCS;
}

test "Source update_from with source_type change" {
    source = Source(
        git_url="https://github.com/test/repo.git",
        source_type=SourceType.DOCS
    );

    source.update_from({"source_type": "jac"});

    assert source.source_type == SourceType.JAC;
}

test "Source update_from with file_patterns as list" {
    source = Source(git_url="https://github.com/test/repo.git");

    source.update_from({"file_patterns": ["*.jac", "*.py"]});

    assert source.file_patterns == "*.jac,*.py";
}

test "Source update_from with file_patterns as string" {
    source = Source(git_url="https://github.com/test/repo.git");

    source.update_from({"file_patterns": "*.md,*.rst"});

    assert source.file_patterns == "*.md,*.rst";
}

test "SourceType enum values" {
    assert SourceType.DOCS.value == "docs";
    assert SourceType.JAC.value == "jac";
    assert SourceType.BOTH.value == "both";
}

test "Source unique IDs" {
    source1 = Source(git_url="https://github.com/test/repo1.git");
    source2 = Source(git_url="https://github.com/test/repo2.git");

    assert source1.id != source2.id;
    assert len(source1.id) > 0;
    assert len(source2.id) > 0;
}

test "Source toggle enabled state" {
    source = Source(
        git_url="https://github.com/test/repo.git",
        enabled=True
    );

    assert source.enabled == True;
    source.enabled = False;
    assert source.enabled == False;
    source.enabled = True;
    assert source.enabled == True;
}
