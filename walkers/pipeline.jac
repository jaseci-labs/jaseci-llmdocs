"""Pipeline execution walker endpoints."""

include:jac models.source;
include:jac models.stage;
include:jac models.pipeline;
include:jac pipeline.sanitizer;
include:jac pipeline.extractor;
include:jac pipeline.assembler;
include:jac pipeline.validator;
include:jac utils.git;

import:py from time import time;
import:py asyncio;
import:py json;

glob ws_manager: WebSocketManager | None = None;

obj WebSocketManager {
    has connections: list = [];

    can connect(ws: object) {
        self.connections.append(ws);
    }

    can disconnect(ws: object) {
        if ws in self.connections {
            self.connections.remove(ws);
        }
    }

    can :async: broadcast(data: dict) {
        message = json.dumps(data);
        for conn in self.connections.copy() {
            try {
                await conn.send_text(message);
            } except Exception {
                if conn in self.connections {
                    self.connections.remove(conn);
                }
            }
        }
    }
}

can get_ws_manager() -> WebSocketManager {
    global ws_manager;
    if ws_manager is None {
        ws_manager = WebSocketManager();
    }
    return ws_manager;
}

can :async: emit_event(event_type: str, data: dict) {
    """Broadcast event to all WebSocket clients."""
    manager = get_ws_manager();
    await manager.broadcast({
        "event": event_type,
        "timestamp": time(),
        "data": data
    });
}

walker get_status {
    """GET /api/status - Get pipeline status."""

    has __specs__: dict = {
        "path": "/api/status",
        "methods": ["GET"]
    };

    can enter with `root entry {
        import:jac main (get_pipeline_state, get_all_stages);

        pipeline = get_pipeline_state();
        stages = get_all_stages();

        stage_data = {};
        for stage in stages {
            stage_data[stage.name] = stage.to_dict();
        }

        report {
            "is_running": pipeline.is_running,
            "current_stage": pipeline.current_stage,
            "error": pipeline.error,
            "stages": stage_data
        };
    }
}

walker get_metrics {
    """GET /api/metrics - Get pipeline metrics."""

    has __specs__: dict = {
        "path": "/api/metrics",
        "methods": ["GET"]
    };

    can enter with `root entry {
        import:jac main (get_pipeline_state, get_all_stages);

        pipeline = get_pipeline_state();
        stages = get_all_stages();

        metrics = {
            "total_duration": pipeline.get_duration(),
            "is_running": pipeline.is_running,
            "validation": pipeline.final_validation,
            "stages": {}
        };

        total_input = 0;
        total_output = 0;

        for stage in stages {
            stage_dict = stage.to_dict();
            metrics["stages"][stage.name] = {
                "duration": stage.get_duration(),
                "input_size": stage.input_size,
                "output_size": stage.output_size,
                "compression_ratio": stage.get_compression_ratio(),
                "file_count": stage.file_count,
                "extra": stage.extra
            };
            total_input += stage.input_size;
            total_output += stage.output_size;
        }

        if total_input > 0 {
            metrics["overall_compression"] = total_output / total_input;
        }

        report metrics;
    }
}

walker get_stages {
    """GET /api/stages - Get all stage details."""

    has __specs__: dict = {
        "path": "/api/stages",
        "methods": ["GET"]
    };

    can enter with `root entry {
        import:jac main (get_all_stages);

        stages = get_all_stages();
        stage_list = [stage.to_dict() for stage in stages];
        report stage_list;
    }
}

async walker run_pipeline {
    """POST /api/run - Run the full pipeline."""

    has __specs__: dict = {
        "path": "/api/run",
        "methods": ["POST"]
    };

    can enter with `root entry {
        import:jac main (get_pipeline_state, get_stage, get_sources);

        pipeline = get_pipeline_state();

        if pipeline.is_running {
            report {"error": "Pipeline already running", "status": 409};
            disengage;
        }

        for stage in [get_stage("fetch"), get_stage("extract"), get_stage("assemble")] {
            if stage {
                stage.reset();
            }
        }

        pipeline.start();
        await emit_event("pipeline_start", {});

        sources = get_sources();
        enabled_sources = [s for s in sources if s.enabled];

        if len(enabled_sources) == 0 {
            pipeline.fail("No enabled sources");
            await emit_event("pipeline_error", {"error": "No enabled sources"});
            report {"error": "No enabled sources", "status": 400};
            disengage;
        }

        try {
            fetch_stage = get_stage("fetch");
            fetch_stage.start();
            pipeline.set_stage("fetch");
            await emit_event("stage_start", {"stage": "fetch"});

            sanitizer = Sanitizer();
            fetch_result = await sanitizer.fetch_and_sanitize(
                enabled_sources,
                progress_callback=|cur, tot, msg| async {
                    fetch_stage.update_progress(cur, tot, msg);
                    await emit_event("progress", {
                        "stage": "fetch",
                        "current": cur,
                        "total": tot,
                        "message": msg
                    });
                }
            );

            fetch_stage.input_size = fetch_result["input_size"];
            fetch_stage.output_size = fetch_result["output_size"];
            fetch_stage.file_count = fetch_result["file_count"];
            fetch_stage.files = fetch_result["files"];
            fetch_stage.complete();
            await emit_event("stage_complete", {"stage": "fetch", "metrics": fetch_stage.to_dict()});

            extract_stage = get_stage("extract");
            extract_stage.start();
            pipeline.set_stage("extract");
            await emit_event("stage_start", {"stage": "extract"});

            extractor = DeterministicExtractor();
            extract_result = extractor.extract_from_directory(
                fetch_result["output_dir"],
                progress_callback=|cur, tot, msg| {
                    extract_stage.update_progress(cur, tot, msg);
                }
            );

            formatted = extractor.format_for_assembly(extract_result);
            extract_stage.input_size = fetch_result["output_size"];
            extract_stage.output_size = len(formatted);
            extract_stage.extra = {
                "signatures": extract_result.total_signatures,
                "examples": extract_result.total_examples,
                "selected_examples": sum(len(v) for v in extractor.select_best_examples(extract_result).values()),
                "keywords": len(extract_result.keywords_found)
            };
            extract_stage.complete();
            await emit_event("stage_complete", {"stage": "extract", "metrics": extract_stage.to_dict()});

            assemble_stage = get_stage("assemble");
            assemble_stage.start();
            pipeline.set_stage("assemble");
            await emit_event("stage_start", {"stage": "assemble"});

            assembler = Assembler();
            assembled = await assembler.assemble(
                extract_result,
                extractor,
                progress_callback=|cur, tot, msg| async {
                    assemble_stage.update_progress(cur, tot, msg);
                    await emit_event("progress", {
                        "stage": "assemble",
                        "current": cur,
                        "total": tot,
                        "message": msg
                    });
                }
            );

            validator = Validator();
            validation = validator.validate_final(assembled);

            validation_data = {
                "is_valid": validation["is_valid"],
                "issues": validation["issues"],
                "missing_patterns": validation["missing_patterns"],
                "patterns_found": len(validator.find_patterns(assembled)),
                "patterns_total": len(validator.CRITICAL_PATTERNS)
            };

            assemble_stage.input_size = extract_stage.output_size;
            assemble_stage.output_size = len(assembled);
            assemble_stage.complete();
            await emit_event("stage_complete", {
                "stage": "assemble",
                "metrics": assemble_stage.to_dict(),
                "validation": validation_data
            });

            pipeline.complete(validation_data);
            await emit_event("pipeline_complete", {
                "validation": validation_data,
                "total_duration": pipeline.get_duration(),
                "metrics": {
                    "fetch": fetch_stage.to_dict(),
                    "extract": extract_stage.to_dict(),
                    "assemble": assemble_stage.to_dict()
                }
            });

            report {
                "message": "Pipeline completed",
                "validation": validation_data,
                "output_size": len(assembled)
            };

        } except Exception as e {
            pipeline.fail(str(e));
            await emit_event("pipeline_error", {"error": str(e)});
            report {"error": str(e), "status": 500};
        }
    }
}

async walker run_stage {
    """POST /api/run/{stage} - Run a specific stage."""

    has __specs__: dict = {
        "path": "/api/run/{stage_name}",
        "methods": ["POST"]
    };

    has stage_name: str;

    can enter with `root entry {
        import:jac main (get_pipeline_state, get_stage, get_sources);

        pipeline = get_pipeline_state();

        if pipeline.is_running {
            report {"error": "Pipeline already running", "status": 409};
            disengage;
        }

        stage = get_stage(self.stage_name);
        if stage is None {
            report {"error": f"Unknown stage: {self.stage_name}", "status": 404};
            disengage;
        }

        pipeline.is_running = True;
        pipeline.set_stage(self.stage_name);
        stage.reset();
        stage.start();
        await emit_event("stage_start", {"stage": self.stage_name});

        try {
            if self.stage_name == "fetch" {
                sources = get_sources();
                enabled_sources = [s for s in sources if s.enabled];

                sanitizer = Sanitizer();
                result = await sanitizer.fetch_and_sanitize(
                    enabled_sources,
                    progress_callback=|cur, tot, msg| async {
                        stage.update_progress(cur, tot, msg);
                        await emit_event("progress", {
                            "stage": "fetch",
                            "current": cur,
                            "total": tot,
                            "message": msg
                        });
                    }
                );
                stage.input_size = result["input_size"];
                stage.output_size = result["output_size"];
                stage.file_count = result["file_count"];
                stage.files = result["files"];

            } elif self.stage_name == "extract" {
                extractor = DeterministicExtractor();
                result = extractor.extract_from_directory("output/0_sanitized");
                formatted = extractor.format_for_assembly(result);
                stage.output_size = len(formatted);
                stage.extra = {
                    "signatures": result.total_signatures,
                    "examples": result.total_examples,
                    "selected_examples": sum(len(v) for v in extractor.select_best_examples(result).values()),
                    "keywords": len(result.keywords_found)
                };

            } elif self.stage_name == "assemble" {
                assembler = Assembler();
                extractor = DeterministicExtractor();
                extracted = extractor.extract_from_directory("output/0_sanitized");
                result = await assembler.assemble(extracted, extractor);
                stage.output_size = len(result);
            }

            stage.complete();
            pipeline.is_running = False;
            await emit_event("stage_complete", {"stage": self.stage_name, "metrics": stage.to_dict()});

            report {"message": f"Stage {self.stage_name} completed", "metrics": stage.to_dict()};

        } except Exception as e {
            stage.fail(str(e));
            pipeline.is_running = False;
            await emit_event("stage_error", {"stage": self.stage_name, "error": str(e)});
            report {"error": str(e), "status": 500};
        }
    }
}
