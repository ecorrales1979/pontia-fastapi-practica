import json
import logging
import os
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any


class Logger:

    def __init__(self) -> None:
        file_path: str = os.getenv("FILE_LOGGER_PATH", "logs/app.log")
        max_bytes: int = int(os.getenv("FILE_LOGGER_MAX_BYTES", "5242880"))
        backup_count: int = int(os.getenv("FILE_LOGGER_BACKUP_COUNT", "3"))
        log_file = Path(file_path)
        log_file.parent.mkdir(parents=True, exist_ok=True)

        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.INFO)

        if not self._logger.handlers:
            handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )
            # Single format for all log messages
            handler.setFormatter(logging.Formatter("%(message)s"))
            self._logger.addHandler(handler)

    def info(self, message: str, context: dict[str, Any] | None = None) -> None:
        line = self._format_line("INFO", message, context)
        self._logger.info(line)

    def warning(self, message: str, context: dict[str, Any] | None = None) -> None:
        line = self._format_line("WARN", message, context)
        self._logger.warning(line)

    def error(
        self,
        message: str,
        trace: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        line = self._format_line("ERROR", message, context, trace)
        self._logger.error(line)

    def critical(
        self,
        message: str,
        trace: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> None:
        line = self._format_line("CRITICAL", message, context, trace)
        self._logger.critical(line)

    def _get_context_str(self, context: dict[str, Any] | None) -> str:
        return f" | Context: {json.dumps(context, ensure_ascii=False)}" if context else ""

    def _get_trace_str(self, trace: str | None) -> str:
        return f"\nTrace: {trace}" if trace else ""

    def _get_date_str(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    def _format_line(
        self,
        level: str,
        message: str,
        context: dict[str, Any] | None = None,
        trace: str | None = None,
    ) -> str:
        ctx = self._get_context_str(context)
        tr = self._get_trace_str(trace)
        date_str = self._get_date_str()
        return f"[{level}] {date_str} {message}{ctx}{tr}"
