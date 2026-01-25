"""Configuration and prompts walker endpoints."""

include:jac config;

import:py from pathlib import Path;
import:py yaml;

walker get_config {
    """GET /api/config - Get current configuration."""

    has __specs__: dict = {
        "path": "/api/config",
        "methods": ["GET"]
    };

    can enter with `root entry {
        path = Path(CONFIG_PATH);
        if path.exists() {
            content = path.read_text();
            report {"config": config.to_dict(), "content": content};
        } else {
            report {"config": config.to_dict(), "content": ""};
        }
    }
}

walker update_config {
    """PUT /api/config - Update configuration."""

    has __specs__: dict = {
        "path": "/api/config",
        "methods": ["PUT"]
    };

    has content: str | None = None;
    has config_data: dict | None = None;

    can enter with `root entry {
        if self.content is not None {
            try {
                path = Path(CONFIG_PATH);
                path.parent.mkdir(parents=True, exist_ok=True);
                path.write_text(self.content);
                config.load(CONFIG_PATH);
                report {"config": config.to_dict(), "message": "Configuration updated"};
            } except Exception as e {
                report {"error": str(e), "status": 500};
            }
        } elif self.config_data is not None {
            config.update_from(self.config_data);
            config.save();
            report {"config": config.to_dict(), "message": "Configuration updated"};
        } else {
            report {"error": "No content or config_data provided", "status": 400};
        }
    }
}

walker list_prompts {
    """GET /api/prompts - List all prompt files."""

    has __specs__: dict = {
        "path": "/api/prompts",
        "methods": ["GET"]
    };

    can enter with `root entry {
        prompts = list_prompts();
        report prompts;
    }
}

walker get_prompt {
    """GET /api/prompts/{filename} - Get prompt content."""

    has __specs__: dict = {
        "path": "/api/prompts/{filename}",
        "methods": ["GET"]
    };

    has filename: str;

    can enter with `root entry {
        content = load_prompt(self.filename);
        if content is not None {
            report {
                "filename": self.filename,
                "content": content
            };
        } else {
            report {"error": "Prompt file not found", "status": 404};
        }
    }
}

walker update_prompt {
    """PUT /api/prompts/{filename} - Update prompt content."""

    has __specs__: dict = {
        "path": "/api/prompts/{filename}",
        "methods": ["PUT"]
    };

    has filename: str;
    has content: str;

    can enter with `root entry {
        if save_prompt(self.filename, self.content) {
            report {
                "filename": self.filename,
                "message": "Prompt updated",
                "size": len(self.content)
            };
        } else {
            report {"error": "Failed to save prompt", "status": 500};
        }
    }
}
